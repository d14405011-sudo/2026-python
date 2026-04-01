# 測試案例說明（TDD）

本專案以 `unittest` 為主，覆蓋核心遊戲邏輯、AI 決策與 UI 初始化。

## 執行方式

### 全部測試
```powershell
cd D:\2026-python\weeks\week-05\solutions\HW-114405011\bigtwo
python -m unittest discover -s tests -v
```

### 單模組測試
```powershell
python -m unittest tests.test_models -v
python -m unittest tests.test_classifier -v
python -m unittest tests.test_finder -v
python -m unittest tests.test_game -v
python -m unittest tests.test_ai -v
python -m unittest tests.test_ui -v
```

## 測試統計（最新）
- 總測試數：53
- 通過：53
- 失敗：0
- 通過率：100%

## 模組覆蓋明細
- `tests/test_models.py`：6
- `tests/test_classifier.py`：19
- `tests/test_finder.py`：5
- `tests/test_game.py`：14
- `tests/test_ai.py`：6
- `tests/test_ui.py`：3

合計：53

## 測試重點

### 模型層（models）
- 牌卡建立與顯示
- 牌面比較（點數、花色）
- 牌組初始化與發牌

### 分類器（classifier）
- 各牌型判定
- 特殊順子判定
- 五張牌型強度比較
- 無效牌型排除

### 搜尋器（finder）
- 合法出牌組合搜尋
- 五張牌型與一條龍搜尋
- 無效組合排除

### 遊戲流程（game）
- 開局必含梅花 3
- 回合控制與過牌機制
- 清桌規則與保護邏輯
- 邊界條件與防呆

### AI 策略（ai）
- 出牌評分
- 不同局面下的選牌策略
- 風險情境應對

### UI（ui）
- App 初始化
- 手牌與卡牌渲染
- 輸入流程整合

## 備註
- `tests/test_randomness.py` 與 `tests/test_shuffle.py` 為隨機性驗證腳本，主要用於觀察統計輸出，不列入上述 53 個單元測試計數。
