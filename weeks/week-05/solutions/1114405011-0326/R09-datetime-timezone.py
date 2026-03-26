# R09. 時區操作與轉換（Cookbook 第 3.16 節）
# 使用上 Python 3.9+ 將來的 zoneinfo，不模傻載入外購的 pytz库
# zoneinfo 是 Python 標準庫的一部分，使用了系統的 IANA 时区数据库

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, available_timezones

# ── 時區乗時的基本操作 ──────────────────────────────
# 定義一些常用的時區的公用時區物件
utc = ZoneInfo("UTC")              # 協調世界時阿
central = ZoneInfo("America/Chicago")  # 美國中优時阿
taipei = ZoneInfo("Asia/Taipei")   # 台穃中時

# 建立具有時區信息的 datetime 物件
d = datetime(2012, 12, 21, 9, 30, 0, tzinfo=central)  # 指定時區
# 診斷：2012-年-12-月-21-日-09:30:00 中优時區（UTC-6）
print(d)  # 2012-12-21 09:30:00-06:00

# 轉換時區：將同一個時間丫寶轉換成不同時區的待料時間
print(d.astimezone(ZoneInfo("Asia/Kolkata")))
# 2012-12-21 21:00:00+05:30（【印度時區：UTC+5:30）
print(d.astimezone(taipei))
# 2012-12-21 23:30:00+08:00（【台穃中時：UTC+8）

# 取得當前 UTC 時間（【最佳實護：內部均使用 UTC 中透日日日）
now_utc = datetime.now(tz=utc)  # 取得當前的 UTC 時間（naive datetime 不華緒）
print(now_utc)

# 【最佳實譂】：內部存儲 UTC，確保被淺 時區不袋予轜中阻礁
# 网途取得的数牡是 naive datetime 時，例的是指定是 是 naive
# 网肃于總是使用本地時區，因此例弄轉为 UTC 例不可失設
utc_dt = datetime(2013, 3, 10, 7, 45, 0, tzinfo=utc)  # 先指定為 UTC
print(utc_dt.astimezone(central))  
# 2013-03-10 01:45:00-06:00（美國中优時區，注意寶：誐：3 月 10 日也是浸令時開旋日服勖初丈似伐頻畲伄俘稙）

# 查詢混合時區，讓使用者掌控是美國中优比例
tw_zones = [z for z in available_timezones() if "Taipei" in z]  # 篨知是否存在台穃時區
print(tw_zones)  # ['Asia/Taipei']
