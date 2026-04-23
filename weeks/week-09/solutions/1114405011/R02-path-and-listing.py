# R02. 路徑操作與目錄列舉（5.11 / 5.12 / 5.13）
# Bloom: Remember — 會用 pathlib 組路徑、檢查存在、列出檔案（學習現代化與跨平台的檔案路徑處理方式）

import os
from pathlib import Path

# ── 5.11 組路徑：pathlib 是現代寫法 ────────────────────
# 使用 Path 物件包裹字串後，可以直接使用斜線 (/) 來串接路徑，取代容易出錯的字串相加。
# 這樣做最大的好處是「跨平台」，在 Windows 執行時會自動轉成反斜線 (\)，在 Mac/Linux 則是正斜線 (/)。
base = Path("weeks") / "week-09"
print(base)              # weeks/week-09（Windows 環境下印出時自動變成反斜線）

# Path 物件內建了許多屬性，方便快速取得路徑的各個部分：
print(base.name)         # 取得完整的檔案或資料夾名稱（week-09）
print(base.parent)       # 取得上一層的父目錄路徑（weeks）
print(base.suffix)       # 取得副檔名，包含小數點。因為 base 是資料夾，所以回傳空字串 '' 

f = Path("hello.txt")
# stem: 取得去掉副檔名後的主檔名 (hello)
# suffix: 取得副檔名 (.txt)
print(f.stem, f.suffix)  # 輸出: hello .txt

# 與舊版 os 模組的相容寫法：os.path.join()
# 以前在 Python 3.4 之前還沒有 pathlib 時，必須用 os.path.join 來組合跨平台路徑。
print(os.path.join("weeks", "week-09", "README.md"))

# ── 5.12 存在判斷 ──────────────────────────────────────
# 利用 Path 物件的方法，可以很直覺地確認檔案或資料夾的狀態
p = Path("hello.txt")
print(p.exists())    # 檢查該路徑的檔案或資料夾「是否存在」（回傳布林值）
print(p.is_file())   # 檢查該路徑「是否為一個檔案」
print(p.is_dir())    # 檢查該路徑「是否為一個資料夾/目錄」

missing = Path("no_such_file.txt")
# 實務上讀取檔案前，常會先檢查檔案是否存在，避免程式報錯終止 (FileNotFoundError)
if not missing.exists():
    print(f"{missing} 不存在，略過讀取")

# ── 5.13 列出資料夾內容 ────────────────────────────────
# Path(".") 代表「當前工作目錄」(Current Working Directory)
here = Path(".")

# 1. os.listdir：傳統寫法，只列出當前層級的所有檔案與資料夾名稱 (回傳純字串)
for name in os.listdir(here):
    print("listdir:", name)

# 2. glob()：pathlib 的寫法，可以支援萬用字元 (例如 *.py 代表所有副檔名為 py 的檔案)
# 只會搜尋「當前層級」，不會進入子資料夾。回傳的是 Path 物件而非純字串。
for p in here.glob("*.py"):
    print("glob:", p)

# 3. rglob()：遞迴 (recursive) 搜尋。除了當前目錄，還會「深入遍歷所有子資料夾」
# 例如 Path("..") 代表上一層目錄，這裡會把上一層包含其底下所有的 .py 檔都找出來
for p in Path("..").rglob("*.py"):
    print("rglob:", p)
    break  # 為了示範版面簡潔，這裡只要印出第一個找到的檔案後就強制中斷迴圈
