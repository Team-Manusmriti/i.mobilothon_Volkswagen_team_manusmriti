"""
Vigilance AI - Integrated CARLA Driver Monitoring + Voice Assistant + Visual Live Indicator
--------------------------------------------------------------------------------------------
Features:
 - Real-time driver monitoring (drowsiness, emotion, attention)
 - Voice assistant with speech I/O and CARLA control
 - Live watchdog for driver-state liveness
 - Visual 'ACTIVE / OFFLINE' banner on OpenCV window
"""

import carla
import cv2
import dlib
import time
import numpy as np
import threading
import pyttsx3
import speech_recognition as sr
from imutils import face_utils
from deepface import DeepFace
from scipy.spatial import distance

# ===============================
# CONFIG
# ===============================
DLIB_MODEL = "models/shape_predictor_68_face_landmarks.dat"
EAR_THRESH = 0.22
MAR_THRESH = 0.65
FATIGUE_BLINK_LIMIT = 40
EMOTION_INTERVAL = 30
SPEED_ALERT_THRESHOLD = 80.0  # km/h
VOICE_RATE = 170
WATCHDOG_TIMEOUT = 10  # seconds before "offline" status

# ===============================
# INIT: CARLA CONNECTION
# ===============================
print("Connecting to CARLA...")
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

vehicle = None
for actor in world.get_actors():
    if actor.type_id.startswith('vehicle.') and actor.attributes.get('role_name') == 'hero':
        vehicle = actor
        break

if not vehicle:
    print("No hero vehicle found!")
    exit()

print("Connected to:", vehicle.type_id)

# ===============================
# INIT: MODELS & SPEECH ENGINES
# ===============================
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(DLIB_MODEL)

engine = pyttsx3.init()
engine.setProperty('rate', VOICE_RATE)
r = sr.Recognizer()

def speak(text):
    print("Assistant:", text)
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=4, phrase_time_limit=4)
        cmd = r.recognize_google(audio).lower()
        print("Heard:", cmd)
        return cmd
    except:
        return ""

# ===============================
# HELPER FUNCTIONS
# ===============================
def ear(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C + 1e-8)

def mar(mouth):
    A = distance.euclidean(mouth[13], mouth[19])
    B = distance.euclidean(mouth[14], mouth[18])
    C = distance.euclidean(mouth[15], mouth[17])
    D = distance.euclidean(mouth[12], mouth[16]) + 1e-8
    return (A + B + C) / (3.0 * D)

def get_speed():
    v = vehicle.get_velocity()
    return 3.6 * (v.x*2 + v.y2 + v.z2)*0.5

# ===============================
# CAMERA SETUP
# ===============================
bp_lib = world.get_blueprint_library()
cam_bp = bp_lib.find("sensor.camera.rgb")
cam_bp.set_attribute("image_size_x", "640")
cam_bp.set_attribute("image_size_y", "480")
cam_bp.set_attribute("fov", "90")

camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
camera = world.spawn_actor(cam_bp, camera_transform, attach_to=vehicle)

frame = None
def camera_callback(image):
    global frame
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    frame = array.reshape((image.height, image.width, 4))[:, :, :3]
camera.listen(camera_callback)

# ===============================
# GLOBAL STATES
# ===============================
driver_state = {"state": "unknown", "emotion": "unknown"}
last_emotion = "unknown"
blink_count = 0
consec_blink_frames = 0
prev_ear = 1.0
frame_idx = 0
last_analysis_time = time.time()
module_alive = True

# ===============================
# DRIVER ANALYSIS THREAD
# ===============================
def analyze_driver():
    global blink_count, consec_blink_frames, prev_ear, frame_idx
    global last_emotion, last_analysis_time, driver_state, module_alive

    while True:
        if frame is None:
            time.sleep(0.05)
            continue

        current = frame.copy()
        gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        frame_idx += 1

        drowsy = "Unknown"
        emotion = last_emotion

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            lEye, rEye, mouth = shape[36:42], shape[42:48], shape[48:68]
            ear_avg = (ear(lEye) + ear(rEye)) / 2.0
            mar_val = mar(mouth)

            if prev_ear > EAR_THRESH and ear_avg <= EAR_THRESH:
                consec_blink_frames += 1
            else:
                consec_blink_frames = 0
            if consec_blink_frames >= 3:
                blink_count += 1
                consec_blink_frames = 0
            prev_ear = ear_avg

            yawn = mar_val > MAR_THRESH
            drowsy = "Drowsy" if ear_avg < EAR_THRESH or yawn or blink_count > FATIGUE_BLINK_LIMIT else "Alert"

            if frame_idx % EMOTION_INTERVAL == 0:
                try:
                    res = DeepFace.analyze(current, actions=['emotion'], enforce_detection=False)
                    emotion = res[0]["dominant_emotion"] if isinstance(res, list) else res["dominant_emotion"]
                except:
                    pass
                last_emotion = emotion

        driver_state["state"] = drowsy.lower()
        driver_state["emotion"] = emotion.lower()
        last_analysis_time = time.time()

        # Visual overlay
        status_color = (0, 255, 0) if module_alive else (0, 0, 255)
        status_text = "ACTIVE" if module_alive else "OFFLINE"
        cv2.putText(current, f"Status: {status_text}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(current, f"State: {drowsy} | Emotion: {emotion}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.imshow("Vigilance AI - Driver Monitor", current)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.05)

# ===============================
# VOICE ASSISTANT THREAD
# ===============================
def voice_assistant():
    global module_alive
    last_state, last_emotion = "", ""

    while True:
        try:
            now = time.time()
            elapsed = now - last_analysis_time

            # Watchdog for liveness
            if elapsed > WATCHDOG_TIMEOUT and module_alive:
                speak("Warning. Driver state analysis module not responding.")
                module_alive = False
            elif elapsed <= WATCHDOG_TIMEOUT and not module_alive:
                speak("Driver analysis module is back online.")
                module_alive = True

            state, emotion = driver_state["state"], driver_state["emotion"]
            speed = get_speed()

            if state != last_state:
                if state == "drowsy":
                    speak("You appear drowsy. Please rest.")
                elif state == "alert" and last_state == "drowsy":
                    speak("You're alert again.")
                last_state = state

            if emotion != last_emotion and emotion not in ["unknown", "neutral"]:
                if emotion in ["angry", "sad", "fear", "disgust"]:
                    speak(f"You seem {emotion}. Please calm down.")
                elif emotion == "happy":
                    speak("You seem happy today. Stay focused.")
                last_emotion = emotion

            if speed > SPEED_ALERT_THRESHOLD:
                speak(f"You are exceeding {SPEED_ALERT_THRESHOLD} kilometers per hour. Please slow down.")

            time.sleep(5)
        except Exception as e:
            print("Voice Assistant Error:", e)
            time.sleep(2)

# ===============================
# COMMAND LISTENER THREAD
# ===============================
def command_listener():
    while True:
        cmd = listen()
        if not cmd:
            continue

        speed = get_speed()
        if "speed" in cmd:
            speak(f"Your current speed is {speed:.1f} kilometers per hour.")
        elif "how am i" in cmd or "driver" in cmd:
            speak(f"You are {driver_state['state']} and seem {driver_state['emotion']}.")
        elif "stop" in cmd:
            vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
            speak("Vehicle stopped.")
        elif "resume" in cmd or "start" in cmd:
            vehicle.apply_control(carla.VehicleControl(throttle=0.5, brake=0.0))
            speak("Resuming drive.")
        elif "exit" in cmd or "quit" in cmd:
            speak("Shutting down Vigilance AI. Drive safe.")
            break
        time.sleep(0.5)

# ===============================
# MAIN
# ===============================
def main():
    speak("Vigilance AI monitoring and live-check assistant activated.")
    threading.Thread(target=analyze_driver, daemon=True).start()
    threading.Thread(target=voice_assistant, daemon=True).start()
    command_listener()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        camera.stop()
        cv2.destroyAllWindows()
        print("\nExiting Vigilance AI...")