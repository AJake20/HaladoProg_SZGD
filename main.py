# Haladó Programozás
# Fájl: main.py
# Székely Gábor Dániel - E5LG6T

import cv2
import cvzone
import math
from sort import *
import ultralytics
import pandas as pd
# Sikeres telepítés ellenőrzése
print("Ultralytics version:", ultralytics.__version__)

model = ultralytics.YOLO('yolov8s.pt')

cap = cv2.VideoCapture('input.mp4')

classnames = ['truck']

tracker = Sort()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (1020, 500))
    results = model.predict(frame)
    a = results[0].boxes.data.detach().cpu().numpy()
    px = pd.DataFrame(a).astype("float")
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


