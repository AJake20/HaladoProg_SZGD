# Haladó Programozás
# Fájl: main.py
# Székely Gábor Dániel - E5LG6T

import cv2
import cvzone
import math
from sort import *
import ultralytics
import pandas as pd
import numpy as np
#print("Ultralytics version:", ultralytics.__version__)

# --- Inicializálás ---
model = ultralytics.YOLO('yolov8s.pt')

# Ellenőrizze, hogy a videó fájl létezik-e és elérhető-e
cap = cv2.VideoCapture('videos/vehicle-counting.mp4')
if not cap.isOpened():
    print("Hiba: Nem sikerült betölteni a videót.")
    exit()

classnames = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat'] 

selected_classes = "truck"

tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
count = 0
offset = 15
down = {}
up = {}


counter_down_set = set()
counter_up_set = set()


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1020, 500))
    
    results = model.predict(frame, verbose=False)
    
    a = results[0].boxes.data
    a = a.detach().cpu().numpy()
    px = pd.DataFrame(a).astype("float")

    dets_list = []
    for index, row in px.iterrows():
        x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])
        conf = float(row[4])
        cls = int(row[5])
        
        # Ellenőrzés, hogy a class index a listában van-e
        if cls < len(classnames):
            class_name = classnames[cls]

            if class_name in selected_classes:
                dets_list.append([x1, y1, x2, y2, conf])
                #cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 1)

    # A SORT frissítése
    if len(dets_list) > 0:
        dets = np.array(dets_list, dtype=float) 
    else:
        dets = np.empty((0, 5), dtype=float) # 5 oszlop (x1, y1, x2, y2, score)

    bbox_id = tracker.update(dets)

    red_line_y = 250
    blue_line_y = 300

    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        x3, y3, x4, y4, id = int(x3), int(y3), int(x4), int(y4), int(id)
        
        cx = int((x3 + x4) / 2)
        cy = int((y3 + y4) / 2)    
        
        if red_line_y < (cy + offset) and red_line_y > (cy - offset):
            down[id] = cy
            
        if id in down:
            if blue_line_y < (cy + offset) and blue_line_y > (cy - offset):
                if id not in counter_down_set:
                    counter_down_set.add(id)
                    cv2.circle(frame, (cx, cy), 5, (180, 180, 180), cv2.FILLED)
                    cv2.putText(frame, str(id), (cx, cy - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (180, 180, 180), 2)
                if id in down:
                     del down[id]
                
        if blue_line_y < (cy + offset) and blue_line_y > (cy - offset):
            up[id] = cy
            
        if id in up:
            if red_line_y < (cy + offset) and red_line_y > (cy - offset):
                if id not in counter_up_set:
                    counter_up_set.add(id)
                    cv2.circle(frame, (cx, cy), 5, (180, 180, 180), cv2.FILLED)
                    cv2.putText(frame, str(id), (cx, cy - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (180, 180, 180), 2)
                if id in up:
                    del up[id]

    text_color = (0, 0, 0)
    red_color = (0, 0, 255)
    blue_color = (255, 0, 0)
    box_color = (100, 100, 100)

    downwards = len(counter_down_set)
    upwards = len(counter_up_set)

    # Vonalak rajzolása
    cv2.line(frame, (50, red_line_y), (970, red_line_y), red_color, 2)

    cv2.line(frame, (50, blue_line_y), (970, blue_line_y), blue_color, 2)

    # Számláló eredmények megjelenítése
    cv2.putText(frame, f'Downward {selected_classes}: {downwards}', (50, 50), cv2.FONT_HERSHEY_COMPLEX,1, (255, 255, 255), 2)
    cv2.putText(frame, f'Upward {selected_classes}: {upwards}', (50, 100), cv2.FONT_HERSHEY_COMPLEX,1, (255, 255, 255), 2)

    cv2.imshow('Vehicle Counting', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
# --- Erőforrások Felszabadítása ---
cap.release()
cv2.destroyAllWindows()