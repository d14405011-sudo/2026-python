# R09. 時區操作與轉換（Cookbook 第 3.16 節）
# 在 Python 3.9+ 中建議使用標準庫的 zoneinfo，不再另外載入外部的 pytz 套件
# zoneinfo 是 Python 標準庫的一部分，使用的是系統的 IANA 時區資料庫

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, available_timezones

# ── 時區相關的基本操作 ──────────────────────────────
# 定義一些常用的時區物件，方便重複使用
utc = ZoneInfo("UTC")              # 協調世界時（UTC）
central = ZoneInfo("America/Chicago")  # 美國中部時間（Central Time）
taipei = ZoneInfo("Asia/Taipei")   # 台北時間（Asia/Taipei）

# 建立具有時區資訊的 datetime 物件
d = datetime(2012, 12, 21, 9, 30, 0, tzinfo=central)  # 指定時區為美國中部時間
# 範例時間：2012-12-21 09:30:00 中部時間（UTC-6）
print(d)  # 2012-12-21 09:30:00-06:00

# 轉換時區：將同一個實際時刻轉換成不同時區的當地時間
print(d.astimezone(ZoneInfo("Asia/Kolkata")))
# 2012-12-21 21:00:00+05:30（印度標準時間：UTC+5:30）
print(d.astimezone(taipei))
# 2012-12-21 23:30:00+08:00（台北時間：UTC+8）

# 取得當前 UTC 時間（最佳實務：內部時間一律使用 UTC 儲存與運算）
now_utc = datetime.now(tz=utc)  # 取得當前的 UTC 時間（避免使用沒有時區的 naive datetime）
print(now_utc)

# 最佳實務：內部儲存 UTC，僅在輸入/輸出時做時區轉換
# 若從網路或資料庫取得的是 naive datetime，需要先確認它代表的是哪個時區
# 若代表本地時間，應先加上正確時區再轉為 UTC，避免時區與夏令時間出錯
utc_dt = datetime(2013, 3, 10, 7, 45, 0, tzinfo=utc)  # 先指定為 UTC
print(utc_dt.astimezone(central))  
# 2013-03-10 01:45:00-06:00（美國中部時間；注意 3 月 10 日是夏令時間切換日）

# 查詢與台北相關的時區名稱，確認系統中是否存在 Asia/Taipei
tw_zones = [z for z in available_timezones() if "Taipei" in z]  # 確認是否存在台北時區
print(tw_zones)  # ['Asia/Taipei']
