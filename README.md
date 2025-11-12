# Haladó Programozás — 1. Járműszámlálás videó alapján

Ez a projekt egy egyszerű demó a járműdetektálásra és -számlálásra. A projekt a következő fontos részeket használja:

- `main.py` — a fő futtatható szkript, ami YOLO detekciót futtat és kirajzolja a detektált járműveket.
- `requirements.txt` — a Python függőségek listája.

Telepítés (Windows / PowerShell)
1. Hozz létre és aktiválj virtuális környezetet (ajánlott):
```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```
2. Telepítsd a függőségeket:
```powershell
pip install -r .\requirements.txt
```

ByteTrack telepítése (opcionális, ha szeretnéd használni a ByteTrack nyomkövetőt)
- Telepítés PyPI/GitHub-ról (ajánlott):
```powershell
pip install git+https://github.com/ifzhang/ByteTrack.git
```
- Vagy ha helyileg van a `ByteTrack` mappa a projekt gyökerében és a repo tartalmaz build/telepítési fájlokat:
```powershell
pip install -e .\ByteTrack
```

Megjegyzés: A projekt `main.py` nem módosítja a `sys.path`-et automatikusan. Ha ByteTrack nincs telepítve, a program figyelmeztetést ír ki és továbbhalad (nem fog meghívni ByteTrack kódot). Ha valaki máshol tárolja a ByteTrack forrást, beállíthatja a `BYTETRACK_PATH` környezeti változót és telepítheti a csomagot helyileg.

Futtatás
```powershell
python main.py
```

Ha bármilyen problémád van a telepítéssel, másold be a hibaüzenetet ide, és segítek a javításban.

