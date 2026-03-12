# R13. 字典列表排序 itemgetter（1.13）

from operator import itemgetter

# rows 是「字典組成的列表」。
rows = [{'fname': 'Brian', 'uid': 1003}, {'fname': 'John', 'uid': 1001}]

print("原始資料：", rows)
# itemgetter('fname') 表示以字典的 fname 欄位當排序鍵。
print("依 fname 排序：", sorted(rows, key=itemgetter('fname')))
# 依 uid 欄位排序。
print("依 uid 排序：", sorted(rows, key=itemgetter('uid')))
# 多欄位排序：先看 uid，再看 fname。
print("依 uid、fname 排序：", sorted(rows, key=itemgetter('uid', 'fname')))
