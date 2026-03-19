# R19. 轉換+聚合：生成器表達式（1.19）


def main() -> None:
    # ==============================================================
    # 生成器表達式要點
    # ==============================================================
    # 生成器表達式類似列表推導式，但用 () 而非 []。
    # 優勢：
    # - 惰性計算：只在需要時才產生值
    # - 記憶體效率高：不會一次將所有結果存進記憶體
    # - 適合搭配聚合函式（sum、min、max、any、all 等）

    # ==============================================================
    # 1) 簡單聚合：sum() 搭配生成器表達式
    # ==============================================================
    nums = [1, 2, 3, 4, 5]
    squares_sum = sum(x * x for x in nums)

    print('1) sum() 搭配生成器表達式:')
    print(f'   nums = {nums}')
    print(f'   sum(x * x for x in nums) = {squares_sum}')
    print(f'   (即 1^2 + 2^2 + 3^2 + 4^2 + 5^2 = {squares_sum})')

    # ==============================================================
    # 2) 字串拼接：join() 搭配生成器表達式
    # ==============================================================
    s = ('ACME', 50, 123.45)
    joined = ','.join(str(x) for x in s)

    print('\n2) join() 搭配生成器表達式:')
    print(f'   s = {s}')
    print(f'   \',\'.join(str(x) for x in s) = {joined}')
    print(f'   (所有元素轉字串並用逗號拼接)')

    # ==============================================================
    # 3) 集合操作：any() 和 all() 搭配生成器表達式
    # ==============================================================
    nums_mixed = [2, 4, 6, 8, 10]
    nums_mixed_odd = [2, 3, 4, 5, 6]

    has_even = any(x % 2 == 0 for x in nums_mixed_odd)
    all_even = all(x % 2 == 0 for x in nums_mixed)

    print('\n3) any() 和 all() 搭配生成器表達式:')
    print(f'   nums_mixed_odd = {nums_mixed_odd}')
    print(f'   any(x % 2 == 0 for x in nums_mixed_odd) = {has_even}')
    print(f'   (是否至少有一個偶數？{has_even})')
    print()
    print(f'   nums_mixed = {nums_mixed}')
    print(f'   all(x % 2 == 0 for x in nums_mixed) = {all_even}')
    print(f'   (是否全是偶數？{all_even})')

    # ==============================================================
    # 4) max/min：尋找最大/最小值
    # ==============================================================
    portfolio = [
        {'name': 'AOL', 'shares': 20},
        {'name': 'YHOO', 'shares': 75},
        {'name': 'ACME', 'shares': 45},
    ]

    min_shares = min(s['shares'] for s in portfolio)
    max_shares = max(s['shares'] for s in portfolio)

    print('\n4) min/max 搭配生成器表達式:')
    print(f'   portfolio = {portfolio}')
    print(f'   min(s[\'shares\'] for s in portfolio) = {min_shares}')
    print(f'   max(s[\'shares\'] for s in portfolio) = {max_shares}')

    # ==============================================================
    # 5) min/max 搭配 key 參數：取整個物件
    # ==============================================================
    # 若想得到「擁有最少股份的整個字典」，用 key 參數指定比較規則
    item_min_shares = min(portfolio, key=lambda s: s['shares'])
    item_max_shares = max(portfolio, key=lambda s: s['shares'])

    print('\n5) min/max 搭配 key 參數（取整個資料項而非單一欄位）:')
    print(f'   min(portfolio, key=lambda s: s[\'shares\']) =')
    print(f'     {item_min_shares}')
    print(f'   max(portfolio, key=lambda s: s[\'shares\']) =')
    print(f'     {item_max_shares}')

    # ==============================================================
    # 6) 生成器表達式 vs 列表推導式
    # ==============================================================
    # 列表推導式：一次生成完整清單，佔用記憶體
    list_comp = [x * x for x in range(5)]

    # 生成器表達式：需要時才產生，省記憶體
    gen_expr = (x * x for x in range(5))

    print('\n6) 生成器表達式 vs 列表推導式:')
    print(f'   list_comp = [x * x for x in range(5)] = {list_comp}')
    print(f'   gen_expr = (x * x for x in range(5))')
    print(f'   type(list_comp) = {type(list_comp)}')
    print(f'   type(gen_expr) = {type(gen_expr)}')
    print(f'   list(gen_expr) = {list(gen_expr)}')
    print(f'   (生成器走訪一次後會被消耗)')

    # 再次嘗試會得到空列表
    print(f'   list(gen_expr) 再次呼叫 = {list(gen_expr)}')

    # ==============================================================
    # 7) 複雜轉換+聚合示範
    # ==============================================================
    # 計算投資組合的總價值（share * price）
    data = [
        {'name': 'ACME', 'shares': 100, 'price': 23.50},
        {'name': 'IBM', 'shares': 50, 'price': 71.80},
        {'name': 'CAT', 'shares': 150, 'price': 40.25},
    ]

    total_value = sum(d['shares'] * d['price'] for d in data)

    print('\n7) 複雜轉換+聚合：計算投資組合總價值')
    print(f'   data = {data}')
    print(f'   total_value = sum(d[\'shares\'] * d[\'price\'] for d in data)')
    print(f'   結果: {total_value:.2f}')


if __name__ == '__main__':
    main()
