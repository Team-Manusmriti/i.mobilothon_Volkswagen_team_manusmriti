"""
VigilanceAI Backend - CARLA Integration Server
Provides real-time vehicle behavior data from CARLA simulator
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np
import cv2

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import carla

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VigilanceAI Backend")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
active_connections: List[WebSocket] = []
carla_client = None
carla_world = None
vehicle = None
camera_sensors = {}
behavior_analyzer = None


class DriverBehaviorData(BaseModel):
    """Driver behavior telemetry data"""
    eyeClosure: float
    yawnDetected: bool
    headPose: str
    gazeDirection: str
    blinkRate: float
    emotionalState: str
    stressLevel: float
    fatigueLevel: float
    heartRate: float
    laneDeviation: float
    steeringStability: float
    speedConsistency: float
    timestamp: str


class VehicleState(BaseModel):
    """Current vehicle state from CARLA"""
    velocity: float
    acceleration: float
    steering_angle: float
    throttle: float
    brake: float
    location: Dict[str, float]
    rotation: Dict[str, float]
    gear: int
    rpm: float


class CARLAManager:
    """Manages CARLA simulator connection and vehicle control"""
    
    def __init__(self, host='localhost', port=2000):
        self.host = host
        self.port = port
        self.client = None
        self.world = None
        self.vehicle = None
        self.sensors = {}
        self.running = False
        
    async def connect(self):
        """Connect to CARLA simulator"""
        try:
            self.client = carla.Client(self.host, self.port)
            self.client.set_timeout(10.0)
            self.world = self.client.get_world()
            logger.info(f"Connected to CARLA server at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to CARLA: {e}")
            return False
    
    async def spawn_vehicle(self):
        """Spawn ego vehicle in CARLA world"""
        try:
            # Get vehicle blueprint
            blueprint_library = self.world.get_blueprint_library()
            vehicle_bp = blueprint_library.filter('vehicle.*')[0]
            
            # Get spawn point
            spawn_points = self.world.get_map().get_spawn_points()
            spawn_point = spawn_points[0] if spawn_points else carla.Transform()
            
            # Spawn vehicle
            self.vehicle = self.world.spawn_actor(vehicle_bp, spawn_point)
            self.vehicle.set_autopilot(True)  # Enable autopilot for simulation
            
            logger.info(f"Spawned vehicle: {vehicle_bp.id}")
            return True
        except Exception as e:
            logger.error(f"Failed to spawn vehicle: {e}")
            return False
    
    async def attach_sensors(self):
        """Attach camera sensors to vehicle for driver monitoring"""
        try:
            blueprint_library = self.world.get_blueprint_library()
            
            # RGB Camera for face detection (dashboard-mounted)
            camera_bp = blueprint_library.find('sensor.camera.rgb')
            camera_bp.set_attribute('image_size_x', '800')
            camera_bp.set_attribute('image_size_y', '600')
            camera_bp.set_attribute('fov', '90')
            
            # Mount camera facing driver (adjust transform as needed)
            camera_transform = carla.Transform(
                carla.Location(x=0.5, y=0.0, z=1.2),
                carla.Rotation(pitch=0, yaw=180, roll=0)
            )
            
            camera = self.world.spawn_actor(
                camera_bp, 
                camera_transform, 
                attach_to=self.vehicle
            )
            
            self.sensors['driver_camera'] = camera
            logger.info("Attached driver monitoring camera")
            
            return True
        except Exception as e:
            logger.error(f"Failed to attach sensors: {e}")
            return False
    
    def get_vehicle_state(self) -> Optional[VehicleState]:
        """Get current vehicle state from CARLA"""
        if not self.vehicle:
            return None
        
        try:
            transform = self.vehicle.get_transform()
            velocity = self.vehicle.get_velocity()
            control = self.vehicle.get_control()
            
            speed = 3.6 * np.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2)  # km/h
            
            return VehicleState(
                velocity=speed,
                acceleration=self.vehicle.get_acceleration().length(),
                steering_angle=control.steer,
                throttle=control.throttle,
                brake=control.brake,
                location={
                    'x': transform.location.x,
                    'y': transform.location.y,
                    'z': transform.location.z
                },
                rotation={
                    'pitch': transform.rotation.pitch,
                    'yaw': transform.rotation.yaw,
                    'roll': transform.rotation.roll
                },
                gear=0,  # CARLA doesn't expose gear directly
                rpm=0    # CARLA doesn't expose RPM directly
            )
        except Exception as e:
            logger.error(f"Error getting vehicle state: {e}")
            return None
    
    def cleanup(self):
        """Clean up CARLA actors"""
        try:
            if self.sensors:
                for sensor in self.sensors.values():
                    if sensor.is_alive:
                        sensor.destroy()
            
            if self.vehicle and self.vehicle.is_alive:
                self.vehicle.destroy()
            
            logger.info("CARLA cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


class BehaviorAnalyzer:
    """Analyzes driver behavior from vehicle telemetry and sensor data"""
    
    def __init__(self):
        self.fatigue_baseline = 20.0
        self.stress_baseline = 30.0
        self.lane_deviation_history = []
        self.steering_history = []
        self.speed_history = []
        self.eye_closure_history = []
        
        # Load face detection model (for driver monitoring simulation)
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
        except Exception as e:
            logger.warning(f"Could not load CV models: {e}")
            self.face_cascade = None
            self.eye_cascade = None
    
    def analyze_from_vehicle_state(self, vehicle_state: VehicleState) -> DriverBehaviorData:
        """Generate driver behavior data from vehicle telemetry"""
        
        # Analyze driving patterns
        self.steering_history.append(abs(vehicle_state.steering_angle))
        self.speed_history.append(vehicle_state.velocity)
        
        if len(self.steering_history) > 50:
            self.steering_history.pop(0)
        if len(self.speed_history) > 50:
            self.speed_history.pop(0)
        
        # Calculate metrics
        steering_stability = self._calculate_steering_stability()
        speed_consistency = self._calculate_speed_consistency()
        lane_deviation = self._estimate_lane_deviation(vehicle_state)
        
        # Estimate fatigue from driving behavior
        fatigue_level = self._estimate_fatigue(
            steering_stability, 
            speed_consistency, 
            lane_deviation
        )
        
        # Estimate stress from driving aggression
        stress_level = self._estimate_stress(vehicle_state)
        
        # Simulate eye closure based on fatigue
        eye_closure = min(80, max(0, fatigue_level * 0.7 + np.random.normal(0, 5)))
        
        # Detect yawning (probabilistic based on fatigue)
        yawn_detected = np.random.random() < (fatigue_level / 200.0)
        
        # Simulate head pose based on fatigue and distraction
        head_pose = self._estimate_head_pose(fatigue_level, stress_level)
        
        # Simulate gaze direction
        gaze_direction = self._estimate_gaze_direction(stress_level, lane_deviation)
        
        # Calculate blink rate (inversely related to fatigue)
        blink_rate = max(5, min(30, 18 - (fatigue_level / 10) + np.random.normal(0, 2)))
        
        # Emotional state
        emotional_state = self._determine_emotional_state(stress_level, fatigue_level)
        
        # Heart rate simulation
        heart_rate = self._simulate_heart_rate(stress_level, vehicle_state.velocity)
        
        return DriverBehaviorData(
            eyeClosure=round(eye_closure, 1),
            yawnDetected=yawn_detected,
            headPose=head_pose,
            gazeDirection=gaze_direction,
            blinkRate=round(blink_rate, 1),
            emotionalState=emotional_state,
            stressLevel=round(stress_level, 1),
            fatigueLevel=round(fatigue_level, 1),
            heartRate=round(heart_rate, 1),
            laneDeviation=round(lane_deviation, 1),
            steeringStability=round(steering_stability, 1),
            speedConsistency=round(speed_consistency, 1),
            timestamp=datetime.now().isoformat()
        )
    
    def _calculate_steering_stability(self) -> float:
        """Calculate steering stability (0-100, higher is more stable)"""
        if len(self.steering_history) < 10:
            return 100.0
        
        # Calculate standard deviation of steering inputs
        std_dev = np.std(self.steering_history[-20:])
        stability = max(0, 100 - (std_dev * 200))
        return stability
    
    def _calculate_speed_consistency(self) -> float:
        """Calculate speed consistency (0-100, higher is more consistent)"""
        if len(self.speed_history) < 10:
            return 100.0
        
        # Calculate coefficient of variation
        mean_speed = np.mean(self.speed_history[-20:])
        if mean_speed < 5:  # Vehicle stopped or very slow
            return 100.0
        
        std_dev = np.std(self.speed_history[-20:])
        cv = (std_dev / mean_speed) * 100
        consistency = max(0, 100 - (cv * 10))
        return consistency
    
    def _estimate_lane_deviation(self, vehicle_state: VehicleState) -> float:
        """Estimate lane deviation from steering patterns"""
        # In real implementation, use lane detection from camera
        # Here we estimate from steering angle magnitude
        deviation = abs(vehicle_state.steering_angle) * 50
        deviation += np.random.normal(0, 5)
        return max(0, min(100, deviation))
    
    def _estimate_fatigue(self, steering_stability: float, 
                         speed_consistency: float, 
                         lane_deviation: float) -> float:
        """Estimate fatigue level from driving patterns"""
        # Poor stability and consistency indicate fatigue
        fatigue = self.fatigue_baseline
        fatigue += (100 - steering_stability) * 0.3
        fatigue += (100 - speed_consistency) * 0.2
        fatigue += lane_deviation * 0.3
        
        # Add temporal increase (fatigue increases over time)
        fatigue += np.random.normal(0, 2)
        
        # Gradual increase with noise
        self.fatigue_baseline = min(95, self.fatigue_baseline + 0.05)
        
        return max(0, min(100, fatigue))
    
    def _estimate_stress(self, vehicle_state: VehicleState) -> float:
        """Estimate stress from driving aggression"""
        stress = self.stress_baseline
        
        # Aggressive throttle/brake usage indicates stress
        stress += vehicle_state.throttle * 20
        stress += vehicle_state.brake * 30
        stress += abs(vehicle_state.steering_angle) * 25
        
        # Random fluctuation
        stress += np.random.normal(0, 5)
        
        self.stress_baseline = max(10, min(90, 
            self.stress_baseline + np.random.normal(0, 1)))
        
        return max(0, min(100, stress))
    
    def _estimate_head_pose(self, fatigue: float, stress: float) -> str:
        """Estimate head pose from behavior"""
        if fatigue > 70:
            return 'down' if np.random.random() > 0.7 else 'forward'
        elif stress > 70:
            return 'sideways' if np.random.random() > 0.85 else 'forward'
        else:
            return 'forward'
    
    def _estimate_gaze_direction(self, stress: float, lane_deviation: float) -> str:
        """Estimate gaze direction"""
        if lane_deviation > 50:
            return 'away' if np.random.random() > 0.7 else 'road'
        elif stress > 60:
            return 'phone' if np.random.random() > 0.9 else 'road'
        else:
            return 'road'
    
    def _determine_emotional_state(self, stress: float, fatigue: float) -> str:
        """Determine emotional state"""
        if stress > 70:
            return 'stressed'
        elif fatigue > 60:
            return 'tired'
        else:
            return 'neutral'
    
    def _simulate_heart_rate(self, stress: float, speed: float) -> float:
        """Simulate heart rate based on stress and speed"""
        base_hr = 70
        stress_hr = (stress / 100) * 30
        speed_hr = min(15, (speed / 100) * 10)
        
        hr = base_hr + stress_hr + speed_hr + np.random.normal(0, 3)
        return max(60, min(110, hr))


# Global instances
carla_manager = CARLAManager()
behavior_analyzer = BehaviorAnalyzer()


@app.on_event("startup")
async def startup_event():
    """Initialize CARLA connection on startup"""
    logger.info("Starting VigilanceAI Backend...")
    
    # Try to connect to CARLA
    connected = await carla_manager.connect()
    if connected:
        await carla_manager.spawn_vehicle()
        await carla_manager.attach_sensors()
        logger.info("CARLA integration ready")
    else:
        logger.warning("CARLA not available - running in simulation mode")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down...")
    carla_manager.cleanup()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "carla_connected": carla_manager.vehicle is not None,
        "active_connections": len(active_connections)
    }


@app.get("/vehicle/state")
async def get_vehicle_state():
    """Get current vehicle state"""
    state = carla_manager.get_vehicle_state()
    if state:
        return state
    return {"error": "Vehicle not available"}


@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    """WebSocket endpoint for real-time telemetry streaming"""
    await websocket.accept()
    active_connections.append(websocket)
    
    logger.info(f"Client connected. Total connections: {len(active_connections)}")
    
    try:
        while True:
            # Get vehicle state from CARLA
            vehicle_state = carla_manager.get_vehicle_state()
            
            if vehicle_state:
                # Analyze driver behavior
                behavior_data = behavior_analyzer.analyze_from_vehicle_state(vehicle_state)
                
                # Send data to client
                await websocket.send_json({
                    "type": "behavior_update",
                    "data": behavior_data.dict()
                })
            else:
                # Fallback: send simulated data if CARLA not available
                simulated_data = generate_simulated_behavior()
                await websocket.send_json({
                    "type": "behavior_update",
                    "data": simulated_data
                })
            
            # Wait before next update (10 Hz update rate)
            await asyncio.sleep(0.1)
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(active_connections)}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


def generate_simulated_behavior() -> dict:
    """Generate simulated behavior data when CARLA is not available"""
    fatigue = np.random.uniform(20, 80)
    stress = np.random.uniform(20, 70)
    
    return {
        "eyeClosure": round(np.random.uniform(10, 60), 1),
        "yawnDetected": np.random.random() > 0.95,
        "headPose": np.random.choice(['forward', 'down', 'sideways'], p=[0.8, 0.15, 0.05]),
        "gazeDirection": np.random.choice(['road', 'phone', 'away'], p=[0.85, 0.10, 0.05]),
        "blinkRate": round(np.random.uniform(12, 22), 1),
        "emotionalState": 'stressed' if stress > 60 else ('tired' if fatigue > 60 else 'neutral'),
        "stressLevel": round(stress, 1),
        "fatigueLevel": round(fatigue, 1),
        "heartRate": round(np.random.uniform(65, 95), 1),
        "laneDeviation": round(np.random.uniform(10, 50), 1),
        "steeringStability": round(np.random.uniform(60, 100), 1),
        "speedConsistency": round(np.random.uniform(70, 100), 1),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)