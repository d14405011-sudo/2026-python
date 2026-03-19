# U7. OrderedDict 的取捨：保序但更吃記憶體（1.7）
#
# 背景：Python 3.7 之前，普通 dict 不保證插入順序
# OrderedDict 提供有序保證，但代價是多佔記憶體（額外的雙向鏈表指標）
# Python 3.7+ 後：普通 dict 已保留插入順序，OrderedDict 多數情況下非必要
#
# OrderedDict 現在主要用於：
# - 相等性比較考慮順序（dict 不考慮順序）
# - 提供 move_to_end() 等順序操作
# - 向下相容舊程式碼

from collections import OrderedDict


def main() -> None:
    # ==============================================================
    # 1) 歷史背景：Python 3.7 前後的差別
    # ==============================================================
    print('1) 歷史背景與現況:')
    print(f'   Python 3.7+ 後，普通 dict 已保留插入順序')
    print(f'   OrderedDict 主要用途已大幅減少')

    print()

    # ==============================================================
    # 2) 普通 dict 保留插入順序
    # ==============================================================
    print('2) 普通 dict 保留插入順序:')

    d = {}
    d['foo'] = 1
    d['bar'] = 2
    d['baz'] = 3

    print(f'   d = {d}')
    print(f'   list(d.keys()) = {list(d.keys())}  (維持插入順序)')

    print()

    # ==============================================================
    # 3) OrderedDict 的基本用法
    # ==============================================================
    print('3) OrderedDict 的基本用法:')

    od = OrderedDict()
    od['foo'] = 1
    od['bar'] = 2
    od['baz'] = 3

    print(f'   od = OrderedDict()')
    print(f'   od[\'foo\'] = 1, od[\'bar\'] = 2, od[\'baz\'] = 3')
    print(f'   list(od.keys()) = {list(od.keys())}  (維持插入順序)')
    print(f'   結果與普通 dict 相同，但內部多佔空間')

    print()

    # ==============================================================
    # 4) 記憶體差異：OrderedDict 內部使用雙向鏈表
    # ==============================================================
    print('4) 記憶體差異說明:')
    print(f'   普通 dict：hash 表 + 動態陣列')
    print(f'   OrderedDict：hash 表 + 雙向鏈表（每個 node 存前後指標）')
    print(f'   OrderedDict 多佔 ~40% 記憶體（取決於內容）')

    import sys
    d = {i: i for i in range(100)}
    od = OrderedDict(d)

    print(f'   範例 (100 個元素):')
    print(f'     dict 大小: {sys.getsizeof(d)} bytes')
    print(f'     OrderedDict 大小: {sys.getsizeof(od)} bytes')

    print()

    # ==============================================================
    # 5) dict vs OrderedDict 的相等性比較
    # ==============================================================
    print('5) 相等性比較：考慮 vs 忽視順序:')

    d1 = {'a': 1, 'b': 2, 'c': 3}
    d2 = {'c': 3, 'a': 1, 'b': 2}

    od1 = OrderedDict({'a': 1, 'b': 2, 'c': 3})
    od2 = OrderedDict({'c': 3, 'a': 1, 'b': 2})

    print(f'   d1 = {d1}')
    print(f'   d2 = {d2}  (元素相同，插入順序不同)')
    print(f'   d1 == d2? {d1 == d2}  (dict 只比較內容，忽視順序)')

    print()
    print(f'   od1 = OrderedDict(d1)')
    print(f'   od2 = OrderedDict(d2)')
    print(f'   od1 == od2? {od1 == od2}  (OrderedDict 考慮順序)')

    print()

    # ==============================================================
    # 6) OrderedDict 特有方法：move_to_end()
    # ==============================================================
    print('6) OrderedDict 特有方法：move_to_end():')

    od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
    print(f'   od = OrderedDict([(\'a\', 1), (\'b\', 2), (\'c\', 3)])')
    print(f'   初始: {list(od.keys())}')

    od.move_to_end('a')
    print(f'   od.move_to_end(\'a\')  -> {list(od.keys())}')

    od.move_to_end('b', last=False)  # 移到最前
    print(f'   od.move_to_end(\'b\', last=False)  -> {list(od.keys())}')

    print()

    # ==============================================================
    # 7) 實務應用：何時使用 OrderedDict
    # ==============================================================
    print('7) 何時使用 OrderedDict:')
    print(f'   ✓ 需要順序敏感的相等性比較')
    print(f'   ✓ 需要 move_to_end() 等操作')
    print(f'   ✓ 需要向下相容 Python 3.6 之前的版本')
    print(f'   ✗ Python 3.7+，單純保留順序 -> 用普通 dict')
    print(f'   ✗ 對記憶體敏感的大規模應用')

    print()

    # ==============================================================
    # 8) 實務應用：LRU 快取模擬
    # ==============================================================
    print('8) 實務應用：使用 move_to_end() 實現 LRU 快取')

    class SimpleLRUCache:
        def __init__(self, max_size=3):
            self.cache = OrderedDict()
            self.max_size = max_size

        def get(self, key):
            if key in self.cache:
                self.cache.move_to_end(key)  # 最近訪問的移到最後
                return self.cache[key]
            return None

        def put(self, key, value):
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)  # 移除最舊的（最前）

    lru = SimpleLRUCache(max_size=3)
    for i in range(5):
        lru.put(f'key{i}', f'value{i}')
        print(f'   put(key{i}, value{i}) -> cache: {list(lru.cache.keys())}')


if __name__ == '__main__':
    main()
