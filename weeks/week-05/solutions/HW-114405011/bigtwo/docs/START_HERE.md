# 🎮 大老二遊戲 - 快速啟動指南

## 最簡單的方式 👇

### ⭐ 推薦：點擊 `開始遊戲.bat`

1. 定位到遊戲資料夾：`d:\2026-python\weeks\week-05\solutions\HW-114405011\bigtwo\`
2. 找到 `開始遊戲.bat` 檔案
3. **雙擊 `開始遊戲.bat`**
4. 遊戲自動啟動！🎮

---

## 其他啟動方式

### 方式 2：建立桌面快捷方式

1. 雙擊 `launchers\Create_Desktop_Shortcut.bat`
2. 快捷方式會自動建立到你的桌面
3. 之後在桌面上直接點擊快捷方式啟動

### 方式 3：使用 launchers 目錄啟動器

1. `launchers\QuickStart.bat`：推薦的統一啟動器
2. `launchers\RunGame.vbs`：無視窗隱形啟動
3. `launchers\Create_Desktop_Shortcut.bat`：建立桌面捷徑

---

## 🔧 系統要求

✅ **已默認檢查：**
- Python 3.9+
- pygame-ce 2.5.7

批處理檔案會自動檢查環境。如果出現錯誤，會提示安裝必要組件。

---

## 📊 各啟動方式對比

| 方式 | 步驟 | 易用度 | 速度 | 需要 Python |
|------|------|--------|------|-----------|
| 開始遊戲.bat | 雙擊 | ⭐⭐⭐⭐⭐ | ⚡⚡ | ✅ 需要 |
| 桌面快捷方式 | 雙擊 | ⭐⭐⭐⭐⭐ | ⚡⚡ | ✅ 需要 |
| QuickStart.bat | 雙擊 | ⭐⭐⭐⭐⭐ | ⚡⚡ | ✅ 需要 |
| RunGame.vbs | 雙擊 | ⭐⭐⭐⭐⭐ | ⚡⚡ | ✅ 需要 |

---

## ❓ 常見問題

### Q: 為什麼雙擊 `.bat` 檔案沒有反應？
**A:** 
- 確認檔案在遊戲資料夾內
- 嘗試使用管理員身份運行
- 檢查防毒軟體是否阻擋

### Q: 出現「找不到 Python」的錯誤？
**A:** 需要安裝 Python 3.9+
- 下載：https://www.python.org/downloads/
- 安裝時勾選 "Add Python to PATH"

### Q: pygame 模組缺失？
**A:** `開始遊戲.bat` 與 `launchers\QuickStart.bat` 都會自動提示安裝。按照提示執行即可。

### Q: 隱形啟動沒有畫面？
**A:** 
- 改用 `開始遊戲.bat` 或 `launchers\QuickStart.bat`
- 確認 `main.py` 與 `ui/`、`game/` 同層存在
- 檢查虛擬環境是否正確安裝依賴

### Q: `QuickStart.bat` 找不到 Python？
**A:**
- 確認根目錄的 `.venv` 是否存在
- 若沒有，先建立虛擬環境再安裝 `pygame-ce`
- 或直接使用 `開始遊戲.bat`

---

## 📝 我優化了什麼？

✅ **代碼優化**
- 移除重複的初始化代碼
- 改進錯誤處理機制
- 添加中文編碼支持

✅ **啟動系統**
- 根目錄啟動器與 `launchers/QuickStart.bat`
- 自動環境檢查
- 桌面快捷方式生成

✅ **發佈系統**
- `RunGame.vbs` 隱形啟動
- 桌面快捷方式工具
- 文件化的啟動說明

---

## 📞 需要幫助？

遊戲啟動或執行時出現問題：

1. 檢查 `GAME_LAUNCHER_GUIDE.md`（詳細故障排除）
2. 查看錯誤信息提示
3. 確認系統環境要求

---

**現在就開始遊戲吧！** 🎲🎴

雙擊 `開始遊戲.bat` 立即開始遊戲！
