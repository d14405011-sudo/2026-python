# U02. 正則表達式進階技巧（Cookbook 第 2.4–2.6 節）
# 主要內容：預編譯正則表達式以提高效率 / sub() 回呼函數 / 保持大小寫一致替換

import re
import timeit
from calendar import month_abbr

# ── 第 2.4 節：預編譯正則表達式以提高效率 ──────────────────────────────
# 直接傳入字串 pattern 時，re 會用內建快取幫你管理「是否需要重編譯」
# 在大量／多樣 pattern 或需重複使用同一 pattern 時，顯式 re.compile() 可避免快取 miss，
# 並讓程式碼可讀性、可控性更好

text = "Today is 11/27/2012. PyCon starts 3/13/2013."
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")  # 預先編譯正則表達式（查找日期格式：XX/XX/XXXX）


def using_module():  # 直接使用模組級 API，由 re 內建快取決定是否重編譯
    return re.findall(r"(\d+)/(\d+)/(\d+)", text)


def using_compiled():  # 使用預編譯的正則物件，適合同一 pattern 被多次重用
    return datepat.findall(text)


# 效能比較：預編譯在大量重複使用時通常會更快
t1 = timeit.timeit(using_module, number=50_000)
t2 = timeit.timeit(using_compiled, number=50_000)
print(f"直接呼叫: {t1:.3f}s  預編譯: {t2:.3f}s")


# ── 第 2.5 節：sub() 回呼函數的高級用法 ────────────────────────────────
# re.sub(pattern, repl, string) 中的 repl 也可以是函式：每次匹配到 pattern 時都會呼叫該函式，並用其回傳值作為替換內容

def change_date(m: re.Match) -> str:
    """根據匹配回呼，將日期轉換成月份縮寫的日期格式"""
    mon_name = month_abbr[int(m.group(1))]  # 取得第 1 個捕獲（月），轉換成月份縮寫
    return f"{m.group(2)} {mon_name} {m.group(3)}"  # 格式為：日 月份縮寫 年


print(datepat.sub(change_date, text))
# 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'


# ── 第 2.6 節：保持大小寫風格一致的替換 ────────────────────
# 在「不分大小寫」搜尋 / 替換時，希望替換後的字，保留原文字的大小寫樣式
# 例如：PYTHON → SNAKE、python → snake、Python → Snake
def matchcase(word: str):
    """建立一個回呼函數，用於在不分大小寫替換時，保留原字串的大小寫樣式

    根據被匹配到的文字樣式，將替換字調整為：
      - 全大寫  ：原字全大寫時（e.g. PYTHON → SNAKE）
      - 全小寫   ：原字全小寫時（e.g. python → snake）
      - 首字母大寫：原字首字母大寫時（e.g. Python → Snake）
      - 其他情況：直接使用傳入的 word
    """
    def replace(m: re.Match) -> str:
        t = m.group()  # 取得完整被匹配到的原文字
        if t.isupper():  # 原文字全為大寫
            return word.upper()
        if t.islower():  # 原文字全為小寫
            return word.lower()
        if t[0].isupper():  # 原文字僅首字母為大寫（Title case）
            return word.capitalize()
        return word  # 其他複雜情況，直接回傳原樣式的替換字

    return replace


# 例子：替換 "python" 為 "snake"，且保留原文的大小写
s = "UPPER PYTHON, lower python, Mixed Python"
print(re.sub("python", matchcase("snake"), s, flags=re.IGNORECASE))
# 'UPPER SNAKE, lower snake, Mixed Snake'
