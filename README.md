# Tello Drone

![Python](https://img.shields.io/badge/Python-3.10.x-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![DJITelloPy](https://img.shields.io/badge/DJITelloPy-2.x-orange)

## Project Description

This project is a Python application that allows you to control the DJI Tello drone using your keyboard. It also includes functionalities to capture images, record videos, and display the real-time video feed using the OpenCV library. The project is designed to be modular, making it easy to maintain and extend.

Key features:

- Drone control via keyboard.
- Display real-time video feed.
- Capture images and videos from the drone feed.

## How to Install the Project

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/FerFilho23/Tello_Drone.git
   cd <PROJECT_FOLDER>
   ```

2. **Create and Activate a Virtual Environment (Recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   Install the required packages listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Project

1. **Connect the Drone**:
   - Ensure the Tello drone is powered on and connected to your computer's Wi-Fi.

2. **Run the Script**:
   Execute the main project file:

   ```bash
   python main.py
   ```

3. **Keyboard Controls**:
   - **Drone Movement**:
     - `w`: Move up
     - `s`: Move down
     - `a`: Rotate left
     - `d`: Rotate right
     - `i`: Move forward
     - `k`: Move backward
     - `l`: Move right
     - `j`: Move left
   - **Media Functions**:
     - `c`: Capture an image.
     - `r`: Start/stop video recording.
   - **Control Actions**:
     - `e`: Take off the drone.
     - `q`: Land the drone.

## References

- [How to Control DJI Tello Drone with Python (YouTube)](https://www.youtube.com/watch?v=LmEcyQnfpDA&t=60s)
- [DJITelloPy Library on GitHub](https://github.com/damiafuentes/DJITelloPy)
