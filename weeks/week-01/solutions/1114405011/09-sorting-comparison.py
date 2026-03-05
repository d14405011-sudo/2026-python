# 9 比較、排序與 key 函式範例
# 這支程式示範三件事：
# 1) Python 的比較規則（以 tuple 為例）
# 2) sorted(..., key=...) 的排序技巧
# 3) min/max 搭配 key 找出最小與最大項目


def demo_tuple_comparison():
    # tuple 會由左到右逐一比較元素
    a = (1, 2)
    b = (1, 3)
    result = a < b

    print("[比較] a:", a)
    print("[比較] b:", b)
    print("[比較] a < b ->", result)


def demo_sort_with_key():
    rows = [{"uid": 3}, {"uid": 1}, {"uid": 2}]

    # key 函式指定「用哪個欄位當排序依據」
    rows_sorted = sorted(rows, key=lambda r: r["uid"])
    rows_sorted_desc = sorted(rows, key=lambda r: r["uid"], reverse=True)

    print("[排序] 原始資料:", rows)
    print("[排序] 依 uid 由小到大:", rows_sorted)
    print("[排序] 依 uid 由大到小:", rows_sorted_desc)


def demo_min_max_with_key():
    rows = [{"uid": 3}, {"uid": 1}, {"uid": 2}]

    # min/max 搭配 key，可以在複雜資料中找極值
    smallest = min(rows, key=lambda r: r["uid"])
    largest = max(rows, key=lambda r: r["uid"])

    print("[極值] uid 最小:", smallest)
    print("[極值] uid 最大:", largest)


def main():
    print("=== 比較、排序與 key 函式範例 ===")
    demo_tuple_comparison()
    demo_sort_with_key()
    demo_min_max_with_key()


if __name__ == "__main__":
    main()
