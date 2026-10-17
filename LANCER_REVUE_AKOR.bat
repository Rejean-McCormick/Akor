@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 run_akor.py --root "%~dp0.." --out "%~dp0output"
) else (
  python run_akor.py --root "%~dp0.." --out "%~dp0output"
)
if errorlevel 1 (
  echo.
  echo Akor preflight could not complete. Check the six sister repositories and Node.js.
  pause
  exit /b 1
)
echo.
echo Read-only review ready: "%~dp0output\REVUE_ENSEIGNANT.html"
start "" "%~dp0output\REVUE_ENSEIGNANT.html"
pause
