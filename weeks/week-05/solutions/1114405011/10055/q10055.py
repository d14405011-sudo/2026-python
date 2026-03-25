"""
UVA 10055 - 複合函數的增減性
題目：判斷複合函數是否為增函數或減函數

解題思路：
========
複合函數的增減性規則：
- 增函數 ∘ 增函數 = 增函數
- 減函數 ∘ 減函數 = 增函數
- 增函數 ∘ 減函數 = 減函數
- 減函數 ∘ 增函數 = 減函數

結論：
- 偶數個減函數 → 增函數（輸出 0）
- 奇數個減函數 → 減函數（輸出 1）

用 0 表示增函數，1 表示減函數
"""

class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) for prefix sums.
    用來維護 0/1 陣列的區間和，以支援單點更新與區間查詢。
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    def update(self, i: int, delta: int) -> None:
        """在位置 i 加上 delta（1-indexed）。"""
        n = self.n
        while i <= n:
            self.tree[i] += delta
            i += i & -i

    def query(self, i: int) -> int:
        """回傳前綴和 sum[1..i]（1-indexed）。"""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def range_sum(self, l: int, r: int) -> int:
        """回傳區間和 sum[l..r]（1-indexed, l <= r）。"""
        if l > r:
            return 0
        return self.query(r) - self.query(l - 1)


def solve_q10055():
    """
    主程式：處理翻轉和查詢操作
    """
    n, q = map(int, input().split())

    # 初始化所有函數為增函數 (0)
    functions = [0] * (n + 1)  # 1-indexed

    # 建立 Fenwick Tree 來維護減函數 (1) 的數量
    bit = FenwickTree(n)

    # 處理 q 個操作
    for _ in range(q):
        operation = list(map(int, input().split()))

        if operation[0] == 1:
            # 翻轉操作：將函數 i 的增減性翻轉
            i = operation[1]

            # 目前狀態
            current = functions[i]
            if current == 0:
                # 由增函數變為減函數
                functions[i] = 1
                bit.update(i, 1)
            else:
                # 由減函數變為增函數
                functions[i] = 0
                bit.update(i, -1)
        else:
            # 查詢操作：查詢複合函數 F(x) = f_L(...f_R(x)...)
            l = operation[1]
            r = operation[2]

            # 計算 [l, r] 範圍內的減函數個數（使用 Fenwick Tree）
            count_decreasing = bit.range_sum(l, r)
            # 輸出結果：偶數個 -> 0，奇數個 -> 1
            result = count_decreasing % 2
            print(result)


if __name__ == "__main__":
    solve_q10055()
