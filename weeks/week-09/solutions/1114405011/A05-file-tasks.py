# A05. 綜合應用：僅寫新檔 + 目錄統計（5.5 / 5.13 / 5.1）
# Bloom: Apply — 把前面學到的 API 組起來解小任務（綜合多項檔案與目錄的操作技巧，解決實際問題）

from pathlib import Path
from datetime import date

# ── 任務一：日記小工具（5.5 的 'x' 模式） ──────────────
# 規則：每天只能建一次；同一天重複執行要提示「已存在」。
# date.today().isoformat() 會產生類似 "2026-04-23" 這種標準格式的字串
today = date.today().isoformat()          
diary = Path(f"diary-{today}.txt")

# 'x' (Exclusive creation 排他性建立) 模式：
# 與 'w' 模式不同，'w' 遇到檔案存在會直接「覆蓋並清空」原有內容；
# 'x' 模式則是「嚴格要求建立新檔」，如果目標檔案已經存在，就會直接拋出 FileExistsError 例外錯誤，
# 這樣可以防止我們不小心把今天已經寫好的日記給洗掉。
try:
    with open(diary, "x", encoding="utf-8") as f:
        f.write(f"# {today} 日記\n")
        f.write("今天學了檔案 I/O。\n")
    print(f"已建立 {diary}")
except FileExistsError:
    # 捕捉到檔案已經存在的錯誤後，顯示提示訊息，並保留原檔案內容不動
    print(f"{diary} 今天已寫過，保留原內容不覆蓋")

# ── 任務二：統計某資料夾裡 .py 檔的行數 ────────────────
# 這個任務結合了目錄走訪 (rglob)、開檔 (open)、以及逐行讀取 (for line in f)
def count_py(folder: Path):
    # 分別記錄：所有行數、非空白行數、定義函式 (def 開頭) 的行數
    total, nonblank, defs = 0, 0, 0
    
    # 遞迴尋找這個資料夾(含子資料夾)內所有的 Python 程式檔 (*.py)
    for p in folder.rglob("*.py"):
        # 使用 errors="replace" 來避免不預期的編碼錯誤 (例如檔案不小心混入了非 utf-8 字元)
        # 用 "" (U+FFFD) 取代無法解碼的字元，確保整批檔案統計不會因為單一錯誤而全盤中斷
        with open(p, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                total += 1
                s = line.strip()  # 去除字串前後的空白與換行符號
                if s:  # 如果清掉空白後字串不為空，代表這是一行有內容的程式碼或註解
                    nonblank += 1
                if s.startswith("def "):  # 判斷這行是不是以 "def " 開頭，代表遇到函式定義
                    defs += 1
    return total, nonblank, defs

# 目標：統計 week-04 的 in-class 資料夾的 .py 檔
# 因為從 weeks/week-09/in-class 出發，要先退回 week-09，再退回 weeks，然後進 week-04/in-class
# ".." 代表上一層目錄
target = Path("..") / ".." / "week-04" / "in-class"

if target.exists():
    total, nonblank, defs = count_py(target)
    print(f"{target}")
    print(f"  總行數       : {total}")
    print(f"  非空白行     : {nonblank}")
    print(f"  def 起頭行數 : {defs}")
else:
    print(f"示範目錄不存在：{target}")

# ── 課堂延伸挑戰（自行嘗試） ───────────────────────────
# 1) 把日記工具改成「附加」模式 'a'：同一天可多次追寫一行時間戳。
# 2) count_py 再多算一個「註解行（以 # 開頭）」的數字。
# 3) 把統計結果用 print(..., sep='\t', file=f) 寫到 stats.tsv。
