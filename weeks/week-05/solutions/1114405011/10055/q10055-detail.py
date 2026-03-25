"""
UVA 10055 - 複合函數的增減性 (詳細版本)

數學原理詳解：
=============

複合函數的定義：
F(x) = f_L(f_{L+1}(... f_R(x)...))

微分的連鎖法則：
F'(x) = f'_L(...) · f'_{L+1}(...) · ... · f'_R(...)

若 f 是增函數，則 f'(x) > 0
若 f 是減函數，則 f'(x) < 0（或 f'(x) < 0）

複合函數的增減性取決於有多少個減函數：
1. 0 個減函數（全增）：F'(x) > 0 → 增函數
2. 1 個減函數：F'(x) < 0 → 減函數
3. 2 個減函數：F'(x) = (-) × (-) = (+) > 0 → 增函數
4. 3 個減函數：F'(x) = (-) × (-) × (-) = (-) < 0 → 減函數
...

結論：減函數個數的奇偶性決定複合函數的性質

實現方式：
========
使用陣列記錄函數狀態：
- 0：增函數
- 1：減函數

操作1（翻轉）：functions[i] = 1 - functions[i]
操作2（查詢）：sum(functions[l:r+1]) % 2
"""

import sys

def solve_q10055_detailed():
    """
    詳細版本的 Q10055 解決方案
    """
    n, q = map(int, input().split())
    
    # 初始化函數陣列
    functions = [0] * (n + 1)  # 0=增函數, 1=減函數
    
    print(f"初始化 {n} 個函數，全部為增函數", file=sys.stderr)
    
    operation_count = 0
    query_count = 0
    
    for op_idx in range(q):
        operation = list(map(int, input().split()))
        
        if operation[0] == 1:
            # 翻轉操作
            operation_count += 1
            i = operation[1]
            old_state = functions[i]
            functions[i] = 1 - functions[i]
            new_state = functions[i]
            state_name_old = "增" if old_state == 0 else "減"
            state_name_new = "增" if new_state == 0 else "減"
            print(f"操作 #{operation_count}: 翻轉 f[{i}] ({state_name_old} → {state_name_new})",
                  file=sys.stderr)
        else:
            # 查詢操作
            query_count += 1
            l = operation[1]
            r = operation[2]
            
            # 計算減函數個數
            decreasing = sum(functions[l:r+1])
            
            # 判斷結果
            result = decreasing % 2
            result_name = "增" if result == 0 else "減"
            
            # 詳細輸出
            function_states = [
                f"f[{i}]={'增' if functions[i]==0 else '減'}"
                for i in range(l, r+1)
            ]
            print(f"查詢 #{query_count}: F({l}..{r}) = {' · '.join(function_states)}",
                  file=sys.stderr)
            print(f"         減函數個數: {decreasing}({result_name}函數) → 輸出 {result}",
                  file=sys.stderr)
            
            print(result)


if __name__ == "__main__":
    solve_q10055_detailed()
