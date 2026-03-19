# =====================================
# R03. 字串清理、對齊、拼接與格式化（2.11–2.16）
# =====================================
# 本模組演示字串處理相關的實用操作：
# 1. strip() - 移除字串兩端的空白或指定字元
# 2. ljust() / rjust() / center() - 對字串進行對齊和填充
# 3. format()/format_map()/f-string - 將變數插入字串
# 4. join() - 用分隔符連接多個字串
# 5. textwrap - 自動換行和縮排

import textwrap


# ── 2.11 清理字元 ─────────────────────────────────────────
# 目標：移除字串指定位置的空白字元或其他字元

s = "  hello world \n"

# strip() - 移除字串兩端的空白字符（空格、標籤、換行符等）
# repr() 是用來顯示字串的表示形式，可以看到特殊字元如 \n
print(repr(s.strip()))  
# 輸出: 'hello world'
#      開始的 2 個空格和結尾的空格及換行符都被移除

# lstrip() - 只移除字串左端（開頭）的空白
print(repr(s.lstrip()))  
# 輸出: 'hello world \n'
#      只移除左邊的空格，右邊的空格和換行符保留

# strip() 可以指定要移除的字元（而不只是空白）
# "-=" 表示移除連字符和等號
print("-----hello=====".strip("-="))  
# 輸出: 'hello'
#      移除了前 5 個連字符和後 5 個等號，只保留中間的 'hello'


# ── 2.13 字串對齐 ─────────────────────────────────────────
# 目標：在指定寬度內對齊字串，並用特定字元填充空白

text = "Hello World"

# ljust(width) - 左對齊（Left Just）
# 在字串右側填充空格，使總長度達到指定寬度
print(text.ljust(20))  
# 輸出: 'Hello World         '
#      字串長度為 11，補充 9 個空格使總長度達到 20

# rjust(width) - 右對齊（Right Just）
# 在字串左側填充空格，使總長度達到指定寬度
print(text.rjust(20))  
# 輸出: '         Hello World'
#      在左邊補充 9 個空格，使總長度達到 20

# center(width, fillchar) - 居中對齊
# 在字串兩側填充指定字元（預設為空格），使總長度達到指定寬度
print(text.center(20, "*"))  
# 輸出: '****Hello World*****'
#      字串居中，兩側用 * 填充（左 4 個，右 5 個）

# format() 函式也可以進行格式化對齊
# "^20" 表示「在寬度 20 內居中對齊」
print(format(text, "^20"))  
# 輸出: '    Hello World     '
#      在寬度 20 內居中，兩側填充空格

# format() 也可以用於數字格式化
# ">10.2f" 表示「右對齊，寬度 10，小數點後 2 位的浮點數」
print(format(1.2345, ">10.2f"))  
# 輸出: '      1.23'
#      數字 1.2345 被格式化為 1.23（保留 2 位小數），並右對齊在寬度 10 內


# ── 2.14 合併拼接 ─────────────────────────────────────────
# 目標：用分隔符把多個字串連接成一個字串

parts = ["Is", "Chicago", "Not", "Chicago?"]

# join() - 最高效的字串拼接方法（推薦使用）
# 用空格作為分隔符，將列表的所有項目連接成一個字串
print(" ".join(parts))  
# 輸出: 'Is Chicago Not Chicago?'
#      各個單詞之間用空格分隔

# 使用逗號作為分隔符
print(",".join(parts))  
# 輸出: 'Is,Chicago,Not,Chicago?'
#      各個項目之間用逗號分隔（如 CSV 格式）

# 連接包含不同類型的資料（需要先轉換成字串）
data = ["ACME", 50, 91.1]

# 使用生成器表達式 str(d) for d in data 將每個元素轉換成字串
print(",".join(str(d) for d in data))  
# 輸出: 'ACME,50,91.1'
#      數字被轉換成字串並用逗號連接


# ── 2.15 插入變量 ─────────────────────────────────────────
# 目標：將變數的值動態插入字串中，生成最終的文本

name, n = "Guido", 37

# 方法 1：使用 format() 和命名參數
s = "{name} has {n} messages."
print(s.format(name=name, n=n))  
# 輸出: 'Guido has 37 messages.'
#      {name} 和 {n} 被替換成對應變數的值

# 方法 2：使用 format_map() 搭配 vars()
# vars() 返回當前本地變數的字典
print(s.format_map(vars()))  
# 輸出: 'Guido has 37 messages.'
#      format_map() 直接從字典中查找變數，適合大量變數的情況

# 方法 3：使用 f-string（Python 3.6+，最簡潔最推薦）
# f-string 在字串前加 f 前綴，在大括號內直接寫表達式
print(f"{name} has {n} messages.")  
# 輸出: 'Guido has 37 messages.'
#      f-string 可讀性最好，效能也最佳


# ── 2.16 指定列寬 ─────────────────────────────────────────
# 目標：自動將長文本按照要求的寬度分行，方便在終端機或文件中顯示

long_s = (
    "Look into my eyes, look into my eyes, the eyes, "
    "not around the eyes, look into my eyes, you're under."
)

# textwrap.fill() - 將文本換行以符合指定寬度
# 第一個參數是要格式化的文本
# 第二個參數是每行的最大字元數
print(textwrap.fill(long_s, 40))
# 輸出：
# Look into my eyes, look into my
# eyes, the eyes, not around the eyes,
# look into my eyes, you're under.
# 文本按 40 個字元寬度自動換行

# 使用 initial_indent 參數為第一行加上縮排
# initial_indent="    " 表示第一行前加 4 個空格
print(textwrap.fill(long_s, 40, initial_indent="    "))
# 輸出：
#     Look into my eyes, look into my
# eyes, the eyes, not around the eyes,
# look into my eyes, you're under.
# 第一行前面多了 4 個空格作為縮排
