# tests/test_task1.py
# TDD 測試：task1_csv_to_json.py 的 filter_by_admission 與 count_by_dept
# 學號：1114405011

import sys
import os
import unittest

# 讓 Python 能找到上一層的 task1_csv_to_json.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from task1_csv_to_json import filter_by_admission, count_by_dept


class TestFilterByAdmission(unittest.TestCase):
    """測試 filter_by_admission 函式"""

    def setUp(self):
        """共用測試資料（每種入學方式使用唯一系所，避免判斷混淆）"""
        self.rows = [
            {"入學方式": "聯合登記分發", "系所名稱": "資訊工程系"},
            {"入學方式": "繁星推甄",     "系所名稱": "電機工程系"},
            {"入學方式": "申請入學",     "系所名稱": "資訊管理系"},
            {"入學方式": "聯合登記分發", "系所名稱": "航運管理系"},
        ]

    def test_filter_keeps_correct_rows(self):
        """正常：過濾後的列入學方式全為「聯合登記分發」"""
        result = filter_by_admission(self.rows, "聯合登記分發")
        self.assertEqual(len(result), 2)
        for r in result:
            self.assertEqual(r["入學方式"], "聯合登記分發")

    def test_filter_removes_others(self):
        """正常：其他入學方式（繁星推甄、申請入學）的列不出現在結果中"""
        result = filter_by_admission(self.rows, "聯合登記分發")
        depts_in_result = {r["系所名稱"] for r in result}
        # 繁星推甄 → 電機工程系 不應出現
        self.assertNotIn("電機工程系", depts_in_result)
        # 申請入學 → 資訊管理系 不應出現
        self.assertNotIn("資訊管理系", depts_in_result)

    def test_filter_empty_input(self):
        """邊界：空 list 輸入時回傳空 list"""
        result = filter_by_admission([], "聯合登記分發")
        self.assertEqual(result, [])

    def test_filter_no_match(self):
        """邊界：無符合條件時回傳空 list"""
        result = filter_by_admission(self.rows, "運動績優單招")
        self.assertEqual(result, [])

    def test_filter_strips_whitespace(self):
        """邊界：入學方式含前後空白時仍可正確過濾"""
        rows_with_space = [
            {"入學方式": " 聯合登記分發 ", "系所名稱": "資訊工程系"},
            {"入學方式": "繁星推甄",        "系所名稱": "電機工程系"},
        ]
        result = filter_by_admission(rows_with_space, "聯合登記分發")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["系所名稱"], "資訊工程系")


class TestCountByDept(unittest.TestCase):
    """測試 count_by_dept 函式"""

    def test_count_by_dept_correct(self):
        """正常：已知資料的系所統計結果正確"""
        rows = [
            {"系所名稱": "資訊工程系"},
            {"系所名稱": "電機工程系"},
            {"系所名稱": "資訊工程系"},
            {"系所名稱": "資訊工程系"},
        ]
        result = count_by_dept(rows)
        self.assertEqual(result["資訊工程系"], 3)
        self.assertEqual(result["電機工程系"], 1)

    def test_count_by_dept_empty(self):
        """邊界：空輸入時回傳空 dict"""
        result = count_by_dept([])
        self.assertEqual(result, {})

    def test_count_by_dept_single(self):
        """邊界：只有一筆資料"""
        rows = [{"系所名稱": "航運管理系"}]
        result = count_by_dept(rows)
        self.assertEqual(result, {"航運管理系": 1})

    def test_count_by_dept_strips_whitespace(self):
        """邊界：系所名稱含空白時仍能正確統計"""
        rows = [
            {"系所名稱": " 資訊工程系 "},
            {"系所名稱": "資訊工程系"},
        ]
        result = count_by_dept(rows)
        self.assertEqual(result.get("資訊工程系", 0), 2)

    def test_count_by_dept_sorted_desc(self):
        """正常：結果應依人數由多到少排序"""
        rows = [
            {"系所名稱": "電機工程系"},
            {"系所名稱": "資訊工程系"},
            {"系所名稱": "資訊工程系"},
            {"系所名稱": "資訊工程系"},
        ]
        result = count_by_dept(rows)
        keys = list(result.keys())
        self.assertEqual(keys[0], "資訊工程系")  # 最多的排第一


if __name__ == "__main__":
    unittest.main(verbosity=2)
