# U06. 時區操作最佳實踐：UTC 優先（3.16）
#
# 核心原則：
# - 內部儲存與運算盡量用 UTC。
# - 只有在輸入/輸出邊界才轉回使用者時區。
#
# 理由：本地時間會受到夏令時間（DST）影響，
# 可能出現「不存在的時間」或「重複的時間」，直接相加減容易出錯。

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

utc = ZoneInfo("UTC")
central = ZoneInfo("America/Chicago")

# 問題示範：直接在本地時間加減，可能跨到 DST 邊界。
# 美國 2013-03-10 凌晨 2:00 會直接跳到 3:00（2:xx 不存在）。
local_dt = datetime(2013, 3, 10, 1, 45, tzinfo=central)
wrong = local_dt + timedelta(minutes=30)
print(f"錯誤結果：{wrong}")  # 2:15（不存在的時間！）

# 正確做法：
# 1) 先轉 UTC
# 2) 在 UTC 做運算
# 3) 顯示時再轉回本地
utc_dt = local_dt.astimezone(utc)
correct = utc_dt + timedelta(minutes=30)
print(f"正確結果：{correct.astimezone(central)}")  # 3:15（跳過了 2:xx）

# 完整流程範例：輸入（本地）-> 轉 UTC 儲存/計算 -> 轉目標時區顯示
user_input = "2012-12-21 09:30:00"
naive = datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")
aware = naive.replace(tzinfo=central).astimezone(utc)
print(f"存 UTC：{aware}")
print(f"顯示台北：{aware.astimezone(ZoneInfo('Asia/Taipei'))}")
