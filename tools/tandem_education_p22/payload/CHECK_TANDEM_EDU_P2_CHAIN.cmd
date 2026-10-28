@echo off
setlocal EnableExtensions DisableDelayedExpansion
set "PYTHONUTF8=1"
chcp 65001 >nul
rem %%~dp0 ends in a backslash. Quoting it directly can absorb the next arg
rem under the Windows C argv parser. Append '.' before the final quote.
set "AKOR_ROOT=%~dp0."
set "WORLDS_ROOT=%~dp0..\..\..\Orgo\Orgo_Worlds"
set "ORGO_ROOT=%~dp0..\..\..\Orgo\Orgo"
set "CHECKER=%~dp0tools\tandem_education_p21\cross_repo_check.py"
if not exist "%CHECKER%" (
  echo [ECHEC] Verificateur P2.1 introuvable 1>&2
  exit /b 2
)
if not exist "%WORLDS_ROOT%\tools\tandem_education_p2\manifest.json" (
  echo [ECHEC] Depot Orgo_Worlds P2 introuvable 1>&2
  exit /b 2
)
if not exist "%ORGO_ROOT%\tools\tandem_education_p2\manifest.json" (
  echo [ECHEC] Depot Orgo P2 introuvable 1>&2
  exit /b 2
)
where py >nul 2>&1
if not errorlevel 1 (
  py -3 "%CHECKER%" --akor "%AKOR_ROOT%" --worlds "%WORLDS_ROOT%" --orgo "%ORGO_ROOT%"
) else (
  python "%CHECKER%" --akor "%AKOR_ROOT%" --worlds "%WORLDS_ROOT%" --orgo "%ORGO_ROOT%"
)
if errorlevel 1 (
  echo [ECHEC] Qualification croisee hors ligne refusee 1>&2
  exit /b 1
)
echo [OK] Qualification croisee P2 hors ligne reussie
endlocal
