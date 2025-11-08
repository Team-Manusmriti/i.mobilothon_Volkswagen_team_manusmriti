import cv2
import numpy as np
import mediapipe as mp
import dlib
import math
import csv
import os
import time
from datetime import datetime
from deepface import DeepFace

CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
EAR_THRESHOLD = 0.21
MAR_THRESHOLD = 0.6
BLINK_DEBOUNCE_FRAMES = 2
FATIGUE_FRAME_LIMIT = 600
FATIGUE_BLINK_LIMIT = 40
EMOTION_INTERVAL_FRAMES = 30
LOG_CSV = "driver_monitor_log.csv"
DLIB_PREDICTOR = "models/shape_predictor_68_face_landmarks.dat"

if not os.path.exists(LOG_CSV):
    with open(LOG_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp","frame_idx","ear","mar","blink_count","drowsiness_state",
            "fatigue_state","dominant_emotion","is_stressed","pitch","yaw","roll"
        ])

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=False)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
UPPER_LIP = 13
LOWER_LIP = 14
MOUTH_LEFT = 78
MOUTH_RIGHT = 308

if not os.path.exists(DLIB_PREDICTOR):
    raise FileNotFoundError("Missing 'shape_predictor_68_face_landmarks.dat'.")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(DLIB_PREDICTOR)

def euclidean(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def calculate_ear(landmarks):
    left = [landmarks[i] for i in LEFT_EYE]
    right = [landmarks[i] for i in RIGHT_EYE]
    left_ear = euclidean(left[1], left[5]) / (euclidean(left[0], left[3]) + 1e-8)
    right_ear = euclidean(right[1], right[5]) / (euclidean(right[0], right[3]) + 1e-8)
    return (left_ear + right_ear) / 2.0

def calculate_mar(landmarks):
    vertical = euclidean(landmarks[UPPER_LIP], landmarks[LOWER_LIP])
    horizontal = euclidean(landmarks[MOUTH_LEFT], landmarks[MOUTH_RIGHT])
    return vertical / (horizontal + 1e-8)

def estimate_head_pose_dlib(gray, predictor):
    faces = detector(gray, 0)
    if len(faces) == 0:
        return None
    face = faces[0]
    shape = predictor(gray, face)
    image_points = np.array([
        (shape.part(30).x, shape.part(30).y),
        (shape.part(8).x, shape.part(8).y),
        (shape.part(36).x, shape.part(36).y),
        (shape.part(45).x, shape.part(45).y),
        (shape.part(48).x, shape.part(48).y),
        (shape.part(54).x, shape.part(54).y)
    ], dtype="double")
    model_points = np.array([
        (0.0, 0.0, 0.0),
        (0.0, -330.0, -65.0),
        (-225.0, 170.0, -135.0),
        (225.0, 170.0, -135.0),
        (-150.0, -150.0, -125.0),
        (150.0, -150.0, -125.0)
    ], dtype="double")
    size = gray.shape
    focal_length = size[1]
    center = (size[1] / 2, size[0] / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")
    dist_coeffs = np.zeros((4, 1))
    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )
    if not success:
        return None
    rmat, _ = cv2.Rodrigues(rotation_vector)
    proj_mat = np.hstack((rmat, translation_vector))
    euler_angles = cv2.decomposeProjectionMatrix(proj_mat)[6]
    pitch, yaw, roll = [float(angle) for angle in euler_angles]
    return (round(pitch, 2), round(yaw, 2), round(roll, 2))

def estimate_emotion_and_stress(bgr_frame):
    try:
        rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        result = DeepFace.analyze(rgb, actions=['emotion'], enforce_detection=False)
        if isinstance(result, list) and len(result) > 0:
            dominant = result[0].get('dominant_emotion', 'unknown')
        elif isinstance(result, dict):
            dominant = result.get('dominant_emotion', 'unknown')
        else:
            dominant = 'unknown'
        is_stressed = dominant in ['angry', 'fear', 'sad', 'disgust']
        return dominant, is_stressed
    except Exception:
        return "unknown", False

def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    frame_idx = 0
    blink_count = 0
    blink_debounce = 0
    prev_ear = 1.0
    yawn_counter = 0
    last_emotion = "unknown"
    last_is_stressed = False
    start_time = time.time()
    print("Starting webcam driver monitoring. Press 'q' to quit.")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_idx += 1
            small_frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            head_pose = estimate_head_pose_dlib(gray, predictor)
            ear = 0.0
            mar = 0.0
            detected_face = False
            if results.multi_face_landmarks:
                detected_face = True
                landmarks = results.multi_face_landmarks[0].landmark
                ear = calculate_ear(landmarks)
                mar = calculate_mar(landmarks)
                if prev_ear > EAR_THRESHOLD and ear <= EAR_THRESHOLD and blink_debounce == 0:
                    blink_count += 1
                    blink_debounce = BLINK_DEBOUNCE_FRAMES
                if blink_debounce > 0:
                    blink_debounce -= 1
                prev_ear = ear
                if mar > MAR_THRESHOLD:
                    yawn_counter += 1
                else:
                    yawn_counter = 0
                yawn_detected = yawn_counter > 15
                if ear < EAR_THRESHOLD or yawn_detected or blink_count > 20:
                    drowsiness_state = "Drowsy"
                elif ear > 0.25 and blink_count < 10:
                    drowsiness_state = "Alert"
                else:
                    drowsiness_state = "Uncertain"
                if frame_idx > FATIGUE_FRAME_LIMIT and blink_count > FATIGUE_BLINK_LIMIT:
                    fatigue_state = "Fatigued"
                else:
                    fatigue_state = "Normal"
            else:
                drowsiness_state = "NoFace"
                fatigue_state = "Unknown"
                yawn_detected = False
            if frame_idx % EMOTION_INTERVAL_FRAMES == 0 and detected_face:
                dominant_emotion, is_stressed = estimate_emotion_and_stress(small_frame)
                last_emotion = dominant_emotion
                last_is_stressed = is_stressed
            else:
                dominant_emotion = last_emotion
                is_stressed = last_is_stressed
            disp = small_frame.copy()
            cv2.putText(disp, f"Frame: {frame_idx}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (220,220,220), 2)
            cv2.putText(disp, f"EAR: {ear:.3f}", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(disp, f"MAR: {mar:.3f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(disp, f"Blinks: {blink_count}", (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(disp, f"Drowsiness: {drowsiness_state}", (10, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            cv2.putText(disp, f"Fatigue: {fatigue_state}", (10, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
            cv2.putText(disp, f"Emotion: {dominant_emotion}", (10, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            cv2.putText(disp, f"Stressed: {is_stressed}", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            if head_pose is not None:
                pitch, yaw, roll = head_pose
                cv2.putText(disp, f"HeadPose (P,Y,R): {pitch},{yaw},{roll}", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
            else:
                cv2.putText(disp, "HeadPose: None", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
            cv2.imshow("Driver Monitor (Webcam)", disp)
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [ts, frame_idx, f"{ear:.3f}", f"{mar:.3f}", blink_count, drowsiness_state, fatigue_state, dominant_emotion, int(is_stressed),
                   (head_pose[0] if head_pose else ""), (head_pose[1] if head_pose else ""), (head_pose[2] if head_pose else "")]
            with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(row)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        face_mesh.close()
        elapsed = time.time() - start_time
        print(f"Session ended. Frames: {frame_idx}, Elapsed: {elapsed:.1f}s, Log: {os.path.abspath(LOG_CSV)}")

if __name__ == "__main__":
    main()