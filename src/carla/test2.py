"""
Vigilance AI – Context-Aware Voice Assistant (Webcam Edition)
-------------------------------------------------------------
Offline system that combines:
 • Real-time driver monitoring (EAR, MAR, emotion)
 • Dynamic text-to-speech with contextual responses
 • Natural voice commands (time, date, weather, mood)
 • Cooldown logic to prevent repetitive alerts
"""

import cv2, dlib, os, time, threading, queue, pyttsx3, speech_recognition as sr
from imutils import face_utils
from deepface import DeepFace
from scipy.spatial import distance
import requests
from bs4 import BeautifulSoup
import datetime, requests, random, platform
import numpy as np
import mediapipe as mp

# ===================== CONFIG =====================
DLIB_MODEL = "backend/models/shape_predictor_68_face_landmarks.dat"
EAR_THRESH, MAR_THRESH = 0.22, 0.65
FATIGUE_BLINK_LIMIT = 40
EMOTION_INTERVAL = 30
VOICE_RATE = 170
WATCHDOG_TIMEOUT = 10
CITY = "Delhi"  # Change for weather
OPENWEATHER_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # optional

# ===================== MODEL CHECK =====================
if not os.path.exists(DLIB_MODEL):
    raise FileNotFoundError(
        f"{DLIB_MODEL} missing – download from https://github.com/davisking/dlib-models "
        "and place it in backend/models/"
    )

# ===================== TTS ENGINE SETUP =====================
system = platform.system().lower()
if "windows" in system:
    engine = pyttsx3.init(driverName='sapi5')
elif "linux" in system:
    engine = pyttsx3.init(driverName='espeak')
elif "darwin" in system:
    engine = pyttsx3.init(driverName='nsss')
else:
    engine = pyttsx3.init()

engine.setProperty("rate", VOICE_RATE)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# ===================== SPEECH QUEUE SYSTEM =====================
speech_queue = queue.Queue()
voice_running = True

def speak_worker():
    """Persistent queue-based voice system."""
    while voice_running:
        try:
            text = speech_queue.get(timeout=1)
        except queue.Empty:
            continue
        if text == "EXIT":
            break
        print("Assistant:", text)
        try:
            rate = random.randint(160, 185)
            engine.setProperty('rate', rate)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Voice error: {e}")
        time.sleep(0.2)


def get_weather_data():

    URL = "https://www.timeanddate.com/weather/india/delhi"

    response = requests.get(URL)
    # print(f"res: {response.content}")  # Print first 100 characters of the response content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find temperature and weather description
    temperature = soup.find("div", class_="h2").text.strip()
    desc = soup.find("p").text.strip()
    return f"The current temperature in Delhi is {temperature} with {desc}."


def speak(command):
    """Convert text to speech with threading"""
    def _speak():
        try:
            # Create a new engine instance for thread safety
            local_engine = pyttsx3.init()
            local_engine.setProperty('rate', 150)
            local_engine.setProperty('volume', 0.9)
            
            local_engine.say(command)
            local_engine.runAndWait()
            local_engine.stop()
            
        except Exception as e:
            pass
    
    thread = threading.Thread(target=_speak)
    thread.daemon = True
    thread.start()
    thread.join(timeout=10)


# ===================== AUDIO INPUT =====================
recognizer = sr.Recognizer()
def listen():
    try:
        with sr.Microphone() as src:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(src, duration=0.5)
            audio = recognizer.listen(src, timeout=4, phrase_time_limit=5)
        cmd = recognizer.recognize_google(audio).lower()
        print("Heard:", cmd)
        return cmd
    except:
        return ""

# ===================== HELPER FUNCTIONS =====================
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
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(DLIB_MODEL)
driver_state = {"state": "unknown", "emotion": "unknown"}
blink_count = consec_blink = 0
prev_ear, frame_idx = 1.0, 0
last_emotion, last_analysis_time = "unknown", time.time()
cooldowns = {"drowsy": 0, "alert": 0, "emotion": {}}
module_alive = True
WS_INTERVAL = 5  # seconds

mp_selfie = mp.solutions.selfie_segmentation
segmentor = mp_selfie.SelfieSegmentation(model_selection=1)

# ===================== DRIVER ANALYSIS =====================
def analyze():
    global blink_count, consec_blink, prev_ear, frame_idx
    global last_emotion, last_analysis_time, module_alive
    global last_sent_state, last_ws_time
    
    # Initialize WebSocket tracking variables
    last_sent_state = {"state": "", "emotion": ""}
    last_ws_time = 0

    print("Initializing camera...")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("Failed to open camera with index 0, trying index 1...")
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            raise RuntimeError("No webcam found. Please check camera connection.")
    
    print("Camera initialized successfully")
    speak("Webcam driver monitoring started.")
    
    while True:
        ok, frame = cap.read()
        if not ok:
            time.sleep(0.05)
            continue

        frame = cv2.resize(frame, (640, 480))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # ============ PERSON SEGMENTATION ============
        try:
            result = segmentor.process(rgb)  # Get mask for body
            mask = result.segmentation_mask
            
            # Improve mask processing
            mask = (mask > 0.3).astype(np.uint8)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.GaussianBlur(mask.astype(np.float32), (3, 3), 0)
            
            # Create blurred background
            blurred_frame = cv2.GaussianBlur(frame, (55, 55), 0)
            
            # Combine with smooth blending
            mask_3d = np.stack([mask] * 3, axis=2)
            frame = (frame * mask_3d + blurred_frame * (1 - mask_3d)).astype(np.uint8)
        except Exception as e:
            print(f"MediaPipe error: {e}")
            # Continue without background blur if MediaPipe fails

        # ================= FACE + MONITOR LOGIC =================
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        frame_idx += 1

        if len(rects) == 0:
            driver_state.update({"state": "unknown", "emotion": "unknown"})
            cv2.putText(frame, "No face detected", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
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
                # Optimized WebSocket - only send on state change or time interval
                current_time = time.time()
                state_changed = (driver_state["state"] != last_sent_state["state"] or 
                               driver_state["emotion"] != last_sent_state["emotion"])
                
                if state_changed or (current_time - last_ws_time > WS_INTERVAL):
                    try:
                        requests.post("http://localhost:8008/update-emotion", 
                                    json=driver_state, timeout=0.3)
                        last_sent_state = driver_state.copy()
                        last_ws_time = current_time
                    except:
                        pass

                last_analysis_time = time.time()
                cv2.putText(frame, f"EAR:{ear_avg:.2f} MAR:{mar_val:.2f}", (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (17, 0, 255), 2)

        status_color = (0, 255, 0) if module_alive else (0, 0, 255)
        cv2.putText(frame, f"Status:{'ACTIVE' if module_alive else 'OFFLINE'}",
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(frame, f"State:{driver_state['state'].upper()} | Emotion:{driver_state['emotion'].upper()}",
                    (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow("Vigilance AI - Webcam Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def get_dynamic_response(key: str):
    res = {
        "drowsy": ["You seem drowsy. Please take a break.", "You're showing signs of fatigue.", "Consider resting soon."],
        "alert": ["You are alert and focused.", "Great job staying attentive!", "Keep up the good focus."],
        "angry": ["You seem angry. Let's take a deep breath.", "Try to stay calm and focused.", "Remember, staying calm is key."],
        "happy": ["You look happy! Keep that positive energy.", "Glad to see you're in a good mood.", "Stay focused and enjoy the drive."],
        "sad": ["You seem sad. Remember, it's okay to feel this way.", "I'm here with you. Stay strong.", "Things will get better. Keep going."],
        "fear": ["You seem fearful. Stay calm and focused.", "Take deep breaths. You're safe.", "Focus on the road ahead."],
    }
    return random.choice(res.get(key, ["Drive safely and stay attentive."]))

# ===================== VOICE ASSISTANT (Context-Aware) =====================
def assistant():
    global module_alive
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

        # Drowsiness alert (20-sec cooldown)
        if state == "drowsy" and now - cooldowns["drowsy"] > 20:
            speak(get_dynamic_response("drowsy"))
            cooldowns["drowsy"] = now
        elif state == "alert" and now - cooldowns["alert"] > 20:
            speak(get_dynamic_response("alert"))
            cooldowns["alert"] = now

        # Emotion response (30-sec cooldown per emotion)
        if emotion not in cooldowns["emotion"]:
            cooldowns["emotion"][emotion] = 0
        if now - cooldowns["emotion"][emotion] > 30 and emotion not in ["unknown", ""]:
            if emotion in ["angry","fear","sad"]:
                speak(get_dynamic_response(emotion))
            elif emotion == "happy":
                speak(get_dynamic_response(emotion))
            cooldowns["emotion"][emotion] = now

        time.sleep(5)

# ===================== COMMAND PROCESSOR =====================
def process_command(cmd):
    cmd = cmd.lower()

    # Conversational context understanding
    if "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")
    if "date" in cmd or "day" in cmd:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}.")
    if "weather" in cmd:
        speak("Checking the weather.")
        speak(get_weather_data())
    if "i'm tired" in cmd or "i am tired" in cmd:
        speak("You seem exhausted. Pull over and take a short break.")
        driver_state["state"] = "drowsy"
    if "i'm angry" in cmd or "i am angry" in cmd:
        speak("It’s okay to feel angry. Let’s take a deep breath together.")
        driver_state["emotion"] = "angry"
    if "i'm sad" in cmd or "i am sad" in cmd:
        speak("I’m here with you. Things will get better. Stay strong.")
        driver_state["emotion"] = "sad"
    if "i'm happy" in cmd or "i am happy" in cmd:
        speak("That’s great to hear! Keep that positive energy.")
        driver_state["emotion"] = "happy"

    if "status" in cmd or "driver" in cmd or "how am i" in cmd:
        s, e = driver_state["state"], driver_state["emotion"]
        speak(f"You are {s} and seem {e}.")
    if "exit" in cmd or "quit" in cmd or "stop" in cmd:
        speak("Shutting down Vigilance AI. Drive safe.")
        speech_queue.put("EXIT")
        return False
    else:
        pass
    return True

def commands():
    while True:
        cmd = listen()
        if not cmd:
            continue
        if not process_command(cmd):
            break

# ===================== MAIN =====================
def main():
    speak("Vigilance AI context-aware assistant activated.")
    threading.Thread(target=analyze, daemon=True).start()
    threading.Thread(target=assistant, daemon=True).start()
    commands()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        speech_queue.put("EXIT")
        print("\nExiting Vigilance AI...")