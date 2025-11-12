# Haladó Programozás
# Fájl: main.py
# Székely Gábor Dániel - E5LG6T

import ultralytics
# Sikeres telepítés ellenőrzése
print("Ultralytics version:", ultralytics.__version__)

import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import *

#  YOLO small modell betöltése
model=YOLO("yolov8s.pt")

class_list = {'car', 'motorcycle', 'bus', 'truck'}

tracker = Tracker()
count = 0
