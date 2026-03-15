# AI_USAGE

## 你問 AI 的 5 個問題

1. `Robot Lost` 的 scent 為什麼要包含方向？
2. 如何設計 `robot_core.py` 才能不依賴 pygame 便於測試？
3. `LOST` 後停止執行指令要在哪一層處理比較好？
4. unittest 要怎麼覆蓋旋轉、越界、scent 三大面向？
5. pygame 的最小互動 MVP 鍵位配置可以怎麼設計？

## 我採用的建議與原因

- 採用「核心邏輯與 UI 分離」：可以提升可測試性與可維護性。
- 採用 `set[(x, y, dir)]`：查詢危險點效率高且精準。
- 採用事件回傳（MOVE/LOST/SCENT_BLOCK）：UI 方便顯示狀態與除錯。
- 採用 `G` 匯出 replay 與 `S` 儲存截圖：可直接產生作業要求的證據檔。

## 我拒絕的建議與原因

- 拒絕把所有邏輯都寫在 pygame loop 裡：會讓測試困難、耦合過高。
- 拒絕 scent 只記 `(x, y)`：不符合題目規則，會造成誤判。
- 拒絕在 Python 3.14 直接安裝舊版 pygame：安裝與編譯失敗風險高，改採 `pygame-ce`。

## 一個 AI 建議不完整、我自行修正的案例

- AI 起初只提醒「越界就 LOST」，但沒有完整說明「同位置同方向的後續機器人要忽略危險 F」。
- 我補上完整條件判斷與測試：先檢查 scent，再決定是 `SCENT_BLOCK` 或 `LOST`。

## 我如何驗證 AI 建議

- 每次改動後都執行：`python -m unittest discover -s tests -p "test_*.py" -v`。
- 針對關鍵規則新增對應測試（例如 scent 擋下後仍可繼續下一指令）。
- 以遊戲內實測確認 `G` 與 `S` 會輸出到 `assets/` 目錄。
