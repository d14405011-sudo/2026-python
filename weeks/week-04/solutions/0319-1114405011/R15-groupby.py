# R15. 分組 groupby（1.15）

# groupby 來自 itertools：可將「連續且鍵值相同」的資料分在同一組
from itertools import groupby
# itemgetter('date') 會回傳一個函式，用來快速取出每筆資料中的 'date' 欄位
from operator import itemgetter

def main() -> None:
    # 範例資料：每個元素都是字典，包含日期(date)與地址(address)
    # 這裡刻意放入「重複日期」與「未排序」資料，方便觀察 groupby 的行為
    rows = [
        {'date': '07/01/2012', 'address': '5412 N CLARK'},
        {'date': '07/04/2012', 'address': '5148 N CLARK'},
        {'date': '07/01/2012', 'address': '5800 E 58TH'},
        {'date': '07/03/2012', 'address': '2122 N CLARK'},
        {'date': '07/04/2012', 'address': '5645 N RAVENSWOOD'},
        {'date': '07/02/2012', 'address': '1060 W ADDISON'},
        {'date': '07/03/2012', 'address': '4801 N BROADWAY'},
    ]

    print('原始資料（未排序）:')
    for row in rows:
        print(row)

    # 使用 groupby 前，務必要先依分組鍵排序。
    # 原因：groupby 只會把「相鄰且鍵值相同」的元素分在同一組，
    # 若未先排序，相同日期可能被拆成多個群組。
    rows.sort(key=itemgetter('date'))

    print('\n排序後資料（依 date）:')
    for row in rows:
        print(row)

    print('\n分組結果:')
    # 依 'date' 進行分組：
    # date  為目前這一組的鍵值（例如 '07/01/2012'）
    # items 為該組對應的迭代器（不是 list）
    for date, items in groupby(rows, key=itemgetter('date')):
        print(f'日期 {date}:')

        # items 是一次性迭代器：走訪完就會被消耗。
        # 若後續還想重複使用，建議先轉成 list。
        grouped_rows = list(items)

        # 逐筆輸出該日期底下的資料
        for i in grouped_rows:
            # i 是該日期群組中的每一筆原始字典資料
            # 例如：{'date': '07/01/2012', 'address': '5412 N CLARK'}
            print(f"  - {i['address']}")

        # 示範：因為我們已經轉成 list，所以可以再次使用 grouped_rows
        print(f'  小計: {len(grouped_rows)} 筆')


if __name__ == '__main__':
    main()
