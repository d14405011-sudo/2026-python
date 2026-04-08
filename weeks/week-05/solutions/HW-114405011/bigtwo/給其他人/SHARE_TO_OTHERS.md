# BigTwo 分享給其他電腦

## 免安裝 Python（EXE 版本）

1. 直接把 `BigTwo.exe` 給對方
2. 對方雙擊即可啟動（Windows）
3. 若被 SmartScreen 擋住：點「其他資訊」->「仍要執行」

## 你要給對方的檔案

1. `bigtwo-share-2026-04-08.zip`
2. 或 `BigTwo.exe`（免安裝 Python）

## 對方電腦安裝步驟（Windows）

1. 解壓縮 `bigtwo-share-2026-04-08.zip`
2. 進入解壓後的 `bigtwo` 資料夾
3. 開啟 PowerShell，執行：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
.\開始遊戲.bat
```

## 對方電腦安裝步驟（macOS）

1. 解壓縮 `bigtwo-share-2026-04-08.zip`
2. 打開 Terminal
3. 進入解壓後的 `bigtwo` 資料夾
4. 執行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## 平台選擇建議

1. Windows 一般使用者：直接雙擊 `BigTwo.exe`
2. Windows 開發者：使用 `bigtwo-share-2026-04-08.zip`
3. macOS 使用者：使用 `bigtwo-share-2026-04-08.zip`

## 已知需求

1. Python 3.9 以上
2. 網路可用於安裝 `pygame-ce`

## 若無法啟動

1. 先確認 Python：`python --version`
2. 再安裝依賴：`pip install -r requirements.txt`
3. 最後手動啟動：`python main.py`