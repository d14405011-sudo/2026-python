# A02. with 語句與 Context Manager
# 「借東西要還」——確保資源一定會被釋放，就算程式出錯也一樣
# 對應 Bloom's Taxonomy：應用（Apply）— 能設計並使用自訂的 with 區塊
# 核心觀念：把「初始化資源」與「清理資源」綁在一起，避免遺漏 close/release

# ── 為什麼需要 with？ ─────────────────────────────────────
# 沒有 with 的開檔方式：如果中途發生例外，close() 可能永遠不會被呼叫

# 不好的寫法
# f = open("demo.txt", "w")
# f.write("hello")
# f.close()   # 如果 write 出錯，這行就不會執行了

# 正確的寫法：with 會自動呼叫 close()，即使出錯也一樣
print("=== with 開檔：自動關閉 ===")
# 進入 with 時：open 檔案並建立檔案物件，綁定給 f
# 離開 with 時：Python 會自動呼叫 f.close()（即使區塊內發生例外）
with open("/tmp/week13_demo.txt", "w") as f:
    f.write("Hello from Week 13\n")

# 再次開啟同一檔案讀取內容，示範 with 的典型「開啟-使用-自動關閉」流程
with open("/tmp/week13_demo.txt", "r") as f:
    print(f.read().strip())

# ── 自己寫 Context Manager（用 class）────────────────────
# 需要實作兩個方法：
#   __enter__：進入 with 區塊時執行，回傳值會被 as 接收
#   __exit__ ：離開 with 區塊時執行（不管有沒有出錯）

import time

class Timer:
    """計時器：進入 with 時開始，離開時印出經過時間"""

    def __enter__(self):
        # 紀錄進入 with 的時間戳記
        self.start = time.time()
        print("⏱  開始計時")
        return self   # 這個值會被 as 接收，例如 as t

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 不論區塊成功或拋例外，都會執行到這裡
        elapsed = time.time() - self.start
        print(f"⏱  結束：{elapsed:.4f} 秒")
        # __exit__ 會收到例外資訊：
        # exc_type: 例外類型（例如 ValueError）
        # exc_val : 例外物件
        # exc_tb  : traceback
        # 回傳 False 代表「不要吞掉例外」，讓外層仍可看到錯誤
        return False  # False = 不吃掉例外（讓錯誤繼續往外傳）

print("\n=== 自訂計時器 ===")
# with Timer() 會依序做：
# 1) 呼叫 __enter__
# 2) 執行 with 區塊主體
# 3) 呼叫 __exit__ 做收尾
with Timer() as t:
    total = sum(range(1_000_000))
print(f"計算結果：{total}")

# ── 更簡單的寫法：@contextmanager ─────────────────────────
# 不用寫 class，用 yield 分隔「進入前」和「離開後」

from contextlib import contextmanager

@contextmanager
def section(title):
    """印出有邊框的區段標題"""
    # yield 前：相當於 __enter__ 的工作（進場）
    print(f"\n{'='*40}")
    print(f"  {title}")
    print(f"{'='*40}")
    yield           # ← with 區塊的程式碼在這裡執行
    # yield 後：相當於 __exit__ 的工作（收尾）
    print(f"{'─'*40}")

print()
with section("Week 13 CPE 模擬考"):
    print("  題目：UVA 11005 Cheapest Base")
    print("  時間限制：20 分鐘")

# ── CPE 應用：截取 stdout，方便測試輸出 ─────────────────
# 有些 CPE 題目會直接 print 答案
# 測試時可以截取 print 的輸出來比對

import io, sys

@contextmanager
def capture_output():
    """暫時把 print 的輸出截取到字串裡"""
    # 先保存原本的 stdout，避免覆寫後找不回來
    old_stdout = sys.stdout
    # 把 stdout 指向記憶體緩衝區（StringIO），之後 print 會寫到這裡
    sys.stdout = buffer = io.StringIO()
    try:
        # 把 buffer 交給 with ... as out 使用
        yield buffer     # with ... as buf 的 buf 就是這個 buffer
    finally:
        # 無論區塊是否出錯，都要還原 stdout，避免影響後續程式
        sys.stdout = old_stdout   # 一定要還原，finally 保證執行

def solve_parity(n):
    """UVA 10931 Parity：計算 n 的二進位裡有幾個 1"""
    # bin(n) 會回傳像 '0b1010'，所以用 [2:] 去掉前綴 '0b'
    bits = bin(n)[2:]
    # 計算二進位字串中 '1' 的數量
    ones = bits.count('1')
    print(f"The parity of {bits} is {ones} (mod 2 is {ones % 2}).")

print("\n=== 截取輸出（測試用）===")
# 進入 capture_output 後，區塊內所有 print 都會被寫進 out
with capture_output() as out:
    solve_parity(10)
    solve_parity(7)

# 取得累積的文字內容（完整字串）
captured = out.getvalue()
print("截取到的輸出：")
print(captured)

# 可以直接拿來做 assertEqual
# 把多行字串拆成每一行，方便逐行比對
lines = captured.strip().split('\n')
print(f"共 {len(lines)} 行輸出")

# 記憶重點 ──────────────────────────────────────────────────
# __enter__ → 進入 with 時執行，回傳值被 as 接收
# __exit__  → 離開 with 時執行（出錯也會執行）
# @contextmanager + yield → 更簡單的寫法，yield 前是 enter，yield 後是 exit
# 常用場景：開檔、計時、測試輸出截取、任何「借了要還」的資源
# 實戰提醒：只要看到程式有「取得資源 + 需要釋放」兩段流程，就很適合用 with
