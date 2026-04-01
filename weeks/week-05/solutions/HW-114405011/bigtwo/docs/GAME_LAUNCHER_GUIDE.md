# 遊戲啟動指南

## 🎮 快速開始

### 方法 1：使用批處理檔案（推薦 - 最簡單）

直接雙擊以下任一檔案即可啟動遊戲：

#### **`開始遊戲.bat`** ⭐
- **用途**：專案根目錄的一鍵啟動器
- **要求**：需要 Python 3.9+
- **優點**：最容易找到、最適合日常使用

**使用步驟：**
1. 定位到遊戲目錄：`weeks/week-05/solutions/HW-114405011/bigtwo/`
2. 雙擊 `開始遊戲.bat`
3. 遊戲自動啟動

### 方法 2：使用 `launchers/QuickStart.bat`

- **用途**：從 `launchers/` 目錄啟動遊戲
- **要求**：需要 Python 3.9+ 或 `.venv`
- **優點**：會自動搜尋本機或上層虛擬環境

### 方法 3：使用 `launchers/RunGame.vbs`

- **用途**：無視窗隱形啟動
- **要求**：同樣需要 Python 或虛擬環境
- **優點**：適合做桌面捷徑

---

### 方法 4：使用 Python 指令（需要終端）

```bash
# 方法 A：直接運行
python main.py

# 方法 B：使用虛擬環境
d:/2026-python/.venv/Scripts/python.exe main.py
```

---

## 🔧 環境要求

### 最小要求
- **Python**: 3.9 或更新版本
- **pygame-ce**: 2.5.7

### 安裝依賴
```bash
# 自動安裝（開始遊戲.bat 與 QuickStart.bat 都會自動檢查）
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
- ✅ 動態光暈效果
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
├── 開始遊戲.bat               根目錄快速啟動
├── launchers/
│   ├── QuickStart.bat         快速啟動（推薦）
│   ├── RunGame.vbs            隱形啟動
│   └── Create_Desktop_Shortcut.bat  桌面快捷方式
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
3. **雙擊 `開始遊戲.bat`**

### 日常使用
- **方法 1**：繼續使用 `開始遊戲.bat`（最簡單）
- **方法 2**：使用 `launchers\QuickStart.bat`
- **方法 3**：建立桌面快捷方式後從桌面啟動

### 分發給他人
1. 執行 `launchers\Create_Desktop_Shortcut.bat` 建立快捷方式
2. 或直接分發整個專案資料夾
3. 接收者可直接雙擊 `開始遊戲.bat` 或桌面捷徑

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

### 問題：QuickStart.bat 找不到 Python

**解決方案：**
1. 檢查 `.venv` 是否存在於專案根目錄
2. 若沒有，先建立虛擬環境並安裝 `pygame-ce`
3. 或直接使用 `開始遊戲.bat`

### 問題：遊戲啟動時顯示亂碼

**解決方案：**
```bash
# `開始遊戲.bat` 與 `launchers\QuickStart.bat` 會自動設置 UTF-8 編碼
# 如果仍有問題，手動設置：
set PYTHONIOENCODING=utf-8
python main.py
```

---

## 📊 啟動方式對比

| 方式 | 速度 | 易用性 | Python 依賴 | 體積 |
|------|------|--------|-----------|------|
| 開始遊戲.bat | ⚡⚡ | ⭐⭐⭐⭐⭐ | 需要 | 小 |
| QuickStart.bat | ⚡⚡ | ⭐⭐⭐⭐ | 需要 | 小 |
| RunGame.vbs | ⚡⚡ | ⭐⭐⭐⭐ | 需要 | 小 |
| Python 指令 | ⚡ | ⭐⭐ | 需要 | 小 |

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
