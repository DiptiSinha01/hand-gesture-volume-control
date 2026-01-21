"""
Hand Gesture Volume Control 🎚️
--------------------------------
Control system volume using thumb–index finger distance
via MediaPipe + OpenCV + Pycaw (Windows only)

Author: <Dipti Sinha>
"""

# =======================
# Imports
# =======================
import cv2
import mediapipe as mp
import math
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# =======================
# UI Helper Functions
# =======================
def draw_glass_panel(img):
    """Draws a translucent glass-style panel"""
    overlay = img.copy()
    cv2.rectangle(overlay, (20, 70), (180, 460), (25, 25, 25), -1)
    cv2.addWeighted(overlay, 0.55, img, 0.45, 0, img)


def draw_volume_ui(img, vol_per, vol_bar):
    """Draws volume bar with smooth color transitions"""

    # Color based on volume percentage
    if vol_per <= 30:
        color = (0, 200, 255)      # Cyan
    elif vol_per <= 60:
        color = (0, 255, 120)      # Green
    elif vol_per <= 85:
        color = (0, 255, 255)      # Yellow
    else:
        color = (0, 0, 255)        # Red

    # Bar outline
    cv2.rectangle(img, (80, 150), (120, 400), (180, 180, 180), 2)

    # Filled bar
    cv2.rectangle(
        img,
        (80, int(vol_bar)),
        (120, 400),
        color,
        cv2.FILLED
    )

    # Percentage text
    cv2.putText(
        img,
        f"{int(vol_per)}%",
        (65, 430),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2
    )


# =======================
# Audio Setup (Windows)
# =======================
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_min, vol_max = volume.GetVolumeRange()[:2]

prev_vol = 0
smooth_factor = 0.2


# =======================
# Camera Setup
# =======================
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("❌ Camera not accessible")
    exit()


# =======================
# MediaPipe Hands Setup
# =======================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils


# =======================
# Main Loop
# =======================
while True:
    success, img = cap.read()
    if not success or img is None:
        print("❌ Failed to read frame")
        continue

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Thumb & index fingertip
            thumb = hand_landmarks.landmark[
                mp_hands.HandLandmark.THUMB_TIP
            ]
            index = hand_landmarks.landmark[
                mp_hands.HandLandmark.INDEX_FINGER_TIP
            ]

            x1, y1 = int(thumb.x * w), int(thumb.y * h)
            x2, y2 = int(index.x * w), int(index.y * h)

            cv2.line(img, (x1, y1), (x2, y2), (0, 200, 255), 4)
            cv2.circle(img, (x1, y1), 10, (0, 200, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 200, 255), cv2.FILLED)

            # Distance between fingers
            length = math.hypot(x2 - x1, y2 - y1)
            length = np.clip(length, 20, 200)

            # Map distance to volume
            vol = np.interp(length, [20, 200], [vol_min, vol_max])
            vol_bar = np.interp(length, [20, 200], [400, 150])
            vol_per = np.interp(length, [20, 200], [0, 100])

            # Smooth volume transition
            smooth_vol = prev_vol + smooth_factor * (vol - prev_vol)
            volume.SetMasterVolumeLevel(smooth_vol, None)
            prev_vol = smooth_vol

            # UI
            draw_glass_panel(img)
            draw_volume_ui(img, vol_per, vol_bar)

    # Title
    cv2.putText(
        img,
        "Hand Gesture Volume Control",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (240, 240, 240),
        2
    )

    cv2.imshow("Hand Gesture Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# =======================
# Cleanup
# =======================
cap.release()
cv2.destroyAllWindows()
