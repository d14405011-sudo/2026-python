# 大老二遊戲（Big Two）

這是一個以 Pygame 實作的單人對戰大老二遊戲（玩家 vs 3 位 AI）。

## 系統需求
- Python 3.9+
- `pygame-ce`（或 `pygame`）

## 安裝與執行

### 快速啟動（Windows）
```powershell
cd D:\2026-python\weeks\week-05\solutions\HW-114405011\bigtwo
.\開始遊戲.bat
```

### 手動啟動
```powershell
cd D:\2026-python\weeks\week-05\solutions\HW-114405011\bigtwo
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 專案結構
```text
bigtwo/
├─ main.py
├─ requirements.txt
├─ README.md
├─ AI_USAGE.md
├─ TEST_CASES.md
├─ TEST_LOG.md
├─ 開始遊戲.bat
├─ game/
├─ ui/
├─ tests/
├─ launchers/
├─ docs/
└─ assets/
```

## 遊戲規則重點

### 牌面大小
- 花色：♣ < ♦ < ♥ < ♠
- 點數：3 < 4 < 5 < 6 < 7 < 8 < 9 < 10 < J < Q < K < A < 2

### 主要牌型
- 單張
- 對子
- 順子（5 張）
- 葫蘆
- 鐵支
- 同花順
- 一條龍（13 張）

註：本專案規則中不使用三條作為獨立可出牌型。

### 操作方式
- 滑鼠左鍵選牌
- Enter：出牌
- P：過牌

## 模式與難度
- 休閒模式：可選 AI 難度（低/中/高）
- 挑戰賽模式：固定高難度，啟用計分與計時

## 測試

### 執行全部測試
```powershell
cd D:\2026-python\weeks\week-05\solutions\HW-114405011\bigtwo
python -m unittest discover -s tests -v
```

### 最新測試結果
- 總測試數：53
- 通過：53
- 失敗：0

詳細請見 `TEST_CASES.md` 與 `TEST_LOG.md`。
