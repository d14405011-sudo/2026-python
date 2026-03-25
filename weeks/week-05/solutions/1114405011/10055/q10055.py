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

def solve_q10055():
    """
    主程式：處理翻轉和查詢操作
    """
    n, q = map(int, input().split())
    
    # 初始化所有函數為增函數 (0)
    functions = [0] * (n + 1)  # 1-indexed
    
    # 處理 q 個操作
    for _ in range(q):
        operation = list(map(int, input().split()))
        
        if operation[0] == 1:
            # 翻轉操作：將函數 i 的增減性翻轉
            i = operation[1]
            functions[i] = 1 - functions[i]
        else:
            # 查詢操作：查詢複合函數 F(x) = f_L(...f_R(x)...)
            l = operation[1]
            r = operation[2]
            
            # 計算 [l, r] 範圍內的減函數個數
            count_decreasing = sum(functions[l:r+1])
            
            # 輸出結果：偶數個 -> 0，奇數個 -> 1
            result = count_decreasing % 2
            print(result)


if __name__ == "__main__":
    solve_q10055()
