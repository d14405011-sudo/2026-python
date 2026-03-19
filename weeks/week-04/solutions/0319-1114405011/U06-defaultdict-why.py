# U6. defaultdict 為何比手動初始化乾淨（1.6）
#
# 問題：使用普通 dict 時，若 key 不存在會拋出 KeyError
# 解決方案：defaultdict 會為不存在的 key 自動創建預設值
# 優勢：
# - 程式碼更簡潔，減少 if 判斷
# - 提高可讀性，意圖更清晰

from collections import defaultdict


def main() -> None:
    # ==============================================================
    # 1) 普通 dict 的問題
    # ==============================================================
    print('1) 普通 dict 的問題：')
    
    d = {}
    print(f'   d = {{}}')
    print(f'   嘗試 d["a"] 取得不存在的 key:')
    try:
        print(f'   d["a"] = {d["a"]}')
    except KeyError as e:
        print(f'   ✗ KeyError: {e}')

    print()

    # ==============================================================
    # 2) 手動初始化的方法（冗長）
    # ==============================================================
    print('2) 手動初始化的方法（要先判斷 key 是否存在）:')

    pairs = [('a', 1), ('a', 2), ('b', 3)]
    print(f'   對 pairs = {pairs} 進行分組')

    # 手動版：一直判斷 key 是否存在
    d = {}
    for k, v in pairs:
        if k not in d:
            d[k] = []
        d[k].append(v)

    print(f'   手動初始化結果: {dict(d)}')
    print(f'   程式碼需要三行：if 判斷、初始化、追加')

    print()

    # ==============================================================
    # 3) 使用 defaultdict（乾淨簡潔）
    # ==============================================================
    print('3) 使用 defaultdict（自動創建預設值）:')

    # defaultdict：省掉初始化分支
    d2 = defaultdict(list)
    print(f'   d2 = defaultdict(list)')

    for k, v in pairs:
        d2[k].append(v)  # 不需要 if 判斷！

    print(f'   處理結果: {dict(d2)}')
    print(f'   程式碼只需一行：直接追加')

    print()

    # ==============================================================
    # 4) defaultdict 的不同工廠函式
    # ==============================================================
    print('4) defaultdict 的不同工廠函式:')

    # defaultdict(list) - 預設是空列表
    dd_list = defaultdict(list)
    dd_list['key'].append('value')
    print(f'   defaultdict(list)[新 key] = {list(dd_list["key"])}')

    # defaultdict(int) - 預設是 0
    dd_int = defaultdict(int)
    dd_int['count'] += 1
    dd_int['count'] += 1
    print(f'   defaultdict(int)[新 key] = {dd_int["count"]}')

    # defaultdict(set) - 預設是空 set
    dd_set = defaultdict(set)
    dd_set['tags'].add('python')
    print(f'   defaultdict(set)[新 key] = {dd_set["tags"]}')

    # defaultdict(dict) - 預設是空 dict
    dd_dict = defaultdict(dict)
    dd_dict['info']['name'] = 'Alice'
    print(f'   defaultdict(dict)[新 key] = {dict(dd_dict["info"])}')

    print()

    # ==============================================================
    # 5) 實務應用：詞頻統計
    # ==============================================================
    print('5) 實務應用：詞頻統計')

    # 文本
    text = 'apple banana apple cherry apple banana'
    words = text.split()
    print(f'   文本: "{text}"')

    # 使用 defaultdict(int) 計算詞頻
    word_count = defaultdict(int)
    for word in words:
        word_count[word] += 1

    print(f'   詞頻統計:')
    for word, count in sorted(word_count.items(), key=lambda x: x[1], reverse=True):
        print(f'     {word}: {count}')

    print()

    # ==============================================================
    # 6) 實務應用：分組
    # ==============================================================
    print('6) 實務應用：分組')

    students = [
        ('Alice', '一班'),
        ('Bob', '二班'),
        ('Charlie', '一班'),
        ('David', '二班'),
        ('Eve', '三班'),
    ]
    print(f'   學生列表: {students}')

    # 按班級分組
    classes = defaultdict(list)
    for name, class_num in students:
        classes[class_num].append(name)

    print(f'   按班級分組:')
    for class_num in sorted(classes.keys()):
        print(f'     {class_num}: {classes[class_num]}')

    print()

    # ==============================================================
    # 7) 自訂工廠函式
    # ==============================================================
    print('7) 自訂工廠函式:')

    # 使用 lambda 作為工廠函式
    dd_default_0 = defaultdict(lambda: 0)
    dd_default_empty_str = defaultdict(lambda: 'N/A')

    print(f'   defaultdict(lambda: 0)[新 key] = {dd_default_0["missing"]}')
    print(f'   defaultdict(lambda: "N/A")[新 key] = {dd_default_empty_str["missing"]}')


if __name__ == '__main__':
    main()
