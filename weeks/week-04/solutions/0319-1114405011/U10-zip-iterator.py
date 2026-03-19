# U10. zip 為何只能用一次（1.8）
#
# zip 返回一個迭代器（iterator），不是列表
# 迭代器被消耗後就無法重複使用
# 若需重複使用，應先轉成列表

def main() -> None:
    # ==============================================================
    # 1) zip 返回迭代器，不是列表
    # ==============================================================
    print('1) zip 返回迭代器，不是列表:')

    prices = {'A': 2.0, 'B': 1.0}
    z = zip(prices.values(), prices.keys())

    print(f'   prices = {prices}')
    print(f'   z = zip(prices.values(), prices.keys())')
    print(f'   type(z) = {type(z)}')
    print(f'   list(z) = 會耗盡迭代器')

    print()

    # ==============================================================
    # 2) 迭代器的一次性特性
    # ==============================================================
    print('2) 迭代器的一次性特性:')

    z = zip(prices.values(), prices.keys())
    print(f'   z = zip(prices.values(), prices.keys())')

    result1 = min(z)
    print(f'   min(z) = {result1}  ✓ 成功')

    print(f'   嘗試 max(z)...')
    try:
        result2 = max(z)
        print(f'   max(z) = {result2}')
    except ValueError as e:
        print(f'   ✗ ValueError: {e}')
        print(f'   原因：迭代器已被 min() 消耗完')

    print()

    # ==============================================================
    # 3) 演示真正的消耗
    # ==============================================================
    print('3) 演示真正的消耗:')

    z = zip([1, 2, 3], ['a', 'b', 'c'])
    print(f'   z = zip([1, 2, 3], [\'a\', \'b\', \'c\'])')

    # 第一次消耗
    print(f'   第一次迭代: list(z) = {list(z)}')

    # 再次消耗（已被耗盡）
    print(f'   第二次迭代: list(z) = {list(z)}  ✗ 空了！')

    print()

    # ==============================================================
    # 4) 解決方案：轉成列表
    # ==============================================================
    print('4) 解決方案：轉成列表')

    prices = {'A': 2.0, 'B': 1.0, 'C': 3.5}
    z = list(zip(prices.values(), prices.keys()))

    print(f'   z = list(zip(prices.values(), prices.keys()))')
    print(f'   type(z) = {type(z)}')
    print(f'   z = {z}')

    print()

    min_val = min(z)
    max_val = max(z)

    print(f'   min(z) = {min_val}  ✓ 成功')
    print(f'   max(z) = {max_val}  ✓ 成功')
    print(f'   list(z) = {z}  ✓ 仍可訪問')

    print()

    # ==============================================================
    # 5) 迭代器 vs 列表的記憶體差異
    # ==============================================================
    print('5) 迭代器 vs 列表的記憶體差異:')

    import sys

    # 大資料集
    large_list1 = range(1000000)
    large_list2 = range(1000000)

    z_iter = zip(large_list1, large_list2)
    z_list = list(zip(large_list1, large_list2))

    print(f'   100 萬元素 zip 物件:')
    print(f'     迭代器大小: {sys.getsizeof(z_iter)} bytes')
    print(f'     列表大小: {sys.getsizeof(z_list) // 1024 // 1024} MB')
    print(f'   迭代器節省大量記憶體，代價是只能用一次')

    print()

    # ==============================================================
    # 6) 實務應用：何時用迭代器 vs 列表
    # ==============================================================
    print('6) 實務應用：何時用迭代器 vs 列表:')

    print(f'   使用迭代器 (zip(...)):')
    print(f'     ✓ 資料量大，記憶體緊張')
    print(f'     ✓ 只需要遍歷一次')
    print(f'     ✗ 需要重複使用')

    print()
    print(f'   使用列表 (list(zip(...))):')
    print(f'     ✓ 需要多次訪問或對元素進行聚合操作')
    print(f'     ✓ 資料量合理，記憶體充足')
    print(f'     ✗ 大資料量場景')

    print()

    # ==============================================================
    # 7) 其他迭代器的一次性特性
    # ==============================================================
    print('7) 其他迭代器的一次性特性:')

    from itertools import count, cycle

    # count() 是無限迭代器
    counter = count(1)
    print(f'   count(1) 的前 3 個值: {[next(counter) for _ in range(3)]}')
    print(f'   再取 3 個值: {[next(counter) for _ in range(3)]}')
    print(f'   (計數器持續遞增，不會重置)')

    print()

    # filter 也是迭代器
    evens = filter(lambda x: x % 2 == 0, range(10))
    print(f'   filter(...) 第一次: {list(evens)}')
    print(f'   filter(...) 第二次: {list(evens)}  ✗ 空了')


if __name__ == '__main__':
    main()
