# 9 比較、排序與 key 函式範例


def main() -> None:
	"""示範比較運算、排序與 key 參數的基本用法。"""

	# 比較運算：tuple 會由左到右逐一比較
	# 先比第一個元素，若相同再比第二個元素
	a = (1, 2)
	b = (1, 3)
	result = a < b

	# 原始資料：每筆資料是字典，uid 代表識別值
	rows = [{"uid": 3}, {"uid": 1}, {"uid": 2}]

	# sorted 會回傳新串列，不會改變原始 rows
	# key 指定「用哪個欄位做排序依據」
	rows_sorted = sorted(rows, key=lambda r: r["uid"])

	# min/max 搭配 key：找出 uid 最小與最大的資料
	smallest = min(rows, key=lambda r: r["uid"])
	largest = max(rows, key=lambda r: r["uid"])

	# 輸出結果，方便觀察每個操作的差異
	print("a =", a)
	print("b =", b)
	print("a < b 的結果：", result)
	print("原始 rows：", rows)
	print("排序後 rows_sorted：", rows_sorted)
	print("uid 最小的資料：", smallest)
	print("uid 最大的資料：", largest)


if __name__ == "__main__":
	main()
