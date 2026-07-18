@echo off
setlocal
cd /d %~dp0

if not exist .venv (
    py -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-app.txt

pyinstaller --noconfirm --clean --windowed --name SilentLearner ^
  --paths core ^
  app\main.py

echo.
echo Ejecutable generado en dist\SilentLearner\SilentLearner.exe
endlocal
