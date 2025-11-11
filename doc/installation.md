# VigilanceAI Installation Guide

Complete installation and setup guide for VigilanceAI - AI-Enhanced Driver Wellness Monitoring system.

## Prerequisites

### System Requirements
- **OS**: Windows 10/11, Linux (Ubuntu 18.04+), macOS 10.15+
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **GPU**: NVIDIA RTX 3070/3080/3090 / NVIDIA RTX 4090 or better
- **VRAM**: 16 Gb or more VRAM
- **Webcam**: For driver monitoring (built-in or external)

### Required Software
- **CARLA Simulator**: 0.9.13+ (for vehicle simulation)
- **Git**: For version control

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/team-manusmriti/i.mobilothon_Volkswagen_team_manusmriti.git
cd i.mobilothon_Volkswagen_team_manusmriti
```

### 2. Backend Setup (Python/CARLA)

#### Install Python Dependencies
```bash
cd src/carla
pip install -r requirements.txt
```

#### Download Required Models
1. **Dlib Face Landmarks Model**:
   - Download `shape_predictor_68_face_landmarks.dat` from [dlib-models](https://github.com/davisking/dlib-models)
   - Place in `src/carla/models/` directory

#### CARLA Simulator Setup
1. **Download CARLA**:
   - Visit [CARLA Releases](https://github.com/carla-simulator/carla/releases)
   - Download CARLA 0.9.13+ for your platform
   - Extract to desired location

2. **Start CARLA Server**:
   ```bash
   # Windows
   CarlaUE4.exe -windowed -ResX=800 -ResY=600

   # Linux
   ./CarlaUE4.sh -windowed -ResX=800 -ResY=600
   ```

### 3. Frontend Setup (React Web App)

#### Install Dependencies
```bash
cd src/frontend/website
npm install
```

#### Environment Configuration
Create `.env` file in `src/frontend/website/`:
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### 4. Mobile App Setup (Android)

#### Prerequisites
- **Android Studio**: Latest version
- **Flutter SDK**: 3.0+ (if using Flutter components)
- **Java JDK**: 11 or higher

#### Build Configuration
```bash
cd src/frontend/app
./gradlew build
```

## Component Configuration

### Backend Configuration
Edit `src/carla/app.py` for custom settings:
```python
# CARLA Connection
CARLA_HOST = "localhost"
CARLA_PORT = 2000

# API Settings
API_HOST = "0.0.0.0"
API_PORT = 8000

# Monitoring Thresholds
EAR_THRESHOLD = 0.21
MAR_THRESHOLD = 0.6
FATIGUE_BLINK_LIMIT = 40
```

### Frontend Configuration
Edit `src/frontend/website/src/config.js`:
```javascript
export const config = {
  apiUrl: process.env.VITE_API_URL || 'http://localhost:8000',
  wsUrl: process.env.VITE_WS_URL || 'ws://localhost:8000',
  updateInterval: 100, // ms
  alertThresholds: {
    fatigue: 70,
    stress: 60
  }
};
```

## Verification

### 1. Test Backend Connection
```bash
cd src/carla
python app.py
```
Expected output: `Starting VigilanceAI Backend...`

### 2. Test Frontend
```bash
cd src/frontend/website
npm run dev
```
Access: `http://localhost:5173`

### 3. Test CARLA Integration
```bash
cd src/carla
python test_p.py  # Test CARLA connection
```

## Troubleshooting

### Common Issues

#### CARLA Connection Failed
- Ensure CARLA server is running on port 2000
- Check firewall settings
- Verify CARLA version compatibility

#### Dlib Model Missing
```bash
# Download and place model file
wget https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
mv shape_predictor_68_face_landmarks.dat src/carla/models/
```

#### Camera Access Denied
- Grant camera permissions to terminal/IDE
- Check if camera is used by another application
- Test with `python test_n.py` (webcam mode)

#### Port Conflicts
- Backend (8000): Change in `app.py`
- Frontend (5173): Change in `vite.config.js`
- CARLA (2000): Start with `-rpc-port=2001`

### Performance Optimization

#### For Low-End Systems
```python
# Reduce processing frequency
EMOTION_INTERVAL = 60  # Increase from 30
FRAME_SKIP = 2  # Process every 2nd frame
```

#### For High-End Systems
```python
# Enable GPU acceleration
USE_GPU = True
BATCH_SIZE = 4
PARALLEL_PROCESSING = True
```

## Development Setup

### IDE Configuration
**VS Code Extensions**:
- Python
- React
- Tailwind CSS IntelliSense
- GitLens

### Debug Configuration
Create `.vscode/launch.json`:
```json
{
  "configurations": [
    {
      "name": "Backend Debug",
      "type": "python",
      "request": "launch",
      "program": "src/carla/app.py",
      "console": "integratedTerminal"
    }
  ]
}
```

## Next Steps

After successful installation:
1. Review [Testing Guide](testing.md) for component testing
2. Check [API Reference](api_reference.md) for integration details
3. Explore [Implementation Guide](implementation.md) for deployment

## Support

For installation issues:
- Check [GitHub Issues](https://github.com/team-manusmriti/i.mobilothon_Volkswagen_team_manusmriti/issues)
- Review component-specific documentation
- Contact team for technical support

---

*Part of VigilanceAI - Built with ❤️ for Volkswagen - i.mobilothon-5.0*