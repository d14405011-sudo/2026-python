# 🔧 遊戲啟動故障排除指南

## ❓ 遊戲無法啟動？

### 狀況 1：雙擊 Run_Game.bat 後沒反應

**症狀**：
- 命令行窗口閃過或什麼都沒有
- 遊戲窗口沒有出現
- 沒有任何錯誤信息

**解決步驟**：

#### 步驟 1：等待（可能在初始化）
- 等待 **3-5 秒**（首次啟動較慢）
- 檢查任務管理員是否有 `python.exe` 進程
  - 按 `Ctrl + Shift + Esc` 打開任務管理員
  - 搜尋「python」
  - 如果有，表示遊戲在運行中

#### 步驟 2：試試備用啟動器
1. 雙擊 `Start_Game.bat`（使用 venv）
2. 等待遊戲啟動

#### 步驟 3：手動執行
1. 打開 PowerShell（Windows）
2. 執行以下命令：
   ```powershell
   cd 'd:\2026-python\weeks\week-05\solutions\11\bigtwo'
   & 'D:\2026-python\.venv\Scripts\python.exe' main.py
   ```
3. 查看是否有錯誤信息
4. 告訴我錯誤信息內容

---

### 狀況 2：出現「找不到...」錯誤

**症狀**：
```
can't open file 'D:\\2026-python\\main.py': [Errno 2] No such file or directory
```

**原因**：工作目錄或路徑配置有誤

**解決**：
1. 驗證 `main.py` 是否存在
   - 應該在：`d:\2026-python\weeks\week-05\solutions\11\bigtwo\main.py`
2. 驗證 Python 執行檔路徑
   - 應該在：`D:\2026-python\.venv\Scripts\python.exe`
3. 如果路徑不同，編輯 `Run_Game.bat`
   - 更新 `set PYTHON_PATH=...` 行
   - 更新 `set GAME_DIR=...` 行

---

### 狀況 3：出現「找不到 Python」

**症狀**：
```
'python' 不是內部或外部命令...
```

**原因**：Python 沒有安裝或路徑不正確

**解決**：
1. 檢查 Python 是否已安裝
   ```powershell
   & 'D:\2026-python\.venv\Scripts\python.exe' --version
   ```
   應該顯示 `Python 3.x.x`

2. 如果顯示錯誤，需要重新安裝 venv
   ```powershell
   cd d:\2026-python
   python -m venv .venv
   .\.venv\Scripts\pip install pygame-ce
   ```

---

### 狀況 4：出現「ImportError: No module named 'pygame'」

**症狀**：
```
ImportError: No module named 'pygame'
ModuleNotFoundError: No module named 'pygame_ce'
```

**原因**：pygame-ce 沒有安裝

**解決**：
```powershell
cd d:\2026-python
.\.venv\Scripts\pip install pygame-ce
```

然後重新雙擊 `Run_Game.bat`

---

### 狀況 5：出現「ModuleNotFoundError: No module named 'ui'」

**症狀**：
```
ModuleNotFoundError: No module named 'ui'
```

**原因**：工作目錄不在遊戲根目錄

**解決**：
1. 確保 `main.py` 和 `ui/` 目錄在同一位置
2. 改到遊戲目錄執行：
   ```powershell
   cd 'd:\2026-python\weeks\week-05\solutions\11\bigtwo'
   python main.py
   ```

---

### 狀況 6：黑屏或無回應

**症狀**：
- 遊戲窗口出現但黑屏
- 點擊無反應

**原因**：
- GPU 驅動問題
- Pygame 初始化失敗

**解決**：
1. 嘗試在 `main.py` 同級目錄建立文件 `debug.txt`：
   ```python
   # 在 main.py 開始加入
   print("Game starting...", flush=True)
   import pygame
   print("Pygame imported...", flush=True)
   ```

2. 更新 GPU 驅動
3. 嘗試在不同的終端運行

---

## ✅ 診斷清單

如果還是無法啟動，逐項檢查：

- [ ] `main.py` 存在
  ```powershell
  Test-Path 'd:\2026-python\weeks\week-05\solutions\11\bigtwo\main.py'
  ```

- [ ] `ui/app.py` 存在
  ```powershell
  Test-Path 'd:\2026-python\weeks\week-05\solutions\11\bigtwo\ui\app.py'
  ```

- [ ] Python 可執行
  ```powershell
  & 'D:\2026-python\.venv\Scripts\python.exe' --version
  ```

- [ ] pygame 已安裝
  ```powershell
  & 'D:\2026-python\.venv\Scripts\python.exe' -c "import pygame; print('OK')"
  ```

- [ ] 可以手動啟動
  ```powershell
  cd 'd:\2026-python\weeks\week-05\solutions\11\bigtwo'
  & 'D:\2026-python\.venv\Scripts\python.exe' main.py
  ```

---

## 📞 需要進一步幫助？

如果上述方法都無法解決，請提供：

1. **錯誤信息的完整內容**（複製貼上）
2. **執行命令**：
   ```powershell
   & 'D:\2026-python\.venv\Scripts\python.exe' --version
   Get-Item 'd:\2026-python\weeks\week-05\solutions\11\bigtwo\main.py'
   Get-Item 'D:\2026-python\.venv\Scripts\python.exe'
   ```
3. **系統信息**：
   - Windows 版本
   - Python 版本

---

## 🎯 快速測試

如果想確認環境設定正確，可以執行此測試指令：

```powershell
# 進入遊戲目錄
cd 'd:\2026-python\weeks\week-05\solutions\11\bigtwo'

# 檢查關鍵檔案
Write-Host "檔案檢查："
Test-Path 'main.py' | Write-Host "  main.py: $_"
Test-Path 'ui/app.py' | Write-Host "  ui/app.py: $_"
Test-Path 'game/game.py' | Write-Host "  game/game.py: $_"

# 檢查 Python 環境
Write-Host "`nPython 檢查："
& 'D:\2026-python\.venv\Scripts\python.exe' --version

# 檢查 pygame
Write-Host "`npygame 檢查："
& 'D:\2026-python\.venv\Scripts\python.exe' -c "import pygame; print(f'pygame-ce version: {pygame.version.ver}')"

# 簡單運行測試
Write-Host "`n啟動測試："
& 'D:\2026-python\.venv\Scripts\python.exe' main.py
```

如果以上都顯示 OK，表示環境設定正確，遊戲應該可以啟動！

---

**最後一招**：直接執行 `Start_Game.bat` 和 `Run_Game.bat` 都試過，都無法工作，那麼：

1. 在文件管理器打開遊戲目錄
2. 右鍵→新增→文字檔案
3. 複製以下內容：
   ```batch
   @echo off
   cd /d d:\2026-python\weeks\week-05\solutions\11\bigtwo
   D:\2026-python\.venv\Scripts\python.exe main.py
   pause
   ```
4. 保存為 `DirectRun.bat`
5. 雙擊執行
6. 如果還是不行，截圖錯誤信息給我
