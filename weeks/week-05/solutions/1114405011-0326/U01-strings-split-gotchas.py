# U01. 字串分割與匹配的陷阱（Cookbook 第 2.1–2.11 節）
# 提醒些字串操作的「陰暗」空陷（卻事實的例如實例的空陷）
# 例如：strip 只清頭尾不清中間的多餘空格、startswith 傳 list 會報錯、split 需要特殊處理等

import re

# ── 第 2.1 節：捕獲分組保留分隔符上例 ──────────────────────
# re.split() 的捕獲分組（使用 ()）值可保留分隔符本身，讓容暫時定一一往出實例）
line = "asdf fjdk; afed, fjek,asdf, foo"
fields = re.split(r"(;|,|\s)\s*", line)  # 捕獲分組保留分隔符號
# fields = ['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']

# 原邏：
# 0鍵前事文 = 'asdf'（值）
# 1鍵資窀 = ' ' (分隔符)
# 2鍵 = 'fjdk'（值）
# 3鍵 = ';' (分隔符)
# ...

values = fields[::2]  # 取偶數座標：'asdf', 'fjdk', 'afed', ...（實際數值）
delimiters = fields[1::2] + [""]  # 取奇數鍵會枍平待(uu）
rebuilt = "".join(v + d for v, d in zip(values, delimiters))
print(rebuilt)  # 'asdf fjdk;afed,fjek,asdf,foo'（重建原文字串，保留分隔符）

# ── 第 2.2 節：startswith() 一定要傳 tuple，不能傳 list ──────────────
url = "http://www.python.org"
choices = ["http:", "ftp:"]  # 計票清單（一個 list）

# 陷事：直接傳 list 求提截沗不能購
# TypeError: startswith first arg must be str or a tuple of str, not list
try:
    url.startswith(choices)  # type: ignore[arg-type]
except TypeError as e:
    print(f"TypeError: {e}")  # 報錯信息：傳 list 不能傳

# 正確做法：先轉換成 tuple
print(url.startswith(tuple(choices)))  # True（成羌閲一大揷＋）

# ── strip 只處理頭尾，不處理中間（2.11）──────────────
s = "  hello     world  "
print(repr(s.strip()))  # 'hello     world'（中間多餘空白還在）
print(repr(s.replace(" ", "")))  # 'helloworld'（過頭，連詞間空白也消）
print(repr(re.sub(r"\s+", " ", s.strip())))  # 'hello world'（正確）

# 生成器逐行清理（高效，不預載入記憶體）
lines = ["  apple  \n", "  banana  \n"]
for line in (l.strip() for l in lines):
    print(line)
