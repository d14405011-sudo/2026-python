# TEST_LOG
# Week 12 - 10908 / 10922 / 10929 / 10931
# 學號：1114405011

## 測試指令

```bash
# 逐一執行 week-12 109xx 測試檔
$tests = Get-ChildItem -Path "weeks/week-12/solutions/1114405011" -Recurse -Filter "test_q109*.py" | Sort-Object FullName
foreach ($t in $tests) {
    d:/2026-python/.venv/Scripts/python.exe "$($t.FullName)"
}
```

## 測試輸出紀錄

```text
===== RUN D:\2026-python\weeks\week-12\solutions\1114405011\10908\test_q10908.py =====
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
===== RUN D:\2026-python\weeks\week-12\solutions\1114405011\10908\test_q10908_hand_typed.py =====
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
===== RUN D:\2026-python\weeks\week-12\solutions\1114405011\10922\test_q10922.py =====
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
===== RUN D:\2026-python\weeks\week-12\solutions\1114405011\10922\test_q10922_hand_typed.py =====
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
===== RUN D:\2026-python\weeks\week-12\solutions\1114405011\10929\test_q10929.py =====
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
===== RUN D:\2026-python\weeks\week-12\solutions\1114405011\10929\test_q10929_hand_typed.py =====
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
===== RUN D:\2026-python\weeks\week-12\solutions\1114405011\10931\test_q10931.py =====
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
===== RUN D:\2026-python\weeks\week-12\solutions\1114405011\10931\test_q10931_hand_typed.py =====
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

## 結果摘要

- 10908：主版 + hand-typed 全通過
- 10922：主版 + hand-typed 全通過
- 10929：主版 + hand-typed 全通過
- 10931：主版 + hand-typed 全通過
- 合計：18 tests，全部通過
