# U04. 類檔案物件 StringIO 與逐行處理（5.6 / 5.1 逐行）
# Bloom: Understand — 知道 file-like 是鴨子型別，能把記憶體當檔案用（理解如何在記憶體中模擬檔案操作與處理大檔案的逐行過濾技巧）

import io
from pathlib import Path

# ── 5.6 StringIO：記憶體裡的「假檔案」 ─────────────────
# io.StringIO() 提供了一個存在於「記憶體」中的文字緩衝區
# 它具備和真實檔案物件 (file object) 一模一樣的方法 (read, write, seek... 等)，這就是所謂的「鴨子型別 (Duck Typing)」
buf = io.StringIO()

# 因為 buff 行為像檔案，所以可以搭配 print(..., file=buf) 將內容寫入記憶體中，而不用產生真正的磁碟 I/O
print("第一行", file=buf)
print("第二行", file=buf)
print("第三行", file=buf)

# getvalue() 是一次性取出目前 StringIO 緩衝區內所有字串的特有方法
text = buf.getvalue()
print("---StringIO 內容---")
print(text)

# 也能當讀檔用：seek 回開頭再逐行讀
# 由於前面寫入文字後，內部「檔案游標 (指標)」會停留在最末端
# 為了從頭讀取，必須使用 seek(0) 將指標歸零移動回檔案開頭
buf.seek(0)

# 接著就可以像處理真實檔案一樣，將 buf 直接作為迭代器逐行讀取
for i, line in enumerate(buf, 1):
    print(i, line.rstrip())  # rstrip() 用來移除結尾的換行符號

# 為什麼有用？任何收 file-like 的 API（csv、json、logging 等等）
# 都能塞 StringIO 進去，不必真的建立實體檔案、寫到磁碟，這點在「單元測試」或是「暫存資料轉換」時非常方便且快速。
import csv
mem = io.StringIO()
writer = csv.writer(mem)  # csv.writer 需要一個「可以寫入文字的檔案物件」，mem 剛好符合條件
writer.writerow(["name", "score"])
writer.writerow(["alice", 90])
print("---CSV in memory---")
print(mem.getvalue())     # 直接拿結果字串，沒有任何實體檔案被建立

# ── 5.1 延伸：逐行處理檔案（大檔友善） ─────────────────
# 先在磁碟上快速製造一個有多行內容與空行的文字檔
src = Path("poem.txt")
src.write_text("床前明月光\n\n疑是地上霜\n\n舉頭望明月\n低頭思故鄉\n", encoding="utf-8")

# 任務：讀取來源檔，過濾所有的空行、加上行號，然後寫到新檔
dst = Path("poem_numbered.txt")

# 使用 with 同時安全地開啟兩個檔案 (一個作讀取 rt，一個作寫入 wt)
# 這種「串流處理」模式是操作巨大檔案的標準 SOP，不會把檔案全塞進記憶體
with open(src, "rt", encoding="utf-8") as fin, \
     open(dst, "wt", encoding="utf-8") as fout:
    n = 0
    for line in fin:               # 逐行迭代：不管檔案多大，一次只讀一行到記憶體
        line = line.rstrip()       # 削掉結尾的空白與預設換行符號
        if not line:
            continue               # 如果字串是空的 (代表原本是空行)，就跳過這回合，不處理
        
        n += 1
        # 將格式化後帶有行號的字串，透過 file=fout 寫出到新檔案
        print(f"{n:02d}. {line}", file=fout)

print("---加行號後---")
print(dst.read_text(encoding="utf-8"))
