# U05. 日期時間的陷阱（3.12–3.15）
#
# 這份範例要解決兩個非常常見的 datetime 問題：
# 1) timedelta 不支援「月」這種可變長度單位。
# 2) datetime.strptime() 在大量資料解析時可能成為效能瓶頸。

import timeit
import calendar
from datetime import datetime, timedelta

# ── timedelta 不支援月份（3.12）──────────────────────
# 因為每個月天數不同（28/29/30/31），
# datetime 無法定義一個固定的「1 month」秒數。
dt = datetime(2012, 9, 23)
try:
    dt + timedelta(months=1)  # type: ignore[call-arg]
except TypeError as e:
    print(f"TypeError: {e}")  # 'months' is an invalid keyword argument


# 正確做法：
# - 先計算目標年月。
# - 再查該月最大天數。
# - 若原日超過該月最大天數，就 clamp 到月底。
#
# 例如 1/31 + 1 個月 -> 2/29（閏年）或 2/28（平年）。
def add_one_month(dt: datetime) -> datetime:
    # 計算目標的年與月
    year = dt.year
    month = dt.month + 1
    if month == 13:
        year += 1
        month = 1

    # 取得目標月份的天數，並把日期限制在該月最後一天
    _, days_in_target_month = calendar.monthrange(year, month)
    day = min(dt.day, days_in_target_month)

    return dt.replace(year=year, month=month, day=day)


print(add_one_month(datetime(2012, 1, 31)))  # 2012-02-29
print(add_one_month(datetime(2012, 9, 23)))  # 2012-10-23

# ── strptime 效能問題（3.15）─────────────────────────
# strptime 的格式解析很方便，但反覆呼叫時成本較高。
# 若輸入格式固定且簡單（例如 YYYY-MM-DD），手動 split 往往更快。
dates = [f"2012-{m:02d}-{d:02d}" for m in range(1, 13) for d in range(1, 29)]


def use_strptime(s: str) -> datetime:
    # 可讀性高、維護簡單，但效能較慢
    return datetime.strptime(s, "%Y-%m-%d")


def use_manual(s: str) -> datetime:
    # 對固定格式字串，手動拆解通常更快
    y, m, d = s.split("-")
    return datetime(int(y), int(m), int(d))


assert use_strptime("2012-09-20") == use_manual("2012-09-20")

t1 = timeit.timeit(lambda: [use_strptime(d) for d in dates], number=100)
t2 = timeit.timeit(lambda: [use_manual(d) for d in dates], number=100)
print(f"strptime: {t1:.3f}s  手動解析: {t2:.3f}s（快 {t1 / t2:.1f} 倍）")
