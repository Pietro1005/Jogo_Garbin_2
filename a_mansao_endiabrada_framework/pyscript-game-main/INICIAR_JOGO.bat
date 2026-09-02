@echo off
title Framework PyScript Game Jam
cd /d "%~dp0"

echo =============================================
echo  FRAMEWORK PYSCRIPT GAME JAM
echo =============================================
echo.
echo Abrindo o jogo em:
echo http://localhost:8000
echo.

start "" http://localhost:8000
python -m http.server 8000

pause
