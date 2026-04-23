# A06. 壓縮檔、臨時資料夾、物件序列化（5.7 / 5.19 / 5.21）
# Bloom: Apply — 能把標準庫工具組合起來解一個小任務（整合 gzip 壓縮、tempfile 暫存管理與 pickle 序列化等進階 I/O 技巧）

import gzip
import pickle
import tempfile
from pathlib import Path

# ── 5.7 讀寫壓縮檔：gzip.open 幾乎和 open 一樣 ─────────
# gzip 模組的 gzip.open() 用法和內建的 open() 幾乎完全相同。
# 它是幫我們在背後偷偷把資料「壓縮後寫入磁碟」或「從磁碟讀取後解壓縮」。
# 同樣地，只要是處理文字模式 ('wt' 或 'rt')，就一定要記得指定 encoding="utf-8" 參數。
with gzip.open("notes.txt.gz", "wt", encoding="utf-8") as f:
    f.write("第一行筆記\n")
    f.write("第二行筆記\n")

# 讀回：直接把 gzip 檔案物件當迭代器逐行讀取，不用預先解壓縮成一個巨大的字串，非常節省記憶體。
with gzip.open("notes.txt.gz", "rt", encoding="utf-8") as f:
    for line in f:
        print("gz:", line.rstrip())

# 當然也支援以位元組模式 ('wb' / 'rb') 處理二進位資料（此時就不需要且不能加 encoding 參數）。
with gzip.open("blob.bin.gz", "wb") as f:
    f.write(b"\x00\x01\x02\x03")

# stat().st_size 可以用來查詢檔案在磁碟上的實際位元組大小 (容量)
print("blob size:", Path("blob.bin.gz").stat().st_size, "bytes")

# ── 5.19 臨時檔案與資料夾：離開 with 自動清理 ──────────
# 場景：有時候程式只需要一個「暫時存放」檔案的地方（例如中介處理檔、下載暫存檔），
# 處理完立刻丟掉，不希望在專案目錄裡留下垃圾。
# tempfile.TemporaryDirectory() 會拜託作業系統借一塊暫存空間，並保證在離開 with 區塊時「連同裡面的檔案一併強制刪除」。
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)  # 原本回傳的是純字串路徑，我們把它包裝成 Path 物件以便操作
    print("暫存資料夾:", tmp)

    # 在這個暫存資料夾裡面建立兩個臨時的文字檔
    (tmp / "a.txt").write_text("hello\n", encoding="utf-8")
    (tmp / "b.txt").write_text("world\n", encoding="utf-8")

    # iterdir() 會列出該目錄下的所有檔案與資料夾
    # 我們逐一印出檔名與內容
    for p in tmp.iterdir():
        print("  ", p.name, "→", p.read_text(encoding="utf-8").rstrip())

# 離開 with 區塊後，tmp 目錄與裡面的 a.txt, b.txt 都被系統清得乾乾淨淨了
print("離開後還存在嗎？", tmp.exists())  # 輸出: False

# 單一臨時檔：NamedTemporaryFile
# delete=False 表示離開 with 時「不要」自動刪除它。
# 這樣做通常是為了把這個路徑 (f.name) 傳給其他外部程式使用。
with tempfile.NamedTemporaryFile("wt", delete=False, suffix=".log",
                                 encoding="utf-8") as f:
    f.write("暫存 log\n")
    log_path = f.name
print("暫存檔位置:", log_path)

# 因為剛剛設定了 delete=False，所以用完之後我們必須要手動呼叫 unlink() 把它刪掉
Path(log_path).unlink()  # 用完自己刪

# ── 5.21 pickle：把 Python 物件「原樣」存檔 ────────────
# pickle 可以對 Python 物件進行「序列化 (Serialize)」與「反序列化」。
# 意思是它可以把整個 dict, list 甚至是自訂類別，轉換成一串 byte 二進位資料存到硬碟，
# 下次讀出來還是可以直接當 dict 或是原物件來操作。
# 優點：非常方便，原汁原味保存結構。
# 缺點：只有 Python 程式看得懂（跨語言請改用 JSON）；格式可能隨版次更新不相容；存在資安風險。
scores = {
    "alice": [90, 85, 92],
    "bob":   [70, 75, 80],
    "carol": [88, 91, 95],
}

# 注意：因為 pickle 轉出的結果是 bytes (二進位)，所以開檔模式一定要用 'wb' 或 'rb'。
# dump() 負責把記憶體對象「傾倒」進檔案裡。
with open("scores.pkl", "wb") as f:
    pickle.dump(scores, f)

# load() 負責把檔案內的資料「讀取並還原」回原本記憶體裡的 Python 對象。
with open("scores.pkl", "rb") as f:
    loaded = pickle.load(f)

# 驗證反序列化出來的結果跟當初存進去的是否一致
print("讀回的物件:", loaded)
print("型別一致?", type(loaded) is dict)         # 輸出: True，依舊保持 dict 的型態
print("內容相等?", loaded == scores)              # 輸出: True
print("alice 平均:", sum(loaded["alice"]) / 3)   # 89.0

# ⚠️ 嚴重安全提醒：
# pickle 在還原物件時（pickle.load），如果有心人士在裡面塞入惡意腳本，
# load 的瞬間惡意腳本就會在你的電腦上被執行 (可以執行任意系統指令)。
# 所以絕對不要對「來路不明」的 .pkl 檔做 load !!

# ── 課堂延伸挑戰 ───────────────────────────────────────
# 1) 把 scores 存成 gzip 壓縮後的 pickle：gzip.open('scores.pkl.gz','wb')
# 2) 用 TemporaryDirectory 跑完整流程（寫→讀→比對），不在專案留任何檔
# 3) 試著 pickle 一個 lambda 函式，觀察錯誤訊息（因為 pickle 不能序列化記憶體中匿名函式的 lambda）
