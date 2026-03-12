# R8. 字典運算：min/max/sorted + zip（1.8）

prices = {'ACME': 45.23, 'AAPL': 612.78, 'FB': 10.75}

print("原始價格字典：", prices)
print("最低價格（value, key）：", min(zip(prices.values(), prices.keys())))
print("最高價格（value, key）：", max(zip(prices.values(), prices.keys())))
print("依價格排序（value, key）：", sorted(zip(prices.values(), prices.keys())))

print("價格最低的股票代號：", min(prices, key=lambda k: prices[k]))
