# VigilanceAI

VigilanceAI redefines driver safety by replacing reactive alerts with proactive, emotionally aware intelligence. It creates a closed-loop system that not only detects risk but actively supports and protects the driver throughout the journey.

This repository contains the VigilanceAI Android/in-vehicle application and modules used to sense driver state, assess risk, and intervene with context-aware assistance.

## Key ideas (one-liner)

- Replace point alerts with proactive coaching and mitigation.
- Combine driver affect (emotion, stress, fatigue) with driving context to calculate risk.
- Close the loop: observe, assess, assist, monitor response, and adapt.

## Quick features

- Real-time driver state detection: drowsiness, distraction, stress, emotions.
- Risk scoring and prioritized interventions (voice, haptics, UI, vehicle-level actions).
- Session logging and anonymized telemetry for analytics and model improvement.
- Extensible architecture for on-device and cloud components.

## Architecture — conceptual overview

The VigilanceAI architecture is split into four main layers: Sensors, Edge Processing, Decision & Intervention, and Cloud Services. The system is designed for low-latency safety-critical response while enabling cloud-assisted learning and analytics.

### High-level ASCII diagram

Sensors  ->  Edge Processing  ->  Decision & Intervention  ->  Vehicle/User
    |              |                      |                    |
    |              |                      |                    +--> Haptic/Audio/UI
    |              |                      |                    +--> Vehicle controls (when available)
    v              v                      v
 (Cameras,  ->  (Preprocessing,    ->  (Risk Engine,        ->  Feedback loops &
    IMU, CAN,      Feature extraction,    Intervention Manager,      Adaptation)
    Microphone)    ML inference)           Policy/Planner)
                                                |                      |
                                                v                      v
                                        On-device models      Telemetry & Model updates
                                                |                      |
                                                +----> Secure Sync ----+

### Components

- Sensors
    - Driver-facing camera(s): face landmarks, gaze, blink rate, head pose.
    - Microphone: voice stress and speech cues (optional, privacy-controlled).
    - Vehicle bus (CAN/OBD): speed, steering, lane-keep assist state, indicators.
    - IMU: accelerometer/gyroscope for sudden maneuvers.

- Edge Processing (on-device)
    - Preprocessing pipeline: camera frame decoding, denoising, normalization.
    - Feature extractors: facial landmarks, eye aspect ratio, head pose, lane position.
    - On-device ML models: emotion detector, drowsiness detector, distraction classifier.
    - Low-latency inference optimized for mobile/embedded (TFLite/ONNX/Rust).

- Decision & Intervention
    - Risk Engine: fuses model outputs, vehicle state, and context to compute a risk score and priority.
    - Policy/Planner: maps risk states to safe interventions (e.g., gentle voice prompt → escalate to haptic alert → request partial autonomy engagement or stop vehicle when supported).
    - Intervention Manager: executes interventions via the app UI, voice, haptics, and optional vehicle integration.
    - Closed-loop feedback: monitors driver response and adapts the intervention strategy.

- Cloud Services (optional)
    - Telemetry ingestion (anonymized): safety events, aggregated metrics, model telemetry.
    - Model management: retrain and push incremental model updates (safe rollout strategies).
    - Analytics & dashboarding: fleet-level insights, safety reports.

### Data flow (step-by-step)

1. Capture sensor data (camera frame, IMU, CAN) on-device.
2. Preprocess and extract features (face keypoints, blink, gaze, speed, lane).
3. Run lightweight ML models to estimate driver state and affect.
4. Risk Engine fuses multi-modal signals with contextual heuristics to compute a risk score.
5. Policy decides the minimal effective intervention based on risk severity and user preferences.
6. Intervention Manager executes (e.g., voice suggestion, haptic vibration, UI prompt, route reroute, request stop).
7. System monitors driver response. If no improvement, escalate per policy. Collect anonymized signals for cloud analytics.

## Small contract (inputs/outputs)

- Inputs: video frames (driver-facing), audio (opt-in), vehicle telemetry (speed, steering), timestamps, route/context.
- Outputs: risk_score (0.0–1.0), state_tags (drowsy, distracted, stressed, angry), recommended_action (string), intervention_level (low/med/high), event logs.
- Error modes: missing camera, poor lighting, sensor failure — system should gracefully degrade to telemetry-only heuristics.

## Edge cases and design considerations

- Low/no camera visibility: fall back to vehicle telemetry and prior state.
- False positives: policy should prefer gentle, reversible interventions first.
- Privacy: raw camera/audio should never be uploaded by default. Use on-device processing + opt-in telemetry with clear user controls.
- Latency: safety interventions must be local and low latency; cloud assists non-critical analytics and model updates.

## Security & privacy

- Raw video/audio are processed locally by default and not stored or transmitted without explicit consent.
- Telemetry is anonymized/hashed and uploaded over TLS using authenticated endpoints.
- Access controls and encryption for stored model weights and logs.

## Where this repository fits

- The Android/Car App module contains UI, services, and the integration glue that runs edge inference and the Intervention Manager.
- Native/model assets and TFLite models live in the `assets/` or `models/` folder of the app module.

## Development & running (high-level)

Prerequisites
- JDK 11 or compatible (per project Gradle settings).
- Android Studio Bumblebee or later for Android/Car App development.

Build and run

1. Open the project in Android Studio.
2. Select the app module and run on a compatible Android device or emulator (camera access required for driver-facing features).
3. For on-device model debugging, use Android Studio's profiler and adb logcat to view inference latency and logs.

Note: This repo uses Gradle Kotlin DSL. If you prefer CLI:

```bash
./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Testing
- Unit test the viewmodels and risk-engine logic.
- For model verification, use a small evaluation harness (TFLite test runner) with representative datasets.

## Developer tips

- Keep ML inference code and policy logic modular and well-tested.
- Implement feature flags for rollout of aggressive interventions.
- Use simulator replay data to iterate on policy without exposing real users.

## Contributing

- If you'd like to contribute, please open an issue describing the feature or bug first.
- Follow the repo's code style and include tests for new logic.

## Roadmap / Next steps

- Add a safe simulated environment for policy validation (closed-loop simulation).
- Implement secure OTA model updates with A/B rollout and canary testing.
- Expand vehicle integrations for controlled vehicle actions where supported.

## Files & structure (quick reference)

- `automotive/` — app modules and Gradle configuration for Android Automotive/Car App.
- `build.gradle.kts`, `settings.gradle.kts` — top-level Gradle config.





