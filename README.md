# 🎚️ Hand Gesture Volume Control

Control your system volume in real time using hand gestures captured via your webcam.  
This project uses computer vision and hand tracking to map the distance between your fingers to system volume.

Built using Python, OpenCV, MediaPipe, and Pycaw (Windows).

---

## 🚀 Features

- Real-time webcam hand tracking
- Thumb–index finger distance based volume control
- Smooth volume transitions (no sudden jumps)
- Glass-style UI overlay with dynamic color feedback
- Low-latency and intuitive control
- Works on Windows

---

## 🛠️ Tech Stack

- Python
- OpenCV
- MediaPipe
- Pycaw (Windows audio control)
- NumPy

---

## 📂 Project Structure

```
hand-gesture-volume-control/
│
├── src/
│   └── main.py
│
├── README.md
├── requirements.txt
├── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository
```
git clone https://github.com/DiptiSinha01/hand-gesture-volume-control.git
cd hand-gesture-volume-control
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

> Make sure Python 3.8+ is installed.  
> This project is Windows-only due to Pycaw.

---

## ▶️ How to Run

```
python src/main.py
```

- Show your hand to the camera
- Pinch thumb and index finger
- Increase distance → volume up
- Decrease distance → volume down
- Press `Q` to exit

---

## 🧠 How It Works

1. MediaPipe detects hand landmarks in real time  
2. Distance between thumb tip and index tip is calculated  
3. Distance is mapped to the system volume range  
4. Volume smoothing prevents abrupt changes  
5. UI provides visual feedback using dynamic colors

---

## 🔮 Future Improvements

- Gesture-based mute/unmute
- Media control (play/pause/next)
- Customizable UI themes
- Cross-platform support

---

## 👩‍💻 Author

Dipti Sinha  
Computer Science (AI/ML)

GitHub: https://github.com/DiptiSinha01

---

⭐ If you like this project, consider giving it a star!
