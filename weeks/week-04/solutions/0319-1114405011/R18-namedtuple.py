# R18. namedtuple（1.18）

from collections import namedtuple


def main() -> None:
    # ==============================================================
    # 1) namedtuple 的基本用法
    # ==============================================================
    # namedtuple 是 tuple 的子類，提供具名欄位訪問。
    # 優勢：
    # - 比 dict 記憶體效率高
    # - 比普通 tuple 更可讀（可用屬性名而非索引)
    # - 不可變（immutable），適合作為函式返回值或字典 key

    Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
    sub = Subscriber('jonesy@example.com', '2012-10-19')

    print('1) namedtuple 基本用法 - Subscriber:')
    print(f'   sub = {sub}')
    print(f'   sub.addr = {sub.addr}')
    print(f'   sub.joined = {sub.joined}')
    print(f'   type(sub) = {type(sub)}')
    print(f'   isinstance(sub, tuple) = {isinstance(sub, tuple)}')

    # ==============================================================
    # 2) 多欄位 namedtuple 與屬性訪問
    # ==============================================================
    Stock = namedtuple('Stock', ['name', 'shares', 'price'])
    s = Stock('ACME', 100, 123.45)

    print('\n2) 多欄位 namedtuple - Stock:')
    print(f'   s = {s}')
    print(f'   s.name = {s.name}')
    print(f'   s.shares = {s.shares}')
    print(f'   s.price = {s.price}')
    print(f'   s[0] = {s[0]}  (也可用索引訪問)')

    # ==============================================================
    # 3) 修改欄位：使用 _replace() 方法
    # ==============================================================
    # 由於 namedtuple 是不可變的，無法直接修改欄位。
    # 使用 _replace() 會產生一個新的 namedtuple 物件（舊的不變）。
    s_modified = s._replace(shares=75)

    print('\n3) 使用 _replace() 更新欄位:')
    print(f'   原本: s = {s}')
    print(f'   修改: s_modified = s._replace(shares=75)')
    print(f'   結果: s_modified = {s_modified}')
    print(f'   原本 s 不變: s = {s}')

    # ==============================================================
    # 4) namedtuple 與普通 tuple 的比較
    # ==============================================================
    # 普通 tuple（低可讀性）
    regular_tuple = ('GOOG', 50, 490.10)
    # 要取 price 得用索引：regular_tuple[2]

    # namedtuple（高可讀性）
    StockNT = namedtuple('Stock', ['name', 'shares', 'price'])
    nt_tuple = StockNT('GOOG', 50, 490.10)
    # 可用屬性名：nt_tuple.price

    print('\n4) 普通 tuple vs namedtuple:')
    print(f'   普通 tuple: {regular_tuple}')
    print(f'     取值: regular_tuple[2] = {regular_tuple[2]}  (低可讀)')
    print(f'   namedtuple: {nt_tuple}')
    print(f'     取值: nt_tuple.price = {nt_tuple.price}  (高可讀)')

    # ==============================================================
    # 5) namedtuple 的實用方法
    # ==============================================================
    Person = namedtuple('Person', ['name', 'age', 'email'])
    person = Person('Alice', 30, 'alice@example.com')

    print('\n5) namedtuple 的實用方法:')
    print(f'   person = {person}')
    print(f'   person._fields = {person._fields}')
    print(f'   person._asdict() = {person._asdict()}')
    print(f'   person._make([\'Bob\', 25, \'bob@example.com\']) =')
    print(f'     {Person._make(["Bob", 25, "bob@example.com"])}')


if __name__ == '__main__':
    main()
