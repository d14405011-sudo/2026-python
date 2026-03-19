# U5. 優先佇列為何要加 index（1.5）
#
# 問題：若用 (priority, item) 二元組作 heap，同優先級會比較 item
# 當 item 不支援 < 比較時，會拋出 TypeError
#
# 解決方案：使用 (priority, index, item) 三元組
# - priority：優先級（正常比較）
# - index：插入順序計數器（保證不會比較 item）
# - item：實際物件

import heapq


class Item:
    """代表優先隊列中的任務或資料項"""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Item({self.name})'


def main() -> None:
    # ==============================================================
    # 1) 問題演示：不加 index 會報 TypeError
    # ==============================================================
    print('1) 問題演示：為什麼不能直接用 (priority, item)?')
    print()

    # 嘗試只用 (priority, item) 的方式
    pq_bad = []
    print('   嘗試用 (priority, item) 來建立優先隊列:')

    heapq.heappush(pq_bad, (-1, Item('task_a')))
    print(f'   heappush((-1, Item("task_a"))) -> 成功')

    # 第二個相同優先級的會觸發問題
    print(f'   嘗試 heappush((-1, Item("task_b")))...')
    try:
        heapq.heappush(pq_bad, (-1, Item('task_b')))
        print(f'   ✓ 成功')
    except TypeError as e:
        print(f'   ✗ TypeError: {e}')
        print(f'   原因：heap 內部需要比較 Item 物件，但 Item 不定義 < 運算')

    print()

    # ==============================================================
    # 2) 解決方案：加上 index
    # ==============================================================
    print('2) 解決方案：加上計數器 index 作為打破平手的依據')
    print()

    pq = []
    idx_counter = 0

    # 建立三元組 (priority, index, item)
    print('   使用 (priority, index, item) 三元組:')

    for name in ['task_a', 'task_b', 'task_c', 'task_d']:
        heapq.heappush(pq, (-1, idx_counter, Item(name)))
        print(f'   heappush((priority=-1, index={idx_counter}, {Item(name)})) -> 堆: {[(p, i, item.name) for p, i, item in pq]}')
        idx_counter += 1

    # 現在即使優先級相同，也會透過 index 進行排序而非比較 item
    print()
    print('   優先級相同時，會用 index 排序，不會比較 Item 物件')

    # ==============================================================
    # 3) 提取元素
    # ==============================================================
    print('\n3) 提取元素（heappop）:')

    while pq:
        priority, index, item = heapq.heappop(pq)
        print(f'   heappop() -> priority={priority}, index={index}, {item}')

    # ==============================================================
    # 4) 實務應用：任務調度系統
    # ==============================================================
    print('\n4) 實務應用：任務調度系統（支援動態優先級調整）')

    class Task:
        """代表一個任務"""
        def __init__(self, task_id, description, priority):
            self.task_id = task_id
            self.description = description
            self.priority = priority

        def __repr__(self):
            return f'Task[{self.task_id}]({self.description}, priority={self.priority})'

    # 任務隊列：(負優先級, 插入順序, 任務)
    task_queue = []
    task_idx = 0

    # 加入任務
    tasks = [
        Task('A', '編譯代碼', 2),
        Task('B', '修復緊急 bug', 1),
        Task('C', '寫文件', 3),
        Task('D', '代碼審查', 1),
    ]

    print('   加入 4 個優先級不同的任務:')
    for task in tasks:
        # 使用負優先級讓優先級小的優先執行
        heapq.heappush(task_queue, (-task.priority, task_idx, task))
        print(f'     加入: {task}')
        task_idx += 1

    print('\n   執行順序（優先級小的先執行）:')
    while task_queue:
        neg_priority, idx, task = heapq.heappop(task_queue)
        priority = -neg_priority
        print(f'     執行: {task}（第 {idx+1} 個加入）')

    # ==============================================================
    # 5) 為什麼 index 很重要？
    # ==============================================================
    print('\n5) 為什麼 index 很重要？')
    print('   - 保證優先級相同時，維持「先進先出」（FIFO）順序')
    print('   - 避免比較複雜物件（它們可能不支援 < 運算）')
    print('   - index 是單調遞增的整數，永遠可以比較')
    print('   - 效率高：整數比較 O(1)，遠快於物件比較')


if __name__ == '__main__':
    main()
