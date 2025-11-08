"""
Vigilance AI – Webcam Edition
-----------------------------
Offline version using your system webcam instead of CARLA.
Performs:
 • Real-time driver state (drowsiness + emotion) monitoring
 • Voice assistant with speech feedback
 • ACTIVE / OFFLINE overlay + watchdog
"""

import cv2, dlib, os, time, threading, pyttsx3, speech_recognition as sr
from imutils import face_utils
from deepface import DeepFace
from scipy.spatial import distance

# ===================== CONFIG =====================
DLIB_MODEL = "backend/models/shape_predictor_68_face_landmarks.dat"
EAR_THRESH, MAR_THRESH = 0.22, 0.65
FATIGUE_BLINK_LIMIT = 40
EMOTION_INTERVAL = 30
VOICE_RATE = 170
WATCHDOG_TIMEOUT = 10

# ===================== MODEL CHECK =====================
if not os.path.exists(DLIB_MODEL):
    raise FileNotFoundError(
        f"{DLIB_MODEL} missing – download from https://github.com/davisking/dlib-models "
        "and place it in backend/models/"
    )

# ===================== INIT =====================
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(DLIB_MODEL)
engine = pyttsx3.init(driverName='sapi5')  # use 'espeak' on Linux
engine.setProperty("rate", VOICE_RATE)
recognizer = sr.Recognizer()

def speak(txt):
    print("Assistant:", txt)
    try:
        engine.say(txt)
        engine.runAndWait()
    except Exception as e:
        print("Voice error:", e)

def listen():
    try:
        with sr.Microphone() as src:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(src, duration=0.5)
            audio = recognizer.listen(src, timeout=4, phrase_time_limit=4)
        return recognizer.recognize_google(audio).lower()
    except:
        return ""

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

# ===================== GLOBAL STATE =====================
driver_state = {"state": "unknown", "emotion": "unknown"}
blink_count = consec_blink = 0
prev_ear, frame_idx = 1.0, 0
last_emotion, last_analysis_time = "unknown", time.time()
module_alive = True

# ===================== ANALYSIS THREAD =====================
def analyze():
    global blink_count, consec_blink, prev_ear, frame_idx
    global last_emotion, last_analysis_time, module_alive
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Webcam not found.")

    speak("Webcam driver monitoring started.")
    while True:
        ok, frame = cap.read()
        if not ok:
            time.sleep(0.05)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        frame_idx += 1

        if len(rects) == 0:
            driver_state.update({"state": "unknown", "emotion": "unknown"})
            cv2.putText(frame, "No face detected", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
        else:
            drowsy, emotion = "Unknown", last_emotion
            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                lEye, rEye, mouth = shape[36:42], shape[42:48], shape[48:68]
                ear_avg = (ear(lEye) + ear(rEye)) / 2.0
                mar_val = mar(mouth)

                if prev_ear > EAR_THRESH and ear_avg <= EAR_THRESH:
                    consec_blink += 1
                else:
                    consec_blink = 0
                if consec_blink >= 3:
                    blink_count += 1
                    consec_blink = 0
                prev_ear = ear_avg

                yawn = mar_val > MAR_THRESH
                drowsy = "Drowsy" if ear_avg < EAR_THRESH or yawn or blink_count > FATIGUE_BLINK_LIMIT else "Alert"

                if frame_idx % (EMOTION_INTERVAL * 5) == 0:
                    try:
                        res = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                        emotion = res[0]["dominant_emotion"] if isinstance(res, list) else res["dominant_emotion"]
                    except:
                        pass
                    last_emotion = emotion

                driver_state.update({"state": drowsy.lower(), "emotion": emotion.lower()})
                last_analysis_time = time.time()
                cv2.putText(frame, f"EAR:{ear_avg:.2f} MAR:{mar_val:.2f}", (10,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255),2)

        # overlay
        status_color = (0,255,0) if module_alive else (0,0,255)
        cv2.putText(frame, f"Status:{'ACTIVE' if module_alive else 'OFFLINE'}",
                    (10,25), cv2.FONT_HERSHEY_SIMPLEX,0.7,status_color,2)
        cv2.putText(frame, f"State:{driver_state['state']} | Emotion:{driver_state['emotion']}",
                    (10,55), cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)
        cv2.imshow("Vigilance AI – Webcam Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# ===================== VOICE ASSISTANT =====================
def assistant():
    global module_alive
    last_state = last_emotion_spoken = ""
    while True:
        now = time.time()
        elapsed = now - last_analysis_time
        if elapsed > WATCHDOG_TIMEOUT and module_alive:
            speak("Warning, driver analysis not responding.")
            module_alive = False
        elif elapsed <= WATCHDOG_TIMEOUT and not module_alive:
            speak("Driver analysis is back online.")
            module_alive = True

        state, emotion = driver_state["state"], driver_state["emotion"]
        if state != last_state:
            if state == "drowsy": speak("You appear drowsy. Please rest.")
            elif state == "alert" and last_state == "drowsy": speak("You are alert again.")
            last_state = state

        if emotion != last_emotion_spoken and emotion not in ["unknown",""]:
            if emotion in ["angry","fear","sad"]: speak("Take a deep breath. Stay calm.")
            elif emotion == "happy": speak("You seem happy. Stay focused.")
            last_emotion_spoken = emotion

        time.sleep(5)

# ===================== COMMAND LISTENER =====================
def commands():
    while True:
        cmd = listen()
        if not cmd: continue
        if "how am i" in cmd or "status" in cmd:
            speak(f"You are {driver_state['state']} and seem {driver_state['emotion']}.")
        elif "exit" in cmd or "quit" in cmd:
            speak("Shutting down Vigilance AI.")
            break

# ===================== MAIN =====================
def main():
    speak("Vigilance AI webcam mode activated.")
    threading.Thread(target=analyze, daemon=True).start()
    threading.Thread(target=assistant, daemon=True).start()
    commands()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        print("\nExiting Vigilance AI.")