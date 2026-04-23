# U03. 文字 vs 位元組、編碼觀念（5.1 encoding / 5.4）
# Bloom: Understand — 能解釋什麼時候用 'rb'、為什麼要指定 encoding（理解二進位與文字模式的差別、編碼與解碼的時機與重要性）

from pathlib import Path

# ── 5.4 二進位讀寫：圖片、zip、任何非文字 ───────────────
# 在這個範例中，我們會手動建構一個符合 PNG 檔案格式「Magic Number（特徵碼/檔頭）」的 byte 陣列
# Magic Number 是作業系統或程式用來辨識檔案類型的關鍵部分，它是一串寫死在檔案最前面的二進位資料。
magic = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
# 寫入二進位檔案不再需要給編碼 (encoding) 參數。以寫入 bytes 的模式建立一個 "fake.png"
Path("fake.png").write_bytes(magic)

# 使用 'rb' (Read Bytes) 模式讀取回來，確認是否寫入成功
with open("fake.png", "rb") as f:
    head = f.read(8)  # 讀取前 8 個位元組
# b'...' 的 b 代表這是 bytes 物件，而非一般字串 (str)
print(head)           # 輸出: b'\x89PNG\r\n\x1a\n'
print(head == magic)  # 輸出: True，確認讀出與寫入的內容完全一樣

# 當我們使用 for 迴圈走訪 bytes 物件時，拿到的會是介於 0~255 之間的「整數 (int)」，而不是字元(str)。
# 這是 bytes 和 str 很大的一個行為差異。
for b in head[:4]:
    print(b, hex(b))  # hex() 會將整數轉換成 16 進位表示字串，例如 137 -> '0x89'

# ── 文字 vs 位元組的型別差 ─────────────────────────────
# 深入了解 str 與 bytes 在 Python 中的型別差異與轉換關係。
s = "你好"
# encode(): 將我們人類看得懂的 Unicode 字串 (str)，根據指定的編碼規則 (如 utf-8)，「編碼」成電腦看得懂的位元組 (bytes)
b = s.encode("utf-8")   
print(s, type(s))       # 輸出: 你好 <class 'str'>
print(b, type(b))       # 輸出: b'\xe4\xbd\xa0\xe5\xa5\xbd' <class 'bytes'>
# decode(): 將位元組 (bytes) 依照指定的編碼規則，還原「解碼」回原本的字串 (str)
print(b.decode("utf-8"))  # 輸出: 你好

# ── 5.1 encoding 參數：寫錯會爛掉 ──────────────────────
# 先用 UTF-8 編碼寫入一段中文測試文字
Path("zh.txt").write_text("中文測試\n", encoding="utf-8")

# 正常讀取：寫入時用什麼編碼，讀出時就要用對應的編碼來解碼 (decode)。
print(Path("zh.txt").read_text(encoding="utf-8"))

# 故意示範錯誤：如果用不正確的編碼來解讀 bytes 資料 (用大五碼 big5 去解碼用 utf-8 寫入的位元組)，
# 會因為對不起來而產生 UnicodeDecodeError 例外錯誤。
try:
    print(Path("zh.txt").read_text(encoding="big5"))
except UnicodeDecodeError as e:
    print("解碼錯誤:", e)

# 小結：
# - 文字檔 → 必須使用 'rt'/'wt' (通常 't' 可省略)，而且強烈建議「一律明示 encoding='utf-8'」。不要依賴系統的預設值，因為 Windows 預設通常是 CP950，與 Mac/Linux (通常是 UTF-8) 會產生相容性問題。
# - 非文字檔（如圖片、壓縮檔、PDF、pickle 物件序列化）→ 必須使用 'rb'/'wb'。因為它們就是純粹的位元組資料，根本不存在什麼「編碼轉換」的問題，所以寫入或讀取時不加、也不能加上 encoding 參數。
