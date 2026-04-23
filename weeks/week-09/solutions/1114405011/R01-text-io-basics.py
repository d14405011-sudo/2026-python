# R01. 文本 I/O 基本式（5.1 / 5.2 / 5.3 / 5.17）
# Bloom: Remember — 會叫出 open/print 的基本參數（熟悉基本檔案讀寫操作與 print 格式控制）

from pathlib import Path

# ── 5.1 讀寫文本檔 ─────────────────────────────────────
# 寫入：mode='wt' 表示以「寫入 (Write) 文字 (Text)」模式開啟。
# 若檔案已存在會被覆蓋。請務必指定 encoding="utf-8" 避免不同作業系統（如 Windows 預設的 CP950）產生亂碼。
path = Path("hello.txt")
with open(path, "wt", encoding="utf-8") as f:
    f.write("你好，Python\n")  # \n 代表換行符號
    f.write("第二行\n")

# 讀回：一次讀取整個檔案 vs 逐行讀取
# 'rt' 代表「讀取 (Read) 文字 (Text)」模式。
with open(path, "rt", encoding="utf-8") as f:
    print(f.read())  # 一次讀取檔案的全部內容成一個字串（只適合小檔案，避免記憶體耗盡）

with open(path, "rt", encoding="utf-8") as f:
    for line in f:  # 直接把檔案物件 f 當作迭代器，每次只讀取一行。處理大檔案時必買的寫法。
        print(line.rstrip())  # 使用 rstrip() 去除行尾多餘的空白或換行符號，避免 print() 再多印一行

# ── 5.2 print 導向檔案 ─────────────────────────────────
# 利用 print 內建的 file 參數，輕鬆將輸出結果寫入檔案，取代原本的終端機畫面顯示。
with open("log.txt", "wt", encoding="utf-8") as f:
    print("登入成功", file=f)
    print("使用者:", "alice", file=f)  # 逗號隔開的多個物件，預設會以空白字元分隔寫入

# ── 5.3 調整分隔符與行終止符 ───────────────────────────
fruits = ["apple", "banana", "cherry"]
with open("fruits.csv", "wt", encoding="utf-8") as f:
    # sep="," 改變多個物件之間的預設分隔符（從空白變成逗號）
    # *fruits 進行解包，等同於 print("apple", "banana", "cherry", sep=",", ...) 
    print(*fruits, sep=",", end="\n", file=f)

# 'at' 表示「附加 (Append) 文字 (Text)」模式。新寫入的內容會接在檔案結尾而不覆蓋舊內容。
with open("fruits.csv", "at", encoding="utf-8") as f:
    # end="," 取代預設的換行("\n")符號。這樣下一次寫入就會接著在同一行。
    print("date", end=",", file=f)
    print("2026-04-23", file=f)

# 利用 pathlib 的 read_text 快速讀取並顯示結果
print(Path("fruits.csv").read_text(encoding="utf-8"))
# 預期輸出結果: 
# apple,banana,cherry
# date,2026-04-23

# ── 5.17 文字模式 vs 位元組模式提醒 ────────────────────
# 檔案開啟模式分得很清楚：
# 'wt' / 'rt' 用於處理「字串 (str)」
# 'wb' / 'rb' 用於處理「二進位資料 (bytes)」，如圖片或二進位封包。不會有 encoding 參數。
try:
    with open("bad.txt", "wt", encoding="utf-8") as f:
        # 強行在文字模式 ('wt') 下寫入位元組字串 (b"...")，會引發 TypeError
        f.write(b"bytes in text mode")  # ← 這行會出錯
except TypeError as e:
    print("錯誤示範:", e)
