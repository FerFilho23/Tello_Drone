# Tello Drone

![Python](https://img.shields.io/badge/Python-3.10.x-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![DJITelloPy](https://img.shields.io/badge/DJITelloPy-2.x-orange?logo=dji&logoColor=white)
![Numpy](https://img.shields.io/badge/numpy-2.x-cyan?logo=numpy&logoColor=white)
![Pygame](https://img.shields.io/badge/pygame-2.x-yellow?logo=pygame&logoColor=white)

## Project Description

This project is a Python application that allows you to control the DJI Tello drone using your keyboard. It also includes an **autonomous control by face tracking**, enabling the drone to follow a detected face in real time using OpenCV.

### Key Features

- **Manual Mode**: Control drone movement via keyboard inputs.
- **Face Tracking Mode**: The drone can detect and track a face automatically.
- Display real-time video feed.
- Capture images and videos from the drone feed.

## How to Install the Project

### 1. Clone the Repository

```bash
git clone https://github.com/FerFilho23/Tello_Drone.git
cd <PROJECT_FOLDER>
```

### 2. Create and Activate a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Ensure all required packages are installed:

```bash
pip install -r requirements.txt
```

## How to Run the Project

### 1. Connect the Drone

- Ensure the Tello drone is powered on and connected to your computer's Wi-Fi.

### 2. Run the Script

Execute the main project file:

```bash
python main.py
```

### 3. Keyboard Controls

- **Control Actions**:
  - `e`: Take off the drone.
  - `q`: Land the drone.
- **Drone Movement**:
  - `w`: Move up
  - `s`: Move down
  - `a`: Rotate left
  - `d`: Rotate right
  - `i`: Move forward
  - `k`: Move backward
  - `l`: Move right
  - `j`: Move left
  - **Autonomous Mode**:
  - `t`: Enable/Disable face tracking.
- **Media Functions**:
  - `c`: Capture an image.
  - `r`: Start/stop video recording.

## References

- [How to Control DJI Tello Drone with Python (YouTube)](https://www.youtube.com/watch?v=LmEcyQnfpDA&t=60s)
- [DJITelloPy Library on GitHub](https://github.com/damiafuentes/DJITelloPy)
