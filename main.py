from djitellopy import Tello
import numpy as np
from time import time
import pygame
import cv2
import os

class Teleop:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((400, 400))
        
        self.key_states = {}
        self.key_press_handled = {}
        
        self.pid = [0.4, 0.4, 0]
        self.error = 0
        self.face_area_range = [5000, 8000]
        
        self.mode = 0 # 0 = Manual; 1 = Face Tracking
    
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

    def manual_control(self):
        """Get keyboard input and translate it into drone commands."""
        roll, pitch, throttle, yaw = 0, 0, 0, 0
        speed = 20

        if self.get_key_down("l"): roll = speed
        elif self.get_key_down("j"): roll = -speed

        if self.get_key_down("i"): pitch = speed
        elif self.get_key_down("k"): pitch = -speed

        if self.get_key_down("w"): throttle = speed
        elif self.get_key_down("s"): throttle = -speed

        if self.get_key_down("a"): yaw = speed
        elif self.get_key_down("d"): yaw = -speed

        return roll, pitch, throttle, yaw
    
    def face_tracking_control(self, face_info, img_width):
        """Control the drone using face tracking"""

        area = face_info[1]
        x, _  = face_info[0]
        pitch = 0
        
        error = x - img_width//2
        yaw = self.pid[0] * error + self.pid[1] * (error - self.error)
        yaw = int(np.clip(yaw, -100, 100))
        
        
        if area > self.face_area_range[0] and area < self.face_area_range[1]:
            pitch = 0
        elif area > self.face_area_range[1]:
            pitch = -20
        elif area < self.face_area_range[0] and area != 0:
            pitch = 20
            
        if x == 0:
            yaw = 0
            error = 0
            
        self.error = error
        return 0, pitch, 0, yaw
    

class Camera:
    def __init__(self, drone=None, frame_width=640, frame_height=480):
        """Initialize the camera, using either the drone or a local webcam."""
        self.drone = drone
        self.video_writer = None
        self.frame_width = frame_width
        self.frame_height = frame_height

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
        return cv2.resize(frame, (self.frame_width, self.frame_height))

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

    def findFace(self, frame):
        """Computer vision method for face detection."""
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        face_cascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(frame_gray, 1.2, 8)
        
        face_list_center = []
        face_list_area = []
        
        for (x,y,face_width,face_height) in faces:
            cv2.rectangle(frame, (x,y), (x+face_width,y+face_height), (255,0,0), 2)
            cx = x + face_width//2
            cy = y + face_height//2
            area = face_width * face_height
            
            face_list_center.append([cx,cy])
            face_list_area.append(area)
            
            cv2.circle(frame, (cx,cy), 5, (0,255,0), cv2.FILLED)
            
        if len(face_list_area) != 0:
            i = face_list_area.index(max(face_list_area))
            return frame, [face_list_center[i], face_list_area[i]]
        else:
            return frame, [[0,0], 0]
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
    camera = Camera(drone)
    
    print(f"Battery: {drone.get_battery()}%")

    try:
        while True:
            # Check battery warning
            check_battery_warning(drone)
            
            # Capture and display the video feed
            frame = camera.get_frame()
            frame, face_info = camera.findFace(frame)
            camera.show_frame(frame)

            # Get keyboard input and send commands to the drone
            teleop.update_key_states()

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
            
            if teleop.get_key_pressed_once("t"):
                if teleop.mode:
                    print("TRACKING MODE OFF")
                    teleop.mode = 0
                else:
                    print("TRACKING MODE ON")
                    teleop.mode = 1
            
            if teleop.mode:
                roll, pitch, throttle, yaw = teleop.face_tracking_control(face_info, camera.frame_width)
            else:
                roll, pitch, throttle, yaw = teleop.manual_control()
        
            drone.send_rc_control(roll, pitch, throttle, yaw)
                

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
