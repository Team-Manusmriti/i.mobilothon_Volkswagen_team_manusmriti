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
    print(f"Collided with: {other_actor_type} (Full ID: {event.other_actor.type_id})")

# --- NEW: Helper function for Anomaly Detection ---
def detect_anomalies(control, speed_kmh):
    """
    Checks for simple driving anomalies based on control input vs. vehicle speed.
    Returns a string describing the anomaly type.
    """
    # --- Define thresholds for detection ---
    # Speeding: 80 km/h
    SPEEDING_THRESHOLD_KMH = 05.0 
    # Hard Braking: Braking at > 30 km/h
    HARD_BRAKE_SPEED_KMH = 30.0 
    # Stuck: Applying throttle but moving at < 1 km/h
    STUCK_SPEED_THRESHOLD_KMH = 1.0 
    STUCK_THROTTLE_THRESHOLD = 0.5 # User must be pressing throttle reasonably hard
    
    # Check for anomalies in order of priority
    
    # 1. Hard Braking
    if control.brake == 1.0 and speed_kmh > HARD_BRAKE_SPEED_KMH:
        return "Hard_Brake"
    
    # 2. Stuck/Blocked
    if control.throttle > STUCK_THROTTLE_THRESHOLD and speed_kmh < STUCK_SPEED_THRESHOLD_KMH:
        return "Stuck/Blocked"
    
    # 3. Excessive Speeding
    if speed_kmh > SPEEDING_THRESHOLD_KMH:
        return "Excessive_Speeding"
    
    # If no anomalies detected
    return "None"

def main():
    # --- Configuration ---
    actor_list = []
    driving_log = []
    log_filename = "driving_pattern_log.csv"
    
    camera = None
    collision_sensor = None
    
    collision_state = {'collided_with': None}
    
    try:
        # --- Connect to Carla ---
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        spectator = world.get_spectator() 
        print("Successfully connected to Carla.")

        # --- Pygame Setup ---
        pygame.init()
        display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Carla: Anomaly Detector")
        
        # --- Get Blueprints ---
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter('model3')[0]
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')
        collision_bp = blueprint_library.find('sensor.other.collision')

        # --- Spawn Actors ---
        spawn_point = random.choice(world.get_map().get_spawn_points())
        vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
        if vehicle is None:
            print("Error: Could not spawn vehicle.")
            return
        actor_list.append(vehicle)
        print(f"Spawned {vehicle.type_id}")

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
        print("  Drive the car using WASD.")
        print(f"  Anomaly, collision, and driving data will be saved to '{log_filename}' on exit.")
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
            if keys[pygame.K_w]:
                control.throttle = 0.8 
                control.reverse = False
                control.brake = 0.0
            elif keys[pygame.K_s]:
                control.throttle = 0.5
                control.brake = 0.0
                control.reverse = True
            else:
                control.throttle = 0.0
                control.brake = 0.0

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
            
            # Check for collision
            collided_with_type = collision_state['collided_with']
            
            # --- NEW: Call the Anomaly Detection function ---
            anomaly_type = detect_anomalies(control, speed_kmh)
            
            # --- MODIFIED: Add anomaly to the log entry ---
            data_entry = {
                'timestamp': snapshot.timestamp.elapsed_seconds,
                'throttle': control.throttle,
                'steer': control.steer,
                'brake': control.brake,
                'speed_kmh': speed_kmh,
                'location_x': transform.location.x,
                'location_y': transform.location.y,
                'location_z': transform.location.z,
                'collision': collided_with_type is not None,
                'collided_with': collided_with_type if collided_with_type else 'None',
                'anomaly': anomaly_type  # --- NEW COLUMN ---
            }
            
            driving_log.append(data_entry)
            
            # Reset collision state for next frame
            collision_state['collided_with'] = None
            
            pygame.display.flip()

    finally:
        # --- Clean Up ---
        print("\nSimulation ended. Cleaning up...")
        pygame.quit() 
        
        if collision_sensor and collision_sensor.is_listening:
            collision_sensor.stop()
            
        if actor_list:
            client.apply_batch([carla.command.DestroyActor(actor) for actor in actor_list])
        
        # --- Save the log file (Unchanged, will now include 'anomaly' column) ---
        if driving_log:
            print(f"Writing {len(driving_log)} driving pattern entries to {log_filename}...")
            headers = driving_log[0].keys() 
            
            with open(log_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(driving_log)
            
            print(f"Successfully saved log to {log_filename}")
        else:
            print("No driving data to save.")
            
        print("Cleanup complete.")

if __name__ == '__main__':
    main()