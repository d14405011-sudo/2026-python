@echo off
REM Clean_Project.bat - Project Cleanup Tool
REM Removes cache, builds, temp files to keep project clean

REM Set encoding for proper character display
%SystemRoot%\System32\chcp.com 65001 >nul
set PYTHONIOENCODING=utf-8

setlocal enabledelayedexpansion

REM Get project root directory
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

echo.
echo ========================================================
echo  Cleanup Tool - Clean_Project.bat v2.0
echo  Project Root: %PROJECT_ROOT%
echo ========================================================
echo.

set "CLEANED_COUNT=0"

echo Scanning and cleaning cache files...
echo.

REM Task 1: Delete all __pycache__ folders
echo [1/6] Deleting __pycache__ folders...
for /r "%PROJECT_ROOT%" %%D in (__pycache__) do (
    if exist "%%D" (
        echo   - Deleting: %%D
        rmdir /s /q "%%D" 2>nul
        if !errorlevel! equ 0 (
            set /a CLEANED_COUNT+=1
        ) else (
            echo   Warning: Cannot delete %%D (may be in use)
        )
    )
)

REM Task 2: Delete all .pyc files
echo.
echo [2/6] Deleting .pyc files...
set "PYCC_COUNT=0"
for /r "%PROJECT_ROOT%" %%F in (*.pyc) do (
    if exist "%%F" (
        del /f /q "%%F" 2>nul
        if !errorlevel! equ 0 (
            set /a PYCC_COUNT+=1
        )
    )
)
if !PYCC_COUNT! gtr 0 (
    echo   - Deleted !PYCC_COUNT! .pyc files
    set /a CLEANED_COUNT+=!PYCC_COUNT!
)

REM Task 3: Delete build/ directory
echo.
echo [3/6] Checking build/ directory...
if exist "%PROJECT_ROOT%build" (
    echo   - Deleting: build/
    rmdir /s /q "%PROJECT_ROOT%build" 2>nul
    if !errorlevel! equ 0 (
        set /a CLEANED_COUNT+=1
    ) else (
        echo   Warning: Cannot delete build/ (may be in use)
    )
) else (
    echo   - build/ does not exist, skipping
)

REM Task 4: Delete dist/ directory
echo.
echo [4/6] Checking dist/ directory...
if exist "%PROJECT_ROOT%dist" (
    echo   - Deleting: dist/
    rmdir /s /q "%PROJECT_ROOT%dist" 2>nul
    if !errorlevel! equ 0 (
        set /a CLEANED_COUNT+=1
    ) else (
        echo   Warning: Cannot delete dist/ (may be in use)
    )
) else (
    echo   - dist/ does not exist, skipping
)

REM Task 5: Delete .egg-info directories
echo.
echo [5/6] Checking .egg-info directories...
for /d %%D in ("%PROJECT_ROOT%*.egg-info") do (
    if exist "%%D" (
        echo   - Deleting: %%D
        rmdir /s /q "%%D" 2>nul
        if !errorlevel! equ 0 (
            set /a CLEANED_COUNT+=1
        )
    )
)

REM Task 6: Delete cache and test files
echo.
echo [6/6] Checking test cache...
if exist "%PROJECT_ROOT%.pytest_cache" (
    echo   - Deleting: .pytest_cache/
    rmdir /s /q "%PROJECT_ROOT%.pytest_cache" 2>nul
)
if exist "%PROJECT_ROOT%.coverage" (
    echo   - Deleting: .coverage
    del /f /q "%PROJECT_ROOT%.coverage" 2>nul
)

echo.
echo [OK] Cleanup complete! Processed !CLEANED_COUNT! items
echo.

REM Verify no remaining __pycache__ files
set "REMAINING=0"
for /r "%PROJECT_ROOT%" %%D in (__pycache__) do (
    if exist "%%D" (
        set /a REMAINING+=1
    )
)

if !REMAINING! gtr 0 (
    echo Warning: !REMAINING! __pycache__ folders still exist (may be in use)
    echo Solution: Please close all Python programs or editors and retry
)

echo.
echo ========================================================
echo  Cleanup Complete!
echo ========================================================
echo.
echo Cleaned items:
echo   - __pycache__ folders (all levels)
echo   - *.pyc files (all levels)
echo   - build/ directory
echo   - dist/ directory
echo   - .egg-info directories
echo   - .pytest_cache/
echo   - .coverage file
echo.
echo Tips:
echo   1. Close Python/IDE if cleanup failed
echo   2. Run cleanup regularly to keep project clean
echo   3. Safe to commit git after cleanup
echo.

pause
exit /b 0
