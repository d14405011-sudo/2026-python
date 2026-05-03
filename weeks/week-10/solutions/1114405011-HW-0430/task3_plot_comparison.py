# task3_plot_comparison.py
# Task 3：將 Task 1 / Task 2 的 @timeit 耗時做成比較圖
# 學號：1114405011
#
# 【加分項實作說明】
#   Bonus 1 — 使用 seaborn 製作設計感比較圖（主題、配色、版面配置全面優化）
#   Bonus 2 — 中文字型正確呈現（依平台自動選擇可用中文字型）
#   Bonus 3 — 創意延伸：雙圖表版面（上：各操作耗時 + 標註；下：分組比較讀取 vs 寫入）
#             + 圖底附加結論摘要文字方塊
#
# 需要：pip install seaborn matplotlib

import os
import platform
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd

# ── 路徑設定 ─────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "output"
OUTPUT_PNG = OUTPUT_DIR / "timing_comparison.png"

# ── Bonus 2：中文字型設定（依平台選擇，確保不亂碼）────────
_CJK_FONTS = {
    "Darwin":  ["Heiti TC", "Arial Unicode MS", "PingFang TC"],
    "Windows": ["Microsoft JhengHei", "Microsoft YaHei"],
    "Linux":   ["Noto Sans CJK TC", "WenQuanYi Zen Hei"],
}.get(platform.system(), ["sans-serif"])

plt.rcParams["font.sans-serif"] = _CJK_FONTS + plt.rcParams.get("font.sans-serif", [])
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False  # 負號正確顯示

# ── 耗時資料（來自 TIMING_REPORT.md 實際量測值）────────────
# Task 1：read_csv、write_json
# Task 2：read_json、write_xml
DATA = {
    "函式":     ["read_csv",  "write_json", "read_json", "write_xml"],
    "耗時(s)":  [0.002442,    0.002385,     0.002562,    0.001698  ],
    "所屬任務": ["Task 1",    "Task 1",     "Task 2",    "Task 2"  ],
    "操作類型": ["讀取",      "寫入",       "讀取",      "寫入"    ],
}
df = pd.DataFrame(DATA)

# Bonus 3 延伸：第二組資料 — 依「操作類型」分組的讀取 vs 寫入平均耗時比較
df_grouped = (
    df.groupby("操作類型", sort=False)["耗時(s)"]
    .mean()
    .reset_index()
    .rename(columns={"耗時(s)": "平均耗時(s)"})
)


# ── Bonus 1 + 2 + 3：繪製雙子圖版面 ──────────────────────
def plot_timing(df: pd.DataFrame, df_grouped: pd.DataFrame, output_path: str) -> None:
    """使用 seaborn 繪製雙子圖：上為各函式耗時長條圖；下為讀取 vs 寫入分組比較。"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Bonus 1 — seaborn 主題：淡灰底格線 + 纖細框線
    sns.set_theme(style="whitegrid", font_scale=1.05)
    # 套用中文字型（sns.set_theme 會重設 rcParams，需要再套一次）
    plt.rcParams["font.sans-serif"] = _CJK_FONTS + plt.rcParams.get("font.sans-serif", [])
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    # Task 色票（深藍 / 橙紅）
    TASK_PALETTE = {"Task 1": "#2E86AB", "Task 2": "#E84855"}
    TYPE_PALETTE = {"讀取": "#3BB273", "寫入": "#F4A261"}

    fig, axes = plt.subplots(
        nrows=2, ncols=1,
        figsize=(9, 9),
        gridspec_kw={"height_ratios": [3, 2], "hspace": 0.55},
    )

    # ── 上圖：各函式耗時（依所屬任務著色） ─────────────────
    ax1 = axes[0]
    bars = sns.barplot(
        data=df, x="函式", y="耗時(s)",
        hue="所屬任務", palette=TASK_PALETTE,
        dodge=False, width=0.55, ax=ax1, legend=True,
    )
    # 在每個 bar 頂端標示精確秒數（Bonus 2 中文標註）
    for patch, (_, row) in zip(ax1.patches, df.iterrows()):
        h = patch.get_height()
        ax1.text(
            patch.get_x() + patch.get_width() / 2,
            h + df["耗時(s)"].max() * 0.018,
            f"{h:.5f}s",
            ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#333333",
        )
    # 標示最慢操作（加上 ▲ 紅色警示標籤）
    slowest_idx = df["耗時(s)"].idxmax()
    slowest_patch = ax1.patches[slowest_idx]
    ax1.annotate(
        "▲ 最慢",
        xy=(slowest_patch.get_x() + slowest_patch.get_width() / 2,
            slowest_patch.get_height()),
        xytext=(0, 28), textcoords="offset points",
        ha="center", fontsize=9, color="#CC0000", fontweight="bold",
        arrowprops=dict(arrowstyle="-|>", color="#CC0000", lw=1.2),
    )
    ax1.set_title("Task 1/2 Function Runtime Comparison\nTask 1/2 各函式執行耗時比較",
                  fontsize=13, fontweight="bold", pad=12)
    ax1.set_xlabel("Function（函式）", fontsize=11)
    ax1.set_ylabel("Runtime / 耗時（秒）", fontsize=11)
    ax1.set_ylim(0, df["耗時(s)"].max() * 1.40)
    ax1.legend(title="所屬任務", loc="upper right", framealpha=0.85)
    sns.despine(ax=ax1, left=False, bottom=False)

    # ── 下圖（Bonus 3）：讀取 vs 寫入 分組平均耗時比較 ─────
    ax2 = axes[1]
    bars2 = sns.barplot(
        data=df_grouped, x="操作類型", y="平均耗時(s)",
        hue="操作類型", palette=TYPE_PALETTE, width=0.45, ax=ax2, legend=False,
    )
    for patch, (_, row) in zip(ax2.patches, df_grouped.iterrows()):
        h = patch.get_height()
        ax2.text(
            patch.get_x() + patch.get_width() / 2,
            h + df_grouped["平均耗時(s)"].max() * 0.025,
            f"均值 {h:.5f}s",
            ha="center", va="bottom", fontsize=10, fontweight="bold", color="#333333",
        )
    ax2.set_title("Bonus 延伸：讀取 vs 寫入 — 跨 Task 平均耗時分組比較",
                  fontsize=11, fontweight="bold", pad=10)
    ax2.set_xlabel("操作類型（讀取 / 寫入）", fontsize=11)
    ax2.set_ylabel("平均耗時（秒）", fontsize=11)
    ax2.set_ylim(0, df_grouped["平均耗時(s)"].max() * 1.40)
    # 手動加上圖例色塊
    patches = [mpatches.Patch(color=v, label=k) for k, v in TYPE_PALETTE.items()]
    ax2.legend(handles=patches, title="操作類型", loc="upper right", framealpha=0.85)
    sns.despine(ax=ax2, left=False, bottom=False)

    # ── Bonus 3：結論摘要文字方塊（底部） ──────────────────
    fastest = df.loc[df["耗時(s)"].idxmin(), "函式"]
    slowest = df.loc[df["耗時(s)"].idxmax(), "函式"]
    read_avg  = df_grouped.loc[df_grouped["操作類型"] == "讀取", "平均耗時(s)"].values[0]
    write_avg = df_grouped.loc[df_grouped["操作類型"] == "寫入", "平均耗時(s)"].values[0]
    faster_op = "讀取" if read_avg < write_avg else "寫入"

    summary = (
        f"[結論摘要] 最快操作：{fastest}　最慢操作：{slowest}\n"
        f"跨 Task 比較：{faster_op}操作的平均耗時較低（讀取均值 {read_avg:.5f}s，寫入均值 {write_avg:.5f}s）\n"
        f"資料量僅 189 筆，各函式差距極小（< 0.001s），放大至萬筆後 write_xml 預期成長最快"
    )
    fig.text(
        0.5, -0.01, summary,
        ha="center", va="top", fontsize=9.2, color="#444444",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#F0F4F8", edgecolor="#AAAAAA", alpha=0.9),
    )

    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"圖表已儲存：{output_path}")


if __name__ == "__main__":
    plot_timing(df, df_grouped, str(OUTPUT_PNG))
