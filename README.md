# Gesture Invisibility

Gesture Invisibility is a real-time computer vision project that creates a virtual invisibility effect controlled using hand gestures.

The system uses MediaPipe for person segmentation and gesture recognition, together with OpenCV for real-time webcam processing and background replacement.

An **open palm** activates the invisibility effect, while a **closed fist** makes the user visible again.

## Features

- Real-time webcam processing
- AI-based person segmentation
- Hand gesture recognition
- Open palm gesture activates invisibility
- Closed fist gesture restores visibility
- Gesture stabilization to prevent accidental activation
- Background capture for virtual invisibility
- Real-time FPS monitoring
- Smoothed FPS calculation for more stable performance readings
- Optimized gesture recognition by processing gestures every second frame
- On-screen status, gesture, FPS, and control information

## How It Works

1. The webcam captures live video frames.
2. The user moves out of the camera view and presses **B** to capture the background.
3. MediaPipe performs person segmentation to identify the user in each frame.
4. MediaPipe Gesture Recognizer detects hand gestures.
5. When an **Open_Palm** gesture is detected consistently, the system replaces the detected person region with the previously captured background, creating the invisibility effect.
6. When a **Closed_Fist** gesture is detected consistently, the original camera view is restored.
7. Gesture recognition is performed every second frame to reduce processing load while keeping the controls responsive.

## Gesture Controls

| Gesture | Action |
|---|---|
| Open Palm ✋ | Activate invisibility |
| Closed Fist ✊ | Return to visible mode |

## Keyboard Controls

| Key | Action |
|---|---|
| B | Capture or recapture the background |
| Q | Quit the application |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SNova844/gesture-invisibility.git
```

### 2. Move into the project folder

```bash
cd gesture-invisibility
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

## Technologies Used

- Python
- OpenCV
- MediaPipe
- MediaPipe Image Segmenter
- MediaPipe Gesture Recognizer

## Performance Optimization

Initial testing showed that running person segmentation and gesture recognition on every frame reduced real-time performance.

To reduce the processing load, gesture recognition was changed to run every second frame while person segmentation continues to run on every frame. This improved performance while maintaining responsive gesture controls.

A moving average of the most recent FPS readings is used to provide a more stable real-time performance measurement.

## Current Limitations

- The invisibility effect depends on a previously captured static background.
- Changes in lighting after background capture can reduce the quality of the effect.
- Physical shadows cast by the user may remain visible because human segmentation identifies the person rather than all shadows produced by the person.
- Segmentation quality may decrease during very fast movement or in difficult lighting conditions.
- Performance depends on the processing capability of the device.

## Future Improvements

- Adaptive background updating for changing environments
- Improved handling of shadows and segmentation boundaries
- Further performance optimization
- Support for additional custom gestures
- Improved graphical user interface
- Optional video recording of the invisibility effect