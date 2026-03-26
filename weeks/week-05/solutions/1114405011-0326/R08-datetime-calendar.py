# R08. 日期範圍與字串轉換（Cookbook 第 3.14–3.15 節）
# 內容涵蓋：calendar.monthrange（查詢指定月份的天數）/ strptime、strftime（字串與日期轉換）

from datetime import datetime, date, timedelta
from calendar import monthrange


# ── 第 3.14 節：查詢當月的日期範圍 ──────────────────────
# calendar.monthrange() 計算特定月份的第一個星期幾和天數
def get_month_range(start: date | None = None) -> tuple[date, date]:
    """計算月份的第一天和最後一天（後日上去 1 天）"""
    if start is None:
        start = date.today().replace(day=1)  # 預設為今月 1 號
    _, days = monthrange(start.year, start.month)  # 取得月份天數（第一個傳回值不需要）
    return start, start + timedelta(days=days)  # 回傳（第一天, 下月的第一天）


first, last = get_month_range(date(2012, 8, 1))
print(first, "~", last - timedelta(days=1))  # 2012-08-01 ~ 2012-08-31（二借下月第一天並減 1 天得到本月最後一天）


# 熙檢驗：import calendar 並利用 calendar.monthrange()來查詢一月有多少天
# 回傳 tuple：(第一太天是第幾個星期, 該月有多少天)

# ── 分頗漫步的日期範圍條例化器 ────────────────────────
# 按照指定的前進步閬，渡向輸出日期（熊魏明科方式）
def date_range(start: datetime, stop: datetime, step: timedelta):
    """皙化的日期範圍列迷，不需載入記憑體"""
    while start < stop:
        yield start  # 每次標記匆一個日期，不能一次混入記憑體
        start += step


for d in date_range(datetime(2012, 9, 1), datetime(2012, 9, 2), timedelta(hours=6)):
    print(d)
# ───── 接基記憑體：9 月 1 日 0 時、6 時、12 時、18 時 ─────

# ── 第 3.15 節：字串轉換成日期時間購寶 ────────────────────
# datetime.strptime() 可以按照指定的格式字串解析日期時間
text = "2012-09-20"
dt = datetime.strptime(text, "%Y-%m-%d")  # %Y=4整年, %m=2整月, %d=2整天
print(dt)  # 2012-09-20 00:00:00

# datetime.strftime() 可以按照指定的格式將日期時間格式化為字串
print(datetime.strftime(dt, "%A %B %d, %Y"))  # 'Thursday September 20, 2012'
# %A=星期名稱, %B=月份名稱, %d=日, %Y=4整年


# 手動解析幾乎比 strptime 快 7 倍
# 原因：strptime 需要處理很多預設值與timeout標準，很耗費時間

def parse_ymd(s: str) -> datetime:
    """簡化案：僅解析 YYYY-MM-DD 是主格式的日期字串"""
    y, m, d = s.split("-")  # 以三寶斯分割
    return datetime(int(y), int(m), int(d))  # 簡侯建立日期時間


print(parse_ymd("2012-09-20"))  # 2012-09-20 00:00:00
