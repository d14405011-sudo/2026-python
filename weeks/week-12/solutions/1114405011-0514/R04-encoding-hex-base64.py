# R04. 十六進位與 Base64 編碼解碼（6.9–6.10）
# binascii / base64 / bytes.hex() / bytes.fromhex()
#
# 本範例重點：
# 1) 了解 bytes 與 str 的差異
# 2) 學會 Hex / Base64 的編碼與解碼
# 3) 理解這兩者是資料「表示方式」，不是加密

import binascii
import base64

# ── 6.9 十六進位（Hex）────────────────────────────────────
# bytes 常用於儲存「原始位元資料」，例如網路封包、檔案內容、二進位協定。
# 下面這串 bytes 代表 UTF-8 編碼後的 "Hello, 世界"。
data = b"Hello, \xe4\xb8\x96\xe7\x95\x8c"   # "Hello, 世界" in UTF-8

# bytes → hex 字串
# binascii.b2a_hex() 會將每個位元組轉成兩位十六進位表示。
# 注意：回傳型別是 bytes（例如 b'48656c...'），不是 str。
hex_str = binascii.b2a_hex(data)
print("b2a_hex：", hex_str)                   # b'48656c6c6f2c ...'

# bytes.hex() 是 bytes 物件的內建方法，回傳型別是 str。
# 在日常開發中通常更直觀，且不需另外 import binascii。
hex_str2 = data.hex()                         # Python 3.5+ 內建方法
print(".hex()：", hex_str2)

# hex 字串 → bytes
# a2b_hex() 可把十六進位表示轉回原始 bytes。
# 這裡傳入的是前面 b2a_hex 產生的 bytes 型態十六進位資料。
restored = binascii.a2b_hex(hex_str)
print("a2b_hex：", restored)

# bytes.fromhex() 可把 str 型態的十六進位字串還原為 bytes。
# 適合搭配 data.hex() 形成一組對稱轉換。
restored2 = bytes.fromhex(hex_str2)           # Python 3.5+
print("fromhex：", restored2)

# 驗證「編碼再解碼」後，內容是否與原始資料完全一致。
assert restored == data     # 確認一致

# ── 6.10 Base64 ───────────────────────────────────────────
# Base64 可把任意 bytes 轉為可列印字元集合（A-Z, a-z, 0-9, +, /, =），
# 常用於需要傳輸純文字的通道（例如 JSON、HTTP、Email）。
msg = b"Python Cookbook"

# 編碼
# b64encode() 輸入 bytes，回傳 bytes。
encoded = base64.b64encode(msg)
print("\nb64encode：", encoded)               # b'UHl0aG9uIENvb2tib29r'

# 解碼
# b64decode() 將 Base64 bytes 還原為原始 bytes。
decoded = base64.b64decode(encoded)
print("b64decode：", decoded)                 # b'Python Cookbook'

# URL-safe Base64（不含 +/，改用 -_）
# 在 URL 或檔名中，+ 與 / 可能需要額外轉義。
# urlsafe_b64encode() 會改用 - 與 _，降低轉義需求。
url_encoded = base64.urlsafe_b64encode(msg)
print("urlsafe：  ", url_encoded)

# ── 應用場景比較 ──────────────────────────────────────────
# Hex    → 可讀性高，長度 2x，常見於 hash / MAC 位址
# Base64 → 長度約 1.33x，常見於 email 附件、HTTP 認證、JWT
#
# 補充：長度特性
# - Hex：每 1 byte 變成 2 個十六進位字元，因此長度固定放大 2 倍。
# - Base64：每 3 bytes 轉 4 字元，平均約放大 4/3（約 1.33 倍），
#           末尾可能用 '=' 做 padding。
#
# 重要觀念：兩者都只是「表示方式」，不是加密！
# 任何人都可直接還原原文，不能用來保護敏感資料。
