# TEST_LOG

日期：2026-05-20
環境：`.venv` Python 3.14.2

## 全量測試

執行方式（逐檔）：

```powershell
$tests = Get-ChildItem -Path "weeks/week-13/solutions/1114405011-0520" -Recurse -Filter "test_*.py" | Sort-Object FullName
foreach ($t in $tests) {
  d:/2026-python/.venv/Scripts/python.exe $t.FullName -v
}
```

結果：所有測試皆 `OK`。

## 手打程式測試紀錄（集中）

### 11005 / test_q11005_hand_typed.py

```text
Exit Code: 0

[STDERR]
test_hand_typed (__main__.Test11005HandTyped.test_hand_typed) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.171s

OK

[STDOUT]
```

### 11063 / test_q11063_hand_typed.py

```text
Exit Code: 0

[STDERR]
test_hand (__main__.Test11063HandTyped.test_hand) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.176s

OK

[STDOUT]
```

### 11150 / test_q11150_hand_typed.py

```text
Exit Code: 0

[STDERR]
test_hand (__main__.Test11150HandTyped.test_hand) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.168s

OK

[STDOUT]
```

### 11321 / test_q11321_hand_typed.py

```text
Exit Code: 0

[STDERR]
test_hand (__main__.Test11321HandTyped.test_hand) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.171s

OK

[STDOUT]
```

### 11332 / test_q11332_hand_typed.py

```text
Exit Code: 0

[STDERR]
test_hand (__main__.Test11332HandTyped.test_hand) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.163s

OK

[STDOUT]
```
