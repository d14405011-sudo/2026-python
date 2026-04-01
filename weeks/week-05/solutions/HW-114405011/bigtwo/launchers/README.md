# 🎮 啟動器 (Launchers)

此目錄包含用於啟動大老二遊戲的工具。

## ⚡ 快速開始

### 🎯 最簡單的方式（推薦）
**只需雙擊 `QuickStart.bat` ✅**

遊戲即刻啟動！

## 📋 可用啟動器

### 1️⃣ 【推薦】QuickStart.bat
- **功能** ⚡：一鍵啟動遊戲
- **特點** ✅：
  - 最簡單、最快速
  - 自動尋找 Python 環境
  - UTF-8 編碼（支援繁體中文）
  - 提供友善的錯誤提示
- **用法**：直接雙擊

### 2️⃣ 【隱形啟動】RunGame.vbs
- **功能**：在後台無窗口啟動遊戲
- **用途**：當你想玩遊戲而不看 CMD 窗口時
- **用法**：雙擊即可

## 🎁 便利工具

### 建立桌面快捷方式
**雙擊 `Create_Desktop_Shortcut.bat`**
→ 在桌面建立「🎮 大老二遊戲」快捷方式
→ 之後直接點擊快捷方式啟動遊戲

## 🚨 常見問題

### Q: 啟動後沒反應？
- 🕐 等待 3-5 秒（初始化需要時間）
- 🔍 檢查任務管理員是否有 python.exe
- 🔄 如果有進程但無窗口，可能已啟動

### Q: 出現「Python 不存在」錯誤？
- 檢查虛擬環境：`D:\2026-python\.venv\Scripts\python.exe`
- 確認已安裝 pygame-ce：`pip install pygame-ce`
- 重新激活虛擬環境：`. .\.venv\Scripts\Activate.ps1`

### Q: 想在 PowerShell 中手動啟動？
```powershell
cd 'd:\2026-python\weeks\week-05\solutions\HW-114405011\bigtwo'
python main.py
```

---

💡 **小提示**：
- 大多數情況下，`QuickStart.bat` 就是你需要的全部！
- 如果要無視窗啟動，試試 `RunGame.vbs`
- 遊戲支援繁體中文，但請確保 UTF-8 編碼已啟用
