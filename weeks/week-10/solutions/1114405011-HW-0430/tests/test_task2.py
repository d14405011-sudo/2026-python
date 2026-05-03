# tests/test_task2.py
# TDD 測試：task2_json_to_xml.py 的 build_xml_tree 函式
# 學號：1114405011

import sys
import os
import unittest
import xml.etree.ElementTree as ET

# 讓 Python 能找到上一層的 task2_json_to_xml.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from task2_json_to_xml import build_xml_tree


def _make_sample_data(n: int = 3) -> dict:
    """建立測試用的 students dict 結構。"""
    students = [
        {"學號": f"113000{i:04d}", "系所名稱": "資訊工程系", "畢業學校": "國立馬公高中", "郵遞區號": "880"}
        for i in range(n)
    ]
    return {
        "來源": "113年新生資料庫",
        "入學方式篩選": "聯合登記分發",
        "總人數": n,
        "系所統計": {"資訊工程系": n},
        "學生清單": students,
    }


class TestBuildXmlTree(unittest.TestCase):

    def test_root_tag_and_attrs(self):
        """正常：根標籤為 students，source 與 total 屬性正確"""
        data = _make_sample_data(3)
        root = build_xml_tree(data)
        self.assertEqual(root.tag, "students")
        self.assertEqual(root.attrib["source"], "113年新生資料庫")
        self.assertEqual(root.attrib["total"], "3")

    def test_student_count_matches(self):
        """正常：XML 中 <student> 數量與 JSON 學生清單一致"""
        data = _make_sample_data(5)
        root = build_xml_tree(data)
        students = root.findall("student")
        self.assertEqual(len(students), 5)

    def test_student_attrs_exist(self):
        """正常：每個 <student> 包含 id、dept、school、zip 屬性"""
        data = _make_sample_data(2)
        root = build_xml_tree(data)
        for s in root.findall("student"):
            self.assertIn("id",     s.attrib)
            self.assertIn("dept",   s.attrib)
            self.assertIn("school", s.attrib)
            self.assertIn("zip",    s.attrib)

    def test_empty_student_list(self):
        """邊界：學生清單為空時，total 屬性應為 '0'，且無 <student> 子節點"""
        data = _make_sample_data(0)
        root = build_xml_tree(data)
        self.assertEqual(root.attrib["total"], "0")
        self.assertEqual(len(root.findall("student")), 0)

    def test_xml_is_valid(self):
        """反例：build_xml_tree 產生的結構可被 ET.tostring + ET.fromstring 正常往返"""
        data = _make_sample_data(4)
        root = build_xml_tree(data)
        xml_bytes = ET.tostring(root, encoding="unicode")
        # 應能正常解析，不拋出例外
        reparsed = ET.fromstring(xml_bytes)
        self.assertEqual(reparsed.tag, "students")
        self.assertEqual(len(reparsed.findall("student")), 4)

    def test_student_id_correct(self):
        """正常：<student> 的 id 屬性與學生清單中的學號一致"""
        data = _make_sample_data(2)
        root = build_xml_tree(data)
        ids_in_xml = {s.attrib["id"] for s in root.findall("student")}
        ids_in_json = {s["學號"] for s in data["學生清單"]}
        self.assertEqual(ids_in_xml, ids_in_json)

    def test_total_reflects_actual_count(self):
        """正常：total 屬性的值等於實際 <student> 節點數量"""
        data = _make_sample_data(7)
        root = build_xml_tree(data)
        self.assertEqual(int(root.attrib["total"]), len(root.findall("student")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
