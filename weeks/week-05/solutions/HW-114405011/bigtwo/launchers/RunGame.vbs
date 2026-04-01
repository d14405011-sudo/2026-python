' ═══════════════════════════════════════════════════════
' 大老二遊戲 - VBScript 隱形啟動器 (v2.0)
' ═══════════════════════════════════════════════════════
' 用途：在沒有控制台窗口的情況下啟動遊戲
' 已移除所有硬編碼路徑，支援動態虛擬環境搜尋
' ═══════════════════════════════════════════════════════

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' 【路徑推導】獲取遊戲根目錄
' 此腳本在 launchers\ 目錄，需向上一級找到遊戲根目錄
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)  ' launchers\
gameDir = fso.GetParentFolderName(scriptDir)                ' 遊戲根目錄
mainPy = fso.BuildPath(gameDir, "main.py")

' 【虛擬環境搜尋策略】優先級從高到低
' 策略 1：遊戲根目錄下的 .venv
pythonExe = ""
venv1Path = fso.BuildPath(gameDir, ".venv\Scripts\pythonw.exe")
if fso.FileExists(venv1Path) then
    pythonExe = venv1Path
    ' WScript.Echo "[✓] 找到本地虛擬環境"
end if

' 策略 2：上一層目錄的 .venv (..\.venv)
if pythonExe = "" then
    parentDir = fso.GetParentFolderName(gameDir)
    venv2Path = fso.BuildPath(parentDir, ".venv\Scripts\pythonw.exe")
    if fso.FileExists(venv2Path) then
        pythonExe = venv2Path
        ' WScript.Echo "[✓] 找到上層虛擬環境"
    end if
end if

' 策略 3：系統路徑（pythonw.exe）
if pythonExe = "" then
    pythonExe = "pythonw.exe"
    ' WScript.Echo "[INFO] 使用系統 Python"
end if

' 【檢查 main.py 是否存在】
if not fso.FileExists(mainPy) then
    ' 無法隱形啟動失敗的對話框，回退到批處理
    shell.Run "cmd /c cd /d """ & gameDir & """ && python main.py", 1, False
    WScript.Quit 1
end if

' 【啟動遊戲】隱形運行（參數 0 表示隱形窗口）
shell.Run """" & pythonExe & """ """ & mainPy & """", 0, False
WScript.Quit 0
