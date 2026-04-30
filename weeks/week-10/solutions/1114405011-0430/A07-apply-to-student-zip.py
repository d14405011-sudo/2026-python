# A07. 綜合應用：把 I/O 技巧套到真實學生資料
# Bloom: Apply — 複習並組合 R01~A06 的 API
#
# 資料來源：assets/npu-stu-109-114-anon.zip（6 屆新生資料庫，學號已匿名）
# 用到的小節對照：
#   5.11 pathlib 組路徑
#   5.12 exists 檢查
#   5.7  zipfile 讀壓縮檔（不解壓）
#   5.1  encoding='utf-8-sig' 處理 Excel 存的 BOM
#   5.6  io.StringIO 把 bytes 轉成 csv 可讀的 file-like
#   5.19 TemporaryDirectory 沙箱輸出
#   5.5  open(..., 'x') 只寫一次的報告檔
#   5.21 pickle 保存跨屆統計快照
#   5.2  print(file=) 寫 Markdown 週報

import csv
# 引入記憶體字串流操作模組，可將字串包裝成檔案物件
import io
# 引入 pickle 模組，用於將 Python 物件序列化為二進位快照（或反序列化還原）
import pickle
# 引入 tempfile 模組，用於建立會自動清理的暫存資料夾或檔案
import tempfile
# 引入 zipfile 模組，負責讀寫 ZIP 壓縮檔
import zipfile
# 從 collections 模組引入 Counter，方便計算清單中各項目的出現次數
from collections import Counter
# 引入 pathlib.Path，提供物件導向的路徑操作
from pathlib import Path

# ── 5.11 / 5.12 找到資料檔 ─────────────────────────────
# 取得目前這個 Python 腳本（__file__）的絕對路徑，並抓出它的父目錄（所在資料夾）
HERE = Path(__file__).resolve().parent
# 透過路徑相加往上找 3 層，定位到 assets 資料夾內的壓縮檔
ZIP_PATH = HERE.parent.parent.parent / "assets" / "npu-stu-109-114-anon.zip"
# 檢查檔案是否存在，如果檔案不存在則會觸發 AssertionError
assert ZIP_PATH.exists(), f"找不到資料：{ZIP_PATH}"
print("資料來源:", ZIP_PATH.name)


# ── 5.7 + 5.6 + 5.1 不解壓讀 zip 裡的 CSV ──────────────
def iter_year_csv(zip_path: Path):
    """
    這是一個生成器函數 (Generator)，會逐年回傳 (yield)：
    年度(字串), CSV的標題列(串列), CSV的內容列(二維串列)。
    """
    # 開啟 zip 壓縮檔（結束 with 區塊時會自動關閉檔案）
    with zipfile.ZipFile(zip_path) as z:
        # 走訪 zip 內部的每個檔案資訊 (ZipInfo)
        for info in z.infolist():
            # 取得檔案名稱
            name = info.filename
            # 如果不是 .csv 結尾的檔案就跳過
            if not name.endswith(".csv"):
                continue
            
            # 從檔名切片擷取前三個字元作為年度。例如：'109'~'114'
            year = name[:3]  

            # 讀取該檔案內容，取得原始二進位資料 (bytes)
            raw = z.read(info)                       
            # 5.1 使用 utf-8-sig 解碼為字串，自動去掉開頭的 BOM（Byte Order Mark）
            text = raw.decode("utf-8-sig")           
            # 5.6 使用 io.StringIO 將字串包裝成一個「類似檔案物件 (file-like)」交給 csv.reader 解析
            reader = csv.reader(io.StringIO(text))   
            # 將解析結果轉換為串列：第一列是 header，其餘為 rows
            rows = list(reader)
            # 將年度、標題列、內容列 yield 出去
            yield year, rows[0], rows[1:]


# ── 跨屆統計 ───────────────────────────────────────────
# 準備一個字典 summary 來儲存各年度的統計結果：{年度: {'total': 總人數, 'by_dept': 系所Counter, 'by_entry': 入學方式Counter}}
summary = {}        
# 準備一個 Counter 用來累計這 6 屆「所有」學生的系所人數總和
all_depts = Counter()

# 透過剛才寫的生成器，逐一取得 (年度, 標題列, 內容列)
for year, header, rows in iter_year_csv(ZIP_PATH):
    # 用 index() 找出 "系所名稱" 與 "入學方式" 在標題列的索引位置
    dept_idx  = header.index("系所名稱")
    entry_idx = header.index("入學方式")

    # 利用生成器表達式與 Counter：
    # 將所有行 (rows) 的這一個欄位抽出來並統計次數，還要檢查長度避免資料缺漏產生 IndexError
    by_dept  = Counter(r[dept_idx]  for r in rows if len(r) > dept_idx)
    by_entry = Counter(r[entry_idx] for r in rows if len(r) > entry_idx)

    # 將今年的統計數據整理存進 summary 字典內
    summary[year] = {
        "total":    len(rows), # 內容列的長度即為該年度總人數
        "by_dept":  by_dept,   # 系所統計
        "by_entry": by_entry,  # 入學方式統計
    }
    # 把今年的系所統計結果整合加到「跨屆總計」的 Counter 中
    all_depts.update(by_dept)

# ── 終端輸出：總覽 ─────────────────────────────────────
print("\n=== 6 屆新生人數 ===")
# sorted(summary) 會把字典的 key (年度字串) 排好序再走訪
for year in sorted(summary):
    # :>4 格式化：靠右對齊，預留 4 個字元寬度
    print(f"  {year} 學年：{summary[year]['total']:>4} 人")

print("\n=== 全體最熱門 5 個系所（累計 6 屆） ===")
# .most_common(n) 方法會回傳出現次數前 n 名的 (項目, 次數) 串列
for dept, n in all_depts.most_common(5):
    print(f"  {n:>4} 人  {dept}")

print("\n=== 114 學年入學方式分布 ===")
# 當 most_common() 不放參數，會按總數由高到底回傳所有元素
for kind, n in summary["114"]["by_entry"].most_common():
    print(f"  {n:>4} 人  {kind}")


# ── 5.19 + 5.5 + 5.2 沙箱產生報告、5.21 存快照 ─────────
# 5.19 使用 tempfile.TemporaryDirectory() 會建立暫存資料夾，離開此 with 區塊後 OS 會自動清掉這個資料夾與內容
with tempfile.TemporaryDirectory() as tmp:
    # 把它轉成 Path 物件，接下來的操作比較方便
    tmp = Path(tmp)

    # 5.21 使用 pickle 保存整個 summary，把剛上面算好的字典「序列化（轉二進位）」存檔，日後可直接 load 不必重算
    snap = tmp / "summary.pkl"
    # open 模式使用 "wb" (write binary) 寫入二進位檔案
    with open(snap, "wb") as f:
        pickle.dump(summary, f)
    # .stat().st_size 可以取得檔案佔據的位元組大小 (bytes)
    print(f"\n快照寫入 {snap.name}：{snap.stat().st_size} bytes")

    # 5.5 'x' 模式 (Exclusive creation) 確保建立的 Markdown 報告檔如果不小心已存在就會報錯，防止被意外覆蓋
    report = tmp / "report.md"
    with open(report, "x", encoding="utf-8") as f:      # 5.5
        # 5.2 print(..., file=f) 將結果印到指定的檔案裡，取代印在終端機
        print("# 6 屆新生概況報告\n", file=f)           
        print("| 學年 | 人數 | 第一大系所 |", file=f)
        print("|------|------|------------|", file=f)
        # 依序把每一年的數據填進 Markdown 表格裡
        for year in sorted(summary):
            # 取出該年度第一大系所的資訊 : [0] 拿取 (學系, 人數)
            top_dept, top_n = summary[year]["by_dept"].most_common(1)[0]
            print(f"| {year} | {summary[year]['total']} | "
                  f"{top_dept} ({top_n}) |", file=f)

    # 5.1 把 Markdown 用 read_text() 一次讀回成字串，然後印出來預覽
    print("\n=== Markdown 報告預覽 ===")
    print(report.read_text(encoding="utf-8"))

    # 驗證檢查 pickle 有無存壞（確認型別、內容一不一致）
    # open 模式改為 "rb" (read binary) 等待讀取二進位資料
    with open(snap, "rb") as f:
        loaded = pickle.load(f)
    print("pickle 讀回 key:", sorted(loaded.keys()))

# 離開 with → tmp 自動清掉，不在專案留任何垃圾檔案
print("\n(沙箱已自動清理)")


# ── 課堂延伸挑戰 ───────────────────────────────────────
# 1) 把報告改寫到 HERE / 'report.md'（改用 'w' 模式會覆蓋，'x' 會報錯）。
# 2) 加一欄「女性比例」：找出性別欄位後用 Counter 統計。
# 3) 把 summary 壓縮存成 summary.pkl.gz（gzip.open('wb') + pickle.dump）。
# 4) 跨屆找出「人數逐年下降最明顯」的系所（需要把 by_dept 按年排成折線）。
