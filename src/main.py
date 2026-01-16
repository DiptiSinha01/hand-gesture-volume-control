# import cv2
# import time
# import numpy as np

# cap=cv2.VideoCapture(0)

# while True:
#     success, img= cap.read()
#     cv2.imshow("Img",img)
#     cv2.waitKey(1)

#########################
#WORKING CAMERA CODE
##########################

# import cv2

# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("ERROR: Camera not accessible")
#     exit()

# while True:
#     success, img = cap.read()
#     if not success:
#         print("Failed to grab frame")
#         break

#     cv2.imshow("Img", img)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

########################
#ACTUAL CODE
#########################

import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)

mp_hands=mp.solutions.hands

hands=mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw=mp.solutions.drawing_utils

while True:
    success, img=cap.read()
    if not success:
        break

    img=cv2.flip(img,1)
    img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    result=hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("Hand Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()