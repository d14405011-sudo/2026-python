# U8. 字典最值為何常用 zip(values, keys)（1.8）
#
# 問題：在字典中找最小/最大值時常想同時獲得 key 和 value
# 直接用 min(prices.values()) 只能得到值，不知道對應的 key
# 解決方案：使用 zip(values, keys) 將兩者配對，一次獲得兩者

def main() -> None:
    # ==============================================================
    # 1) 直接用 min/max on dict 的問題
    # ==============================================================
    print('1) 直接用 min/max on dict 的問題:')

    prices = {'A': 2.0, 'B': 1.0, 'C': 3.5}
    print(f'   prices = {prices}')

    print(f'   min(prices) = {min(prices)}  (比較 keys，不是 values!)')
    print(f'   max(prices) = {max(prices)}')

    print()

    # ==============================================================
    # 2) min/max on values 只能得到值，不知道 key
    # ==============================================================
    print('2) min/max on values 只能得到值，不知道 key:')

    min_value = min(prices.values())
    max_value = max(prices.values())

    print(f'   min(prices.values()) = {min_value}')
    print(f'   max(prices.values()) = {max_value}')
    print(f'   ✗ 不知道 {min_value} 對應哪個 key')

    print()

    # ==============================================================
    # 3) 使用 zip(values, keys) 一次拿到兩者
    # ==============================================================
    print('3) 使用 zip(values, keys) 一次拿到兩者:')

    # 將 values 和 keys 配對成 (value, key) 的 tuple
    pairs = list(zip(prices.values(), prices.keys()))
    print(f'   list(zip(prices.values(), prices.keys())) = {pairs}')

    min_pair = min(pairs)
    max_pair = max(pairs)

    print(f'   min(...) = {min_pair}  (最小 value = {min_pair[0]}, key = {min_pair[1]})')
    print(f'   max(...) = {max_pair}  (最大 value = {max_pair[0]}, key = {max_pair[1]})')

    print()

    # ==============================================================
    # 4) 一行寫法（習慣用法）
    # ==============================================================
    print('4) 一行寫法（習慣用法）:')

    min_value, min_key = min(zip(prices.values(), prices.keys()))
    max_value, max_key = max(zip(prices.values(), prices.keys()))

    print(f'   min_value, min_key = min(zip(prices.values(), prices.keys()))')
    print(f'   -> min_value={min_value}, min_key={min_key}')
    print()
    print(f'   max_value, max_key = max(zip(prices.values(), prices.keys()))')
    print(f'   -> max_value={max_value}, max_key={max_key}')

    print()

    # ==============================================================
    # 5) 與 dict.items() 的對比
    # ==============================================================
    print('5) 與 dict.items() 的對比:')

    print(f'   使用 min(prices.items(), key=lambda x: x[1]):')
    min_item = min(prices.items(), key=lambda x: x[1])
    print(f'   -> {min_item}')

    print()
    print(f'   使用 min(zip(prices.values(), prices.keys())):')
    min_zip = min(zip(prices.values(), prices.keys()))
    print(f'   -> {min_zip}  (注意順序是 (value, key))')

    print()

    # ==============================================================
    # 6) 為什麼 zip 方式有優勢
    # ==============================================================
    print('6) 為什麼 zip 方式有優勢:')
    print(f'   ✓ min/max 會自動按第一個元素比較')
    print(f'   ✓ 不需要提供 key 函式，簡潔明快')
    print(f'   ✓ 對多層比較（先比 value，再比 key）友善')

    print()

    # ==============================================================
    # 7) 實務應用：找股票最低和最高價格
    # ==============================================================
    print('7) 實務應用：找股票最低和最高價格')

    stocks = {'AAPL': 150.25, 'MSFT': 300.45, 'GOOGL': 2800.15, 'AMZN': 3200.00}
    print(f'   stocks = {stocks}')

    cheapest_price, cheapest_ticker = min(zip(stocks.values(), stocks.keys()))
    most_expensive_price, most_expensive_ticker = max(zip(stocks.values(), stocks.keys()))

    print(f'   最便宜: {cheapest_ticker} = ${cheapest_price}')
    print(f'   最昂貴: {most_expensive_ticker} = ${most_expensive_price}')

    print()

    # ==============================================================
    # 8) 進階應用：依序排列
    # ==============================================================
    print('8) 進階應用：依序排列所有股票價格')

    sorted_stocks = sorted(zip(stocks.values(), stocks.keys()))
    print(f'   sorted(zip(stocks.values(), stocks.keys())):')
    for price, ticker in sorted_stocks:
        print(f'     ${price:8.2f} - {ticker}')


if __name__ == '__main__':
    main()
