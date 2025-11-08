import carla
import pygame
import random
import time
import math
import threading
import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket, Body
import logging
from fastapi.middleware.cors import CORSMiddleware

# FastAPI App
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

current_speed = 0.0  # Shared speed variable for WebSocket
exit_simulation = False  # To stop simulation safely
driver_emotion = {"emotion": "happy", "state": "unknown"}


@app.websocket("/ws/emotion")
async def emotion_stream(websocket: WebSocket):
    await websocket.accept()
    print("✅ Emotion WebSocket client connected")  # Log when connected

    try:
        while True:
            print("📡 Sending emotion:", driver_emotion)  # Log every send
            await websocket.send_json(driver_emotion)     # Send updated emotion
            await asyncio.sleep(0.2) 
    except Exception as e:
        print("❌ Emotion WebSocket closed:", e)


@app.post("/update-emotion")
async def update_emotion(data: dict = Body(...)):
    global driver_emotion
    print("✅ Emotion updated:", data)
    driver_emotion = data
    return {"status": "updated"}


# ✅ WebSocket Route
@app.websocket("/ws/speed")
async def ws_speed(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({"speed": current_speed})
            await asyncio.sleep(0.1)
    except:
        pass

# ✅ Start FastAPI server in a separate thread
def start_websocket_server():
    uvicorn.run(app, host="0.0.0.0", port=8008)

# ✅ Main CARLA Manual Control Loop
def carla_simulation():
    global current_speed, exit_simulation

    pygame.init()
    display = pygame.display.set_mode((400, 200))  # small window only for key input
    pygame.display.set_caption("CARLA Manual Control")

    # Connect to CARLA
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    spawn_points = world.get_map().get_spawn_points()

    # Spawn vehicle
    vehicle_bp = blueprint_library.filter("model3")[0]
    vehicle = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))
    if not vehicle:
        print("⚠ Vehicle could not be spawned!")
        return
    print("🚗 Vehicle spawned for manual control.")

    # Set spectator camera
    spectator = world.get_spectator()

    control = carla.VehicleControl()

    try:
        while not exit_simulation:
            # Use wait_for_tick() instead of tick() - this prevents flickering
            world.wait_for_tick()

            # Better camera angle - spectator follows vehicle
            vehicle_transform = vehicle.get_transform()
            
            # Position camera behind and above the vehicle
            spectator_transform = carla.Transform(
                vehicle_transform.location + carla.Location(z=3) - vehicle_transform.get_forward_vector() * 8.0,
                vehicle_transform.rotation
            )
            spectator.set_transform(spectator_transform)

            # Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_simulation = True

            keys = pygame.key.get_pressed()

            # Manual driving
            control.throttle = 1.0 if keys[pygame.K_w] else 0.0
            control.brake = 1.0 if keys[pygame.K_s] else 0.0
            control.steer = -0.5 if keys[pygame.K_a] else (0.5 if keys[pygame.K_d] else 0.0)

            vehicle.apply_control(control)

            # Speed calculation
            velocity = vehicle.get_velocity()
            current_speed = 3.6 * velocity.length()  # Simpler calculation using length()

    finally:
        vehicle.destroy()
        pygame.quit()
        print("✅ Simulation Ended")

if __name__ == "__main__":
    threading.Thread(target=start_websocket_server, daemon=True).start()
    carla_simulation()
