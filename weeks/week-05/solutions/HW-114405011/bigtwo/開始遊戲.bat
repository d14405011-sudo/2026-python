@echo off
REM 大老二遊戲 - 快速啟動器
REM 動態路徑搜索，支援任意磁碟和目錄

REM 設定編碼以支援正確的中文顯示
%SystemRoot%\System32\chcp.com 65001 >nul
set PYTHONIOENCODING=utf-8

REM 進入遊戲根目錄
cd /d "%~dp0"

echo 正在啟動大老二遊戲...
echo.

REM 優先級 1: 同層目錄的虛擬環境
if exist ".venv\Scripts\python.exe" (
    echo [✓] 找到虛擬環境: .venv
    ".venv\Scripts\python.exe" main.py
    goto cleanup
)

REM 優先級 2: 上層目錄的虛擬環境 (../../../.venv)
if exist "..\..\..\.venv\Scripts\python.exe" (
    echo [✓] 找到虛擬環境: ..\..\..\.venv
    "..\..\..\.venv\Scripts\python.exe" main.py
    goto cleanup
)

REM 優先級 3: 系統 Python
echo [INFO] 使用系統 Python
python main.py
goto cleanup

:cleanup
REM 錯誤檢查
if %errorlevel% neq 0 (
    echo.
    echo ========================================================
    echo  啟動失敗 - 錯誤碼: %errorlevel%
    echo ========================================================
    echo.
    echo 故障排除：
    echo.
    echo 1. 檢查虛擬環境是否已建立
    echo    執行：python -m venv .venv
    echo.
    echo 2. 安裝必要的套件
    echo    執行：pip install -r requirements.txt
    echo.
    echo 3. 也可嘗試直接安裝 pygame
    echo    執行：pip install pygame-ce
    echo.
    echo 4. 檢查 Python 版本
    echo    執行：python --version
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