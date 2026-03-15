# TEST_LOG

## 1) Red（先失敗）

- 執行指令：

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

- 測試總數：12
- 通過：10
- 失敗：2
- 失敗摘要：
  - scent 當時只記 `(x, y)`，導致同格不同方向被錯誤攔截。
  - LOST 後仍繼續跑指令，history 長度不正確。
- 修正重點（1~2 句）：
  - scent key 改成 `(x, y, dir)`。
  - 在 `run_commands` 中若 `state.lost` 立即中止後續迴圈。

## 2) Green（全通過）

- 執行指令：

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

- 測試總數：12
- 通過：12
- 失敗：0
- 修改說明（1~2 句）：
  - 完成 scent 與 LOST 的收斂邏輯後，再補上 UVA 範例測試。
  - 重跑全部測試，全數通過。

## 3) Refactor（在全綠下提升品質）

- 執行指令：

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

- 測試總數：15
- 通過：15
- 失敗：0
- 修改說明（1~2 句）：
  - 新增防呆驗證（非法方向、負地圖尺寸）與 scent-block 後續指令測試，提升規格覆蓋完整度。
  - 新增 `G` 匯出 `replay.gif`、`S` 儲存 `gameplay.png`，讓交付證據可直接由遊戲內產生。

## 4) Bonus Refactor（加分項完成）

- 執行指令：

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

- 測試總數：15
- 通過：15
- 失敗：0
- 修改說明（1~2 句）：
  - 介面全面改為中文一致訊息，並新增 `M` 輸出 10x10 矩陣快照與 scent 容器內容。
  - 保持核心規則不變，確保加分功能不影響原本作業正確性。
