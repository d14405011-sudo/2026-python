# 8 容器操作與推導式範例
# 這支程式示範：
# 1) List Comprehension（清單推導式）
# 2) Dict Comprehension（字典推導式）
# 3) Generator Expression（生成器表達式）


def demo_list_comprehension():
	nums = [1, -2, 3, -4]

	# 只保留大於 0 的元素
	positives = [n for n in nums if n > 0]

	print("[List 推導式] 原始 nums:", nums)
	print("[List 推導式] 正數 positives:", positives)


def demo_dict_comprehension():
	pairs = [("a", 1), ("b", 2), ("c", 3)]

	# 把 (key, value) 配對轉成字典
	lookup = {k: v for k, v in pairs}

	print("[Dict 推導式] 原始 pairs:", pairs)
	print("[Dict 推導式] 轉換後 lookup:", lookup)


def demo_generator_expression():
	nums = [1, -2, 3, -4]

	# 生成器不會一次建立完整清單，會在需要時計算
	squares_sum = sum(n * n for n in nums)

	print("[Generator] nums 平方和:", squares_sum)


def main():
	print("=== 容器操作與推導式範例 ===")
	demo_list_comprehension()
	demo_dict_comprehension()
	demo_generator_expression()


if __name__ == "__main__":
	main()
