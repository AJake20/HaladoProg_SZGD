Haladó Programozás — 1. Beadandó: Járműszámlálás videóanalízissel

Szerző: Székely Gábor Dániel (E5LG6T)

Rövid leírás
-----------
Ez a projekt egy demonstrációs alkalmazás, amely videófelvételeken detektálja, követi és számlálja a kiválasztott járműtípusokat.Például egy ujonnan megépített autópályán forgalomfigyelésre tökéletes alkalmas lenne megállapítani milyen szazálékban használják a tehergépjárművek az új aszfaltot.
A cél bemutatni a detektálás (YOLOv8) és a követés (SORT) egyszerű integrációját, valamint egy stabil számlálási logikát két vízszintes vonal között.

Fő komponensek
----------------
- Detektor: YOLOv8s (`yolov8s.pt`) — ultralytics könyvtár.
- Követés: SORT (Simple Online and Realtime Tracking) — Kalman-filter és IoU alapú asszociáció; implementáció: `sort.py`. https://github.com/abewley/sort/tree/master
- Feldolgozás / megjelenítés: OpenCV (`cv2`), adatkezeléshez numpy és pandas.

Működési elv
------------
1. A `main.py` képkockáról képkockára hívja a YOLO detektort.
2. A detektált bounding boxokat (x1, y1, x2, y2) és score-okat (konfidencia) átalakítja a SORT által elvárt formátumba: `[x1, y1, x2, y2, score]` (N×5 numpy tömb).
3. A SORT tracker frissíti a nyomvonalakat, és minden nyomvonalhoz (track) egyedi ID-t rendel.
4. A számlálás két vízszintes vonal között történik: ha egy ID először az egyik vonalnál jelenik meg, majd később a másiknál, az áthaladást egyszer rögzítjük.

Számlálási logika (részletek)
----------------------------
- Vonalak: a Vörös vonal y=250, a Kék vonal y=300.
- Tolerancia: `offset = 15` pixel; az áthaladást akkor tekintjük érvényesnek, ha az objektum középpontja ezen érték ± tartományában van.
- Az ismételt számlálás elkerülése: a már számlált track ID-ket halmazokban tároljuk (`counter_down_set`, `counter_up_set`), így egy ID csak egyszer kerül beleszámításra.

Példa (logika röviden):

```python
# dets: np.array([[x1,y1,x2,y2,score], ...]) vagy np.empty((0,5))
bbox_id = tracker.update(dets)
for x1,y1,x2,y2,tid in bbox_id:
        cx = (x1+x2)//2; cy = (y1+y2)//2
        # red_line_y, blue_line_y és offset alapján döntünk az áthaladásról
```

Vizualizáció
------------
- A bounding boxok és track ID-k a képen jelennek meg.
- A számlálók (Downward / Upward) a bal felső sarokban kerülnek megjelenítésre.

Telepítés és futtatás (Windows PowerShell)
-----------------------------------------
1. Virtuális környezet létrehozása és aktiválása:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Függőségek telepítése:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. A bemeneti videó ellenőrzése (`videos/vehicle-counting.mp4` alapértelmezett), majd futtatás:

```powershell
python main.py
```

Kilépés: a videóablakban nyomd meg a `q` billentyűt.

Fontos konfigurációk a `main.py`-ben
-----------------------------------
- `model = YOLO('yolov8s.pt')` — modellfájl helye.
- `selected_classes` — figyelt osztályok; használj listát vagy halmazt, pl. `{'truck', 'car'}` (NE stringet: `"truck"` hibásan karakter-alapú `in` ellenőrzést okoz).
- `Sort(max_age=..., min_hits=..., iou_threshold=...)` — tracker paraméterek a követés stabilitásához.
- `red_line_y`, `blue_line_y`, `offset` — a számlálási zóna paraméterei.

Ismert korlátok és továbbfejlesztési javaslatok
---------------------------------------------
- A SORT egyszerű és gyors, de nem rendelkezik re-identification (re-ID) képességgel. Nagy torlódás vagy jelentős átfedés esetén előfordulhat ID-váltás.