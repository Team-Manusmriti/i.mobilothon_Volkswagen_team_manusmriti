# Head Pose Analysis + Traffic Analysis + Anomaly + Driving Patterns + Crash Detection
import carla
import random
import time
import os
import pygame
import csv

# --- NEW: Imports for Head Pose ---
import threading
import cv2
import dlib
import numpy as np

# --- Helper function to simplify actor type names (Unchanged) ---
def get_simple_collision_type(actor_type_id):
    if 'vehicle' in actor_type_id: return 'car'
    if 'pedestrian' in actor_type_id: return 'pedestrian'
    if 'pole' in actor_type_id or 'streetlamp' in actor_type_id: return 'pole'
    if 'wall' in actor_type_id or 'building' in actor_type_id: return 'building/wall'
    if 'trafficlight' in actor_type_id: return 'traffic_light'
    if 'static.vegetation' in actor_type_id: return 'vegetation'
    return 'other'

# --- Anomaly Detection function (Unchanged) ---
def detect_anomalies(control, speed_kmh):
    SPEEDING_THRESHOLD_KMH = 05.0 
    HARD_BRAKE_SPEED_KMH = 30.0 
    STUCK_SPEED_THRESHOLD_KMH = 1.0 
    STUCK_THROTTLE_THRESHOLD = 0.5 
    
    if control.brake == 1.0 and speed_kmh > HARD_BRAKE_SPEED_KMH: return "Hard_Brake"
    if control.throttle > STUCK_THROTTLE_THRESHOLD and speed_kmh < STUCK_SPEED_THRESHOLD_KMH: return "Stuck/Blocked"
    if speed_kmh > SPEEDING_THRESHOLD_KMH: return "Excessive_Speeding"
    return "None"

# --- Collision Callback (Unchanged) ---
def on_collision(event, state_dict):
    other_actor_type = get_simple_collision_type(event.other_actor.type_id)
    state_dict['collided_with'] = other_actor_type
    print(f"\n--- CRASH DETECTED! ---")
    print(f"Collided with: {other_actor_type}")

# --- AI Traffic Spawner (Unchanged) ---
def spawn_ai_traffic(client, world, num_vehicles):
    print(f"Spawning {num_vehicles} AI vehicles...")
    traffic_actor_list = []
    vehicle_bps = world.get_blueprint_library().filter('vehicle.*')
    spawn_points = world.get_map().get_spawn_points()
    
    if num_vehicles > len(spawn_points):
        num_vehicles = len(spawn_points)

    traffic_manager = client.get_trafficmanager()
    traffic_manager.set_global_distance_to_leading_vehicle(3.0) 
    random.shuffle(spawn_points)

    for i in range(num_vehicles):
        blueprint = random.choice(vehicle_bps)
        spawn_point = spawn_points[i]
        vehicle = world.try_spawn_actor(blueprint, spawn_point)
        if vehicle:
            traffic_actor_list.append(vehicle)
            vehicle.set_autopilot(True)
    
    print(f"Successfully spawned {len(traffic_actor_list)} AI vehicles.")
    return traffic_actor_list

# --- NEW: Head Pose Analysis Function (Runs in a separate thread) ---
def run_head_pose_analysis(distraction_event_id, stop_event):
    """
    Runs the head pose detection loop.
    - distraction_event_id: The Pygame event ID to post when distracted.
    - stop_event: A threading.Event to signal when to stop the loop.
    """
    print("[Head Pose Thread] Starting...")
    
    # --- Configurable Thresholds ---
    YAW_THRESHOLD = 25  # Degrees left/right
    PITCH_THRESHOLD = 20 # Degrees up/down
    COOLDOWN_SECONDS = 3.0 # Time between alerts
    
    last_beep_time = 0.0
    last_print_state = ""

    try:
        # --- 1. Load Models ---
        print("[Head Pose Thread] Loading dlib models...")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
        print("[Head Pose Thread] Models loaded.")
        
        # --- 2. Start Webcam ---
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[Head Pose Thread] Error: Could not open webcam.")
            return

        # 3D model points (generic face model)
        model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            (225.0, 170.0, -135.0),      # Right eye right corner
            (-150.0, -150.0, -125.0),    # Left Mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ], dtype=np.float64)
        
        # Get frame size (needed for camera matrix)
        ret, frame = cap.read()
        if not ret:
            print("[Head Pose Thread] Error: Could not read from webcam.")
            cap.release()
            return
            
        size = frame.shape
        # Camera internals (approximate)
        focal_length = size[1]
        center = (size[1]/2, size[0]/2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype=np.float64
        )
        dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion

        # --- 3. Main Detection Loop ---
        print("[Head Pose Thread] Running... (Press ESC in main window to quit)")
        while not stop_event.is_set():
            current_print_state = ""
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.1)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)

            if len(faces) > 0:
                face = faces[0] # Use the first face detected
                
                # Get 2D landmarks
                shape = predictor(gray, face)
                image_points = np.array([
                    (shape.part(30).x, shape.part(30).y),     # Nose tip
                    (shape.part(8).x, shape.part(8).y),       # Chin
                    (shape.part(36).x, shape.part(36).y),     # Left eye
                    (shape.part(45).x, shape.part(45).y),     # Right eye
                    (shape.part(48).x, shape.part(48).y),     # Left mouth
                    (shape.part(54).x, shape.part(54).y)      # Right mouth
                ], dtype=np.float64)

                # --- 3D Pose Estimation ---
                (success, rotation_vector, translation_vector) = cv2.solvePnP(
                    model_points, image_points, camera_matrix, dist_coeffs
                )

                # Convert rotation vector (radians) to degrees
                # rvec[0] = Pitch, rvec[1] = Yaw, rvec[2] = Roll
                pitch_deg = rotation_vector[0].item() * (180.0 / np.pi)
                yaw_deg = rotation_vector[1].item() * (180.0 / np.pi)

                # --- 4. Distraction Check ---
                current_time = time.time()
                if (abs(yaw_deg) > YAW_THRESHOLD) or (abs(pitch_deg) > PITCH_THRESHOLD):
                    # --- MODIFIED: Set state to DISTRACTED ---
                    current_print_state = "DISTRACTED"
                    
                    if (current_time - last_beep_time) > COOLDOWN_SECONDS:
                        print(f"[Head Pose Thread] DISTRACTION! Yaw: {yaw_deg:.1f}, Pitch: {pitch_deg:.1f}")
                        pygame.event.post(pygame.event.Event(distraction_event_id))
                        last_beep_time = current_time
                else:
                    # --- MODIFIED: Set state to ATTENTIVE ---
                    current_print_state = "ATTENTIVE"
            
            else:
                # --- MODIFIED: Set state to FACE_NOT_DETECTED ---
                current_print_state = "FACE_NOT_DETECTED"
                            
            if current_print_state != last_print_state:
                if current_print_state == "ATTENTIVE":
                    print("[Head Pose Thread] Status: Looking at screen.")
                elif current_print_state == "DISTRACTED":
                    print("[Head Pose Thread] Status: Looking away.")
                elif current_print_state == "FACE_NOT_DETECTED":
                    print("[Head Pose Thread] Status: Face not detected.")
                
                # Update the last state
                last_print_state = current_print_state
        
            # Reduce CPU usage, this loop doesn't need to be 60fps
            time.sleep(0.05)

    except FileNotFoundError as e:
        print(f"[Head Pose Thread] Error: Missing file! {e.filename}")
        print("[Head Pose Thread] Please download 'shape_predictor_68_face_landmarks.dat' and place it in the script folder.")
    except Exception as e:
        print(f"[Head Pose Thread] An unexpected error occurred: {e}")
    finally:
        cap.release()
        print("[Head Pose Thread] Stopped.")


def main():
    # --- Configuration ---
    actor_list = [] 
    traffic_actor_list = [] 
    driving_log = []
    log_filename = "driving_pattern_log.csv"
    
    camera = None
    collision_sensor = None
    
    collision_state = {'collided_with': None}
    last_traffic_count = 0
    TRAFFIC_DETECTION_RADIUS = 50.0
    
    # --- NEW: Head Pose Thread variables ---
    pose_thread = None
    stop_thread_event = threading.Event()
    DISTRACTION_EVENT = pygame.USEREVENT + 1
    
    try:
        # --- NEW: Initialize Pygame Audio Mixer ---
        pygame.mixer.init()
        try:
            distraction_sound = pygame.mixer.Sound("alert.wav")
        except pygame.error:
            print("Error: 'alert.wav' not found. Distraction sound will be disabled.")
            distraction_sound = None

        # --- Connect to Carla ---
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        spectator = world.get_spectator() 
        print("Successfully connected to Carla.")
        
        # --- Spawn AI traffic ---
        traffic_actor_list = spawn_ai_traffic(client, world, 50)

        # --- Pygame Setup (Video) ---
        pygame.init() # Video part
        display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Carla: Full Driver Monitoring System")
        
        # --- Get Blueprints ---
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter('model3')[0]
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')
        collision_bp = blueprint_library.find('sensor.other.collision')

        # --- Spawn Our Actors ---
        spawn_point = random.choice(world.get_map().get_spawn_points())
        vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
        if vehicle is None:
            print("Error: Could not spawn OUR vehicle (spawn point likely occupied).")
            return
        actor_list.append(vehicle)
        print(f"Spawned OUR vehicle: {vehicle.type_id}")

        camera_transform = carla.Transform(carla.Location(x=1.5, z=1.7))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        actor_list.append(camera)

        collision_sensor = world.spawn_actor(collision_bp, carla.Transform(), attach_to=vehicle)
        actor_list.append(collision_sensor)
        
        # --- Setup Sensor Listeners ---
        collision_sensor.listen(lambda event: on_collision(event, collision_state))
        
        # --- NEW: Start the Head Pose Thread ---
        pose_thread = threading.Thread(
            target=run_head_pose_analysis, 
            args=(DISTRACTION_EVENT, stop_thread_event),
            daemon=True # Ensures thread exits if main script crashes
        )
        pose_thread.start()

        # --- Main Simulation Loop ---
        running = True
        control = carla.VehicleControl()
        
        print("\n--- Starting Manual Control ---")
        print("  Driver monitoring (head pose) is ACTIVE.")
        print("  ESC or Close Window: Quit")
        
        while running:
            world.wait_for_tick()
            
            # --- Spectator Camera ---
            vehicle_transform = vehicle.get_transform()
            spectator_transform = carla.Transform(
                vehicle_transform.location + carla.Location(z=3) - vehicle_transform.get_forward_vector() * 8.0,
                vehicle_transform.rotation
            )
            spectator.set_transform(spectator_transform)
            
            # --- Pygame Events (Main Thread) ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                # --- NEW: Listen for the custom distraction event ---
                elif event.type == DISTRACTION_EVENT:
                    print("--- DISTRACTION DETECTED! (Sound played) ---")
                    if distraction_sound:
                        distraction_sound.play()

            # --- Control logic (Unchanged) ---
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                control.throttle = 0.8; control.reverse = False; control.brake = 0.0
            elif keys[pygame.K_s]:
                control.throttle = 0.5; control.brake = 0.0; control.reverse = True
            else:
                control.throttle = 0.0; control.brake = 0.0
            if keys[pygame.K_a]:
                control.steer = -0.5
            elif keys[pygame.K_d]:
                control.steer = 0.5
            else:
                control.steer = 0.0
            vehicle.apply_control(control)

            # --- Data Logging Block (Unchanged) ---
            snapshot = world.get_snapshot()
            transform = vehicle.get_transform()
            velocity = vehicle.get_velocity()
            speed_kmh = 3.6 * velocity.length()
            
            collided_with_type = collision_state['collided_with']
            anomaly_type = detect_anomalies(control, speed_kmh)
            
            # --- Traffic Analysis (Unchanged) ---
            current_traffic_count = 0
            my_location = transform.location
            for ai_vehicle in traffic_actor_list:
                if ai_vehicle.is_alive:
                    distance = my_location.distance(ai_vehicle.get_location())
                    if distance < TRAFFIC_DETECTION_RADIUS:
                        current_traffic_count += 1
            
            if current_traffic_count != last_traffic_count:
                print(f"Traffic Analysis: {current_traffic_count} cars within {TRAFFIC_DETECTION_RADIUS}m")
                last_traffic_count = current_traffic_count
            
            # --- Data Logging (Unchanged) ---
            data_entry = {
                'timestamp': snapshot.timestamp.elapsed_seconds,
                'throttle': control.throttle, 'steer': control.steer, 'brake': control.brake,
                'speed_kmh': speed_kmh,
                'location_x': transform.location.x, 'location_y': transform.location.y,
                'collision': collided_with_type is not None,
                'collided_with': collided_with_type if collided_with_type else 'None',
                'anomaly': anomaly_type
            }
            driving_log.append(data_entry)
            
            collision_state['collided_with'] = None
            pygame.display.flip()

    finally:
        # --- Clean Up ---
        print("\nSimulation ended. Cleaning up...")
        
        # --- NEW: Safely stop the head pose thread ---
        if pose_thread:
            print("Stopping head pose analysis thread...")
            stop_thread_event.set() # Signal the thread to stop
            pose_thread.join()      # Wait for the thread to finish
        
        pygame.quit() 
        
        if collision_sensor and collision_sensor.is_listening:
            collision_sensor.stop()
            
        print(f"Destroying our vehicle and sensors ({len(actor_list)} actors)...")
        if actor_list:
            client.apply_batch([carla.command.DestroyActor(actor) for actor in actor_list])
        
        print(f"Destroying AI traffic ({len(traffic_actor_list)} actors)...")
        if traffic_actor_list:
            client.apply_batch([carla.command.DestroyActor(actor) for actor in traffic_actor_list])
        
        # --- Save the log file (Unchanged) ---
        if driving_log:
            print(f"Writing {len(driving_log)} driving pattern entries to {log_filename}...")
            headers = driving_log[0].keys() 
            with open(log_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(driving_log)
            print(f"Successfully saved log to {log_filename}")
        
        print("Cleanup complete.")

if __name__ == '__main__':
    main()