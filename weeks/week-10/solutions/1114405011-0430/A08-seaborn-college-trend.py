# A08. 用 seaborn 畫 109~114 學年各學院生源分析圖
# Bloom: Apply — 把 A07 的統計成果交給視覺化套件
#
# 需要：pip install seaborn matplotlib pandas
#
# 用到的 I/O 技巧延續 A07：
#   5.7  zipfile 不解壓讀 CSV
#   5.1  utf-8-sig 去 BOM
#   5.6  io.StringIO → csv
#   5.11 pathlib
#   5.5  open('x') 不覆蓋輸出檔

import csv
import io
import platform
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ── 中文字型：依平台挑一個有的 ─────────────────────────
# matplotlib 在 macOS 預設抓不到 PingFang TC，用系統內建的 Heiti TC / Arial Unicode MS
# 這裡建立一個字典來判斷現在的作業系統，以便選擇適當的繁體中文字型
_CJK_FONTS = {
    "Darwin":  ["Heiti TC", "Arial Unicode MS", "PingFang TC"],       # macOS 專用字型
    "Windows": ["Microsoft JhengHei", "Microsoft YaHei"],             # Windows 微軟正黑體/微軟雅黑體
    "Linux":   ["Noto Sans CJK TC", "WenQuanYi Zen Hei"],             # Linux 思源黑體/文泉驛正黑
}.get(platform.system(), ["sans-serif"]) # 若皆無符合則預設使用無襯線字型


def _apply_cjk_font():
    """sns.set_theme 會重設 rcParams，需要在它之後再套一次。"""
    # 將找到的中文字型加入到 matplotlib 的字型清單最前端，確保優先套用
    plt.rcParams["font.sans-serif"] = _CJK_FONTS + plt.rcParams["font.sans-serif"]
    # 設定主要字體系列為無襯線字型
    plt.rcParams["font.family"] = "sans-serif"
    # 解決 matplotlib 畫負號 (minus sign) 時會顯示為方塊的編碼問題
    plt.rcParams["axes.unicode_minus"] = False


_apply_cjk_font() # 第一次套用字型設定

# ── 系所 → 學院 對照表（NPU 三大學院） ─────────────────
# 定義將「系所名稱」對應到所屬「學院」的字典 (對照表)
DEPT_TO_COLLEGE = {
    # 人文暨管理學院
    "應用外語系":       "人文暨管理學院",
    "航運管理系":       "人文暨管理學院",
    "行銷與物流管理系": "人文暨管理學院",
    "觀光休閒系":       "人文暨管理學院",
    "資訊管理系":       "人文暨管理學院",
    "餐旅管理系":       "人文暨管理學院",
    # 海洋資源暨工程學院
    "水產養殖系":       "海洋資源暨工程學院",
    "海洋遊憩系":       "海洋資源暨工程學院",
    "食品科學系":       "海洋資源暨工程學院",
    # 電資工程學院
    "資訊工程系":       "電資工程學院",
    "電信工程系":       "電資工程學院",
    "電機工程系":       "電資工程學院",
}

# ── 5.11 定位資料 ─────────────────────────────────────
# 取得目前執行 Python 檔案所在的資料夾絕對路徑
HERE = Path(__file__).resolve().parent
# 往上推三層資料夾，並進入 "assets" 資料夾組合出 ZIP 檔的完整路徑
ZIP_PATH = HERE.parent.parent.parent / "assets" / "npu-stu-109-114-anon.zip"
# 防呆機制：確保指向的 ZIP 檔案確實存在，否則會拋出 AssertionError 例外
assert ZIP_PATH.exists(), f"找不到：{ZIP_PATH}"


# ── 5.7 + 5.6 + 5.1 讀 zip 內所有 CSV 成一張 long-form 表 ─
def load_long_frame(zip_path: Path) -> pd.DataFrame:
    """從 ZIP 壓縮檔內直接讀取各年度新生資料，解析成為 Pandas DataFrame 以供後續操作"""
    records = []
    # 使用 zipfile 開啟 ZIP 壓縮檔，避免解壓縮占用實體磁碟空間
    with zipfile.ZipFile(zip_path) as z:
        # 遍歷提取 ZIP 中的所有檔案資訊
        for info in z.infolist():
            # 過濾掉非 CSV 結尾的檔案（例如系統隱藏檔 .DS_Store 等）
            if not info.filename.endswith(".csv"):
                continue
            # 從檔名切出前三個字元作爲學年 (例如：從 "109年新生資料庫.csv" 擷取出 "109")
            year = info.filename[:3]                     # '109'..'114'
            # 讀取壓縮檔內的單一檔案內容，並使用 utf-8-sig 解碼，自動幫我們過濾掉檔案開頭的 BOM 標記
            text = z.read(info).decode("utf-8-sig")      # 去 BOM
            # 將解析好的記憶體文字區塊 (text) 放進 StringIO 串流，並用 csv.DictReader 將其視為一般檔案進行讀取
            reader = csv.DictReader(io.StringIO(text))   # 當檔讀
            # 逐列解析成字典資料
            for row in reader:
                # 取得該位新生的系所名稱，並用 strip 去除前後多餘的空白
                dept = row.get("系所名稱", "").strip()
                # 如果沒有系所資訊（欄位空值）則跳過這筆新生
                if not dept:
                    continue
                # 將整理好的資料存入串列，採用 Long-Form Data (展開式資料：每一筆紀錄皆是一名新生)
                records.append({
                    "學年": int(year),  # 轉為整數型態
                    "學院": DEPT_TO_COLLEGE.get(dept, "其他"),  # 依對照表找到相對應學院，沒找到就標成預設值「其他」
                    "系所": dept,       # 原始登錄的系所
                })
    # 利用整理好裝有字典的 list (records) 轉換建立為 Pandas DataFrame 表格型態
    return pd.DataFrame.from_records(records)


df = load_long_frame(ZIP_PATH)
print("總筆數:", len(df))
print(df.head()) # 印出最前頭的 5 筆紀錄來檢查載入的資料格式

# 透過 groupby 進行樞紐資料分組：計算「各學年、各學院」的實際就讀人數
pivot = (df.groupby(["學年", "學院"])
           .size() # size() 會去計算每個群組內部擁有的列數 (即為該類別下就讀人數)
           .reset_index(name="人數")) # 將群組計算出來的這一直行數字賦予欄位名稱 "人數"，同時將階層式的 index 轉回一般的 DataFrame 欄位
print("\n各學年各學院:")
# 利用 pivot 操作把長表倒過來變寬表 (Wide-Form：學年作列、學院當行顯示)，方便在終端機檢視
print(pivot.pivot(index="學年", columns="學院", values="人數"))


# ── seaborn 繪圖 ──────────────────────────────────────
# 設定 seaborn 整體顯示的主題風格：套用白底且有網格 (whitegrid)、縮放大小 context 為 talk (字級較大適合呈現)、色彩佈景為 Set2
sns.set_theme(style="whitegrid", context="talk", palette="Set2")
_apply_cjk_font()  # 重新蓋回中文字型 (因為上面的 set_theme 會刷新設定，需再次呼叫自訂函式把中文字體註冊回來)

# 準備畫布 (fig) 與兩塊子繪圖區 (axes)：1 行 2 欄，整張圖片寬度 15 英吋、高度 6 英吋
# gridspec_kw 用來調整兩個子圖彼此的寬度比例：左圖和右圖分別占全圖的 1.3 與 1 比例寬度
fig, axes = plt.subplots(1, 2, figsize=(15, 6),
                         gridspec_kw={"width_ratios": [1.3, 1]})

# 圖 A (折線＋散點)：表示「各學院新生人數逐年趨勢」，放在左方的子圖 axes[0]
# sns.lineplot 綁定資料來源 (pivot)，並用 hue 以「學院」做為分層著色的變化
sns.lineplot(data=pivot, x="學年", y="人數", hue="學院",
             marker="o", markersize=10, linewidth=2.5, ax=axes[0]) # 加上標點(圓形)、調大標示點、加粗線條寬度
# 設定左圖標題、字體大小並且留些間距 (pad)
axes[0].set_title("109–114 各學院新生人數趨勢", fontsize=16, pad=12)
# 強制只顯示資料中有出現過的「整數年度」為X軸刻度 (避免 matplotlib 自動畫出 109.5 這類不存在的小數刻度)
axes[0].set_xticks(sorted(pivot["學年"].unique()))
# 產生這張折線圖專屬圖例，放到右上方並且繪製它的邊框 (frameon=True)
axes[0].legend(title="學院", loc="upper right", frameon=True)

# 透過迴圈走訪 DataFrame (pivot) 的每一列數值，在折線點上方手動加上純數字的「人數」標籤
for _, r in pivot.iterrows():
    axes[0].annotate(int(r["人數"]), # 要標示出來的人數文字 (轉成整數避免小數點)
                     (r["學年"], r["人數"]), # 在圖表裡的哪個資料點位 (X, Y) 進行標註
                     textcoords="offset points", xytext=(0, 8), # 以點位作基準整體往上偏移 8 個單位，不擋到原本的圓形資料點
                     ha="center", fontsize=9, alpha=0.8) # 置中對齊(ha)、縮小字體、加入些微透明度(alpha)

# 圖 B (堆疊長條)：表示「各學年內部的學院比例結構」，放在右方的子圖 axes[1]
# 將 pivot 再次轉換成 Wide-Form 寬表以方便畫出多特徵的累積長條，如有空缺年份需用 0 去填補 NaN 保證維度完整 (fillna(0))
pivot_wide = pivot.pivot(index="學年", columns="學院", values="人數").fillna(0)
# 取 Pandas 內建的繪圖擴充，宣告要繪製堆疊型長條圖 (stacked=True)，指定給右方的 axes[1] 圖紙
pivot_wide.plot(kind="bar", stacked=True,
                ax=axes[1], colormap="Set2", width=0.75, edgecolor="white") # 設定長條寬度 0.75，並為區塊周圍加上白邊線增添立體感
# 設定右側子圖各種屬性、標題及名稱
axes[1].set_title("各學年學院結構（堆疊）", fontsize=16, pad=12)
axes[1].set_ylabel("人數")
# 將橫向 X 軸的顯示標籤 (年份) 轉回水平不要傾斜 (rotation=0)
axes[1].tick_params(axis="x", rotation=0)
# 也是把這張圖的圖例放在右上角並調小字體以免喧賓奪主
axes[1].legend(title="學院", loc="upper right", fontsize=9)

# 設定整個主畫布共用的「總標題」文字
fig.suptitle("國立澎湖科技大學  109–114 學年新生生源分析",
             fontsize=18, fontweight="bold", y=1.02) # 以 y=1.02 稍微往上提一點，以免跟子圖擠在一起
# tight_layout 讓 matplotlib 幫我們智慧計算版面去擠壓子圖間距，預防圖例或字體重疊並被切斷
fig.tight_layout()

# ── 5.5 'x' 模式輸出：檔已存在就保留舊的 ────────────────
# 組合出我們產出的結果靜態圖片最終要在哪裡被儲存
OUT = HERE / "A08-college-trend.png"
try:
    # 嘗試以 'xb' ('x' 代表獨佔式建立專屬寫入: exclusive creation, 'b' 代表二進位: binary) 方式寫入圖片結果
    # !! 'x' 模式特性 !!：只要檔案存在，Python 會直接拋出 FileExistsError 不做任何改變達成不覆寫舊檔目的
    with open(OUT, "xb") as f:
        # 繪圖成果寫入 f 指向的檔案系統位置，並將畫質設定在 dpi=150 / 啟用緊湊包圍盒避免切到文字(bbox_inches="tight")
        fig.savefig(f, dpi=150, bbox_inches="tight")
    print(f"\n圖檔已寫入：{OUT.name}")
except FileExistsError:
    # 這裡捕捉到了檔案已存在防護，印出溫馨提示不進行任圖片覆寫
    print(f"\n{OUT.name} 已存在，保留舊檔（要重畫請先刪除）")

# 將畫好並上色的動態視窗直接顯示在螢幕上供我們調整和觀賞結果
plt.show()

# ── 延伸挑戰 ──────────────────────────────────────────
# 1) 改畫「各系所」熱力圖：sns.heatmap(pivot_by_dept, annot=True, fmt='d')
# 2) 加一張圓餅圖：114 學年學院占比
# 3) 把年度 x 軸改成 '109學年'~'114學年' 字串（需轉型 + set_xticklabels）
