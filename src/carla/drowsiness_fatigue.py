import carla
import cv2
import dlib
import time
import numpy as np
import os
import json
from queue import Queue
from scipy.spatial import distance
from deepface import DeepFace
from imutils import face_utils
import random

# === Configuration ===
DLIB_MODEL = "models/shape_predictor_68_face_landmarks.dat"
LOG_TXT = "carla_driver_log.txt"
STATE_JSON = "driver_state.json"
EAR_THRESH = 0.22
EAR_CONSEC_FRAMES = 3
MAR_THRESH = 0.65
FATIGUE_FRAME_LIMIT = 600
FATIGUE_BLINK_LIMIT = 40
EMOTION_INTERVAL = 30
YAW_THRESHOLD_DEG = 20.0
PITCH_THRESHOLD_DEG = 18.0
SMOOTH_ALPHA = 0.4

# === Load Dlib Model ===
if not os.path.exists(DLIB_MODEL):
    raise FileNotFoundError("Missing shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(DLIB_MODEL)

# === Frame Queue for Thread-Safe Display ===
frame_queue = Queue()

# === Monitoring State ===
frame_idx = blink_count = consec_blink_frames = 0
prev_ear = 1.0
yawn_counter = 0
last_emotion = "unknown"
last_is_stressed = False
last_emotion_frame = 0
smooth_yaw = smooth_pitch = smooth_roll = 0.0
distracted_frame_counter = 0
attention_state = "Unknown"
start_time = time.time()

# === Helper Functions ===
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C + 1e-8)

def mouth_aspect_ratio(mouth):
    A = distance.euclidean(mouth[13], mouth[19])
    B = distance.euclidean(mouth[14], mouth[18])
    C = distance.euclidean(mouth[15], mouth[17])
    D = distance.euclidean(mouth[12], mouth[16]) + 1e-8
    return (A + B + C) / (3.0 * D)

def head_pose_from_landmarks(landmarks, frame):
    image_points = np.array([
        landmarks[30], landmarks[8], landmarks[36], landmarks[45], landmarks[48], landmarks[54]
    ], dtype="double")
    model_points = np.array([
        (0.0, 0.0, 0.0), (0.0, -330.0, -65.0),
        (-225.0, 170.0, -135.0), (225.0, 170.0, -135.0),
        (-150.0, -150.0, -125.0), (150.0, -150.0, -125.0)
    ])
    size = frame.shape
    focal = size[1]
    center = (size[1] / 2.0, size[0] / 2.0)
    camera_matrix = np.array([[focal, 0, center[0]], [0, focal, center[1]], [0, 0, 1]], dtype="double")
    dist_coeffs = np.zeros((4, 1))
    success, rvec, tvec = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)
    if not success:
        return None
    rmat, _ = cv2.Rodrigues(rvec)
    proj = np.hstack((rmat, tvec))
    euler = cv2.decomposeProjectionMatrix(proj)[6]
    return [float(x) for x in euler]

def get_actor_by_filter(world, pattern, timeout=10.0, poll_interval=0.5):
    """Helper: safely get first actor matching a filter, with simple retry/polling"""
    deadline = time.time() + float(timeout)
    while time.time() < deadline:
        actors = world.get_actors().filter(pattern)
        if actors:
            return actors[0]
        time.sleep(poll_interval)
    return None

# === CARLA Setup ===
client = carla.Client("localhost", 2000)
client.set_timeout(10.0)
world = client.get_world()
blueprint_library = world.get_blueprint_library()

camera_bp = blueprint_library.find("sensor.camera.rgb")
camera_bp.set_attribute("image_size_x", "640")
camera_bp.set_attribute("image_size_y", "480")
camera_bp.set_attribute("fov", "90")

vehicle = get_actor_by_filter(world, "vehicle.*", timeout=10.0)
if vehicle is None:
    # Best-effort: try to spawn a vehicle so monitoring can proceed.
    try:
        vehicle_bps = blueprint_library.filter('vehicle.*')
        spawn_points = world.get_map().get_spawn_points()
        if vehicle_bps and spawn_points:
            bp = random.choice(vehicle_bps)
            spawn_point = random.choice(spawn_points)
            vehicle = world.try_spawn_actor(bp, spawn_point) or world.spawn_actor(bp, spawn_point)
            print(f"Spawned vehicle {vehicle.type_id} at {spawn_point}")
    except Exception as e:
        print(f"Vehicle spawn attempt failed: {e}")

if vehicle is None:
    raise RuntimeError("No vehicle actor found or spawned. Ensure CARLA is running and a vehicle is available.")

camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

# === Camera Callback ===
def camera_callback(image):
    frame = np.array(image.raw_data).reshape((image.height, image.width, 4))[:, :, :3]
    frame = np.ascontiguousarray(frame, dtype=np.uint8)
    frame_queue.put(frame)

camera.listen(camera_callback)

# === Frame Processing ===
def process_image(frame):
    global frame_idx, blink_count, consec_blink_frames, prev_ear, yawn_counter
    global last_emotion, last_is_stressed, last_emotion_frame
    global smooth_yaw, smooth_pitch, smooth_roll, distracted_frame_counter, attention_state

    frame_idx += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    ear = mar = pitch_deg = yaw_deg = roll_deg = 0.0
    drowsiness = fatigue_state = "Unknown"

    for rect in rects:
        shape = predictor(gray, rect)
        shape_np = face_utils.shape_to_np(shape)
        leftEye = shape_np[36:42]
        rightEye = shape_np[42:48]
        mouth = shape_np[48:68]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        mar = mouth_aspect_ratio(mouth)

        if prev_ear > EAR_THRESH and ear <= EAR_THRESH:
            consec_blink_frames += 1
        else:
            consec_blink_frames = 0
        if consec_blink_frames >= EAR_CONSEC_FRAMES:
            blink_count += 1
            consec_blink_frames = 0
        prev_ear = ear

        yawn_counter = yawn_counter + 1 if mar > MAR_THRESH else 0
        yawn_detected = yawn_counter > 12

        fatigue_state = "Fatigued" if frame_idx > FATIGUE_FRAME_LIMIT and blink_count > FATIGUE_BLINK_LIMIT else "Normal"
        drowsiness = "Drowsy" if ear < EAR_THRESH or yawn_detected or blink_count > 20 else "Alert" if ear > 0.26 and blink_count < 10 else "Uncertain"

        pose = head_pose_from_landmarks([(int(x), int(y)) for (x, y) in shape_np], frame)
        if pose:
            pitch_deg, yaw_deg, roll_deg = pose
            smooth_yaw = SMOOTH_ALPHA * yaw_deg + (1 - SMOOTH_ALPHA) * smooth_yaw
            smooth_pitch = SMOOTH_ALPHA * pitch_deg + (1 - SMOOTH_ALPHA) * smooth_pitch
            smooth_roll = SMOOTH_ALPHA * roll_deg + (1 - SMOOTH_ALPHA) * smooth_roll

        distracted_frame_counter += 1 if abs(smooth_yaw) > YAW_THRESHOLD_DEG or abs(smooth_pitch) > PITCH_THRESHOLD_DEG else -1
        distracted_frame_counter = max(0, distracted_frame_counter)
        attention_state = "Distracted" if distracted_frame_counter >= 8 else "Attentive"

        if frame_idx - last_emotion_frame >= EMOTION_INTERVAL:
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                dominant = result[0].get("dominant_emotion", "unknown") if isinstance(result, list) else result.get("dominant_emotion", "unknown")
                last_emotion = dominant
                last_is_stressed = dominant in ["angry", "fear", "sad", "disgust"]
            except:
                pass
            last_emotion_frame = frame_idx

    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_line = (
        f"{ts} | Frame: {frame_idx} | EAR: {ear:.3f} | MAR: {mar:.3f} | Blinks: {blink_count} | "
        f"Drowsiness: {drowsiness} | Fatigue: {fatigue_state} | Emotion: {last_emotion} | "
        f"Stress: {'Stressed' if last_is_stressed else 'Calm'} | Pitch: {smooth_pitch:.2f} | "
        f"Yaw: {smooth_yaw:.2f} | Roll: {smooth_roll:.2f} | Attention: {attention_state}\n"
    )

    with open(LOG_TXT, "a", encoding="utf-8") as f:
        f.write(log_line)
    
    # Save state for voice assistant
    state_data = {
        "drowsiness": drowsiness,
        "fatigue": fatigue_state,
        "attention": attention_state,
        "emotion": last_emotion,
        "stressed": last_is_stressed,
        "ear": ear,
        "mar": mar,
        "timestamp": ts
    }
    with open(STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(state_data, f)

    # === Overlay for Real-Time Display ===
    cv2.putText(frame, f"EAR: {ear:.3f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    cv2.putText(frame, f"MAR: {mar:.3f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
    cv2.putText(frame, f"Emotion: {last_emotion}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255), 2)
    cv2.putText(frame, f"Stress: {'Stressed' if last_is_stressed else 'Calm'}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,128,255), 2)
    cv2.putText(frame, f"Attention: {attention_state}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
    cv2.putText(frame, f"Drowsiness: {drowsiness}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
    cv2.putText(frame, f"Fatigue: {fatigue_state}", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

    cv2.imshow("CARLA Driver Monitor", frame)
    return state_data

# === Main Loop: Display and Shutdown ===
try:
    print("Monitoring started. Press 'q' to quit.")
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            process_image(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Interrupted by user.")
finally:
    camera.stop()
    cv2.destroyAllWindows()
    elapsed = time.time() - start_time
    print(f"Session ended. Frames: {frame_idx}. Elapsed: {elapsed:.1f}s")
    print(f"Log saved to: {os.path.abspath(LOG_TXT)}")