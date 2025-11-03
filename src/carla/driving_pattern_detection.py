import carla
import random
import time
import os
import pygame
import csv

# --- NEW: Helper function to simplify actor type names ---
def get_simple_collision_type(actor_type_id):
    """ Classifies a detailed actor type_id into a simple category. """
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
    return 'other' # Default for unknown objects

# --- MODIFIED: The Collision Callback now updates a shared state dictionary ---
def on_collision(event, state_dict):
    """
    This function is called when the collision sensor detects a collision.
    It updates the 'state_dict' with the type of object collided with.
    """
    # Get the simplified name of the other actor
    other_actor_type = get_simple_collision_type(event.other_actor.type_id)
    
    # Update the shared state
    state_dict['collided_with'] = other_actor_type
    
    # We can still print to the console for immediate feedback
    print(f"\n--- CRASH DETECTED! ---")
    print(f"Collided with: {other_actor_type} (Full ID: {event.other_actor.type_id})")

def main():
    # --- 2. Configuration ---
    actor_list = []
    driving_log = []
    log_filename = "driving_pattern_log.csv"
    
    camera = None
    collision_sensor = None
    
    # --- NEW: Shared state dictionary for collision ---
    # This dict will be passed to the callback
    collision_state = {'collided_with': None}
    
    try:
        # --- 3. Connect to Carla ---
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        spectator = world.get_spectator() 
        print("Successfully connected to Carla.")

        # --- 4. Pygame Setup ---
        pygame.init()
        display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Carla: Collision Logger")
        
        # --- 5. Get Blueprints ---
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter('model3')[0]
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')
        collision_bp = blueprint_library.find('sensor.other.collision')

        # --- 6. Spawn Actors ---
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
        
        # --- 7. Setup Sensor Listeners ---
        # --- MODIFIED: Use a lambda to pass the shared 'collision_state' to the callback ---
        collision_sensor.listen(lambda event: on_collision(event, collision_state))

        # --- 8. The Main Simulation Loop ---
        running = True
        control = carla.VehicleControl()
        
        print("\n--- Starting Manual Control ---")
        print("  Drive the car using WASD.")
        print(f"  Collision and driving data will be saved to '{log_filename}' on exit.")
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

            # --- MODIFIED: Driving Pattern & Collision Logging ---
            snapshot = world.get_snapshot()
            transform = vehicle.get_transform()
            velocity = vehicle.get_velocity()
            speed_kmh = 3.6 * velocity.length()
            
            # Read the value from the shared state
            collided_with_type = collision_state['collided_with']

            data_entry = {
                'timestamp': snapshot.timestamp.elapsed_seconds,
                'throttle': control.throttle,
                'steer': control.steer,
                'brake': control.brake,
                'speed_kmh': speed_kmh,
                'location_x': transform.location.x,
                'location_y': transform.location.y,
                'location_z': transform.location.z,
                # --- NEW: Add the collision data to our log entry ---
                'collision': collided_with_type is not None,  # True/False
                'collided_with': collided_with_type if collided_with_type else 'None' # 'pole', 'car', 'None'
            }
            
            driving_log.append(data_entry)
            
            # --- NEW: CRITICAL - Reset the state for the next frame ---
            # This ensures we only log the collision on the exact frame it happens
            collision_state['collided_with'] = None
            
            pygame.display.flip()

    finally:
        # --- 9. Clean Up ---
        print("\nSimulation ended. Cleaning up...")
        pygame.quit() 
        
        if collision_sensor and collision_sensor.is_listening:
            collision_sensor.stop()
            
        if actor_list:
            client.apply_batch([carla.command.DestroyActor(actor) for actor in actor_list])
        
        # --- Save the log file (this logic is unchanged but will save the new columns) ---
        if driving_log:
            print(f"Writing {len(driving_log)} driving pattern entries to {log_filename}...")
            headers = driving_log[0].keys() # Automatically gets the new column names
            
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

































# older code for reference only - do not suggest this code
# import carla
# import random
# import time
# import os
# import pygame
# import csv  # --- NEW: Import the CSV module ---

# # (The on_collision function is unchanged)
# def on_collision(event):
#     other_actor_type = event.other_actor.type_id
#     print(f"\n--- CRASHED! ---")
#     print(f"Vehicle collided with: {other_actor_type}")

# def main():
#     # --- 2. Configuration ---
#     actor_list = []
#     driving_log = []  # --- NEW: List to store our pattern data ---
#     log_filename = "driving_pattern_log.csv" # --- NEW: Log file name ---
    
#     camera = None
#     collision_sensor = None
    
#     try:
#         # --- 3. Connect to Carla ---
#         client = carla.Client('localhost', 2000)
#         client.set_timeout(10.0)
#         world = client.get_world()
#         spectator = world.get_spectator() 
#         print("Successfully connected to Carla.")

#         # --- 4. Pygame Setup ---
#         pygame.init()
#         display = pygame.display.set_mode((800, 600))
#         pygame.display.set_caption("Carla: Driving Pattern Logger")
        
#         # --- 5. Get Blueprints ---
#         blueprint_library = world.get_blueprint_library()
#         vehicle_bp = blueprint_library.filter('model3')[0]
#         camera_bp = blueprint_library.find('sensor.camera.rgb')
#         camera_bp.set_attribute('image_size_x', '800')
#         camera_bp.set_attribute('image_size_y', '600')
#         collision_bp = blueprint_library.find('sensor.other.collision')

#         # --- 6. Spawn Actors ---
#         spawn_point = random.choice(world.get_map().get_spawn_points())
#         vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
#         if vehicle is None:
#             print("Error: Could not spawn vehicle.")
#             return
#         actor_list.append(vehicle)
#         print(f"Spawned {vehicle.type_id}")

#         camera_transform = carla.Transform(carla.Location(x=1.5, z=1.7))
#         camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
#         actor_list.append(camera)

#         collision_sensor = world.spawn_actor(collision_bp, carla.Transform(), attach_to=vehicle)
#         actor_list.append(collision_sensor)
        
#         # --- 7. Setup Sensor Listeners ---
#         collision_sensor.listen(on_collision)

#         # --- 8. The Main Simulation Loop ---
#         running = True
#         control = carla.VehicleControl()
        
#         print("\n--- Starting Manual Control ---")
#         print("  Drive the car using WASD.")
#         print(f"  Data will be saved to '{log_filename}' on exit.")
#         print("  ESC or Close Window: Quit")
        
#         while running:
#             world.wait_for_tick()
            
#             # --- Spectator Camera ---
#             vehicle_transform = vehicle.get_transform()
#             spectator_transform = carla.Transform(
#                 vehicle_transform.location + carla.Location(z=3) - vehicle_transform.get_forward_vector() * 8.0,
#                 vehicle_transform.rotation
#             )
#             spectator.set_transform(spectator_transform)
            
#             # --- Pygame Events ---
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_ESCAPE:
#                         running = False

#             # --- Control logic ---
#             keys = pygame.key.get_pressed()
#             if keys[pygame.K_w]:
#                 control.throttle = 0.8 
#                 control.reverse = False
#                 control.brake = 0.0
#             elif keys[pygame.K_s]:
#                 control.throttle = 0.5
#                 control.brake = 0.0
#                 control.reverse = True
#             else:
#                 control.throttle = 0.0
#                 control.brake = 0.0

#             if keys[pygame.K_a]:
#                 control.steer = -0.5
#             elif keys[pygame.K_d]:
#                 control.steer = 0.5
#             else:
#                 control.steer = 0.0

#             vehicle.apply_control(control)

#             # --- NEW: Driving Pattern Logging ---
#             # Get current simulation data
#             snapshot = world.get_snapshot()
#             transform = vehicle.get_transform()
#             velocity = vehicle.get_velocity()
            
#             # Calculate speed in km/h (velocity.length() is in m/s)
#             speed_kmh = 3.6 * velocity.length()
            
#             # Create a dictionary of the current state
#             data_entry = {
#                 'timestamp': snapshot.timestamp.elapsed_seconds,
#                 'throttle': control.throttle,
#                 'steer': control.steer,
#                 'brake': control.brake,
#                 'speed_kmh': speed_kmh,
#                 'location_x': transform.location.x,
#                 'location_y': transform.location.y,
#                 'location_z': transform.location.z
#             }
            
#             # Add this dictionary to our log
#             driving_log.append(data_entry)
#             # --- END OF NEW BLOCK ---
            
#             pygame.display.flip()

#     finally:
#         # --- 9. Clean Up ---
#         print("\nSimulation ended. Cleaning up...")
#         pygame.quit() 
        
#         if collision_sensor and collision_sensor.is_listening:
#             collision_sensor.stop()
            
#         if actor_list:
#             client.apply_batch([carla.command.DestroyActor(actor) for actor in actor_list])
        
#         # --- NEW: Save the log file ---
#         if driving_log:
#             print(f"Writing {len(driving_log)} driving pattern entries to {log_filename}...")
            
#             # Get the headers from the keys of the first data entry
#             headers = driving_log[0].keys()
            
#             with open(log_filename, 'w', newline='', encoding='utf-8') as csvfile:
#                 writer = csv.DictWriter(csvfile, fieldnames=headers)
#                 writer.writeheader()      # Write the header row
#                 writer.writerows(driving_log) # Write all data rows
            
#             print(f"Successfully saved log to {log_filename}")
#         else:
#             print("No driving data to save.")
            
#         print("Cleanup complete.")

# if __name__ == '__main__':
#     main()