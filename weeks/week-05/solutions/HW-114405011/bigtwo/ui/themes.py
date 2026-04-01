# -*- coding: utf-8 -*-
"""
遊戲主題配置系統
支持多種視覺風格主題
"""

THEMES = {
    'winter': {
        'name': '冬季夜晚',
        'description': '深藍夜空 + 暖金光斑',
        'bg_top': (18, 35, 52),           # 深夜藍
        'bg_bottom': (8, 18, 32),         # 更深的夜藍
        'felt_line': (35, 72, 100),       # 棋盤線
        'glow_color': (255, 200, 80),     # 金色光斑
        'glow_alpha': 32,
        'card_back': (45, 108, 165),      # 深藍卡背
        'card_back_dark': (28, 72, 115),
        'button_primary': (200, 150, 60), # 金色按鈕
        'button_hover': (220, 170, 80),
    },
    'neon': {
        'name': '霓光未來',
        'description': '賽博朋克風格',
        'bg_top': (25, 15, 45),           # 深紫
        'bg_bottom': (10, 25, 45),        # 深青藍
        'felt_line': (80, 40, 120),       # 紫線
        'glow_color': (100, 255, 200),    # 青綠霓光
        'glow_alpha': 28,
        'card_back': (60, 45, 120),       # 紫藍卡背
        'card_back_dark': (40, 25, 85),
        'button_primary': (100, 200, 255),# 青藍按鈕
        'button_hover': (150, 220, 255),
    },
    'summer': {
        'name': '夏日明朗',
        'description': '清爽明亮風格',
        'bg_top': (70, 130, 180),         # 亮藍
        'bg_bottom': (100, 160, 210),     # 淺藍
        'felt_line': (60, 120, 180),      # 藍線
        'glow_color': (255, 220, 100),    # 暖黃光
        'glow_alpha': 24,
        'card_back': (100, 150, 200),     # 淺藍卡背
        'card_back_dark': (70, 110, 160),
        'button_primary': (60, 160, 220), # 淺藍按鈕
        'button_hover': (100, 180, 240),
    },
    'default': {
        'name': '經典深藍',
        'description': '原始配色',
        'bg_top': (22, 44, 63),
        'bg_bottom': (11, 27, 45),
        'felt_line': (28, 63, 83),
        'glow_color': (74, 144, 217),
        'glow_alpha': 24,
        'card_back': (58, 131, 198),
        'card_back_dark': (39, 94, 152),
        'button_primary': (34, 140, 201),
        'button_hover': (20, 168, 233),
    },
    'dark_purple': {
        'name': '黑紫帝王',
        'description': '高級深紫 + 粉紫光效',
        'bg_top': (35, 5, 45),            # 深紫黑
        'bg_bottom': (15, 10, 35),        # 更深紫黑
        'felt_line': (60, 20, 80),        # 紫線
        'glow_color': (255, 100, 200),    # 粉紫光
        'glow_alpha': 35,
        'card_back': (70, 30, 100),       # 深紫卡
        'card_back_dark': (45, 15, 65),
        'button_primary': (200, 80, 150), # 粉紫按鈕
        'button_hover': (220, 120, 170),
    },
    'tech_green': {
        'name': '科技綠幕',
        'description': '駭客電影風格',
        'bg_top': (5, 40, 15),            # 深綠黑
        'bg_bottom': (2, 20, 8),          # 深黑綠
        'felt_line': (20, 80, 40),        # 亮綠線
        'glow_color': (0, 255, 100),      # 亮綠光
        'glow_alpha': 40,
        'card_back': (25, 80, 50),        # 綠卡背
        'card_back_dark': (15, 50, 30),
        'button_primary': (0, 200, 100),  # 亮綠按鈕
        'button_hover': (50, 255, 150),
    },
    'royal_gold': {
        'name': '皇金璀璨',
        'description': '奢華金色 + 暗紅光',
        'bg_top': (40, 30, 20),           # 深棕金
        'bg_bottom': (20, 15, 10),        # 深棕黑
        'felt_line': (80, 60, 40),        # 金線
        'glow_color': (255, 180, 0),      # 皇金光
        'glow_alpha': 38,
        'card_back': (100, 70, 40),       # 金棕卡
        'card_back_dark': (60, 40, 20),
        'button_primary': (220, 150, 0),  # 皇金按鈕
        'button_hover': (255, 200, 50),
    },
    'sunset': {
        'name': '夕陽火燒',
        'description': '溫暖夕陽風格',
        'bg_top': (50, 30, 10),           # 深橙紅
        'bg_bottom': (100, 40, 10),       # 更深紅
        'felt_line': (150, 70, 30),       # 橙線
        'glow_color': (255, 150, 50),     # 橙紅光
        'glow_alpha': 36,
        'card_back': (120, 60, 30),       # 深橙卡
        'card_back_dark': (80, 35, 15),
        'button_primary': (200, 100, 30), # 橙紅按鈕
        'button_hover': (230, 140, 60),
    },
}

def get_theme(theme_name='default'):
    """取得指定主題配置"""
    return THEMES.get(theme_name, THEMES['default']).copy()

def get_all_themes():
    """取得所有可用主題名稱"""
    return list(THEMES.keys())
