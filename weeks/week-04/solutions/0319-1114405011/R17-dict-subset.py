# R17. 字典子集（1.17）

def main() -> None:
	# 原始字典：key 為股票代號，value 為股價
	prices = {
		'ACME': 45.23,
		'AAPL': 612.78,
		'IBM': 205.55,
		'HPQ': 37.20,
		'FB': 10.75,
		'YHOO': 16.35,
	}

	print('原始字典 prices:')
	print(prices)

	# ------------------------------------------------------------
	# 1) 依 value 條件建立字典子集
	# ------------------------------------------------------------
	# 語法重點：字典推導式 {k: v for k, v in prices.items() if 條件}
	# 這裡保留「股價大於 200」的項目。
	expensive_stocks = {k: v for k, v in prices.items() if v > 200}

	print('\n1) 價格大於 200 的股票:')
	print(expensive_stocks)

	# ------------------------------------------------------------
	# 2) 依 key 條件建立字典子集
	# ------------------------------------------------------------
	# 用 set 儲存欲保留的股票代號，
	# 成員測試（k in tech_names）時間複雜度平均為 O(1)，效率佳。
	tech_names = {'AAPL', 'IBM', 'MSFT'}
	tech_stocks = {k: v for k, v in prices.items() if k in tech_names}

	print('\n2) 只保留指定代號（tech_names）中的股票:')
	print(f'tech_names = {tech_names}')
	print(tech_stocks)

	# ------------------------------------------------------------
	# 補充：直接對 keys 做集合運算，再組回字典
	# ------------------------------------------------------------
	# prices.keys() 與 tech_names 都可參與集合運算，
	# 交集 (&) 代表同時存在於兩者的 key。
	common_keys = prices.keys() & tech_names
	tech_stocks_v2 = {k: prices[k] for k in common_keys}

	print('\n補充寫法（先取 key 交集，再組字典）:')
	print(f'共同 key: {common_keys}')
	print(tech_stocks_v2)


if __name__ == '__main__':
	main()
