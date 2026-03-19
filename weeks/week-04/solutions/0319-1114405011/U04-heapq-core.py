# U4. heap 為何能高效拿 Top-N（1.4）
#
# heap（堆）是一種特殊的二元樹資料結構，具有以下特性：
# - 最小堆（min-heap）：父節點 <= 子節點，根節點永遠是最小值
# - heapq 模組提供最小堆實現
# - heappush：O(log n), heappop：O(log n), heapify：O(n)
# - 適合找 Top-N 個最小或最大元素

import heapq


def main() -> None:
    # ==============================================================
    # 1) 基本概念：heapify 與堆的性質
    # ==============================================================
    # 原始無序列表
    nums = [5, 1, 9, 2, 8, 3]

    print('1) 基本概念：heapify 將列表轉換成最小堆')
    print(f'   原始列表: {nums}')

    # 複製一份備用（因為 heapify 會直接修改原列表）
    h = nums[:]
    heapq.heapify(h)  # 原地轉換成最小堆

    print(f'   heapify(h) 後: {h}')
    print(f'   h[0] = {h[0]}  （最小值永遠在根節點）')

    # ==============================================================
    # 2) 堆的結構（陣列表示法）
    # ==============================================================
    print('\n2) 堆的陣列表示法（索引關係）:')
    print(f'   h = {h}')
    print(f'   對索引 i：左子 = 2*i+1, 右子 = 2*i+2, 父 = (i-1)//2')
    print(f'   ')
    print(f'   h[0] = {h[0]} (根節點，最小值)')
    print(f'   h[1] = {h[1]}, h[2] = {h[2]} (第一層子節點)')
    print(f'   h[3] = {h[3]}, h[4] = {h[4]}, h[5] = {h[5]} (第二層子節點)')

    # ==============================================================
    # 3) 逐次提取最小值：heappop
    # ==============================================================
    print('\n3) 逐次提取最小值（heappop）:')

    h = [1, 2, 3, 5, 8, 9]  # 已是最小堆
    print(f'   初始堆: {h}')

    extracted = []
    while h:
        m = heapq.heappop(h)  # 每次 pop 都拿到並移除最小值
        extracted.append(m)
        print(f'   heappop() -> {m}, 剩餘堆: {h}')

    print(f'   提取順序: {extracted}  (自動排序)')

    # ==============================================================
    # 4) 加入新元素：heappush
    # ==============================================================
    print('\n4) 加入新元素（heappush）:')

    h = [1, 5, 3]
    print(f'   初始堆: {h}')

    for val in [2, 4]:
        heapq.heappush(h, val)
        print(f'   heappush({val}) -> {h}')

    # ==============================================================
    # 5) 實務應用：找 Top-N 個最小元素
    # ==============================================================
    print('\n5) 實務應用：找 Top-3 個最小的數字')

    numbers = [64, 25, 12, 22, 11, 90, 88, 45, 33, 7, 56]
    print(f'   原始數字: {numbers}')

    # 方法 1：使用 nsmallest
    top_3_smallest = heapq.nsmallest(3, numbers)
    print(f'   heapq.nsmallest(3, numbers) = {top_3_smallest}')

    # 方法 2：使用 nlargest
    top_3_largest = heapq.nlargest(3, numbers)
    print(f'   heapq.nlargest(3, numbers) = {top_3_largest}')

    # ==============================================================
    # 6) 應用：優先隊列（Priority Queue）
    # ==============================================================
    print('\n6) 應用：優先隊列（Priority Queue）')

    # 使用 heap 實現優先隊列
    pq = []

    # 加入任務（優先級, 任務 ID, 描述）
    heapq.heappush(pq, (3, 'task-1', '低優先級任務'))
    heapq.heappush(pq, (1, 'task-2', '高優先級任務'))
    heapq.heappush(pq, (2, 'task-3', '中等優先級任務'))

    print('   加入 3 個優先級不同的任務:')
    print('     (3, task-1, 低優先級)')
    print('     (1, task-2, 高優先級)')
    print('     (2, task-3, 中等優先級)')

    print('   處理順序（優先級小的先執行）:')
    while pq:
        priority, task_id, desc = heapq.heappop(pq)
        print(f'     執行: [{priority}] {task_id} - {desc}')

    # ==============================================================
    # 7) 應用：找 Top-K 個最大元素（使用負數技巧）
    # ==============================================================
    print('\n7) 應用：找 Top-K 個最大元素（利用最小堆）')

    numbers = [3, 8, 5, 2, 9, 1, 7]
    k = 3

    # 技巧：使用負數轉換最小堆為最大堆
    negated = [-x for x in numbers]
    heapq.heapify(negated)

    print(f'   原始數字: {numbers}')
    print(f'   找 Top-{k} 個最大的數字:')

    top_k = []
    for _ in range(k):
        top_k.append(-heapq.heappop(negated))

    print(f'   結果: {sorted(top_k, reverse=True)}')


if __name__ == '__main__':
    main()
