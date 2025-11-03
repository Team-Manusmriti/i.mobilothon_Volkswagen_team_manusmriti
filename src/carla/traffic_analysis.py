# Traffic Analysis + Anomaly + Driving Patterns + Crash Detection
import carla
import random
import time
import os
import pygame
import csv

# --- Helper function to simplify actor type names (Unchanged) ---
def get_simple_collision_type(actor_type_id):
    if 'vehicle' in actor_type_id:
        return 'car'
    if 'pedestrian' in actor_type_id:
        return 'pedestrian'
    if 'pole' in actor_type_id or 'streetlamp' in actor_type_id:
        return 'pole'
    if 'wall' in actor_type_id or 'building' in actor_type_id:
        return 'building/wall'
    if 'trafficlight' in actor_type_id:
        return 'traffic_light'
    if 'static.vegetation' in actor_type_id:
        return 'vegetation'
    return 'other'

# --- Collision Callback (Unchanged) ---
def on_collision(event, state_dict):
    other_actor_type = get_simple_collision_type(event.other_actor.type_id)
    state_dict['collided_with'] = other_actor_type
    print(f"\n--- CRASH DETECTED! ---")
    print(f"Collided with: {other_actor_type}")

# --- Anomaly Detection function (Unchanged) ---
def detect_anomalies(control, speed_kmh):
    SPEEDING_THRESHOLD_KMH = 05.0 
    HARD_BRAKE_SPEED_KMH = 30.0 
    STUCK_SPEED_THRESHOLD_KMH = 1.0 
    STUCK_THROTTLE_THRESHOLD = 0.5 
    
    if control.brake == 1.0 and speed_kmh > HARD_BRAKE_SPEED_KMH:
        return "Hard_Brake"
    if control.throttle > STUCK_THROTTLE_THRESHOLD and speed_kmh < STUCK_SPEED_THRESHOLD_KMH:
        return "Stuck/Blocked"
    if speed_kmh > SPEEDING_THRESHOLD_KMH:
        return "Excessive_Speeding"
    return "None"

# --- NEW: Function to spawn AI Traffic ---
def spawn_ai_traffic(client, world, num_vehicles):
    """
    Spawns a fleet of AI-controlled vehicles using Traffic Manager.
    Returns a list of the spawned actor objects.
    """
    print(f"Spawning {num_vehicles} AI vehicles...")
    traffic_actor_list = []
    blueprint_library = world.get_blueprint_library()
    vehicle_bps = blueprint_library.filter('vehicle.*') # Get all vehicle blueprints
    spawn_points = world.get_map().get_spawn_points()
    
    if num_vehicles > len(spawn_points):
        print(f"Warning: Requested {num_vehicles}, but only {len(spawn_points)} spawn points available.")
        num_vehicles = len(spawn_points)

    # --- Get Traffic Manager ---
    traffic_manager = client.get_trafficmanager()
    # Set a global distance of 3m between AI cars
    traffic_manager.set_global_distance_to_leading_vehicle(3.0) 
    
    # Shuffle spawn points to scatter cars
    random.shuffle(spawn_points)

    for i in range(num_vehicles):
        blueprint = random.choice(vehicle_bps)
        spawn_point = spawn_points[i]
        
        # Try to spawn the actor
        vehicle = world.try_spawn_actor(blueprint, spawn_point)
        
        if vehicle:
            # Add to our list for cleanup
            traffic_actor_list.append(vehicle)
            # --- Tell Traffic Manager to control this car ---
            vehicle.set_autopilot(True)
        else:
            print(f"Could not spawn AI vehicle at {spawn_point.location}")

    print(f"Successfully spawned {len(traffic_actor_list)} AI vehicles.")
    return traffic_actor_list

def main():
    # --- Configuration ---
    actor_list = [] # List for our car + sensors
    traffic_actor_list = [] # --- NEW: List for all AI cars ---
    driving_log = []
    log_filename = "driving_pattern_log.csv"
    
    camera = None
    collision_sensor = None
    
    collision_state = {'collided_with': None}
    
    # --- NEW: State for Traffic Analysis ---
    last_traffic_count = 0
    TRAFFIC_DETECTION_RADIUS = 50.0 # 50 meters
    
    try:
        # --- Connect to Carla ---
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        spectator = world.get_spectator() 
        print("Successfully connected to Carla.")
        
        # --- NEW: Spawn the AI traffic ---
        # We pass the client and world, and ask for 50 cars
        traffic_actor_list = spawn_ai_traffic(client, world, 50)

        # --- Pygame Setup ---
        pygame.init()
        display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Carla: Full Traffic Simulation")
        
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

        # --- Main Simulation Loop ---
        running = True
        control = carla.VehicleControl()
        
        print("\n--- Starting Manual Control ---")
        print("  Drive the car using WASD. AI traffic is active.")
        print(f"  Live traffic analysis will be printed to the console.")
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
            
            # --- Pygame Events ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # --- Control logic ---
            keys = pygame.key.get_pressed()
            # (Control logic is unchanged...)
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

            # --- Data Logging Block ---
            snapshot = world.get_snapshot()
            transform = vehicle.get_transform()
            velocity = vehicle.get_velocity()
            speed_kmh = 3.6 * velocity.length()
            
            collided_with_type = collision_state['collided_with']
            anomaly_type = detect_anomalies(control, speed_kmh)
            
            # --- NEW: Traffic Analysis Logic ---
            current_traffic_count = 0
            my_location = transform.location
            for ai_vehicle in traffic_actor_list:
                if ai_vehicle.is_alive: # Check if car hasn't been destroyed
                    ai_location = ai_vehicle.get_location()
                    distance = my_location.distance(ai_location)
                    if distance < TRAFFIC_DETECTION_RADIUS:
                        current_traffic_count += 1
            
            # --- NEW: Intelligent Printing ---
            if current_traffic_count != last_traffic_count:
                print(f"Traffic Analysis: {current_traffic_count} cars within {TRAFFIC_DETECTION_RADIUS}m")
                last_traffic_count = current_traffic_count
            
            # --- Data Logging (Unchanged, but logging continues) ---
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
        pygame.quit() 
        
        if collision_sensor and collision_sensor.is_listening:
            collision_sensor.stop()
            
        # --- MODIFIED: Destroy BOTH actor lists ---
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