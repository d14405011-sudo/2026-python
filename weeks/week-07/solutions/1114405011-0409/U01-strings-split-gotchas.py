# U01. 字串分割與匹配的陷阱（2.1–2.11）
#
# 本檔示範三個在實務上很常踩雷的字串處理情境：
# 1) 用 re.split() 分割時，如何保留分隔符，並回組回原字串。
# 2) str.startswith() / str.endswith() 第二個參數型別限制（必須是 tuple）。
# 3) strip() 只會處理「字串頭尾」空白，不會動到中間空白。
#
# 建議學習方式：
# - 先看每段註解理解原理。
# - 再觀察 print 結果，對照「預期」與「實際」的差異。
# - 最後自行修改測試資料，確認你真的掌握行為。

import re

# ── 捕獲分組保留分隔符（2.1）─────────────────────────
# 一般 re.split() 會把分隔符丟掉；若你後續需要「重建原字串」
# 或想做分隔符統計，就必須把分隔符保留下來。
#
# 關鍵：在 split pattern 用「捕獲分組」(...)，分隔符就會一起出現在結果中。
line = "asdf fjdk; afed, fjek,asdf, foo"
fields = re.split(r"(;|,|\s)\s*", line)
# split 後的陣列型態會像：值, 分隔符, 值, 分隔符, ...
values = fields[::2]  # 偶數索引是資料值
delimiters = fields[1::2] + [""]  # 奇數索引是分隔符，尾端補空字串方便 zip
rebuilt = "".join(v + d for v, d in zip(values, delimiters))
print(rebuilt)  # 'asdf fjdk;afed,fjek,asdf,foo'

# ── startswith 必須傳 tuple（2.2）────────────────────
# 這是非常常見的 TypeError：
# - list 看起來像可放多個前綴，但 startswith 不接受 list。
# - 正確做法是 tuple，例如 ('http:', 'ftp:')。
#
# 若前綴來源是 list，記得先 tuple(list_var)。
url = "http://www.python.org"
choices = ["http:", "ftp:"]
try:
    url.startswith(choices)  # type: ignore[arg-type]
except TypeError as e:
    print(f"TypeError: {e}")  # 不能傳 list！
print(url.startswith(tuple(choices)))  # True（轉成 tuple 才行）

# ── strip 只處理頭尾，不處理中間（2.11）──────────────
# 常見誤解：以為 strip() 會把所有空白都清掉。
# 事實上 strip() 只處理頭尾，字串中間完全不動。
#
# 三種寫法比較：
# 1) strip()：保留詞間空白（但數量不變）
# 2) replace(" ", "")：把所有空白刪掉（通常太激進）
# 3) re.sub(r"\s+", " ", s.strip())：標準化成單一空白（常用）
s = "  hello     world  "
print(repr(s.strip()))  # 'hello     world'（中間多餘空白還在）
print(repr(s.replace(" ", "")))  # 'helloworld'（過頭，連詞間空白也消）
print(repr(re.sub(r"\s+", " ", s.strip())))  # 'hello world'（正確）

# 生成器逐行清理（高效，不預載入記憶體）
# 在處理大檔案時，不要先讀成完整 list 再清理。
# 這裡用 generator expression 逐行處理，可降低記憶體占用。
lines = ["  apple  \n", "  banana  \n"]
for line in (l.strip() for l in lines):
    print(line)
