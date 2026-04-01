# 大老二遊戲

這是一個基於 Pygame 實作的單人大老二卡牌遊戲（你對戰 3 個 AI）。  
採用 **TDD（測試驅動開發）** 方法論，擁有 50 個單元測試與完整的代碼文件。

## 系統需求
- Python 3.9+
- pygame-ce（社區版本）或 pygame
- 虛擬環境（推薦 venv）

## 安裝與執行

### 快速启動（使用批處理文件）
```powershell
# Windows PowerShell
cd D:\2026-python\weeks\week-05\solutions\11\bigtwo
.\開始遊戲.bat          # 主啟動器
# 或
.\launchers\QuickStart.bat  # 備用啟動器
```

### 手動启動
```bash
# 1. 激活虛擬環境
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 運行遊戲
python main.py
```

## 項目結構
```
bigtwo/
├── main.py                 # 遊戲主程式入口
├── requirements.txt        # 依賴清單
├── README.md              # 本檔案
├── TEST_CASES.md          # 測試用例說明
├── TEST_LOG.md            # 測試執行紀錄
├── AI_USAGE.md            # AI 協作說明
│
├── game/                   # 核心遊戲邏輯
│   ├── models.py          # Card、Deck、Hand、Player 資料模型
│   ├── classifier.py      # 牌型分類與大小比較
│   ├── finder.py          # 合法出牌搜尋器
│   ├── ai.py              # AI 決策引擎
│   └── game.py            # 遊戲流程控制
│
├── ui/                     # 圖形用戶界面
│   ├── app.py             # 主應用/遊戲循環
│   ├── render.py          # 牌卡與場景渲染
│   ├── input.py           # 鼠標/鍵盤輸入
│   ├── effects.py         # 視覺效果（背景、粒子、光暈）
│   └── sound.py           # 音效管理框架
│
├── tests/                  # 自動化測試套件
│   ├── test_models.py     # 模型層測試（6 個測試）
│   ├── test_classifier.py # 牌型分類測試（19 個測試）
│   ├── test_finder.py     # 搜尋器測試（5 個測試）
│   ├── test_game.py       # 遊戲流程測試（12 個測試）
│   ├── test_ai.py         # AI 策略測試（5 個測試）
│   └── test_ui.py         # UI 渲染測試（3 個測試）
│
├── launchers/             # 遊戲啟動腳本
│   ├── QuickStart.bat     # 統一啟動器
│   ├── Create_Desktop_Shortcut.bat  # 桌面快捷方式
│   ├── RunGame.vbs        # 無控制台啟動
│   ├── README.md          # 啟動器使用說明
│   └── LAUNCHERS_GUIDE.md # 啟動器管理指南
│
└── assets/                # 資源文件
    └── sounds/            # （待完善）音效資源
        ├── play_card.wav
        ├── pass_turn.wav
        ├── win_game.wav
        └── ...
```

## 遊戲規則

### 牌的大小順序
1. **花色強弱**（從小到大）：♣ 梅花 < ♦ 方塊 < ♥ 紅心 < ♠ 黑桃
2. **點數強弱**（從小到大）：3 < 4 < 5 < 6 < 7 < 8 < 9 < 10 < J < Q < K < A < 2

### 牌型（由弱到強）
| 牌型 | 張數 | 說明 | 例子 |
|------|------|------|------|
| 單張 | 1 | 任意單張牌 | ♠3 |
| 對子 | 2 | 點數相同的 2 張牌 | ♥5, ♣5 |
| 順子 | 5 | 5 張連續點數的牌 | ♣3, ♦4, ♥5, ♠6, ♣7 |
| 葫蘆 | 5 | 3 張同點 + 2 張同點 | ♦5, ♥5, ♠5, ♣10, ♦10 |
| 鐵支 | 5 | 4 張同點 + 1 張任意 | ♣K, ♦K, ♥K, ♠K, ♣3 |
| 同花順 | 5 | 5 張同花色且連續的牌 | ♠5, ♠6, ♠7, ♠8, ♠9 |
| 一條龍 | 13 | 13 種點數各一張，可直接全出 | ♣3, ♦4, ..., ♠2 |

### 遊戲流程
1. **發牌**：每位玩家獲得 13 張牌
2. **起手牌**：持有 ♣3（梅花 3）的玩家首先出牌
3. **輪流出牌**：
   - 若桌上無牌，可以出任何牌或牌組（單張、對子、三條、五張組合）
   - 若桌上有牌，必須出與桌牌相同張數的牌，且點數或牌型更強才能壓過
   - 無法壓過或不想出牌時，可以「過牌（Pass）」

### 計分系統
```
扣分 = 剩餘牌數 × 基礎倍數 × 老二倍數
老二倍數 = 2^(手中老二張數)
```

**例子**：
- 9 張無老二：9 × 2 × 1 = 18 分
- 5 張 4 個老二：5 × 1 × 16 = 80 分

### 操作方式
- **選牌**：使用滑鼠左鍵點擊手牌。被選中的牌會向上浮起。若要取消，再次點擊即可。
- **出牌**：直接按「Enter 鍵」，或是點擊下方的 `出牌 (Enter)` 按鈕。
- **過牌**：直接按「P 鍵」，或是點擊下方的 `過牌 (P)` 按鈕。
  *(只有當前桌上有其他人出的牌時才可以 Pass。)*

### 休閒模式（Casual）
- **AI 難度**：可選擇低、中、高難度
- **計分**：無計分（輕鬆對戰）
- **計時**：無逾時計時
- **適合**：練習遊戲、放鬆遊玩

### 挑戰賽模式（Ranked）
- **AI 難度**：固定困難模式（最強 AI）
- **計分**：啟用賽制計分系統
- **計時**：啟用逾時計時（15 秒）
- **適合**：競爭性遊戲、技能挑戰

### AI 難度參數
| 難度 | 隨機性 | 描述 |
|------|--------|------|
| 低 | 0.2 | AI 經常做出不理想決策 |
| 中 | 0.5 | AI 策略與隨機性平衡 |
| 高 | 0.8 | AI 主要使用最優策略（預設休閒模式） |
| 困難 | 1.0 | AI 完全按最優策略出牌（挑戰賽固定） |

## 視覺設計

### 主題系統
遊戲支持多種視覺主題，根據遊戲模式自動切換：

| 主題 | 特點 | 應用場景 |
|------|------|----------|
| 🌙 冬季夜晚 | 深藍夜空 + 暖金光斑 | 挑戰賽模式（競技感） |
| ☀️ 夏日明朗 | 清爽明亮 + 淺藍色調 | 休閒模式（友善感） |
| 🌈 霓光未來 | 賽博朋克風格 | 可選主題 |
| 💎 經典深藍 | 原始配色 | 預設主題 |

## 測試與品質保證

### 自動化測試
```bash
# 執行全部 50 個測試
python -m unittest discover -s tests -v

# 執行特定模塊
python -m unittest tests.test_models -v      # 模型層
python -m unittest tests.test_classifier -v  # 牌型分類
python -m unittest tests.test_ai -v          # AI 策略
```

### 測試覆蓋
- ✅ **50 個單元測試**，全部通過
- ✅ **6 個測試模塊**：models、classifier、finder、game、ai、ui
- ✅ **執行時間**：~17 秒
- ✅ **覆蓋範圍**：遊戲邏輯、AI 決策、牌型判定、UI 渲染

### 驗證腳本
```bash
# 驗證發牌隨機性
python test_randomness.py

# 驗證洗牌隨機性
python test_shuffle.py

# 驗證項目清理
python Clean_Project.bat
```

參見 [TEST_CASES.md](TEST_CASES.md) 與 [TEST_LOG.md](TEST_LOG.md) 獲取詳細說明。

## 故障排除

### 啟動問題

**問題**：遊戲無法啟動
```bash
[ERROR] 缺少 pygame 模組
```
**解決**：
```bash
pip install pygame-ce
# 或指定版本
pip install "pygame-ce>=2.0"
```

**問題**：批處理文件運行報錯
```
ModuleNotFoundError: No module named 'game'
```
**解決**：
```bash
# 確保在遊戲目錄下執行
cd weeks/week-05/solutions/11/bigtwo
.\開始遊戲.bat
```

### 編碼問題（Windows 中文）

**問題**：Windows PowerShell 顯示亂碼
```
大老二遊戲啟動器 → [garbled Chinese characters]
```
**解決**：
1. 批處理文件內置 `chcp 65001` 和 `PYTHONIOENCODING=utf-8`
2. 若仍有問題，在 PowerShell 中執行：
```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$env:PYTHONIOENCODING='utf-8'
```

### 性能問題

**問題**：遊戲畫面卡頓

**檢查清單**：
- 運行 `Clean_Project.bat` 清理快取
- 關閉其他應用釋放 GPU 資源
- 檢查顯示卡驅動是否最新
- 降低 AI 難度減少計算量

## 最近修正（2026-03-29）

### 修正內容
1. **啟動器標準化**
   - 修正 `開始遊戲.bat` 編碼問題（UTF-8 + chcp 65001）
   - 刪除 5 個冗餘啟動文件
   - 建立 LAUNCHERS_GUIDE.md

2. **發牌隨機性驗證**
   - 創建 test_randomness.py - 驗證分配隨機性
   - 創建 test_shuffle.py - 驗證位置隨機性
   - 確認系統正常運作（20 局測試）

3. **文件補齊**
   - 擴展 README.md 添加完整項目結構
   - 補充 AI_USAGE.md 協作過程
   - 更新 TEST_LOG.md 驗證紀錄

### 已驗證項目
- ✅ 發牌隨機性良好
- ✅ 洗牌功能正常
- ✅ 啟動流程標準化
- ✅ 所有文件齊全
- ✅ 編碼問題解決

請參見 [AI_USAGE.md](AI_USAGE.md) 與 [TEST_LOG.md](TEST_LOG.md) 了解詳細修正過程。

### 視覺增強特性
- **動態光斑**：6層漸進式光暈效果，模擬柔和照明
- **卡牌設計**：
  - 多層陰影增加立體感
  - 增強邊框和選中效果
  - 精心設計的卡牌背面圖案
- **按鈕美化**：漸層效果 + 陰影 + 懸停動畫
- **邊界高亮**：增加遊戲畫面的視覺深度

### ✨ 新增視覺增強系統 （v2.0）

#### 新增主題（共 8 個）
除了原有 4 個主題，新增 4 個帥氣主題：
- 🌙 `dark_purple` - **黑紫帝王** ⭐ 最高級
- 💻 `tech_green` - **科技綠幕** ⭐ 最酷（駭客風）
- 👑 `royal_gold` - **皇金璀璨** ⭐ 最華麗
- 🔥 `sunset` - **夕陽火燒** ⭐ 最溫暖

#### 視覺效果系統

| 效果類型 | 說明 | 觸發時機 |
|---------|------|---------|
| **粒子爆炸** | 發牌時 8 粒子四散，勝利時 20 彩色粒子上升 | 出牌/勝利 |
| **卡牌動畫** | 翻轉（3D）、彈跳、發光脈動 | 出牌/選牌 |
| **邊框光效** | 立體邊框、按鈕發光、光澤效果 | UI 渲染 |
| **背景流動** | 15 個浮動粒子創造動感背景 | 持續 |
| **光暈脈動** | 3 層漸層光暈，模擬真實光源 | 特殊事件 |

#### 相關文檔
- 📖 [`VISUAL_ENHANCEMENT.md`](VISUAL_ENHANCEMENT.md) - 詳細整合指南
- ⚡ [`VISUAL_ENHANCEMENT_QUICK_REFERENCE.md`](VISUAL_ENHANCEMENT_QUICK_REFERENCE.md) - 快速參考卡
- 💻 [`UI_INTEGRATION_EXAMPLE.md`](UI_INTEGRATION_EXAMPLE.md) - 整合代碼範例
- 🎬 [`ui/visual_demo.py`](ui/visual_demo.py) - 互動演示程式

#### 快速預覽
```bash
# 執行演示程式看所有效果
python ui/visual_demo.py

按鍵說明：
  1-8: 切換主題
  SPACE: 發牌特效
  V: 勝利爆炸
  R: 重置
  Q: 退出
```

#### 核心模組
- `ui/effects.py` - 視覺效果引擎（新增）
  - `ParticleEffect` - 粒子系統
  - `CardAnimation` - 動畫系統
  - `BorderDecorator` - 邊框裝飾
  - `BackgroundEffect` - 背景特效
  - `GlowEffect` - 光暈脈動

## 快速開始

### 🚀 最簡單的方式
直接雙擊 **`launchers/Run_Game.bat`** 即可啟動遊戲！

### 📖 新手導引
不確定如何開始？閱讀 **`docs/START_HERE.md`** 獲得逐步指引。

### 🎮 遊戲啟動方式

| 方式 | 檔案 | 說明 |
|------|------|------|
| 🖥️ 簡易啟動 | `launchers/Run_Game.bat` | **推薦** - 自動偵測環境 |
| 🐍 直接執行 | `python main.py` | 需要先安裝依賴 |
| 📌 桌面快捷 | `launchers/Create_Desktop_Shortcut.bat` | 在桌面建立快捷方式 |
| 🔨 獨立 EXE | `launchers/build_exe.bat` | 編譯為可執行檔 |

## 📁 完整目錄結構

```
bigtwo/
├── 【核心檔案】
├── main.py                          # 遊戲進入點
├── README.md                        # ✅ 本檔案（英文說明）
├── AI_USAGE.md                      # AI 策略文檔
├── TEST_CASES.md                    # 測試用例說明
├── TEST_LOG.md                      # 測試執行記錄
│
├── 【遊戲邏輯】
├── game/                            # 大老二核心邏輯
│   ├── __init__.py
│   ├── models.py                    # 牌牌、牌組、玩家模型
│   ├── classifier.py                # 牌型分類和比較邏輯
│   ├── ai.py                        # AI 策略引擎
│   ├── finder.py                    # 牌型搜尋器（找出合法出牌）
│   └── game.py                      # 遊戲流程控制
│
├── 【使用者介面】
├── ui/                              # Pygame 圖形介面
│   ├── __init__.py
│   ├── app.py                       # 遊戲應用主類
│   ├── render.py                    # 圖形渲染引擎（含主題支持）
│   ├── input.py                     # 輸入事件處理
│   ├── themes.py                    # 視覺主題配置系統（已擴展 8 主題）
│   ├── effects.py                   # ✨ 視覺效果引擎（新增）
│   └── visual_demo.py               # 🎬 視覺效果演示程式（新增）
│
├── 【遊戲資源】
├── assets/                          # 遊戲資源 
│   └── （圖片、字體等）
│
├── 【測試】
├── tests/                           # 單元測試
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_classifier.py
│   ├── test_ai.py
│   └── ... (共 49 個測試，全部通過)
│
├── 【📚 文檔】
├── docs/                            # 文檔和指南
│   ├── README.md                    # 文檔索引
│   ├── START_HERE.md                # 新手快速開始
│   ├── README_CN.md                 # 完整中文文檔
│   ├── GAME_LAUNCHER_GUIDE.md       # 啟動器使用說明
│   ├── LAUNCHER_COMPLETION_REPORT.md
│   ├── VISUAL_ENHANCEMENT_PLAN.md
│   ├── VISUAL_IMPROVEMENT_REPORT.md
│   ├── COMPLETION_SUMMARY.md
│   ├── FINAL_VERIFICATION.md
│   └── QUICK_START.txt
│
├── 【✨ 視覺增強文檔】
├── VISUAL_ENHANCEMENT_SUMMARY.md         # 📋 增強總結（新增）
├── VISUAL_ENHANCEMENT.md                 # 📖 詳細指南（新增）
├── VISUAL_ENHANCEMENT_QUICK_REFERENCE.md # ⚡ 快速參考卡（新增）
├── UI_INTEGRATION_EXAMPLE.md             # 💻 代碼範例（新增）
│
├── 【🚀 啟動器】
├── launchers/                       # 遊戲啟動器
│   ├── README.md                    # 啟動器說明
│   ├── Run_Game.bat                 # ⭐ 主要啟動器（推薦）
│   ├── Start_Game.bat               # venv 啟動器
│   ├── Create_Desktop_Shortcut.bat  # 快捷方式生成器
│   └── build_exe.bat                # EXE 構建工具
│
├── 【🔨 構建系統】
├── build/                           # 構建配置
│   ├── README.md                    # 構建說明
│   └── build_executable.spec        # PyInstaller 配置
│
└── .gitignore                       # Git 忽略列表
```

### 📋 目錄用途快速參考

| 目錄 | 用途 | 何時需要 |
|------|------|----------|
| **docs/** | 📚 所有文檔和指南 | 需要瞭解遊戲或使用 |
| **launchers/** | 🚀 遊戲啟動腳本 | 啟動遊戲、建立快捷方式 |
| **build/** | 🔨 構建配置 | 編譯為 EXE 檔案 |
| **game/** | 🎮 遊戲邏輯核心 | 開發人員修改邏輯 |
| **ui/** | 🎨 圖形界面代碼 | 開發人員修改介面 |
| **tests/** | ✅ 測試程式 | 驗證功能正常性 |
| **assets/** | 🎭 遊戲資源 | 遊戲運行時使用 |
