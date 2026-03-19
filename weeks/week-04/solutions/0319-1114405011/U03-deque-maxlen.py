# U3. deque(maxlen=N) 為何能保留最後 N 筆（1.3）
#
# deque（雙向隊列）搭配 maxlen 參數的特性：
# - 當元素數量超過 maxlen 時，會自動從另一端移除舊元素
# - 頻繁的左端追加操作時，性能優於 list（O(1) vs O(n)）
# - 常用於「保留最近 N 筆記錄」或「滑動視窗」場景

from collections import deque


def main() -> None:
    # ==============================================================
    # 1) 基本示範：maxlen 的自動移除機制
    # ==============================================================
    # 建立一個最多容納 3 個元素的 deque
    q = deque(maxlen=3)

    print('1) 基本示範：maxlen 的自動移除機制')
    print(f'   建立 deque(maxlen=3)')

    # 逐個追加 5 個數字，觀察 deque 如何自動移除舊元素
    for i in [1, 2, 3, 4, 5]:
        q.append(i)
        print(f'   append({i}) -> deque = {list(q)}')

    # 最終只保留最後 3 筆（3, 4, 5）
    print(f'   最終結果：{list(q)}  (只保留最後 3 筆)')

    # ==============================================================
    # 2) 與普通 list 的比較
    # ==============================================================
    print('\n2) deque(maxlen) vs list:')

    # 使用普通 list（無大小限制）
    regular_list = []
    for i in [1, 2, 3, 4, 5]:
        regular_list.append(i)
    print(f'   list.append() -> {regular_list}  (所有元素都保留)')

    # 使用 deque(maxlen=3)（自動保留最後 3 筆）
    limited_deque = deque(maxlen=3)
    for i in [1, 2, 3, 4, 5]:
        limited_deque.append(i)
    print(f'   deque(maxlen=3).append() -> {list(limited_deque)}  (只保留最後 3 筆)')

    # ==============================================================
    # 3) 從左端追加的性能優勢
    # ==============================================================
    print('\n3) 從左端追加（appendleft）:')

    q = deque(maxlen=3)
    for i in [1, 2, 3, 4]:
        q.appendleft(i)  # 從左端追加
        print(f'   appendleft({i}) -> deque = {list(q)}')

    print(f'   最終結果：{list(q)}  (最左的元素最早加入)')

    # ==============================================================
    # 4) 實務應用：保留最近 N 筆操作記錄
    # ==============================================================
    print('\n4) 實務應用：保留最近 5 筆操作記錄')

    operations = deque(maxlen=5)
    user_actions = ['登入', '修改檔案 A', '刪除檔案 B', '下載檔案 C', '上傳檔案 D', '登出', '重新登入']

    for action in user_actions:
        operations.append(action)
        print(f'   執行: {action:15} -> 記錄 = {list(operations)}')

    print(f'   最終保留的最近 5 筆操作：{list(operations)}')

    # ==============================================================
    # 5) 實務應用：滑動視窗（計算移動平均）
    # ==============================================================
    print('\n5) 實務應用：滑動視窗（計算最近 3 天的平均溫度）')

    temps = deque(maxlen=3)
    daily_temps = [20, 22, 21, 23, 25, 24, 22]

    for day, temp in enumerate(daily_temps, 1):
        temps.append(temp)
        avg = sum(temps) / len(temps)
        print(f'   第 {day} 天 ({temp}°C) -> 最近 3 天的溫度 = {list(temps)}, 平均 = {avg:.1f}°C')

    # ==============================================================
    # 6) maxlen=None 的情形
    # ==============================================================
    print('\n6) maxlen=None（無大小限制）:')

    unlimited_deque = deque(maxlen=None)
    print(f'   deque(maxlen=None) 的 maxlen 屬性 = {unlimited_deque.maxlen}')
    print(f'   （None 表示無大小限制，行為同普通 list）')


if __name__ == '__main__':
    main()
