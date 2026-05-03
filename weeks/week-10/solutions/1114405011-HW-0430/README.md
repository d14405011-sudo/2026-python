# README.md
# Week 10 作業 — 資料格式轉換
# 學號：1114405011 林煉棠

---

## ✅ 完成項目

| 項目 | 狀態 |
|------|------|
| Task 1：CSV → JSON（過濾 + 統計 + 輸出） | ✅ 完成 |
| Task 2：JSON → XML | ✅ 完成 |
| Task 3：@timeit 耗時比較圖 | ✅ 完成 |
| TDD 測試（tests/test_task1.py：10 個，tests/test_task2.py：7 個） | ✅ 全部通過（17 tests） |
| TEST_LOG.md（Red → Green 各一輪） | ✅ 完成 |
| TIMING_REPORT.md | ✅ 完成 |
| **Bonus 1：seaborn 製作設計感比較圖** | ✅ 完成 |
| **Bonus 2：圖中中文字正確顯示（無亂碼）** | ✅ 完成 |
| **Bonus 3：雙圖表版面 + 讀取 vs 寫入分組比較 + 結論摘要文字方塊** | ✅ 完成 |

---

## 🌟 加分項（Bonus）說明

### Bonus 1 — seaborn 設計感比較圖

使用 `seaborn.set_theme(style="whitegrid")` 取代原本的 matplotlib 預設主題，並套用 Task 專屬色票（深藍 / 橙紅），讓每組 Task 的操作一目了然。同時搭配 `sns.despine()` 移除多餘的邊框，整體視覺更乾淨。

### Bonus 2 — 中文字正確顯示

在 `task3_plot_comparison.py` 頂部以 `platform.system()` 動態選擇各作業系統對應的繁體中文字型（Windows 使用 `Microsoft JhengHei`、macOS 使用 `Heiti TC`、Linux 使用 `Noto Sans CJK TC`），並在 `sns.set_theme()` 調用後補充重設 `rcParams`（因為 seaborn 初始化會覆蓋字型設定）。圖中所有標題、座標軸標籤、標註文字均以中文正確呈現，無亂碼。

### Bonus 3 — 創意延伸：雙子圖 + 分組比較 + 結論摘要

`timing_comparison.png` 分成上下兩個子圖：
- **上圖（主圖）**：四個函式的個別耗時長條圖，依 Task 著色，並在最慢操作上加上 `▲ 最慢` 紅色標示箭頭
- **下圖（延伸圖）**：將四個操作依「讀取 / 寫入」類型跨 Task 分組計算均值，提供第二個維度的比較視角（讀取均值 vs 寫入均值）
- **底部文字方塊**：動態產生的「結論摘要」，自動填入最快 / 最慢操作名稱、各分組均值、以及資料量擴展性的預測結論

---

## 📁 檔案結構

```
1114405011-HW-0430/
├── task1_csv_to_json.py        # CSV 讀取 + 過濾 + 統計 + 輸出 JSON
├── task2_json_to_xml.py        # 讀取 JSON + 輸出 XML
├── task3_plot_comparison.py    # 讀取 timeit 結果並繪製比較圖
├── output/                     # 由程式自動產生
│   ├── students.json
│   ├── students.xml
│   └── timing_comparison.png
├── tests/
│   ├── test_task1.py           # 10 個測試
│   └── test_task2.py           # 7 個測試
├── TIMING_REPORT.md
├── TEST_LOG.md
├── AI_USAGE.md
└── README.md
```

---

## 🚀 執行方式

```bash
# 先確認在作業資料夾內
cd weeks/week-10/solutions/1114405011-HW-0430

# Task 1：讀取 CSV → 輸出 output/students.json
python task1_csv_to_json.py

# Task 2：讀取 JSON → 輸出 output/students.xml（需先執行 task1）
python task2_json_to_xml.py

# Task 3：輸出 output/timing_comparison.png（需先執行 task1 / task2）
python task3_plot_comparison.py

# 執行全部測試
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## ⏱️ @timeit 裝飾器的運作說明

`@timeit` 是一個基於閉包（Closure）的高階函式，它接收一個名為 `func` 的目標函式，並回傳包裝好的 `wrapper` 函式。每當我們呼叫被裝飾的 `func`（例如 `read_csv`），實際上會執行 `wrapper`：它利用 `time.perf_counter()` 來精確計算執行該函式所花費的核心時間。程式碼中同時加上了 `@functools.wraps(func)`，這能保留原始函式的名稱、模組與 `__doc__` 註解等描述資料（metadata），使得被裝飾的函式在報錯或是呼叫 `help()` 函數時，不至於會變成辨識不清的裝飾器實作細節，有效提升了專案後期的可維護性。

---

## 🐛 最難理解的 bug 及修正

**Bug：** 執行 `tests/test_task1.py` 測試套件時，`test_filter_removes_others` 這個檢查邊界情況的測試失敗，並出現如下錯誤：
```python
AssertionError: '電機工程系' unexpectedly found in ['電機工程系']
```

**原因分析：** 經過檢視後發現，這是 TDD 設計過程中測試資料不良所引起的。最初在建構假資料（Mock Data）時，同時指派了「聯合登記分發 → 電機工程系」以及「繁星推甄 → 電機工程系」。因此在執行過濾函數 `filter_by_admission` 保留「聯合登記分發」後，「電機工程系」自然還存留在該結果中。而針對反面案例所寫的 `assertNotIn("電機工程系", ...)` 就會誤認為我們沒有好好把所有「繁星推甄」資料過濾掉，導致了無法通過測試（即使程式的過濾邏輯本身完全正確）。這不是這支 Python 程式有錯，而是測試案例寫錯帶來的假警報。

**修正方式：** 將測試輸入用的 `self.rows` 調整為每種「入學方式」皆對應不重複的「系所」。例如：`繁星推甄` 限定對應 `電機工程系`；`聯合登記分發` 限定為 `資訊工程系` 及 `航運管理系`，不再共用系所名稱。接著修改驗證程式碼，改為先藉由集合（set comprehension）提取出所有的 `系所名稱` 為 `depts_in_result`，再分別檢驗對應到不合格輸入方式的系所都不在此集合中。如此一來便徹底排除了誤判。
