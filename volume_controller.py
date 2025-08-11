#!/usr/bin/env python
# coding: utf-8

# In[7]:


import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ================== Initialization ==================
# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640) # Set width
cap.set(4, 480) # Set height

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize pycaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get the valid volume range from your system
vol_range = volume.GetVolumeRange() # This is typically (-65.25, 0.0) for Windows
min_vol = vol_range[0]
max_vol = vol_range[1]

# ================== Main Loop ==================
while True:
    success, img = cap.read()
    if not success:
        continue

    # Flip the image horizontally for a mirror-view display
    img = cv2.flip(img, 1)
    
    # Convert the BGR image to RGB for MediaPipe
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image to find hands
    results = hands.process(img_rgb)

    landmark_list = []
    # If a hand is detected, process its landmarks
    if results.multi_hand_landmarks:
        # We'll use the first detected hand
        my_hand = results.multi_hand_landmarks[0]
        
        # Draw the skeleton on the hand
        mp_draw.draw_landmarks(img, my_hand, mp_hands.HAND_CONNECTIONS)

        # Extract landmark coordinates into a list
        for id, lm in enumerate(my_hand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            landmark_list.append([id, cx, cy])
    
    # If landmarks were extracted, perform gesture calculation
    if len(landmark_list) != 0:
        # Get coordinates for thumb tip (4) and index finger tip (8)
        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[8][1], landmark_list[8][2]
        
        # Calculate the distance between thumb and index finger
        length = math.hypot(x2 - x1, y2 - y1)
        
        # --- Volume Mapping ---
        # Hand distance range (needs tuning): ~20 to ~200
        # System volume range: min_vol to max_vol
        
        # Map the finger distance to the system's volume range
        vol = np.interp(length, [20, 200], [min_vol, max_vol])
        
        # Set the system volume
        volume.SetMasterVolumeLevel(vol, None)
        
        # --- Visual Feedback ---
        # Draw a visual line and circles on the fingertips
        cv2.circle(img, (x1, y1), 12, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Change color of the line when gesture is active (fingers are close)
        if length < 20:
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

    # --- Draw a static Volume Bar for reference ---
    vol_percent = int(np.interp(volume.GetMasterVolumeLevel(), [min_vol, max_vol], [0, 100]))
    vol_bar_height = int(np.interp(vol_percent, [0, 100], [400, 150]))
    
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3) # Bar outline
    cv2.rectangle(img, (50, vol_bar_height), (85, 400), (0, 255, 0), cv2.FILLED) # Filled bar
    cv2.putText(img, f'{vol_percent} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    # Display the final image
    cv2.imshow("AI Hand Gesture Volume Control", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ================== Cleanup ==================
cap.release()
cv2.destroyAllWindows()


# In[ ]:




