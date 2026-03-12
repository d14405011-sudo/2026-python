# R13. 字典列表排序 itemgetter（1.13）
# ------------------------------------------------------------
# itemgetter 可用來指定「字典欄位」當排序依據，
# 讓 key 函式寫法更簡潔。
# ------------------------------------------------------------

from operator import itemgetter

rows = [
	{'fname': 'Brian', 'uid': 1003},
	{'fname': 'John', 'uid': 1001},
	{'fname': 'David', 'uid': 1002},
	{'fname': 'John', 'uid': 1000},
]
print("原始 rows =", rows)

print("\n=== 依 fname 排序 ===")
rows_by_name = sorted(rows, key=itemgetter('fname'))
print("rows_by_name =", rows_by_name)

print("\n=== 依 uid 排序 ===")
rows_by_uid = sorted(rows, key=itemgetter('uid'))
print("rows_by_uid =", rows_by_uid)

print("\n=== 先 uid 再 fname（多鍵排序）===")
rows_by_uid_name = sorted(rows, key=itemgetter('uid', 'fname'))
print("rows_by_uid_name =", rows_by_uid_name)
