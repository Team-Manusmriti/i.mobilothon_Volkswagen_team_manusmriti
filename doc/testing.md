# VigilanceAI Testing Guide

Comprehensive testing guide for all VigilanceAI components including test scripts, validation procedures, and performance benchmarks.

## Testing Overview

VigilanceAI includes multiple testing scripts for different components:
- **Driver Monitoring**: Webcam-based and CARLA-integrated testing
- **Vehicle Simulation**: CARLA integration and crash detection
- **Frontend**: Web application and mobile app testing
- **Backend**: API endpoints and WebSocket connections

## Test Scripts Directory

### Backend/CARLA Tests (`src/carla/`)

| Script | Purpose | Usage | Dependencies |
|--------|---------|-------|--------------|
| `test_n.py` | Webcam driver monitoring (offline mode) | `python test_n.py` | Webcam, dlib model |
| `test_p.py` | CARLA blueprint discovery | `python test_p.py` | CARLA server |
| `test_crash.py` | Collision detection in CARLA | `python test_crash.py` | CARLA server, pygame |
| `test2.py` | Additional CARLA tests | `python test2.py` | CARLA server |
| `app.py` | Full backend server with WebSocket | `python app.py` | All dependencies |
| `main.py` | Basic backend entry point | `python main.py` | Minimal setup |

## Detailed Test Descriptions

### 1. Webcam Driver Monitoring (`test_n.py`)

**Purpose**: Tests driver monitoring using system webcam without CARLA dependency.

**Features Tested**:
- Eye Aspect Ratio (EAR) calculation for drowsiness detection
- Mouth Aspect Ratio (MAR) for yawn detection  
- Facial emotion recognition using DeepFace
- Head pose estimation with dlib landmarks
- Voice assistant integration with speech recognition
- Real-time fatigue and stress level calculation

**How to Run**:
```bash
cd src/carla
python test_n.py
```

**Expected Output**:
- Live webcam feed with overlay metrics
- Real-time EAR/MAR values
- Drowsiness state detection (Alert/Drowsy/Unknown)
- Emotion recognition (happy, sad, angry, etc.)
- Voice commands: "how am i", "status", "exit"

**Key Metrics**:
- EAR Threshold: 0.22 (below = drowsy)
- MAR Threshold: 0.65 (above = yawning)
- Blink Limit: 40 (fatigue detection)

### 2. CARLA Blueprint Discovery (`test_p.py`)

**Purpose**: Discovers available CARLA blueprints for particles and static props.

**Features Tested**:
- CARLA server connection
- Blueprint library access
- Particle system availability
- Static prop enumeration

**How to Run**:
```bash
# Start CARLA first
CarlaUE4.exe -windowed

# Run test
cd src/carla  
python test_p.py
```

**Expected Output**:
```
--- 1. Available 'particle' blueprints ---
static.prop.particle.smoke
static.prop.particle.fire

--- 2. Available 'static.prop' blueprints ---
static.prop.wall01
static.prop.ramp
```

### 3. Collision Detection (`test_crash.py`)

**Purpose**: Tests vehicle collision detection and crash response in CARLA.

**Features Tested**:
- Vehicle spawning and manual control
- Collision sensor attachment
- Real-time collision event detection
- Manual driving with WASD controls
- Spectator camera following

**How to Run**:
```bash
# Start CARLA first
CarlaUE4.exe -windowed

# Run crash test
cd src/carla
python test_crash.py
```

**Controls**:
- `W`: Accelerate forward
- `S`: Reverse
- `A`: Steer left  
- `D`: Steer right
- `ESC`: Exit simulation

**Expected Output**:
- Vehicle spawned in CARLA world
- Manual control enabled
- Collision detection: "--- CRASHED! --- Vehicle collided with: [object_type]"

### 4. Full Backend Server (`app.py`)

**Purpose**: Complete VigilanceAI backend with CARLA integration and WebSocket streaming.

**Features Tested**:
- CARLA vehicle spawning and sensor attachment
- Real-time driver behavior analysis
- WebSocket telemetry streaming
- Vehicle state monitoring
- Behavioral pattern analysis

**How to Run**:
```bash
# Start CARLA first
CarlaUE4.exe -windowed

# Run backend server
cd src/carla
python app.py
```

**API Endpoints**:
- `GET /`: Health check
- `GET /vehicle/state`: Current vehicle telemetry
- `WebSocket /ws/telemetry`: Real-time behavior streaming

**Expected Output**:
```
Starting VigilanceAI Backend...
Connected to CARLA server at localhost:2000
Spawned vehicle: vehicle.tesla.model3
Attached driver monitoring camera
CARLA integration ready
```

### 5. CARLA Driver Monitor (`carla_driver_monitor.py`)

**Purpose**: Integrated driver monitoring with CARLA vehicle simulation.

**Features Tested**:
- CARLA camera sensor integration
- Real-time face detection and analysis
- Driver state logging to CSV
- Head pose estimation
- Emotion and stress detection
- Attention state monitoring

**How to Run**:
```bash
# Ensure CARLA is running with a vehicle
cd src/carla
python carla_driver_monitor.py
```

**Output Files**:
- `driver_monitor_log.csv`: Detailed monitoring data
- `driver_state.json`: Current driver state for voice assistant

### 6. Drowsiness Detection (`drowsiness_fatigue.py`)

**Purpose**: Advanced drowsiness and fatigue detection with CARLA integration.

**Features Tested**:
- Multi-modal fatigue detection
- Smoothed head pose tracking
- Attention state classification
- Real-time logging and state export
- Integration with voice assistant

**How to Run**:
```bash
# Ensure CARLA vehicle is available
cd src/carla
python drowsiness_fatigue.py
```

**Key Features**:
- Smoothed head pose with configurable thresholds
- Distraction detection based on gaze direction
- Fatigue scoring with temporal analysis
- JSON state export for external systems

## Frontend Testing

### Web Application (`src/frontend/website/`)

**Development Server**:
```bash
cd src/frontend/website
npm run dev
```

**Build Testing**:
```bash
npm run build
npm run preview
```

**Component Tests**:
- Dashboard real-time updates
- WebSocket connection stability
- Responsive design validation
- Cross-browser compatibility

### Mobile Application (`src/frontend/app/`)

**Build and Test**:
```bash
cd src/frontend/app
./gradlew build
./gradlew test
```

**Device Testing**:
- Install APK on Android device
- Test automotive integration
- Validate UI responsiveness

## Integration Testing

### End-to-End Workflow

1. **Start CARLA Server**:
   ```bash
   CarlaUE4.exe -windowed -ResX=1280 -ResY=720
   ```

2. **Launch Backend**:
   ```bash
   cd src/carla
   python app.py
   ```

3. **Start Frontend**:
   ```bash
   cd src/frontend/website
   npm run dev
   ```

4. **Validate Data Flow**:
   - Check WebSocket connection in browser console
   - Verify real-time telemetry updates
   - Test emergency protocol activation

### Performance Benchmarks

**Target Metrics**:
- Frame Processing: 30 FPS minimum
- WebSocket Latency: <100ms
- Memory Usage: <2GB total
- CPU Usage: <50% on modern hardware

**Monitoring Commands**:
```bash
# Monitor system resources
htop  # Linux
taskmgr  # Windows

# Check network connections
netstat -an | grep 8000
```

## Test Validation Checklist

### Driver Monitoring
- [ ] EAR calculation accuracy (±0.01)
- [ ] Blink detection reliability (>95%)
- [ ] Emotion recognition confidence (>80%)
- [ ] Head pose estimation precision (±5°)
- [ ] Voice command recognition (>90%)

### Vehicle Integration  
- [ ] CARLA connection stability
- [ ] Vehicle spawning success
- [ ] Sensor attachment verification
- [ ] Collision detection accuracy
- [ ] Manual control responsiveness

### System Integration
- [ ] WebSocket connection stability
- [ ] Real-time data streaming (10Hz)
- [ ] Frontend-backend synchronization
- [ ] Emergency protocol activation
- [ ] Cross-platform compatibility

## Troubleshooting Test Issues

### Common Test Failures

**Camera Access Denied**:
```bash
# Grant camera permissions
sudo chmod 666 /dev/video0  # Linux
# Check Privacy settings on Windows/Mac
```

**CARLA Connection Timeout**:
```bash
# Verify CARLA is running
netstat -an | grep 2000
# Check firewall settings
# Restart CARLA server
```

**Missing Dependencies**:
```bash
# Reinstall requirements
pip install -r requirements.txt
# Download dlib model
wget https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2
```

**Performance Issues**:
```python
# Reduce processing load
EMOTION_INTERVAL = 60  # Increase interval
FRAME_SKIP = 2  # Process every 2nd frame
```

## Automated Testing

### Continuous Integration
```yaml
# .github/workflows/test.yml
name: VigilanceAI Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: pip install -r src/carla/requirements.txt
      - name: Run unit tests
        run: python -m pytest tests/
```

### Test Coverage
```bash
# Install coverage tools
pip install pytest coverage

# Run with coverage
coverage run -m pytest tests/
coverage report
coverage html
```

## Performance Testing

### Load Testing
```bash
# Test WebSocket connections
python scripts/load_test_websocket.py --connections 10

# Monitor resource usage
python scripts/monitor_performance.py --duration 300
```

### Stress Testing
```bash
# High-frequency data processing
python test_stress.py --fps 60 --duration 600

# Memory leak detection  
python test_memory.py --iterations 1000
```

## Test Reports

### Generate Test Report
```bash
# Run all tests and generate report
python scripts/run_all_tests.py --output test_report.html
```

**Report Includes**:
- Component test results
- Performance benchmarks
- Error logs and diagnostics
- Recommendations for optimization

---

*Part of VigilanceAI - Built with ❤️ for Volkswagen - i.mobilothon-5.0*