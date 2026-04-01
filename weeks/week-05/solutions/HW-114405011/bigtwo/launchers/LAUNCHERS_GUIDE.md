# 啟動器管理指南

## 📋 當前啟動器清單

本目錄包含多個啟動遊戲的腳本。為了減少維護困擾，建議只保留以下核心啟動器：

### ✅ 建議保留的啟動器

#### 1. **開始遊戲.bat** (專案根目錄)
- 位置: `{project_root}\開始遊戲.bat`
- 用途: 最簡單的啟動器，雙擊即可執行
- 特點:
  - 自動尋找虛擬環境 (.venv 或 ../.venv)
  - 支援中文顯示 (chcp 65001 + PYTHONIOENCODING)
  - 完整的錯誤檢查
  - 程式結束後自動暫停，便於查看錯誤訊息
- **推薦用於**: 日常遊戲開發與測試

#### 2. **QuickStart.bat** (launchers 目錄)
- 位置: `{project_root}\launchers\QuickStart.bat`
- 用途: 進階啟動器，支援多種環境配置
- 特點:
  - 支援從任何目錄執行
  - 完整的虛擬環境搜尋策略
  - 詳細的診斷輸出
- **推薦用於**: 自動化指令碼、CI/CD 流程

#### 3. **RunGame.vbs** (launchers 目錄)
- 位置: `{project_root}\launchers\RunGame.vbs`
- 用途: 隱形啟動遊戲（無控制台視窗）
- 特點:
  - 動態虛擬環境搜尋
  - 無控制台輸出（適合釋出版本）
  - 必須配合快捷方式使用
- **推薦用於**: 桌面快捷方式、最終使用者執行

### ❌ 建議刪除/合併的啟動器

下列文件功能重複或已過時，建議刪除：

```
launchers/
├── QUICK.bat              # 與 QuickStart.bat 重複
├── Run_Game.bat           # 功能不完整
├── Start.bat              # 與 開始遊戲.bat 重複
├── Start_Game.bat         # 與 開始遊戲.bat 重複
└── build_exe.bat          # 建構指令碼，不屬於遊戲啟動
```

## 🔧 環境檢查清單

所有保留的啟動器都應遵循以下標準：

- [ ] 使用 `%SystemRoot%\System32\chcp.com 65001` 設定編碼
- [ ] 設定 `PYTHONIOENCODING=utf-8` 環境變數
- [ ] 移除所有特殊裝飾線 (═══、╔╗╚╝等)
- [ ] 包含虛擬環境搜尋邏輯（優先級順序）
- [ ] 錯誤檢查: `if errorlevel` 或 `if %errorlevel%`
- [ ] 程式結尾包含 `pause` 以查看錯誤訊息
- [ ] 支援相對路徑，無硬編碼絕對路徑

## 📝 虛擬環境搜尋優先級

所有啟動器應按以下順序搜尋虛擬環境：

```
優先級 1: {game_root}\.venv\Scripts\python.exe
優先級 2: {game_root}\..\.venv\Scripts\python.exe  (從 launchers 目錄執行時)
優先級 3: 系統 Python (python.exe)
```

## 🚀 清理步驟

### 第一步: 備份舊啟動器
```bash
mkdir backup_launchers
move launchers\QUICK.bat backup_launchers\
move launchers\Start.bat backup_launchers\
move launchers\Start_Game.bat backup_launchers\
move launchers\Run_Game.bat backup_launchers\
```

### 第二步: 驗證核心啟動器正常工作
```bash
# 測試開始遊戲.bat
cd {project_root}
開始遊戲.bat

# 或測試 QuickStart.bat
cd launchers
QuickStart.bat
```

### 第三步: 更新文件列表
更新 `.gitignore` 以排除舊啟動器：

```gitignore
# 舊啟動器 (保留備份於 backup_launchers/)
launchers/QUICK.bat
launchers/Start.bat
launchers/Start_Game.bat
launchers/Run_Game.bat
```

## 🎯 使用場景

### 場景 1: 日常開發
```bash
# 直接執行根目錄的啟動器
開始遊戲.bat
```

### 場景 2: 自動化測試
```bash
# 從任意目錄執行
launchers\QuickStart.bat
```

### 場景 3: 建立桌面快捷方式
```bash
# 執行快捷方式建立工具
launchers\Create_Desktop_Shortcut.bat

# 或手動指向:
# 目標: {game_root}\launchers\RunGame.vbs
# 起始位置: {game_root}
```

## ✅ 品質檢查

在刪除舊啟動器前，請確保：

1. **功能測試**
   - [ ] 本機 .venv 能否成功啟動遊戲
   - [ ] 上層目錄 .venv 能否成功啟動遊戲
   - [ ] 系統 Python 能否作為備選方案啟動
   - [ ] 錯誤情況下能否顯示有用的訊息

2. **編碼測試**
   - [ ] 控制台訊息正確顯示繁體中文 (非亂碼)
   - [ ] 路徑顯示正確 (含中文資料夾名稱)

3. **相容性測試**
   - [ ] Windows 10 / 11
   - [ ] 不同的 Python 版本 (3.8+)
   - [ ] 虛擬環境配置

## 📞 故障排除

| 症狀 | 原因 | 解決方案 |
|------|------|---------|
| 出現亂碼 | 編碼設定不正確 | 確保啟動器開頭有 `chcp 65001` 和 `PYTHONIOENCODING=utf-8` |
| 找不到 Python | 虛擬環境不存在 | 執行 `python -m venv .venv` |
| 遊戲閃退 | 缺少依賴套件 | 執行 `pip install -r requirements.txt` |
| 關閉後看不到錯誤 | 缺少 pause | 在啟動器末尾加上 `pause` |

---

**最後更新**: 2026-03-29  
**維護者**: Copilot Agent  
**版本**: 2.0 (已標準化)
