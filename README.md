# Hand Gesture Recognition with MediaPipe & OpenCV

This project implements real-time hand gesture recognition using a webcam. It uses Google's [MediaPipe](https://mediapipe.dev/) for hand tracking and OpenCV for visualization. Recognized gestures can be mapped to specific control actions (e.g., turning a fan on/off, increasing/decreasing speed).

## ✋ Recognized Gestures

| Gesture                         | Meaning                  |
|-------------------------------|--------------------------|
| ✊ (All fingers down)           | OFF                      |
| 🖐️ (All fingers up)             | ON                       |
| ☝️ (Index finger only)          | Increase Speed (Fan)     |
| 🤟 (Index, Middle, Ring up)     | Maximum Speed (Fan)      |
| ✌️ (Index, Middle up)           | Decrease Speed (Fan)     |
| ❓ (Other combinations)         | Unknown Gesture          |

## 🧠 How It Works

- Uses MediaPipe to detect 21 hand landmarks.
- Finger state (up/down) is detected based on relative landmark positions.
- Gesture is inferred from the finger configuration.

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- OpenCV
- MediaPipe

Install dependencies:

```bash
pip install opencv-python mediapipe
