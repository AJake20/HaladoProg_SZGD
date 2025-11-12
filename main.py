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

classnames = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck']

tracker = Sort()
count = 0
offset = 2  # vonal vastagsága
down = {}
up = {}

counter_down = []
counter_up = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1020, 500))
    results = model.predict(frame)
    a = results[0].boxes.data
    a = a.detach().cpu().numpy()
    px = pd.DataFrame(a).astype("float")
    #print(px)

    # Build detection array in format expected by SORT: [[x1,y1,x2,y2,score], ...]
    dets_list = []
    for index, row in px.iterrows():
        x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])
        conf = float(row[4])
        cls = int(row[5])
        class_name = classnames[cls]
        if class_name == 'truck':
            dets_list.append([x1, y1, x2, y2])

    if len(dets_list) > 0:
        dets = np.array(dets_list, dtype=float)
    else:
        dets = np.empty((0, 4), dtype=float)

    bbox_id = tracker.update(dets)

    red_line_y = 250
    blue_line_y = 350

    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        cx = int((x3 + x4) / 2)
        cy = int((y3 + y4) / 2)
        #cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        #cv2.putText(frame, str(int(id)), (cx, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
        #if red_line_y < cy + offset and red_line_y > cy - offset:
        #    down[id] = cy
        #    if id in down:
        #        cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        #        cv2.putText(frame, str(int(id)), (cx, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
        
        #if blue_line_y < cy + offset and blue_line_y > cy - offset:
        #    up[id] = cy
        #    if id in up:
        #        cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        #        cv2.putText(frame, str(int(id)), (cx, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
        if red_line_y < cy + offset and red_line_y > cy - offset:
            down[id] = cy
        if id in down:
            if blue_line_y < cy + offset and blue_line_y > cy - offset:
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                cv2.putText(frame, str(int(id)), (cx, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
                counter_down.append(id)
        
        if blue_line_y < cy + offset and blue_line_y > cy - offset:
            up[id] = cy
        if id in up:
            if red_line_y < cy + offset and red_line_y > cy - offset:
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                cv2.putText(frame, str(int(id)), (cx, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
                counter_up.append(id)
    
    #print(down)
    #print(up)
    #print(bbox_id)
    text_color = (255, 0, 255)
    red_color = (0, 0, 255)
    blue_color = (255, 0, 0)

    cv2.line(frame, (250, 250), (750, 250), red_color, 2)
    cv2.putText(frame, "Red Line", (500, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.9, red_color, 2)

    cv2.line(frame, (50, 350), (950, 350), blue_color, 2)
    cv2.putText(frame, "Blue Line", (700, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.9, blue_color, 2)

    
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


