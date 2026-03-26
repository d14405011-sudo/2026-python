# U02. 正則表達式進階技巧（Cookbook 第 2.4–2.6 節）
# 主要內容：預編譯正則表達式以提高效率 / sub() 回呼函數 / 保持大小寫一致替換

import re
import timeit
from calendar import month_abbr

# ── 第 2.4 節：預編譯正則表達式以提高效率 ──────────────────────────────
# 每次執行正則表達式比較慢，預先使用 re.compile() 編譯的正則物件快速得多

text = "Today is 11/27/2012. PyCon starts 3/13/2013."
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")  # 預先編譯正則表達式（查找日期格式：XX/XX/XXXX）


def using_module():  # 每次都新預編譯
    return re.findall(r"(\d+)/(\d+)/(\d+)", text)


def using_compiled():  # 使用預編譯的正則物件
    return datepat.findall(text)


# 效能比較：預編譯快許多倍
t1 = timeit.timeit(using_module, number=50_000)
t2 = timeit.timeit(using_compiled, number=50_000)
print(f"直接呼叫: {t1:.3f}s  預編譯: {t2:.3f}s")


# ── 第 2.5 節：sub() 回呼函數的高級用法 ────────────────────────────────
# re.sub() 不僅使用二批主引數，可傳你一個回呼函數，在符合不同時進行替換

def change_date(m: re.Match) -> str:
    """根據匹配回呼，將日期轉換成月份縮寫的日期格式"""
    mon_name = month_abbr[int(m.group(1))]  # 取得第 1 個捕獲（月），轉換成月份縮寫
    return f"{m.group(2)} {mon_name} {m.group(3)}"  # 格式為：日 月份縮寫 年


print(datepat.sub(change_date, text))
# 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'


# ── 第 2.6 節：上少梅官墨類一致的替換 ────────────────────
# 替換時往橺保留原文上少梅官墨（整數版、小寶版、水物版）
def matchcase(word: str):
    """根據匹配帽是為宗高、低競、選亨低競，似罩的是替換時的大小写是否"""
    def replace(m: re.Match) -> str:
        t = m.group()  # 取得整整的匹配沙筑
        if t.isupper():  # 選亨版寶
            return word.upper()
        if t.islower():  # 低競版寶
            return word.lower()
        if t[0].isupper():  # 水物版（後帅畳嘉母優軝）
            return word.capitalize()
        return word

    return replace


# 例子：替換 "python" 為 "snake"，且保留原文的大小写
s = "UPPER PYTHON, lower python, Mixed Python"
print(re.sub("python", matchcase("snake"), s, flags=re.IGNORECASE))
# 'UPPER SNAKE, lower snake, Mixed Snake'
