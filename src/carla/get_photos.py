import carla
import random
import time
import os
import pygame # Import the new library

# --- 1. Helper Class for Timed Image Saving ---
# This class will be our new camera callback
class ImageSaver:
    def __init__(self, output_dir, save_interval=0.5):
        self.output_dir = output_dir
        self.save_interval = save_interval
        self.last_save_time = time.time() # Store the time of the last save
        self.image_count = 0

    # This __call__ method makes an instance of the class 'callable'
    # carla.Sensor.listen() will call this method on each new image
    def __call__(self, image):
        current_time = time.time()
        # Check if 0.5 seconds have passed since the last save
        if current_time - self.last_save_time >= self.save_interval:
            # Save the image
            filename = f'{self.output_dir}/{image.frame:06d}.png'
            image.save_to_disk(filename)
            
            # Update the last save time
            self.last_save_time = current_time
            self.image_count += 1
            print(f"Saved {filename}")

def main():
    # --- 2. Configuration ---
    actor_list = []
    image_saver = None
    output_dir = "_out_manual" # New output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # --- 3. Connect to Carla ---
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        spectator = world.get_spectator()
        print("Successfully connected to Carla.")

        # --- 4. Pygame Setup ---
        pygame.init()
        # Create a small window (800x600) to capture keys
        display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Carla Manual Control")
        
        # --- 5. Get Blueprints ---
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter('model3')[0]
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')

        # --- 6. Spawn Actors ---
        spawn_point = random.choice(world.get_map().get_spawn_points())
        vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
        if vehicle is None:
            print("Error: Could not spawn vehicle.")
            return
        actor_list.append(vehicle)
        print(f"Spawned {vehicle.type_id}")

        # Attach camera
        camera_transform = carla.Transform(carla.Location(x=1.5, z=1.7))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        actor_list.append(camera)
        print(f"Spawned and attached {camera.type_id}")

        # --- 7. Setup Camera Callback ---
        # Create an instance of our ImageSaver class
        image_saver = ImageSaver(output_dir, save_interval=0.5)
        # Pass the instance to the listen() method
        camera.listen(image_saver)

        # --- 8. The Main Simulation Loop ---
        running = True
        control = carla.VehicleControl() # Create a control object
        
        print("--- Starting Manual Control ---")
        print("  W: Throttle | S: Brake")
        print("  A: Steer Left | D: Steer Right")
        print("  ESC or Close Window: Quit")
        
        while running:
            # Sync our script with the simulator's tick
            world.wait_for_tick()
            
            # Center the spectator camera on the car
            vehicle_transform = vehicle.get_transform()
            spectator_transform = carla.Transform(
                # Location: 8m behind the car and 3m up
                vehicle_transform.location + carla.Location(z=3) - vehicle_transform.get_forward_vector() * 8.0,
                # Rotation: Same as the car's
                vehicle_transform.rotation
            )
            spectator.set_transform(spectator_transform)
            
            # Process Pygame events (like closing the window or pressing ESC)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # --- This is the core control logic ---
            # Get the state of all keys (is it 'down' or 'up'?)
            keys = pygame.key.get_pressed()

            # Throttle and Brake
            if keys[pygame.K_w]:
                control.throttle = 0.8 # 80% throttle
                control.reverse = False
                control.brake = 0.0
            elif keys[pygame.K_s]:
                control.throttle = 0.0
                control.brake = 1.0 # 100% brake
                control.reverse = False
            elif keys[pygame.K_x]:
                control.throttle = 0.5
                control.reverse = True
                control.brake = 0.0
            else:
                # If neither W nor S is pressed, no throttle, no brake
                control.throttle = 0.0
                control.brake = 0.0

            # Steering
            if keys[pygame.K_a]:
                control.steer = -0.5 # 50% steer left
            elif keys[pygame.K_d]:
                control.steer = 0.5 # 50% steer right
            else:
                # If neither A nor D, no steering
                control.steer = 0.0

            # Apply the calculated control to the vehicle
            vehicle.apply_control(control)
            
            # Update the Pygame display (just to keep the window responsive)
            pygame.display.flip()


    finally:
        # --- 9. Clean Up ---
        print("\nSimulation ended. Cleaning up...")
        pygame.quit() # Close the pygame window
        
        if camera and camera.is_listening:
            camera.stop()
            
        if actor_list:
            client.apply_batch([carla.command.DestroyActor(actor) for actor in actor_list])
        
        if image_saver:
            print(f"Cleanup complete. Saved {image_saver.image_count} images to '{output_dir}'.")
        else:
            print("Cleanup complete. No images were saved (object not initialized).")

if __name__ == '__main__':
    main()