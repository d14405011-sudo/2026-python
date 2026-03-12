# R13. 字典列表排序 itemgetter（1.13）

from operator import itemgetter

rows = [{'fname': 'Brian', 'uid': 1003}, {'fname': 'John', 'uid': 1001}]

print("原始資料：", rows)
print("依 fname 排序：", sorted(rows, key=itemgetter('fname')))
print("依 uid 排序：", sorted(rows, key=itemgetter('uid')))
print("依 uid、fname 排序：", sorted(rows, key=itemgetter('uid', 'fname')))
