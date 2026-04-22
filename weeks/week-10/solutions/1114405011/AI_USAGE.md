# AI_USAGE

## 我如何使用 AI
- 請 AI 協助讀取 week-10 五題題目，先建立主版本與 easy 版本的解法骨架。
- 請 AI 依既有命名規則整理資料夾（每題獨立資料夾、q題號.py、q題號-easy.py、test_q題號.py）。
- 請 AI 產生 hand-typed 版本（無註解）與 hand-typed 對應測試。
- 請 AI 協助整理測試紀錄檔，並轉成可提交的 Markdown 測試報告。

## 我採用的建議
- 先完成可執行程式，再補齊單元測試與測試紀錄。
- easy 版保留較直覺、好記的寫法，hand-typed 版維持精簡且無註解。
- 使用分題測試檔（test_qxxxx.py、test_qxxxx_hand_typed.py）以利快速定位失敗題目。
- 測試時避免使用根目錄一次 discover（可能出現 0 tests），改採各題號資料夾逐一執行。

## 我沒有直接採用的建議
- 將所有題目測試併成單一整合測試檔。
- 原因：與既有作業骨架不一致，且分題維護與追錯效率較低。

## 人工檢查
- 人工確認檔案命名、資料夾結構、easy/hand-typed 是否齊全。
- 人工檢查 hand-typed 版本不含註解。
- 人工檢查測試輸出與 TEST_LOG、TEST_LOG_HAND_TYPED 內容一致。
