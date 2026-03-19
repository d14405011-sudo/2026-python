# U9. groupby 為何一定要先 sort（1.15）
#
# 核心概念：groupby 只分組「相鄰且鍵值相同」的元素
# 若資料未排序，相同鍵值會被拆成多個群組
# 解決方案：必須先依分組鍵排序，才能保證分組正確

from itertools import groupby
from operator import itemgetter


def main() -> None:
    # ==============================================================
    # 1) 問題演示：未排序的資料會被分成多段
    # ==============================================================
    print('1) 問題演示：未排序資料的錯誤分組')

    rows = [
        {'date': '07/02/2012', 'x': 1},
        {'date': '07/01/2012', 'x': 2},
        {'date': '07/02/2012', 'x': 3},
    ]

    print(f'   原始資料（未排序）:{rows}')
    print()
    print('   使用 groupby（不排序）:')

    for k, g in groupby(rows, key=itemgetter('date')):
        items = list(g)
        print(f'   日期 {k}: {items}  ({len(items)} 筆)')

    print()
    print('   ✗ 問題：07/02 被分成兩個群組（第 1 筆和第 3 筆）')
    print('   因為 groupby 只看「相鄰」的元素，第 2 筆打斷了連續性')

    print()

    # ==============================================================
    # 2) 解決方案：先排序再分組
    # ==============================================================
    print('2) 解決方案：先排序再分組')

    print(f'   原始資料:{rows}')
    
    # 排序後
    rows.sort(key=itemgetter('date'))
    print(f'   排序後:{rows}')

    print()
    print('   使用 groupby（排序後）:')

    for k, g in groupby(rows, key=itemgetter('date')):
        items = list(g)
        print(f'   日期 {k}: {items}  ({len(items)} 筆)')

    print(f'   ✓ 正確：同日期的集中在一起')

    print()

    # ==============================================================
    # 3) 為什麼 groupby 要求排序的原因
    # ==============================================================
    print('3) 為什麼 groupby 要求排序的原因:')
    print(f'   - groupby 是「串流式」處理，不重新排序資料')
    print(f'   - 只檢查「連續」的相同元素')
    print(f'   - 優勢：O(n) 時間、常數空間')
    print(f'   - 代價：必須預先排序')

    print()

    # ==============================================================
    # 4) 實務對比：groupby vs defaultdict
    # ==============================================================
    print('4) 實務對比：groupby vs defaultdict')

    from collections import defaultdict

    data = [
        {'dept': 'sales', 'name': 'Alice'},
        {'dept': 'eng', 'name': 'Bob'},
        {'dept': 'sales', 'name': 'Charlie'},
        {'dept': 'eng', 'name': 'David'},
    ]

    print(f'   資料:{data}')

    # 方法 1：使用 groupby（需排序）
    print()
    print('   方法 1：groupby（需先排序）')
    data_sorted = sorted(data, key=itemgetter('dept'))
    result1 = {}
    for k, g in groupby(data_sorted, key=itemgetter('dept')):
        result1[k] = [item['name'] for item in g]

    for dept, names in result1.items():
        print(f'     {dept}: {names}')

    # 方法 2：使用 defaultdict（不需排序）
    print()
    print('   方法 2：defaultdict（不需排序）')
    result2 = defaultdict(list)
    for item in data:
        result2[item['dept']].append(item['name'])

    for dept in sorted(result2.keys()):
        print(f'     {dept}: {result2[dept]}')

    print()

    # ==============================================================
    # 5) 何時用 groupby vs defaultdict
    # ==============================================================
    print('5) 何時用 groupby vs defaultdict:')
    print(f'   groupby:')
    print(f'     ✓ 資料已排序，想保持分組順序')
    print(f'     ✓ 適合一次性串流處理（記憶體效率高）')
    print(f'     ✗ 需要排序（O(n log n) 成本）')
    print()
    print(f'   defaultdict:')
    print(f'     ✓ 資料無序，分組後需整理')
    print(f'     ✓ 對大資料集合友善（不需預排序）')
    print(f'     ✗ 記憶體成本接近 dict')


if __name__ == '__main__':
    main()
