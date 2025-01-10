import pygame
from djitellopy import Tello
from time import time
import cv2
import os

class Teleop:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((400, 400))
        self.key_states = {}
        self.key_press_handled = {}

    def update_key_states(self):
        """Update key states based on Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.key_states[event.key] = True
                self.key_press_handled[event.key] = False
            elif event.type == pygame.KEYUP:
                self.key_states[event.key] = False
                self.key_press_handled[event.key] = False

    def get_key_down(self, key_name):
        """Check if a specific key is being held down."""
        key = getattr(pygame, f'K_{key_name}', None)
        return self.key_states.get(key, False)

    def get_key_pressed_once(self, key_name):
        """Check if a specific key was pressed and not handled yet."""
        key = getattr(pygame, f'K_{key_name}', None)
        if key and self.key_states.get(key, False) and not self.key_press_handled.get(key, True):
            self.key_press_handled[key] = True
            return True
        return False

    def get_drone_controls(self):
        """Get keyboard input and translate it into drone commands."""
        lr, fb, ud, yv = 0, 0, 0, 0
        speed = 30

        if self.get_key_down("l"): lr = speed
        elif self.get_key_down("j"): lr = -speed

        if self.get_key_down("i"): fb = speed
        elif self.get_key_down("k"): fb = -speed

        if self.get_key_down("w"): ud = speed
        elif self.get_key_down("s"): ud = -speed

        if self.get_key_down("a"): yv = speed
        elif self.get_key_down("d"): yv = -speed

        return lr, fb, ud, yv

class DroneCamera:
    def __init__(self, drone=None):
        """Initialize the camera, using either the drone or a local webcam."""
        self.drone = drone
        self.video_writer = None

        if drone:
            self.drone.streamon()
        else:
            self.capture = cv2.VideoCapture(0)

    def get_frame(self):
        """Capture a frame from the camera."""
        if self.drone:
            frame = self.drone.get_frame_read().frame
        else:
            ret, frame = self.capture.read()
            if not ret:
                raise RuntimeError("Failed to capture frame from webcam.")
        return cv2.resize(frame, (360, 240))

    def show_frame(self, frame):
        """Display the captured frame."""
        # Convert the frame to RGB before saving
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("DRONE", frame)
        cv2.waitKey(1)

    def save_frame(self, frame, save_path="captures"):
        """Save the current frame to a file."""
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # Convert the frame to RGB before saving
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        filename = os.path.join(save_path, "capture_{}.jpg".format(int(time())))
        cv2.imwrite(filename, frame_rgb)
        print(f"Image saved to {filename}")


    def start_video_recording(self, save_path="videos"):
        """Start recording video."""
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        filename = os.path.join(save_path, "video_{}.mp4".format(int(time())))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(filename, fourcc, 30.0, (360, 240))
        print(f"Started recording video to {filename}")

    def record_frame(self, frame):
        """Record a frame to the video file."""
        if self.video_writer is not None:
            # Convert the frame to RGB before recording
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.video_writer.write(frame_rgb)

    def stop_video_recording(self):
        """Stop recording video."""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
            print("Stopped video recording.")

def check_battery_warning(drone):
    """Check and warn if the battery level is below 20%."""
    battery_level = drone.get_battery()
    if battery_level <= 20:
        print("Warning: Battery level is critically low (<= 20%)! Land the drone immediately.")

def main():
    """Main function to control the drone."""
    teleop = Teleop()
    drone = Tello()
    drone.connect()

    camera = DroneCamera(drone)
    
    print(f"Battery: {drone.get_battery()}%")

    try:
        while True:
            teleop.update_key_states()

            # Capture and display the video feed
            frame = camera.get_frame()
            camera.show_frame(frame)

            # Check battery warning
            check_battery_warning(drone)

            # Get keyboard input and send commands to the drone
            lr, fb, ud, yv = teleop.get_drone_controls()
            drone.send_rc_control(lr, fb, ud, yv)

            # Get keyboard input for saving or recording frames
            if teleop.get_key_pressed_once("c"):
                camera.save_frame(frame)

            if teleop.get_key_pressed_once("r"):
                if camera.video_writer is None:
                    camera.start_video_recording()
                else:
                    camera.stop_video_recording()

            if camera.video_writer is not None:
                camera.record_frame(frame)

            if teleop.get_key_pressed_once("q"):
                drone.land()
                
            if teleop.get_key_pressed_once("e"):
                drone.takeoff()
            

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if camera.video_writer is not None:
            camera.stop_video_recording()
        if drone.is_flying:
            drone.land()
        cv2.destroyAllWindows()
        pygame.quit()

if __name__ == "__main__":
    main()
