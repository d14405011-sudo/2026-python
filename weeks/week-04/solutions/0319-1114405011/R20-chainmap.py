# R20. ChainMap 合併映射（1.20）

from collections import ChainMap


def main() -> None:
    # ==============================================================
    # ChainMap 的概念
    # ==============================================================
    # ChainMap 將多個字典「串聯」起來，提供統一的查詢視圖。
    # 特色：
    # - 不真的合併字典，只建立一個視圖
    # - 搜尋順序：第一個字典 -> 第二個 -> ...
    # - 修改時影響第一個字典，查詢時依序檢查
    # - 常用於配置文件層級覆蓋場景(如: 環境變數 > 設定檔 > 預設值)

    # ==============================================================
    # 1) 基本用法：多層字典查詢
    # ==============================================================
    a = {'x': 1, 'z': 3}
    b = {'y': 2, 'z': 4}
    c = ChainMap(a, b)

    print('1) 基本用法：ChainMap 的多層查詢')
    print(f'   a = {a}')
    print(f'   b = {b}')
    print(f'   c = ChainMap(a, b)')
    print(f'   c[\'x\'] = {c["x"]}  (來自 a)')
    print(f'   c[\'y\'] = {c["y"]}  (來自 b)')
    print(f'   c[\'z\'] = {c["z"]}  (來自 a，因為 a 優先度高)')

    # ==============================================================
    # 2) 搜尋順序演示
    # ==============================================================
    # 當存在相同鍵時，優先使用前面的字典（優先度高）
    config_default = {'timeout': 30, 'retries': 3, 'debug': False}
    config_user = {'timeout': 60, 'debug': True}
    config_combined = ChainMap(config_user, config_default)

    print('\n2) 搜尋順序演示（配置文件場景）:')
    print(f'   config_default = {config_default}')
    print(f'   config_user = {config_user}')
    print(f'   config_combined = ChainMap(config_user, config_default)')
    print(f'   config_combined[\'timeout\'] = {config_combined["timeout"]}  (來自 config_user)')
    print(f'   config_combined[\'retries\'] = {config_combined["retries"]}  (來自 config_default)')
    print(f'   config_combined[\'debug\'] = {config_combined["debug"]}  (來自 config_user)')

    # ==============================================================
    # 3) ChainMap 是視圖，不是合併副本
    # ==============================================================
    # 修改原始字典會影響 ChainMap 的查詢結果
    dict1 = {'a': 1}
    dict2 = {'b': 2}
    chain = ChainMap(dict1, dict2)

    print('\n3) ChainMap 是視圖，不是合併副本:')
    print(f'   dict1 = {dict1}')
    print(f'   dict2 = {dict2}')
    print(f'   chain = ChainMap(dict1, dict2)')
    print(f'   chain[\'a\'] = {chain["a"]}')

    dict1['a'] = 10
    print(f'   修改後: dict1[\'a\'] = 10')
    print(f'   chain[\'a\'] = {chain["a"]}  (反映了修改)')

    # ==============================================================
    # 4) 修改 ChainMap 會影響第一個字典
    # ==============================================================
    chain['a'] = 100
    print(f'   修改 chain[\'a\'] = 100')
    print(f'   dict1[\'a\'] = {dict1["a"]}  (第一個字典被修改)')
    print(f'   dict2 = {dict2}  (第二個字典未變)')

    # ==============================================================
    # 5) ChainMap vs dict.update()（淺合併）
    # ==============================================================
    # ChainMap：視圖，保持原字典獨立
    # dict.update()：產生新字典，原字典不受影響
    
    user_config = {'host': 'localhost', 'port': 8080}
    default_config = {'host': '0.0.0.0', 'port': 5000, 'timeout': 30}

    # 方法 1：使用 ChainMap
    chain_view = ChainMap(user_config, default_config)

    # 方法 2：使用 dict.update()
    merged_dict = default_config.copy()
    merged_dict.update(user_config)

    print('\n5) ChainMap vs dict.update():')
    print(f'   user_config = {user_config}')
    print(f'   default_config = {default_config}')
    print()
    print(f'   ChainMap 方式: {dict(chain_view)}')
    print(f'   update() 方式: {merged_dict}')
    print()
    print(f'   兩者結果相同，但 ChainMap 不修改原字典、記憶體效率較高')

    # ==============================================================
    # 6) 實務應用：三層配置級聯
    # ==============================================================
    # 常見場景: 環境變數 > 使用者設定 > 預設值
    defaults = {'db': 'sqlite', 'log_level': 'INFO', 'workers': 4}
    user_settings = {'db': 'postgres', 'workers': 8}
    env_override = {'log_level': 'DEBUG'}

    config = ChainMap(env_override, user_settings, defaults)

    print('\n6) 實務應用：三層配置級聯:')
    print(f'   defaults = {defaults}')
    print(f'   user_settings = {user_settings}')
    print(f'   env_override = {env_override}')
    print(f'   config = ChainMap(env_override, user_settings, defaults)')
    print()
    print(f'   config[\'db\'] = {config["db"]}  (來自 user_settings)')
    print(f'   config[\'log_level\'] = {config["log_level"]}  (來自 env_override)')
    print(f'   config[\'workers\'] = {config["workers"]}  (來自 user_settings)')

    # ==============================================================
    # 7) ChainMap 的常用方法
    # ==============================================================
    cm = ChainMap({'a': 1}, {'b': 2}, {'c': 3})

    print('\n7) ChainMap 的常用方法:')
    print(f'   cm = ChainMap({{"a": 1}}, {{"b": 2}}, {{"c": 3}})')
    print(f'   cm.maps = {cm.maps}  (所有底層字典)')
    print(f'   list(cm.keys()) = {list(cm.keys())}')
    print(f'   list(cm.values()) = {list(cm.values())}')
    print(f'   dict(cm) = {dict(cm)}  (轉成普通 dict)')


if __name__ == '__main__':
    main()
