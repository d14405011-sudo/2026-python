# R01. 函數彈性簽章
# 讓函數可以接受「不固定數量」的參數，提升彈性與泛用性
# 對應 Bloom's Taxonomy：記憶（Remember）— 背得出語法

# ── *args：不定個數的位置參數 ─────────────────────────────
# *args 允許函數接受任意多個「位置參數」
# 常見於加總、串接等彈性需求


# *args 會把所有額外的位置參數收集成一個 tuple
def add_all(*args):
    """args 在函數內是一個 tuple"""
    return sum(args)


print("=== *args：不定個數的位置參數 ===")
print(add_all(1, 2))            # 3，等同 sum((1,2))
print(add_all(1, 2, 3, 4, 5))  # 15，等同 sum((1,2,3,4,5))
print(add_all())                # 0（空的 tuple 也沒問題）

# ── **kwargs：不定個數的關鍵字參數 ───────────────────────
# **kwargs 允許函數接受任意多個「名稱=值」的參數
# 在函數內會自動收集成一個 dict


# **kwargs 會把所有額外的關鍵字參數收集成 dict
def make_student(**kwargs):
    """建立學生資料，欄位可以自由指定"""
    return kwargs


print("\n=== **kwargs：不定個數的關鍵字參數 ===")
s = make_student(name="王小明", grade=85, seat=12)  # 參數自訂欄位
print(s)   # {'name': '王小明', 'grade': 85, 'seat': 12}

# ── keyword-only：強制用名稱呼叫 ─────────────────────────
# * 後面的參數「一定要具名」填寫，避免順序搞錯


# * 之後的參數必須用名稱指定，不能只靠順序
def send_score(student_id, *, subject, score):
    """* 之後的參數必須具名，避免搞混"""
    print(f"學號 {student_id}｜{subject}：{score} 分")


print("\n=== keyword-only：強制具名，避免填錯順序 ===")
send_score("411234001", subject="數學", score=90)   # 正確，subject/score 必須明確指定
# send_score("411234001", "數學", 90)  # ← 這樣會 TypeError！因為 subject/score 不能只靠順序


# ── 三種參數混合使用 ──────────────────────────────────────
# 綜合：普通參數、*args、具名預設參數
def report(title, *scores, prefix="成績"):
    """title 普通參數，scores 不定個數，prefix 有預設值"""
    avg = sum(scores) / len(scores) if scores else 0
    print(f"{prefix}報告－{title}：平均 {avg:.1f}")


print("\n=== 混合：普通 + *args + 預設值 ===")
report("期中考", 80, 90, 70)  # title=期中考, scores=(80,90,70), prefix=預設
report("期末考", 95, 85, 75, 100, prefix="最終")  # prefix 可自訂

# ── 記憶重點 ──────────────────────────────────────────────
# *args   → tuple，接受任意個「值」
# **kwargs → dict，接受任意個「名稱=值」
# *（單獨）→ 後面的參數一定要具名
# 順序：普通參數 → *args → keyword-only（*之後）→ **kwargs
#
# 小技巧：
# - *args、**kwargs 可同時用於「包裝」與「解包」參數
# - 實務上常見於 API、資料處理、彈性報表等場景
