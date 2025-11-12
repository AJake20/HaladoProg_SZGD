# Haladó Programozás
# Fájl: main.py
# Székely Gábor Dániel - E5LG6T

import ultralytics
# Sikeres telepítés ellenőrzése
print("Ultralytics version:", ultralytics.__version__)

import cv2
import pandas as pd
from ultralytics import YOLO
#from tracker import *

#  YOLO small modell betöltése
model=YOLO("yolov8s.pt")

class_list = {'car', 'motorcycle', 'bus', 'truck'}

#tracker = Tracker()
count = 0

# Videó megnyitása
cap = cv2.VideoCapture("input.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame)
    # Tesztelés
    #print(results)
    a = results[0].boxes.data
    a = a.detach().cpu().numpy()
    px = pd.DataFrame(a).astype("float")
    #print(px)

    cv2.imshow("Frame", frame)
    # Kilépés 'q' billentyűvel
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()