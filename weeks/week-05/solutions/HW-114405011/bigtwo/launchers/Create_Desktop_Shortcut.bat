@echo off
REM =======================================================
REM Create Desktop Shortcut (Improved v2.0)
REM Set working directory to game root for correct assets loading
REM =======================================================

setlocal enabledelayedexpansion
where chcp >nul 2>&1
if not errorlevel 1 chcp 65001 >nul

REM [Dynamic path] Resolve game root from this script location
for %%A in ("%~dp0..") do set "GAME_ROOT=%%~fA"

REM [Launcher paths]
set "LAUNCHER=%GAME_ROOT%\launchers\QuickStart.bat"
set "VBS_LAUNCHER=%GAME_ROOT%\launchers\RunGame.vbs"
set "ICON_FILE=%GAME_ROOT%\assets\icon-v2.ico"
if not exist "%ICON_FILE%" set "ICON_FILE=%GAME_ROOT%\assets\icon.ico"

echo.
echo =======================================================
echo  Create Desktop Shortcut
echo =======================================================
echo.
echo Game root: %GAME_ROOT%
echo.

REM [Validate required files]
if not exist "%LAUNCHER%" (
    echo [ERROR] QuickStart.bat not found
    echo         Expected path: %LAUNCHER%
    pause
    exit /b 1
)

if not exist "%GAME_ROOT%\main.py" (
    echo [ERROR] main.py not found
    echo         Expected path: %GAME_ROOT%\main.py
    pause
    exit /b 1
)

if not exist "%GAME_ROOT%\assets" (
    echo [WARN] assets folder not found
    echo        Shortcut will still be created, but game resources may be missing
)

REM [Get desktop path]
for /f "delims=" %%D in ('powershell -NoProfile -Command "[Environment]::GetFolderPath('Desktop')"') do set "DESKTOP=%%D"
if "%DESKTOP%"=="" set "DESKTOP=%USERPROFILE%\Desktop"

REM [Shortcut path]
set "SHORTCUT=%DESKTOP%\BigTwo_Game.lnk"

REM [Delete existing shortcut]
if exist "%SHORTCUT%" (
    del "%SHORTCUT%" >nul 2>&1
    echo [OK] Deleted old shortcut
)

REM =======================================================
REM [Create shortcut] Use PowerShell and set working directory
REM =======================================================

echo [INFO] Creating shortcut...

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ws=New-Object -ComObject WScript.Shell; " ^
    "$s=$ws.CreateShortcut('%SHORTCUT%'); " ^
    "$s.TargetPath='%LAUNCHER%'; " ^
    "$s.WorkingDirectory='%GAME_ROOT%'; " ^
    "$s.IconLocation='%ICON_FILE%,0'; " ^
    "$s.Description='Big Two Game - Quick Start'; " ^
    "$s.WindowStyle=1; " ^
    "$s.Save(); " ^
    "Write-Host '[OK] Shortcut created successfully' -ForegroundColor Green"

if exist "%SHORTCUT%" (
    echo.
    echo =======================================================
    echo  Shortcut created successfully
    echo =======================================================
    echo.
    echo Location: %SHORTCUT%
    echo Working directory: %GAME_ROOT%
    echo.
    echo Notes:
    echo   - Working directory is set to game root
    echo   - assets/ resources should load correctly
    echo   - Double-click the shortcut to start the game
    echo.
) else (
    echo.
    echo [ERROR] Failed to create shortcut
    echo.
)

pause
exit /b 0
