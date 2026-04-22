# Week 10 Homework - 1114405011

## 完成題目
- UVA 10226
- UVA 10235
- UVA 10242
- UVA 10252
- UVA 10268

## 資料夾與命名模式
- 每題使用獨立資料夾（例如 `10226/`）。
- 每題至少包含：
  - `q題號.py`：主版本
  - `q題號-easy.py`：較容易記憶版本
  - `test_q題號.py`：對應單元測試

## 測試方式
在本資料夾執行：

```bash
python -m unittest discover -s . -p "test_q*.py" -v
```

## 測試紀錄
- 測試輸出保存在 `TEST_LOG.txt`。
- 測試案例設計說明請見 `TEST_CASES.md`。
