import pygame
from djitellopy import Tello
from time import sleep
import cv2

class Teleop:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((400, 400))

    def get_key(self, key_name):
        """Check if a specific key is pressed."""
        pygame.event.pump()  # Process event queue
        key_input = pygame.key.get_pressed()
        key = getattr(pygame, f'K_{key_name.upper()}', None)
        return key_input[key] if key else False

class DroneCamera:
    def __init__(self, drone):
        """Initialize the drone camera."""
        self.drone = drone
        self.drone.streamon()

    def get_frame(self):
        """Capture a frame from the drone's camera."""
        frame = self.drone.get_frame_read().frame
        return cv2.resize(frame, (360, 240))

    def show_frame(self, frame):
        """Display the captured frame."""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("DRONE", frame)
        cv2.waitKey(1)

def get_keyboard_input(teleop):
    """Get input from the keyboard and translate it into drone commands."""
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 30

    if teleop.get_key("l"): lr = speed
    elif teleop.get_key("j"): lr = -speed

    if teleop.get_key("i"): fb = speed
    elif teleop.get_key("k"): fb = -speed

    if teleop.get_key("w"): ud = speed
    elif teleop.get_key("s"): ud = -speed

    if teleop.get_key("a"): yv = speed
    elif teleop.get_key("d"): yv = -speed

    return lr, fb, ud, yv

def main():
    """Main function to control the drone."""
    teleop = Teleop()
    drone = Tello()
    drone.connect()

    print(f"Battery: {drone.get_battery()}%")

    camera = DroneCamera(drone)

    try:
        while True:
            # Capture and display the video feed
            frame = camera.get_frame()
            camera.show_frame(frame)

            # Get keyboard input and send commands to the drone
            lr, fb, ud, yv = get_keyboard_input(teleop)
            drone.send_rc_control(lr, fb, ud, yv)
            sleep(0.02)
            
            if teleop.getKey("q"): drone.land()
            if teleop.getKey("e"): drone.takeoff()
            
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if drone.is_flying:
            drone.land()
        cv2.destroyAllWindows()
        pygame.quit()

if __name__ == "__main__":
    main()
