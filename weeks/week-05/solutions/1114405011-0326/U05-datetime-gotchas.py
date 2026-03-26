# U05. 日期時間的陷阱（Cookbook 第 3.12–3.15 節）
# 內容涵蓋：timedelta 不支援月份參數 / strptime 效能問題 / date 運算注意事項

import timeit
import calendar
from datetime import datetime, timedelta

# ── timedelta 不支援月份（3.12）──────────────────────
# timedelta 只支援天、秒、微秒等單位，不支援月份參數
# 原因：月份長度不一定（28-31 天），無法精確定義
dt = datetime(2012, 9, 23)
try:
    dt + timedelta(months=1)  # type: ignore[call-arg]
except TypeError as e:
    print(f"TypeError: {e}")  # 'months' is an invalid keyword argument


# 正確做法：用 calendar 取得目標月份天數，並將日期 clamp 到該月最後一天
# 例如：1月31日 + 1個月 = 2月29日（閏年）或 2月28日（平年）
def add_one_month(dt: datetime) -> datetime:
    """
    為日期加上1個月，並自動處理月份長度差異
    例如：1月31日 + 1個月 = 2月29日（閏年）或 2月28日（平年）
    """
    # 計算目標的年與月
    year = dt.year
    month = dt.month + 1
    if month == 13:  # 超過12月，進到下一年
        year += 1
        month = 1

    # 取得目標月份的天數，並把日期限制在該月最後一天
    _, days_in_target_month = calendar.monthrange(year, month)
    day = min(dt.day, days_in_target_month)  # 確保日期不超過該月最後一天

    return dt.replace(year=year, month=month, day=day)


print(add_one_month(datetime(2012, 1, 31)))  # 2012-02-29（閏年，自動調整）
print(add_one_month(datetime(2012, 9, 23)))  # 2012-10-23

# ── strptime 效能問題（3.15）─────────────────────────
# datetime.strptime() 要處理很多預設值和標準，因此較慢
# 如果日期格式固定（如 YYYY-MM-DD），手動解析快 7 倍以上

dates = [f"2012-{m:02d}-{d:02d}" for m in range(1, 13) for d in range(1, 29)]


def use_strptime(s: str) -> datetime:
    """使用標準的 strptime 解析"""
    return datetime.strptime(s, "%Y-%m-%d")


def use_manual(s: str) -> datetime:
    """手動解析（對於固定格式很快）"""
    y, m, d = s.split("-")
    return datetime(int(y), int(m), int(d))


assert use_strptime("2012-09-20") == use_manual("2012-09-20")

t1 = timeit.timeit(lambda: [use_strptime(d) for d in dates], number=100)
t2 = timeit.timeit(lambda: [use_manual(d) for d in dates], number=100)
print(f"strptime: {t1:.3f}s  手動解析: {t2:.3f}s（快 {t1 / t2:.1f} 倍）")
