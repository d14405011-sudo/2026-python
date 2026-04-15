# U07. 隨機種子與安全亂數（3.11）
#
# 這份範例釐清兩種「隨機」的用途差異：
# 1) random：偽隨機，可重現，適合模擬/遊戲/測試。
# 2) secrets：密碼學安全亂數，不可預測，適合安全用途。

import random
import secrets

# 相同種子 -> 相同序列（可重現）
# 這在單元測試、除錯和教學場景非常有用，
# 因為每次執行都能得到同一組結果。
random.seed(42)
seq1 = [random.randint(1, 100) for _ in range(5)]
random.seed(42)
seq2 = [random.randint(1, 100) for _ in range(5)]
print(seq1 == seq2)  # True

# 不同 Random 實例各自獨立
# 你可以建立多個獨立亂數流，避免互相影響。
rng1 = random.Random(1)
rng2 = random.Random(2)
print(rng1.random(), rng2.random())  # 各自的隨機流

# 密碼學安全亂數（不可預測，不能設種子）
# 用於 token、驗證碼、密碼重設連結、session key 等安全需求。
print(secrets.randbelow(100))  # 密碼學安全整數
print(secrets.token_hex(16))  # 密碼學安全 hex 字串
print(secrets.token_bytes(16))  # 密碼學安全 bytes

# 重要總結：
# - 需要「可重現」-> random
# - 需要「不可預測」-> secrets
# random 不適合密碼、token、session key 等安全場景。
