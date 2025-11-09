# VigilanceAI API Reference

## Backend API Specification

The VigilanceAI backend provides RESTful APIs and WebSocket connections for real-time driver monitoring and vehicle telemetry.

**Base URL**: `http://localhost:8000`

## REST Endpoints

### Health Check
```http
GET /
```

**Response**:
```json
{
  "status": "running",
  "carla_connected": true,
  "active_connections": 2
}
```

### Vehicle State
```http
GET /vehicle/state
```

**Response**:
```json
{
  "velocity": 45.2,
  "acceleration": 2.1,
  "steering_angle": 0.15,
  "throttle": 0.6,
  "brake": 0.0,
  "location": {
    "x": 123.45,
    "y": 67.89,
    "z": 0.5
  },
  "rotation": {
    "pitch": 0.0,
    "yaw": 90.0,
    "roll": 0.0
  },
  "gear": 3,
  "rpm": 2500.0
}
```

## WebSocket Connections

### Real-Time Telemetry Stream
```
WebSocket: ws://localhost:8000/ws/telemetry
```

**Message Format**:
```json
{
  "type": "behavior_update",
  "data": {
    "eyeClosure": 25.5,
    "yawnDetected": false,
    "headPose": "forward",
    "gazeDirection": "road",
    "blinkRate": 18.2,
    "emotionalState": "neutral",
    "stressLevel": 32.1,
    "fatigueLevel": 28.7,
    "heartRate": 72.5,
    "laneDeviation": 15.3,
    "steeringStability": 85.2,
    "speedConsistency": 92.1,
    "timestamp": "2024-01-15T10:30:45.123Z"
  }
}
```

## Data Models

### DriverBehaviorData
| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `eyeClosure` | float | 0-100 | PERCLOS percentage |
| `yawnDetected` | boolean | - | Yawning detection flag |
| `headPose` | string | forward/down/sideways | Head orientation |
| `gazeDirection` | string | road/phone/away | Eye gaze direction |
| `blinkRate` | float | 5-30 | Blinks per minute |
| `emotionalState` | string | neutral/stressed/tired | Current emotion |
| `stressLevel` | float | 0-100 | Stress percentage |
| `fatigueLevel` | float | 0-100 | Fatigue percentage |
| `heartRate` | float | 60-110 | Heart rate (BPM) |
| `laneDeviation` | float | 0-100 | Lane keeping score |
| `steeringStability` | float | 0-100 | Steering consistency |
| `speedConsistency` | float | 0-100 | Speed maintenance |
| `timestamp` | string | ISO 8601 | Data timestamp |

### VehicleState
| Field | Type | Description |
|-------|------|-------------|
| `velocity` | float | Speed in km/h |
| `acceleration` | float | Acceleration magnitude |
| `steering_angle` | float | Steering input (-1 to 1) |
| `throttle` | float | Throttle position (0-1) |
| `brake` | float | Brake pressure (0-1) |
| `location` | object | GPS coordinates (x, y, z) |
| `rotation` | object | Vehicle orientation (pitch, yaw, roll) |
| `gear` | integer | Current gear |
| `rpm` | float | Engine RPM |

## Frontend Integration

### WebSocket Connection Example
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/telemetry');

ws.onopen = () => {
  console.log('Connected to VigilanceAI backend');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'behavior_update') {
    updateDashboard(message.data);
  }
};

ws.onclose = () => {
  console.log('Disconnected from backend');
  // Implement reconnection logic
};
```

### React Hook Example
```javascript
import { useState, useEffect } from 'react';

export function useWellnessData() {
  const [behaviorData, setBehaviorData] = useState(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/telemetry');
    
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'behavior_update') {
        setBehaviorData(message.data);
      }
    };

    return () => ws.close();
  }, []);

  return { behaviorData, connected };
}
```

## AI Processing Pipeline

### 1. Data Collection
- **Video Stream**: Cabin camera feed at 30 FPS
- **Vehicle Telemetry**: CAN bus data at 100 Hz
- **Sensor Fusion**: IMU, GPS, and environmental sensors

### 2. Feature Extraction
- **Facial Landmarks**: 68-point face detection
- **Eye Metrics**: PERCLOS calculation and blink detection
- **Emotion Analysis**: DeepFace emotion classification
- **Driving Patterns**: Steering and speed analysis

### 3. Behavioral Analysis
- **Fatigue Detection**: Multi-modal fatigue scoring
- **Stress Recognition**: Physiological and behavioral indicators
- **Attention Monitoring**: Gaze tracking and head pose
- **Anomaly Detection**: Unusual driving patterns

### 4. Decision Engine
- **Risk Assessment**: Real-time wellness scoring
- **Intervention Logic**: Context-aware response selection
- **Emergency Detection**: Critical event identification
- **Personalization**: Adaptive baseline adjustment

## Error Handling

### WebSocket Errors
```json
{
  "type": "error",
  "code": "CONNECTION_LOST",
  "message": "CARLA simulator disconnected",
  "timestamp": "2024-01-15T10:30:45.123Z"
}
```

### Common Error Codes
| Code | Description | Action |
|------|-------------|--------|
| `CONNECTION_LOST` | CARLA simulator disconnected | Switch to simulation mode |
| `SENSOR_ERROR` | Camera or sensor failure | Use fallback detection |
| `PROCESSING_ERROR` | AI model processing failed | Log error and continue |
| `INVALID_DATA` | Malformed telemetry data | Validate and sanitize |

## Performance Monitoring

### Metrics Endpoint
```http
GET /metrics
```

**Response**:
```json
{
  "processing_latency_ms": 45,
  "detection_accuracy": 0.95,
  "active_connections": 3,
  "frames_processed": 1500,
  "errors_count": 2,
  "uptime_seconds": 3600
}
```

### Health Checks
- **Latency**: <50ms for critical alerts
- **Accuracy**: >95% for fatigue detection
- **Availability**: 99.9% uptime target
- **Throughput**: 10 updates per second

## Documentation Navigation

| Document | Description |
|----------|-------------|
| [Implementation Guide](implementation.md) | Technical deployment and setup |
| [System Architecture](architecture.md) | Multi-layered system design |
| [Process Flow](process_flow.md) | Monitoring workflow and decision logic |
| [Interface Documentation](README.md#user-interface-documentation) | All UI specifications |

---

*Part of VigilanceAI - Built with ❤️ for Volkswagen - i.mobilothon-5.0*
---