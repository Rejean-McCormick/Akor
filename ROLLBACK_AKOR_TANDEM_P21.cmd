@echo off
setlocal
set "PYTHONUTF8=1"
chcp 65001 >nul
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  py -3 "%~dp0tools\tandem_education_p21\manager.py" ROLLBACK
) else (
  python "%~dp0tools\tandem_education_p21\manager.py" ROLLBACK
)
if errorlevel 1 (
 echo [ECHEC] Akor P2.1 ROLLBACK
 exit /b 1
)
endlocal
