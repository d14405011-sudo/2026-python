# TEST_LOG.md
# TDD Red → Green 執行紀錄
# 學號：1114405011

---

## Task 1

### Red（失敗紀錄）

**執行指令：**
```bash
python -m unittest tests/test_task1.py -v
```

**結果（task1_csv_to_json.py 尚未建立時）：**
```
ERROR: test_filter_keeps_correct_rows (test_task1.TestFilterByAdmission)
ImportError: cannot import name 'filter_by_admission' from 'task1_csv_to_json'

Ran 1 test in 0.001s

FAILED (errors=1)
```

**失敗原因：** `filter_by_admission` 函式尚未實作，測試無法 import 而拋出 `ImportError`，這是預期的 Red 狀態。

---

### Green（通過紀錄）

**執行指令：**
```bash
python -m unittest tests/test_task1.py -v
```

**結果（task1_csv_to_json.py 實作完成後）：**
```
test_count_by_dept_correct ... ok
test_count_by_dept_empty ... ok
test_count_by_dept_single ... ok
test_count_by_dept_sorted_desc ... ok
test_count_by_dept_strips_whitespace ... ok
test_filter_empty_input ... ok
test_filter_keeps_correct_rows ... ok
test_filter_no_match ... ok
test_filter_removes_others ... ok
test_filter_strips_whitespace ... ok

Ran 10 tests in 0.003s

OK
```

**讓測試通過的關鍵修改：**
- `filter_by_admission`：使用 list comprehension 比對 `r.get("入學方式", "").strip() == method.strip()`，加上 `.strip()` 處理前後空白
- `count_by_dept`：使用 `collections.Counter` 統計系所名稱，並以人數由多到少排序回傳

---

## Task 2

### Red（失敗紀錄）

**執行指令：**
```bash
python -m unittest tests/test_task2.py -v
```

**結果（task2_json_to_xml.py 尚未建立時）：**
```
ERROR: test_root_tag_and_attrs (test_task2.TestBuildXmlTree)
ImportError: cannot import name 'build_xml_tree' from 'task2_json_to_xml'

Ran 1 test in 0.001s

FAILED (errors=1)
```

**失敗原因：** `build_xml_tree` 函式尚未實作，`ImportError` 是預期的 Red 狀態。

---

### Green（通過紀錄）

**執行指令：**
```bash
python -m unittest tests/test_task2.py -v
```

**結果（task2_json_to_xml.py 實作完成後）：**
```
test_empty_student_list ... ok
test_root_tag_and_attrs ... ok
test_student_attrs_exist ... ok
test_student_count_matches ... ok
test_student_id_correct ... ok
test_total_reflects_actual_count ... ok
test_xml_is_valid ... ok

Ran 7 tests in 0.003s

OK
```

**讓測試通過的關鍵修改：**
- `build_xml_tree`：建立根節點 `<students source=... total=...>`，再以 `for` 迴圈逐筆呼叫 `ET.SubElement` 建立 `<student id=... dept=... school=... zip=.../>`
- `total` 屬性使用 `str(len(students_list))` 確保型別為字串（XML 屬性值皆為字串）

---

## 全數通過（17 tests）

```bash
python -m unittest discover -s tests -p "test_*.py" -v

Ran 17 tests in 0.001s

OK
```
