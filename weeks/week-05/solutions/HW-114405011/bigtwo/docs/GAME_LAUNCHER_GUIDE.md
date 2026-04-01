# 遊戲啟動指南

## 🎮 快速開始

### 方法 1：使用批處理檔案（推薦 - 最簡單）

直接雙擊以下任一檔案即可啟動遊戲：

#### **`Run_Game.bat`** ⭐
- **用途**：一鍵啟動遊戲
- **要求**：需要 Python 3.9+
- **優點**：無需任何配置，最簡單快速

**使用步驟：**
1. 定位到遊戲目錄：`weeks/week-05/solutions/11/bigtwo/`
2. 雙擊 `Run_Game.bat`
3. 遊戲自動啟動

#### **`Start_Game.bat`**
- **用途**：使用虛擬環境啟動
- **要求**：需要虛擬環境 `.venv`
- **優點**：確保使用正確的 Python 環境

---

### 方法 2：使用 Python 指令（需要終端）

```bash
# 方法 A：直接運行
python main.py

# 方法 B：使用虛擬環境
d:/2026-python/.venv/Scripts/python.exe main.py
```

---

### 方法 3：生成獨立 EXE 檔案（最專業）

生成 `.exe` 檔案後，用戶無需安裝 Python 就能執行。

**第一次使用时的設置步驟：**

1. **準備環境**
   ```bash
   # 安裝 PyInstaller（只需一次）
   pip install pyinstaller
   ```

2. **生成 EXE**
   雙擊 `build_exe.bat`
   
   或使用命令行：
   ```bash
   pyinstaller build_executable.spec
   ```

3. **運行 EXE**
   - 生成的 EXE 位於 `dist/Big_Two.exe`
   - 雙擊即可運行（完全獨立，不需要 Python）

**優點：**
- 無需安裝 Python
- 可分發給其他用戶
- 啟動速度快

---

## 🔧 環境要求

### 最小要求
- **Python**: 3.9 或更新版本
- **pygame-ce**: 2.5.7

### 安裝依賴
```bash
# 自動安裝（Run_Game.bat 會自動檢查）
pip install pygame-ce

# 或手動安裝
pip install pygame-ce==2.5.7
```

---

## ⚡ 性能優化

遊戲已進行以下優化：

### 代碼級別
- ✅ 移除重複的初始化代碼
- ✅ 改進了錯誤處理
- ✅ 優化了模組導入
- ✅ 支持 UTF-8 編碼（避免亂碼）

### UI 級別  
- ✅ 動態光暈效果（6 層）
- ✅ 高效的卡牌渲染
- ✅ 主題切換優化
- ✅ 記憶體使用優化

### 遊戲邏輯
- ✅ AI 多難度支持（無性能損失）
- ✅ 計分系統優化
- ✅ 路線搜索優化

---

## 📋 檔案結構

```
bigtwo/
├── main.py                     主程式（優化版）
├── Run_Game.bat               快速啟動（推薦）
├── Start_Game.bat             虛擬環境啟動
├── build_exe.bat              EXE 生成器
├── build_executable.spec      PyInstaller 配置
├── ui/
│   ├── app.py
│   ├── render.py
│   ├── input.py
│   └── themes.py
├── game/
│   ├── game.py
│   ├── ai.py
│   ├── models.py
│   ├── classifier.py
│   └── finder.py
└── tests/
    └── ...
```

---

## 🚀 推薦使用流程

### 首次運行
1. 確保 Python 3.9+ 已安裝
2. 定位到遊戲目錄
3. **雙擊 `Run_Game.bat`**

### 日常使用
- **方法 1**：繼續使用 `Run_Game.bat`（最簡單）
- **方法 2**：生成 `Big_Two.exe`（無需 Python）

### 分發給他人
1. 執行 `build_exe.bat` 生成 EXE
2. 將 `dist/Big_Two.exe` 分發
3. 接收者無需任何配置，直接雙擊運行

---

## 🐛 故障排除

### 問題：執行 .bat 檔案時出現「命令找不到」

**解決方案：**
```bash
# 確認 Python 已添加到 PATH
python --version

# 如果找不到，重新安裝 Python（勾選「Add Python to PATH」）
```

### 問題：缺少 pygame 模組

**解決方案：**
```bash
# 安裝 pygame-ce
pip install pygame-ce

# 使用虛擬環境時
d:/2026-python/.venv/Scripts/pip install pygame-ce
```

### 問題：EXE 無法啟動或速度很慢

**解決方案：**
1. 確保系統有足夠磁碟空間（EXE 大約 100-150MB）
2. 重新執行 `build_exe.bat` 重新生成
3. 檢查防毒軟體是否阻擋

### 問題：遊戲啟動時顯示亂碼

**解決方案：**
```bash
# Run_Game.bat 會自動設置 UTF-8 編碼
# 如果仍有問題，手動設置：
set PYTHONIOENCODING=utf-8
python main.py
```

---

## 📊 啟動方式對比

| 方式 | 速度 | 易用性 | Python 依賴 | 體積 |
|------|------|--------|-----------|------|
| Run_Game.bat | ⚡⚡ | ⭐⭐⭐⭐⭐ | 需要 | 小 |
| Start_Game.bat | ⚡⚡ | ⭐⭐⭐ | 需要 | 小 |
| Python 指令 | ⚡ | ⭐⭐ | 需要 | 小 |
| Big_Two.exe | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 不需要 | 大 (~120MB) |

---

## 📝 技術細節

### main.py 優化
- 增強的錯誤處理
- UTF-8 編碼支持（Windows）
- 優雅的退出機制

### 批處理檔案特性
- 自動檢測環境
- 錯誤提示
- 編碼設置
- 自動路徑調整

### PyInstaller 配置
- 優化的構建設定
- 隱藏導入支持
- 打包資料檔案
- 無主控台視窗（exe 模式）

---

## 💡 進階用法

### 自訂主題啟動
編輯 `main.py`，在 `BigTwoApp()` 初始化前添加：
```python
# 設定預設主題
default_theme = 'winter'  # 或 'summer', 'neon', 'default'
```

### 命令行參數（未來支持）
```bash
# 預留用於未來擴展
python main.py --theme winter
python main.py --fullscreen
```

---

**最後更新：2025 年 3 月**
**狀態：✅ 所有啟動方式正常運行**
