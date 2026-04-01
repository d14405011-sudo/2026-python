# 🎮 遊戲啟動說明

## ⭐ 最簡單的方式（推薦）

### 在 Windows 中啟動

**只需 1 步：雙擊 `Start.bat`**

1. 打開專案根目錄（main.py 所在位置）
2. 雙擊 `Start.bat`
3. 遊戲即刻啟動！ ✅

不需要指定路徑，程式會自動尋找 Python 環境。

---

## 📋 可用啟動器

| 檔案 | 位置 | 用途 | 推薦度 |
|------|------|------|--------|
| **Start.bat** | 專案根目錄 | 快速啟動遊戲 | ⭐⭐⭐ 推薦 |
| `Create_Desktop_Shortcut.bat` | launchers | 建立桌面快捷方式 | ⭐⭐ |
| `QuickStart.bat` | launchers | 統一啟動器 | ⭐⭐ |
| `RunGame.vbs` | launchers | 隱形啟動 | ⭐ 備用 |
| `Run_Game.bat` | launchers | 標準啟動 | ⭐ 備用 |

---

## 💡 其他啟動方式

### 在 PowerShell 中啟動
```powershell
cd <遊戲根目錄>
python main.py
```

### 建立桌面快捷方式
1. 雙擊 `launchers/Create_Desktop_Shortcut.bat`
2. 在桌面上會出現「🎮 大老二遊戲」快捷方式
3. 之後直接點擊快捷方式即可啟動

---

## 🚨 常見問題

### Q: 雙擊 Start.bat 後沒反應？
**A:**  
1. 等待 3-5 秒（首次啟動較慢）
2. 檢查是否已安裝 pygame-ce：
   ```
   pip install -r requirements.txt
   ```
3. 檢查任務管理員是否有 python.exe 進程

### Q: 出現「Python 不存在」錯誤？
**A:**  
1. 確認虛擬環境存在（`.venv` 目錄）
2. 執行：`pip install pygame-ce>=2.5.0`
3. 或使用 PowerShell 手動執行：`python main.py`

### Q: 想看 CMD 窗口和日誌輸出？
**A:**  
1. 進入 `launchers/` 目錄
2. 雙擊 `QuickStart.bat` 或 `Run_Game.bat`

---

## ✅ 驗證遊戲已正確安裝

遊戲無法啟動時，逐項檢查：

- [ ] `Run_Game.bat` 檔案存在
- [ ] `main.py` 存在（bigtwo 根目錄）
- [ ] `D:\2026-python\.venv\Scripts\python.exe` 存在
- [ ] Windows 沒有防火牆/殺毒軟體擋住
- [ ] Python 版本 3.9 以上
- [ ] pygame-ce 已安裝

## 🚨 常見問題

### Q: 雙擊後沒反應
**A:** 
1. 等待 3-5 秒（遊戲初始化需要時間）
2. 檢查任務管理員的背景程序（python.exe）
3. 如果還是沒有，試試方式 2（桌面快捷方式）

### Q: 出現「找不到...」錯誤
**A:** 
1. 確認路徑沒有被移動
2. 試試重新執行 `Run_Game.bat`
3. 或直接執行 `python main.py`（見下方）

### Q: 想要有 CMD 窗口看日誌
**A:** 
1. 編輯 `Run_Game.bat`
2. 找到這行：`start "" /b "%PYTHON_PATH%" main.py >nul 2>&1`
3. 改成：`"%PYTHON_PATH%" main.py`
4. 保存後重新執行

## 💻 手動啟動方式

如果批檔不工作，可以手動執行：

### 方式 1：在 PowerShell 中
```powershell
cd 'd:\2026-python\weeks\week-05\solutions\11\bigtwo'
& 'D:\2026-python\.venv\Scripts\python.exe' main.py
```

### 方式 2：在 Command Prompt 中
```cmd
cd d:\2026-python\weeks\week-05\solutions\11\bigtwo
D:\2026-python\.venv\Scripts\python.exe main.py
```

### 方式 3：在 VS Code 終端中
```bash
cd weeks/week-05/solutions/11/bigtwo
python main.py
```

## 📞 技術細節

### 環境配置
- **Python 路徑**：`D:\2026-python\.venv\Scripts\python.exe`
- **遊戲目錄**：`d:\2026-python\weeks\week-05\solutions\11\bigtwo`
- **字元編碼**：UTF-8（支持中文）
- **啟動方式**：靜默啟動（隱藏 CMD 窗口）

### 依賴檢查
遊戲需要以下模組：
- pygame-ce （已在 venv 中安裝）
- 標準庫（sys, os, random, math 等）

## 🎯 預期行為

執行 `Run_Game.bat` 後：
1. ✅ 命令行窗口短暫出現（自動關閉）
2. ✅ 遊戲窗口出現（Pygame 視窗）
3. ✅ 遊戲開始（進入菜單或遊戲界面）

## 🔄 下次啟動

第一次設定好後，**以後只需**：
- 雙擊 `Run_Game.bat`
- **或**雙擊桌面快捷方式

無需再做其他設定！

---

**相關檔案**：
- 📁 launchers/ - 啟動器目錄
- 📄 Run_Game.bat - 主啟動器
- 🐍 main.py - 遊戲進入點

**需要幫助？** 檢查上方「常見問題」或查看 docs/ 中的詳細文檔
