## VigilanceAI – AI-Enhanced Driver Wellness Monitoring

**Volkswagen Hackathon Submission – Team Manusmriti**


VigilanceAI is an intelligent co-pilot engineered to redefine road safety by prioritizing the driver's overall well-being. Unlike conventional systems that react only when danger is imminent, VigilanceAI takes a proactive approach. It leverages multi-modal AI to integrate cabin video analytics—monitoring signs of drowsiness, stress, and medical distress—with real-time vehicle dynamics such as driving patterns and erratic behavior.

This enables a dual-layered support system:

- **Conversational AI Co-Pilot**: Offers real-time, context-aware assistance to manage everyday fatigue and stress. Whether it's suggesting alternate routes during traffic congestion or playing soothing music, it adapts to the driver's needs.
- **Emergency Event Detection System**: Goes beyond basic inactivity alerts to detect serious medical emergencies, collisions, or sudden loss of control. It automatically activates safety protocols to stabilize the vehicle and summon help.

VigilanceAI transforms driver assistance from passive monitoring to active care—serving as a trusted companion on every journey.

## Problem Statement

**AI-Enhanced Driver Wellness Monitoring**

>Fatigue and stress significantly reduce driver alertness, increasing the risk of accidents. Using cabin video, steering behavior, and optional wearables, create a solution that detects drowsiness or stress levels and suggests safe, non-distracting interventions to keep drivers and passengers safe.

---

## Key Features

### 1. Real-Time Driver & Vehicle Monitoring
- **Multimodal Fatigue Detection**: Eye-blink rate (PERCLOS), yawning, head position, and steering behavior.
- **Facial Emotion Recognition (FER)**: Detects stress, distraction, and cognitive load.
- **Erratic Driving Pattern Analysis**: Monitors lane discipline, acceleration, and steering input.
- **Vehicle Anomaly Detection**: Uses G-force and gyroscopic data to detect collisions or loss of control.

### 2. Proactive AI Co-Pilot
- **Conversational AI**: Offers context-aware suggestions like calming music or alternate routes.
- **Personalized Wellness Baseline**: Learns driver habits for tailored interventions.
- **Non-Intrusive Alerts**: Avoids startling alarms, focusing on supportive dialogue.

### 3. Automated Emergency Response
- **Critical Event Detection**: Identifies medical emergencies, rollovers, and high-G impacts.
- **Vehicle Securement Protocol**: Activates hazard lights, controlled braking, and lane assist.
- **Emergency eCall**: Sends GPS and event data to responders and emergency contacts.

---

## Architecture Overview

![Architecture Diagram](https://github.com/user-attachments/assets/7543fddb-9264-492d-9f38-e3716281f96f)

---

## Process Flow

![Process Flow](https://github.com/user-attachments/assets/8418a9f4-dd7d-480e-9827-a54178245812)

---

## Wireframes

| Dashboard | Wellness Monitor | Emergency Protocol | AI Co-Pilot |
|----------|------------------|--------------------|-------------|
| ![](https://github.com/user-attachments/assets/eb3d2d55-dc38-4055-812a-27bb8c70ee55) | ![](https://github.com/user-attachments/assets/d522455b-b064-4a53-b152-0bca2df6e2c4) | ![](https://github.com/user-attachments/assets/48361d5d-ca96-48f3-a3aa-8161036d3b24) | ![](https://github.com/user-attachments/assets/966ff889-2ca3-4104-a76d-1fc13b98e6d8) |

---

## Technologies Used

### AI & ML Core
- Python, TensorFlow, PyTorch, OpenCV
- Scikit-learn for wellness score fusion

### Backend & Simulation
- FastAPI / Flask for backend logic
- CARLA Simulator for testing
- NumPy / Pandas for sensor data analysis

### Embedded Integration
- Raspberry Pi, CAN Bus, OBD-II
- Infrared cameras, microphones, and sensors
  
---


## Made with 💗 for Volkswagen- i.mobilothon-5.0 
