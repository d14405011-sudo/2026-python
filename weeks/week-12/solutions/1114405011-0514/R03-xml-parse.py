# R03. XML 解析基礎（6.3）
# xml.etree.ElementTree：find / findall / get / text / iter
#
# XML（eXtensible Markup Language）是一種標記語言，
# 用於表示結構化資料，廣泛應用於配置檔案、資料交換等場景。
# Python 的 xml.etree.ElementTree 模組提供了輕量級的 XML 解析工具。

import xml.etree.ElementTree as ET  # 匯入內建的 XML 解析模組

# ── 範例 XML ─────────────────────────────────────────────
# 準備一段範例 XML 字串，模擬 RSS 資訊流的結構。
# RSS 是一種用於發布頻道內容（如新聞、部落格文章）的 XML 格式。
xml_data = """
<rss version="2.0">
  <channel>
    <title>Planet Python</title>
    <item>
      <title>討論 Python 型別提示</title>
      <link>https://example.com/1</link>
      <author>Alice</author>
    </item>
    <item>
      <title>asyncio 最佳實踐</title>
      <link>https://example.com/2</link>
      <author>Bob</author>
    </item>
  </channel>
</rss>
"""

# ── 解析字串 ─────────────────────────────────────────────
# 使用 ET.fromstring() 將 XML 字串解析為 Element 樹的根節點。
root = ET.fromstring(xml_data)
print("根標籤：", root.tag)           # 輸出根節點的標籤名稱，例如 <rss>
print("屬性：",   root.attrib)        # 輸出根節點的屬性字典，例如 {'version': '2.0'}

# ── find / findall ────────────────────────────────────────
# find()：尋找第一個符合條件的子節點
# findall()：尋找所有符合條件的子節點
channel = root.find("channel")
print("頻道名稱：", channel.find("title").text)  # 取得 <title> 的文字內容

# 取得所有 item 節點，並逐一解析其內容
for item in root.findall("channel/item"):
    title  = item.find("title").text   # 取得 <title> 的文字內容
    author = item.find("author").text  # 取得 <author> 的文字內容
    print(f"  [{author}] {title}")

# ── iter：遍歷所有同名標籤 ───────────────────────────────
# iter()：遞迴遍歷所有子節點，尋找指定標籤名稱的節點
print("\n所有 <title>：")
for elem in root.iter("title"):
    print(" ", elem.text)  # 輸出每個 <title> 節點的文字內容

# ── 從檔案解析 ───────────────────────────────────────────
# 如果 XML 資料存於檔案，可使用 ET.parse() 讀取並解析。
# tree = ET.parse("data.xml")
# root = tree.getroot()  # 取得根節點

# ── 取得屬性 .get() ───────────────────────────────────────
# 使用 .get() 方法取得節點的屬性值，若屬性不存在可指定預設值。
version = root.get("version")
print("\nRSS 版本：", version)        # 輸出屬性 version 的值，例如 2.0
print("不存在的屬性：", root.get("missing", "預設值"))  # 若屬性不存在，回傳 "預設值"
