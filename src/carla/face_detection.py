from deepface import DeepFace
import cv2
import os
from datetime import datetime

def get_driver_emotion_state(frame):
    """
    Analyze a frame and return emotion and stress status.
    """
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        is_stressed = emotion in ['angry', 'fear', 'sad']
        return {'emotion': emotion, 'is_stressed': is_stressed}
    except Exception as e:
        print(f"Detection error: {e}")
        return {'emotion': 'undetected', 'is_stressed': False}

def resize_to_screen(frame, screen_width=1920, screen_height=1080, scale=0.9):
    h, w = frame.shape[:2]
    scale_factor = min((screen_width / w), (screen_height / h)) * scale
    return cv2.resize(frame, (int(w * scale_factor), int(h * scale_factor)))

def log_emotion_state(log_file, frame_number, emotion, is_stressed):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{timestamp}, Frame {frame_number}, Emotion: {emotion}, Stressed: {is_stressed}\n")

def analyze_webcam(log_file="emotion_log.txt"):
    cap = cv2.VideoCapture(0)
    print("🔴 Webcam mode started. Press 'q' to quit.")
    frame_number = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        state = get_driver_emotion_state(frame)
        frame_number += 1
        log_emotion_state(log_file, frame_number, state['emotion'], state['is_stressed'])

        frame = resize_to_screen(frame)
        cv2.putText(frame, f"{state['emotion']} | Stress: {state['is_stressed']}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Webcam Emotion Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"📝 Emotion log saved to {log_file}")

def analyze_video(video_path, log_file="emotion_log.txt"):
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    print(f"🎞 Analyzing video: {video_path} — Press 'q' to quit.")
    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        state = get_driver_emotion_state(frame)
        frame_number += 1
        log_emotion_state(log_file, frame_number, state['emotion'], state['is_stressed'])

        frame = resize_to_screen(frame)
        cv2.putText(frame, f"{state['emotion']} | Stress: {state['is_stressed']}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Video Emotion Detection", frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"📝 Emotion log saved to {log_file}")

# 🧭 Choose mode
print("Choose mode:\n1 - Real-time webcam\n2 - Analyze video file")
choice = input("Enter 1 or 2: ")

if choice == '1':
    analyze_webcam()
elif choice == '2':
    video_path = input("Enter full path to video file: ").strip('"')
    analyze_video(video_path)
else:
    print("⚠ Invalid choice. Please enter 1 or 2.")