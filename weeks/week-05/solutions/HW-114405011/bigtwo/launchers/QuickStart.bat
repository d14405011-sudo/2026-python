@echo off
REM 大老二遊戲 - 統一啟動器 (QuickStart)
REM 已移除所有硬編碼路徑，支援任意磁碟和目錄

setlocal enabledelayedexpansion

REM 支援 UTF-8 編碼（繁體中文）
%SystemRoot%\System32\chcp.com 65001 >nul
set PYTHONIOENCODING=utf-8

REM 動態找到遊戲根目錄（此腳本在 launchers 目錄）
set "SCRIPT_DIR=%~dp0"
set "GAME_DIR=%SCRIPT_DIR%.."

echo ========================================================
echo  大老二遊戲啟動器
echo ========================================================
echo.
echo 遊戲目錄: %GAME_DIR%
echo.

REM 虛擬環境搜尋策略（優先級從高到低）
set "VENV_PYTHON="

REM 策略 1: 本地虛擬環境（同級目錄 .venv）
if exist "%GAME_DIR%\.venv\Scripts\python.exe" (
    set "VENV_PYTHON=%GAME_DIR%\.venv\Scripts\python.exe"
    echo [✓] 找到虛擬環境: .venv
    goto launch
)

REM 策略 2: 上層虛擬環境（..\.venv）
if exist "%GAME_DIR%\..\.venv\Scripts\python.exe" (
    set "VENV_PYTHON=%GAME_DIR%\..\.venv\Scripts\python.exe"
    echo [✓] 找到虛擬環境: ..\.venv
    goto launch
)

REM 策略 3: 系統 Python
echo [INFO] 未找到虛擬環境，嘗試使用系統 Python...
set "VENV_PYTHON=python.exe"

:launch
REM 驗證遊戲檔案
if not exist "%GAME_DIR%\main.py" (
    echo.
    echo [ERROR] main.py 未找到
    echo 期望路徑: %GAME_DIR%\main.py
    echo.
    pause
    exit /b 1
)

cd /d "%GAME_DIR%"
echo.
echo 正在啟動大老二遊戲...
echo.

REM 執行遊戲
"%VENV_PYTHON%" main.py

REM 錯誤檢查
if errorlevel 1 (
    echo.
    echo ========================================================
    echo  啟動失敗
    echo ========================================================
    echo.
    echo 故障排除：
    echo   1. 檢查虛擬環境: python -m venv .venv
    echo   2. 安裝套件: pip install -r requirements.txt
    echo   3. 檢查版本: python --version
    echo.
) else (
    echo.
    echo ========================================================
    echo  遊戲已正常結束
    echo ========================================================
    echo.
)

pause
exit /b %errorlevel%
