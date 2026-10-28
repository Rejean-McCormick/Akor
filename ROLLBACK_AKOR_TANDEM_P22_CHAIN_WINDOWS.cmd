@echo off
setlocal
set "PYTHONUTF8=1"
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  py -3 "%~dp0tools\tandem_education_p22\manager.py" ROLLBACK
) else (
  python "%~dp0tools\tandem_education_p22\manager.py" ROLLBACK
)
if errorlevel 1 exit /b 1
endlocal
