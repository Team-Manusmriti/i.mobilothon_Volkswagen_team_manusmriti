import carla
import random
import time
import os
import pygame

# --- 1. NEW: The Collision Callback Function ---
# This function will be triggered by the simulator when a collision occurs
def on_collision(event):
    """
    This function is called when the collision sensor detects a collision.
    'event' is a carla.CollisionEvent object.
    """
    # Get the type of the other actor we collided with
    other_actor_type = event.other_actor.type_id
    
    # Print a clear message to the terminal
    print(f"\n--- CRASHED! ---")
    print(f"Vehicle collided with: {other_actor_type}")

def main():
    # --- 2. Configuration ---
    actor_list = []
    camera = None           # We still spawn the camera, just don't use it
    collision_sensor = None # Variable for our new sensor
    
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
        pygame.display.set_caption("Carla Manual Control (with Crash Detection)")
        
        # --- 5. Get Blueprints ---
        blueprint_library = world.get_blueprint_library()
        
        # Vehicle blueprint
        vehicle_bp = blueprint_library.filter('model3')[0]
        
        # Camera blueprint (we keep it for potential future use)
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')

        # --- NEW: Collision Sensor Blueprint ---
        collision_bp = blueprint_library.find('sensor.other.collision')

        # --- 6. Spawn Actors ---
        spawn_point = random.choice(world.get_map().get_spawn_points())
        vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
        if vehicle is None:
            print("Error: Could not spawn vehicle.")
            return
        actor_list.append(vehicle)
        print(f"Spawned {vehicle.type_id}")

        # Spawn camera (still attached)
        camera_transform = carla.Transform(carla.Location(x=1.5, z=1.7))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        actor_list.append(camera)
        print(f"Spawned and attached {camera.type_id}")

        # --- NEW: Spawn Collision Sensor ---
        # We attach it to the vehicle with a default Transform
        collision_sensor = world.spawn_actor(collision_bp, carla.Transform(), attach_to=vehicle)
        actor_list.append(collision_sensor)
        print(f"Spawned and attached {collision_sensor.type_id}")

        # --- 7. Setup Sensor Listeners ---
        # --- NEW: Tell the collision sensor to call 'on_collision' when it triggers ---
        collision_sensor.listen(on_collision)
        
        # We have removed the camera.listen() call, so no images will be saved.

        # --- 8. The Main Simulation Loop ---
        running = True
        control = carla.VehicleControl()
        
        print("\n--- Starting Manual Control ---")
        print("  Drive the car using WASD. Try to crash into something.")
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
            pygame.display.flip()

    finally:
        # --- 9. Clean Up ---
        print("\nSimulation ended. Cleaning up...")
        pygame.quit() 
        
        # --- NEW: Stop the collision sensor listener ---
        if collision_sensor and collision_sensor.is_listening:
            collision_sensor.stop()
            
        # This batch command will destroy the vehicle, camera, AND collision sensor
        if actor_list:
            client.apply_batch([carla.command.DestroyActor(actor) for actor in actor_list])
        
        print("Cleanup complete.")

if __name__ == '__main__':
    main()