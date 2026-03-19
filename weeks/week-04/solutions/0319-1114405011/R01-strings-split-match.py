# =====================================
# R01. 字串分割與匹配（2.1–2.3）
# =====================================
# 本模組演示三個字串處理主題：
# 1. re.split() - 使用正規表達式的多分隔符分割
# 2. startswith() / endswith() - 檢查字串開頭/結尾
# 3. fnmatch - Shell 風格的通配符匹配

import re  # 導入正規表達式模組
from fnmatch import fnmatch, fnmatchcase  # 導入 fnmatch 函式用於通配符匹配


# ── 2.1 多界定符分割 ───────────────────────────────────────
# 目標：將包含多種分隔符（分號、逗號、空白）的字串分割成單詞列表

line = "asdf fjdk; afed, fjek,asdf, foo"

# 使用 re.split() 以及正規表達式模式分割
# [;,\s] 表示「分號、逗號或任意空白字元」是分隔符
# \s* 表示在分隔符之後可能跟著零個或多個空白字元（用來移除多餘空格）
print(re.split(r"[;,\s]\s*", line))
# 輸出: ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# 非捕獲分組 (?:...) 做法：分組但不保留分隔符
# 和上面的結果相同，但方式更明確地列舉分隔符
# (?:,|;|\s) 表示「逗號 或 分號 或 空白」（不捕獲該組）
print(re.split(r"(?:,|;|\s)\s*", line))
# 輸出: ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']


# ── 2.2 開頭/結尾匹配 ───────────────────────────────────────
# 目標：檢查字串是否以特定前綴或後綴開始或結束

filename = "spam.txt"

# endswith() - 檢查字串是否以給定的後綴結尾
print(filename.endswith(".txt"))  # True - 檔名確實以 ".txt" 結尾

# startswith() - 檢查字串是否以給定的前綴開始
print(filename.startswith("file:"))  # False - 檔名不以 "file:" 開始

# 進階用法：同時檢查多種後綴
# 必須傳入 tuple（例如 (".c", ".h")），不能傳 list（例如 [".c", ".h"]）
filenames = ["Makefile", "foo.c", "bar.py", "spam.c", "spam.h"]

# 列表推導式：篩選所有以 ".c" 或 ".h" 結尾的檔名
print([name for name in filenames if name.endswith((".c", ".h"))])
# 輸出: ['foo.c', 'spam.c', 'spam.h'] - 只有 C 語言檔被篩選出來


# ── 2.3 Shell 通配符匹配 ────────────────────────────────────
# 目標：使用 Shell 風格的萬用字元模式進行靈活的字串匹配
#       （類似終端機中 ls *.txt 的模式）

# fnmatch() - 預設不區分大小寫（在 Unix/Linux 不同系統表現可能不同）
print(fnmatch("foo.txt", "*.txt"))  
# True - "foo.txt" 符合 "*.txt" 模式（* 代表任意字元序列）

print(fnmatch("Dat45.csv", "Dat[0-9]*"))  
# True - "Dat45.csv" 符合 "Dat[0-9]*" 模式
#        [0-9] 表示「0 到 9 的任意單一數字」
#        * 表示之後可有任意字元序列

# fnmatchcase() - 強制區分大小寫版本
# 這個函式在所有平台上都會區分字母的大小寫
print(fnmatchcase("foo.txt", "*.TXT"))  
# False - "foo.txt" 不符合 "*.TXT" 模式（因為 "txt" ≠ "TXT"）

# 實用例子：篩選地址清單
addresses = ["5412 N CLARK ST", "1060 W ADDISON ST", "1039 W GRANVILLE AVE"]

# 用 fnmatchcase() 重新篩選所有以 " ST" 結尾的地址（區分大小寫）
# * 表示任意前綴，ST 表示必須以「空格加 ST」結尾
print([a for a in addresses if fnmatchcase(a, "* ST")])
# 輸出: ['5412 N CLARK ST', '1060 W ADDISON ST'] - 只有 ST 結尾的地址
