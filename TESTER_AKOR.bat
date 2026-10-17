@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 -m unittest discover -s tests -v
) else (
  python -m unittest discover -s tests -v
)
if errorlevel 1 (
  echo Akor tests failed.
  pause
  exit /b 1
)
echo Akor tests finished.
pause
