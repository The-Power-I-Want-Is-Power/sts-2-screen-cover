@echo off
REM Double-click this to install deps (first run only) and launch the prank.
REM The `keyboard` library needs admin to capture global hotkeys reliably.
REM If F8 doesn't fire, right-click run.bat -> Run as administrator.

cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python not found on PATH. Install Python 3 from python.org and re-run.
    pause
    exit /b 1
)

python -c "import pydirectinput, keyboard" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
)

python screen_cover.py
