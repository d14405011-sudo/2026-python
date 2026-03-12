# 8 容器操作與推導式範例


def main() -> None:
	"""示範串列推導式、字典推導式與生成器表達式。"""

	# 原始數列：包含正數與負數
	nums = [1, -2, 3, -4]

	# 串列推導式：只保留大於 0 的數字
	positives = [n for n in nums if n > 0]

	# 鍵值配對資料（通常可視為小型表格或查詢來源）
	pairs = [("a", 1), ("b", 2)]

	# 字典推導式：把配對清單轉成字典，方便用 key 查值
	lookup = {k: v for k, v in pairs}

	# 生成器表達式：逐一產生平方值，直接交給 sum 計算總和
	# 優點是不用先建立完整中間串列，較省記憶體
	squares_sum = sum(n * n for n in nums)

	# 輸出結果，方便觀察每個步驟的處理成果
	print("原始數列：", nums)
	print("正數清單（串列推導式）：", positives)
	print("配對轉字典（字典推導式）：", lookup)
	print("平方和（生成器表達式）：", squares_sum)


if __name__ == "__main__":
	main()
