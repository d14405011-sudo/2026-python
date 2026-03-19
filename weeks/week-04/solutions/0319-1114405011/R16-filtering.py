# R16. 過濾：推導式 / generator / filter / compress（1.16）

from itertools import compress


def is_int(val: str) -> bool:
    """
    判斷字串是否可被轉為整數。

    參數:
        val: 欲檢查的字串

    回傳:
        True  -> 可轉成 int
        False -> 無法轉成 int
    """
    try:
        int(val)
        return True
    except ValueError:
        return False


def main() -> None:
    # ------------------------------------------------------------
    # 1) 串列推導式（List Comprehension）
    # ------------------------------------------------------------
    # 特色：語法精簡、一次產生完整 list，適合資料量不大且要立即使用結果的情境。
    mylist = [1, 4, -5, 10, -7, 2]
    positive_list = [n for n in mylist if n > 0]

    print('1) 串列推導式過濾正數:')
    print(f'   原始資料: {mylist}')
    print(f'   過濾結果: {positive_list}')

    # ------------------------------------------------------------
    # 2) 生成器推導式（Generator Expression）
    # ------------------------------------------------------------
    # 特色：惰性計算，不會一次把所有結果放進記憶體；適合大量資料或串流處理。
    # 注意：生成器走訪一次後會被消耗，若要重複使用需重新建立。
    positive_gen = (n for n in mylist if n > 0)

    print('\n2) 生成器推導式過濾正數:')
    print(f'   生成器物件: {positive_gen}')
    print(f'   第一次取用(list): {list(positive_gen)}')
    print(f'   第二次取用(list): {list(positive_gen)}  <- 已被消耗，結果為空')

    # ------------------------------------------------------------
    # 3) filter(函式, 可迭代物件)
    # ------------------------------------------------------------
    # filter 會保留讓函式回傳 True 的元素。
    # 這裡用 is_int 過濾出可轉整數的字串。
    values = ['1', '2', '-3', '-', 'N/A', '100', '5.5']
    valid_int_strings = list(filter(is_int, values))

    print('\n3) filter 搭配自訂函式 is_int:')
    print(f'   原始字串: {values}')
    print(f'   可轉整數: {valid_int_strings}')

    # ------------------------------------------------------------
    # 4) itertools.compress(資料, 遮罩)
    # ------------------------------------------------------------
    # compress 會根據布林遮罩保留資料：
    # 遮罩為 True 的位置保留、False 的位置捨棄。
    addresses = ['a1', 'a2', 'a3', 'a4']
    counts = [0, 3, 10, 6]
    more_than_5_mask = [n > 5 for n in counts]
    selected_addresses = list(compress(addresses, more_than_5_mask))

    print('\n4) compress 依布林遮罩過濾資料:')
    print(f'   addresses: {addresses}')
    print(f'   counts:    {counts}')
    print(f'   遮罩(mask): {more_than_5_mask}')
    print(f'   過濾結果: {selected_addresses}')


if __name__ == '__main__':
    main()
