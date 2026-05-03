# AI_USAGE.md
# AI 使用說明
# 學號：1114405011

## 1. 我問了哪些問題

在實作本週任務的過程中，我向 AI（GitHub Copilot / ChatGPT）提出了以下幾個輔助性問題：
1. `functools.wraps` 放在裝飾器裡面具體的作用是什麼？如果不加上這行指令，後續維護或 debug 時會引發哪些具體的不良影響？
2. 關於 XML 的美化：`ET.indent()` 方法是什麼時候（哪個 Python 版本）才加入標準函式庫的？考量到相容性，有沒有針對舊版 Python 同樣能實現換行與縮排的作法？
3. 在讀取 `113年新生資料庫.csv` 時，所謂的 `UTF-8-BOM` 編碼與一般 `UTF-8` 差在哪裡？為什麼一定得用 `encoding='utf-8-sig'` 才能避開亂碼或欄位辨識錯誤？
4. 當要統計系所人數時，使用 `collections.Counter` 取代一般宣告 `dict` 再用 `for` 迴圈逐漸遞增的方法，優勢與缺點在哪裡？哪種寫法更加 Pythonic？
5. 如何在輸出最終的 `students.xml` 檔案時，在文件首行加上標準的 XML 宣告文字 `<?xml version="1.0" encoding="utf-8"?>` 以符合規定格式？

## 2. AI 建議我有採用的部分

- 在處理字典鍵值存取時，採用 `r.get("入學方式", "").strip()` 搭配空字串預設值。這樣的寫法可以有效防止 CSV 檔內有缺漏資料或空格造成 `KeyError` 中斷整個程式，非常安全。
- 在 `count_by_dept` 中，採用了 `collections.Counter`，並在最後結合 `sorted(..., key=lambda x: x[1], reverse=True)`，使得回傳的字典自動以人數由多至少完成排列，既簡潔又高效。
- 在 Task 2 的檔案輸出環節：採納了呼叫 `tree.write(..., encoding="utf-8", xml_declaration=True)` 將 XML 結構直接寫出檔案的標準方法，完整包含了 XML 的宣告頭。
- 引入 `os.makedirs(os.path.dirname(filepath), exist_ok=True)` 處理輸出路徑，避免因為一開始沒有建立 `output` 資料夾而引發 `FileNotFoundError` 報錯。

## 3. AI 建議我拒絕的部分及原因

- **建議直接用第三方套件 `lxml` 或是 `xmltodict` 來建構與輸出 XML**：我拒絕了這項建議。因為這門課程的核心是先深入理解 Python 的「標準函式庫」，考量到了之後專案搬移時不應具備過高的依賴性。再者本作業明確要求使用 `xml.etree.ElementTree` 來處理。
- **建議將 `@timeit` 擴充成更高階的「帶參數裝飾器（Parameterized Decorator）」**：例如可以使用 `@timeit(label="特定操作")` 功能來產生客製化報告。我予以拒絕，原因在於目前的 `def timeit(func)` 設計已經足以完成此次效能量測的作業需求。這類過度設計（Over-engineering）反而會讓邏輯難以理解且測試變得複雜。
- **建議直接用 `pandas` 套件以一行程式碼如 `df.to_json()` 來做 Task 1 的轉換**：我也沒有採用。因作業明確旨在訓練我們對字串轉換、字元過濾、字典操作的底層控制能力，而不是當一個只會呼叫現成框架包裝指令的使用者。

## 4. AI 輸出執行後發現有誤的案例

**問題情境：** 利用 AI 產生 TDD 單元測試代碼以便驗證「`filter_by_admission` 邏輯是否把不要的入學方式都刪掉了」時，AI 提供了一段測試斷言（Assertion）：`self.assertNotIn(r["系所名稱"], ["電機工程系"])`，藉此驗證非登記分發的資料是否被正確剔除。

**發現錯誤：** 
當我執行 `python -m unittest` 後，終端機報錯了：`AssertionError: '電機工程系' unexpectedly found in ['電機工程系']`。
經手動追查，是因為當初傳入的自訂假資料包含了：
- `{"入學方式": "聯合登記分發", "系所名稱": "電機工程系"}`
- `{"入學方式": "繁星推甄", "系所名稱": "電機工程系"}`

因此在順利過濾出「聯合登記分發」後，結果中理所當然地還留著「電機工程系」這筆項目。而 AI 產生的測試代碼太過粗略，只檢查特定的「系所字串」有無出現，忽略了多重條件的對應關係。

**後續修正過程：** 
1. 我先檢視測試失敗的 Stack Trace 找出是在哪一個檢查點 `FAIL`。
2. 明白這是一個 False Alarm（假警報）後，我重新設定了 `setUp` 裡面的 `self.rows` 結構，強制規定：每種類型的「入學方式」只對應獨立且唯一的「系所名稱」（例如繁星推甄的假資料，全部叫 電機工程系；聯合登記分發的全部叫 航運管理系）。
3. 將檢驗條件改為以過濾出的集合作為基準，即 `depts_in_result = {r["系所名稱"] for r in result}`，並清楚定義排除：`self.assertNotIn("電機工程系", depts_in_result)`，終於使此 TDD 測試通過 `Green` 的標準。
