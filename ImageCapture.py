from djitellopy import tello
from time import sleep
import cv2

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.streamon()

while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow("DRONE", img)
    cv2.waitKey(1)