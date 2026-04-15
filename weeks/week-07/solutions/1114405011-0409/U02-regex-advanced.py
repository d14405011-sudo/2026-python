# U02. 正則表達式進階技巧（2.4–2.6）
#
# 本檔聚焦在三個實務情境：
# 1) 反覆比對同一個 pattern 時，re.compile() 是否有價值？
# 2) re.sub() 如何透過 callback 進行「有邏輯」的替換？
# 3) 文字替換時，如何保留原字詞大小寫風格？

import re
import timeit
from calendar import month_abbr

# ── 預編譯效能（2.4）──────────────────────────────────
# 當同一個正則會被執行很多次，先 compile 往往更有效率，
# 因為 pattern 解析成本只付一次，不必每次呼叫都重複解析。
text = "Today is 11/27/2012. PyCon starts 3/13/2013."
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")


def using_module():
    return re.findall(r"(\d+)/(\d+)/(\d+)", text)


def using_compiled():
    return datepat.findall(text)


t1 = timeit.timeit(using_module, number=50_000)
t2 = timeit.timeit(using_compiled, number=50_000)
print(f"直接呼叫: {t1:.3f}s  預編譯: {t2:.3f}s")


# ── sub 回呼函數（2.5）────────────────────────────────
# 需求：把 MM/DD/YYYY 改成 DD Mon YYYY
# 若用固定字串替換，邏輯會很快變複雜。
# 更好的方式是使用 callback，讓每次 match 都能客製化處理。
def change_date(m: re.Match) -> str:
    # m.group(1) = 月, group(2) = 日, group(3) = 年
    # month_abbr[11] -> 'Nov'
    mon_name = month_abbr[int(m.group(1))]
    return f"{m.group(2)} {mon_name} {m.group(3)}"


print(datepat.sub(change_date, text))
# 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'


# ── 保持大小寫一致的替換（2.6）───────────────────────
# 如果原文有 UPPER / lower / Title 等不同大小寫風格，
# 直接替換會破壞可讀性，因此我們做一個「大小寫感知」替換器。
def matchcase(word: str):
    def replace(m: re.Match) -> str:
        t = m.group()
        if t.isupper():
            return word.upper()
        if t.islower():
            return word.lower()
        if t[0].isupper():
            return word.capitalize()
        return word

    return replace


s = "UPPER PYTHON, lower python, Mixed Python"
# flags=re.IGNORECASE 讓 python/PYTHON/Python 都會被匹配
print(re.sub("python", matchcase("snake"), s, flags=re.IGNORECASE))
# 'UPPER SNAKE, lower snake, Mixed Snake'
