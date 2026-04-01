# -*- coding: utf-8 -*-
import math
import pygame
from ui.themes import get_theme

class Renderer:
    """Game renderer."""
    # 基礎顏色（跨主題通用）
    COLORS = {
        'spade_club': (40, 44, 52),
        'heart_diamond': (220, 86, 76),
        'player': (245, 196, 54),
        'ai': (176, 193, 206),
        'selected': (246, 204, 70),
        'panel_bg': (12, 24, 39, 180),
        'panel_border': (78, 108, 132),
        'button_disabled': (88, 113, 133),
        'text_primary': (240, 244, 250),
        'text_muted': (176, 193, 206)
    }
    CARD_WIDTH = 68
    CARD_HEIGHT = 100
    TEXT_FONT_CANDIDATES = [
        "Microsoft JhengHei",
        "微軟正黑體",
        "Microsoft YaHei",
        "SimHei",
        "Arial Unicode MS",
    ]
    CARD_FONT_CANDIDATES = [
        "Times New Roman",
        "Georgia",
        "PMingLiU",
        "MingLiU",
        "Noto Serif CJK TC",
        "Arial Unicode MS",
        "Microsoft JhengHei",
    ]

    def __init__(self, width=800, height=600, theme='default'):
        self.width = width
        self.height = height
        self.theme = get_theme(theme)
        self.background_style = 'diagonal'  # diagonal | grid | clean
        self.table_style = 'blue'           # blue | green | red
        self.card_back_style = 'ring'       # ring | diamond | minimal
        
        # 背景緩存機制
        self._background_cache = None
        self._cache_key = None  # 追蹤緩存對應的設定（width, height, theme, style等）
        
        # 合併主題顏色到 COLORS
        self.COLORS.update({
            'bg_top': self.theme['bg_top'],
            'bg_bottom': self.theme['bg_bottom'],
            'felt_line': self.theme['felt_line'],
            'card_back': self.theme['card_back'],
            'card_back_dark': self.theme['card_back_dark'],
            'button': self.theme['button_primary'],
            'button_hover': self.theme['button_hover'],
        })
        self.glow_color = self.theme['glow_color']
        self.glow_alpha = self.theme['glow_alpha']
        self.font = self._load_font(21, candidates=self.TEXT_FONT_CANDIDATES)
        self.small_font = self._load_font(17, candidates=self.TEXT_FONT_CANDIDATES)
        self.title_font = self._load_font(34, bold=True, candidates=self.TEXT_FONT_CANDIDATES)
        self.rank_font = self._load_font(32, bold=True, candidates=self.CARD_FONT_CANDIDATES)
        self.rank_small_font = self._load_font(20, bold=True, candidates=self.CARD_FONT_CANDIDATES)
        self._suit_font_cache = {}
        self._mini_rank_font_cache = {}

    def set_background_style(self, style_name='diagonal'):
        if style_name in ('diagonal', 'grid', 'clean'):
            self.background_style = style_name
            self._cache_key = None  # 標記緩存失效

    def set_table_style(self, style_name='blue'):
        if style_name in ('blue', 'green', 'red'):
            self.table_style = style_name
            self._cache_key = None  # 標記緩存失效

    def set_card_back_style(self, style_name='ring'):
        if style_name in ('ring', 'diamond', 'minimal'):
            self.card_back_style = style_name

    def _load_font(self, size, bold=False, candidates=None):
        if candidates is None:
            candidates = self.TEXT_FONT_CANDIDATES
        for name in candidates:
            matched = pygame.font.match_font(name, bold=bold)
            if matched:
                return pygame.font.Font(matched, size)
        return pygame.font.Font(None, size)

    def set_theme(self, theme_name='default'):
        """運行時切換主題"""
        self.theme = get_theme(theme_name)
        self.COLORS.update({
            'bg_top': self.theme['bg_top'],
            'bg_bottom': self.theme['bg_bottom'],
            'felt_line': self.theme['felt_line'],
            'card_back': self.theme['card_back'],
            'card_back_dark': self.theme['card_back_dark'],
            'button': self.theme['button_primary'],
            'button_hover': self.theme['button_hover'],
        })
        self.glow_color = self.theme['glow_color']
        self.glow_alpha = self.theme['glow_alpha']
        self._cache_key = None  # 主題改變時失效緩存

    def update_size(self, width, height):
        self.width = width
        self.height = height
        base_size = max(18, min(24, width // 46))
        title_size = max(28, min(42, width // 26))
        self.font = self._load_font(base_size, candidates=self.TEXT_FONT_CANDIDATES)
        self.small_font = self._load_font(max(15, base_size - 3), candidates=self.TEXT_FONT_CANDIDATES)
        self.title_font = self._load_font(title_size, bold=True, candidates=self.TEXT_FONT_CANDIDATES)
        self.rank_font = self._load_font(max(28, base_size + 10), bold=True, candidates=self.CARD_FONT_CANDIDATES)
        self.rank_small_font = self._load_font(max(18, base_size - 1), bold=True, candidates=self.CARD_FONT_CANDIDATES)
        self._cache_key = None  # 視窗大小改變時失效緩存

    def draw_table_background(self, screen):
        """繪製表格背景（使用 Surface 緩存優化效能）"""
        
        # 生成緩存鍵，用於判斷是否需要重新繪製靜態部分
        current_key = (
            self.width, self.height, 
            self.table_style, self.background_style,
            id(self.COLORS['bg_top']), id(self.COLORS['bg_bottom']),
            id(self.COLORS['felt_line'])
        )
        
        # 如果緩存不存在或參數改變，重新繪製靜態背景
        if self._background_cache is None or self._cache_key != current_key:
            self._background_cache = pygame.Surface((self.width, self.height))
            
            # === 靜態部分：漸層背景 ===
            for y in range(self.height):
                t = y / max(1, self.height - 1)
                r = int(self.COLORS['bg_top'][0] * (1 - t) + self.COLORS['bg_bottom'][0] * t)
                g = int(self.COLORS['bg_top'][1] * (1 - t) + self.COLORS['bg_bottom'][1] * t)
                b = int(self.COLORS['bg_top'][2] * (1 - t) + self.COLORS['bg_bottom'][2] * t)
                pygame.draw.line(self._background_cache, (r, g, b), (0, y), (self.width, y))

            # 桌布色調覆蓋（可切換）
            tint_map = {
                'blue': (25, 72, 115, 26),
                'green': (18, 92, 58, 36),
                'red': (112, 36, 44, 34),
            }
            tint = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            tint.fill(tint_map.get(self.table_style, tint_map['blue']))
            self._background_cache.blit(tint, (0, 0))

            # 背景紋理（可切換）
            line_color = self.COLORS['felt_line']
            if self.background_style == 'diagonal':
                spacing = 44
                for x in range(-self.height, self.width, spacing):
                    pygame.draw.line(self._background_cache, line_color, (x, 0), (x + self.height, self.height), 1)
            elif self.background_style == 'grid':
                spacing = 52
                for x in range(0, self.width, spacing):
                    pygame.draw.line(self._background_cache, line_color, (x, 0), (x, self.height), 1)
                for y in range(0, self.height, spacing):
                    pygame.draw.line(self._background_cache, line_color, (0, y), (self.width, y), 1)
            else:  # clean
                spacing = 80
                dot = pygame.Surface((8, 8), pygame.SRCALPHA)
                pygame.draw.circle(dot, (*line_color, 80), (4, 4), 2)
                for x in range(0, self.width, spacing):
                    for y in range(0, self.height, spacing):
                        self._background_cache.blit(dot, (x, y))

            # 邊界高亮
            pygame.draw.line(self._background_cache, self.COLORS['felt_line'], (0, 0), (self.width, 0), 2)
            pygame.draw.line(self._background_cache, (*self.COLORS['bg_bottom'], 100), (0, self.height - 1), (self.width, self.height - 1), 2)
            
            self._cache_key = current_key

        # 將緩存的背景繪製到螢幕
        screen.blit(self._background_cache, (0, 0))

        # === 動態部分：動畫光斑效果（每幀更新） ===
        ticks = pygame.time.get_ticks() / 1000.0
        for i in range(6):  # 6層光斑
            # 動畫路徑參數
            offset_x = math.sin(ticks + i * 0.5) * 40
            offset_y = math.cos(ticks * 0.7 + i * 0.4) * 30
            
            cx = int(self.width * (0.15 + i * 0.15) + offset_x)
            cy = int(self.height * (0.25 + (i % 3) * 0.25) + offset_y)
            
            radius = 48 + (i * 4)
            # 創建漸層光暈
            glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            # 多層漸層
            for r in range(radius, 0, -4):
                alpha = int(self.glow_alpha * (1 - (radius - r) / radius) * 0.8)
                pygame.draw.circle(glow, (*self.glow_color, alpha), (radius, radius), r)
            
            # 確保光暈完全在屏幕內
            screen.blit(glow, (cx - radius, cy - radius))

    def _rank_text(self, rank_val):
        if rank_val == 14:
            return "A"
        if rank_val == 11:
            return "J"
        if rank_val == 12:
            return "Q"
        if rank_val == 13:
            return "K"
        if rank_val == 15:
            return "2"
        return str(rank_val)

    def _suit_text(self, suit):
        return ["♣", "♦", "♥", "♠"][suit]

    def _suit_color(self, suit):
        # 圖二風格：黑桃/梅花深色，紅心/方塊紅色。
        if suit in (3, 0):  # spade, club
            return (33, 26, 28)
        return (219, 77, 68)

    def _draw_suit_symbol(self, screen, suit, color, center, size):
        # 使用標準 Unicode 花色字元，風格接近圖二。
        glyph = self._suit_text(suit)
        font_size = max(18, size + 4)
        suit_font = self._suit_font_cache.get(font_size)
        if suit_font is None:
            suit_font = self._load_font(font_size, bold=True, candidates=self.CARD_FONT_CANDIDATES)
            self._suit_font_cache[font_size] = suit_font
        symbol = suit_font.render(glyph, True, color)
        rect = symbol.get_rect(center=center)
        screen.blit(symbol, rect)

    def draw_card(self, screen, card, x: int, y: int, selected: bool = False):
        lift = 18 if selected else 0
        y -= lift

        # 增強的陰影效果
        shadow = pygame.Surface((self.CARD_WIDTH + 8, self.CARD_HEIGHT + 8), pygame.SRCALPHA)
        # 多層陰影 - 增加深度感
        for i in range(3, 0, -1):
            alpha = 60 - i * 15
            pygame.draw.rect(shadow, (0, 0, 0, alpha), 
                           pygame.Rect(i, i, self.CARD_WIDTH + 8 - i*2, self.CARD_HEIGHT + 8 - i*2),
                           border_radius=8)
        screen.blit(shadow, (x - 4, y - 4))

        # 卡牌主體
        rect = pygame.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)
        pygame.draw.rect(screen, (253, 253, 252), rect, border_radius=8)
        
        # 增強的邊框 - 雙層邊框
        pygame.draw.rect(screen, (180, 190, 200), rect, 2, border_radius=8)
        pygame.draw.rect(screen, (164, 173, 182), rect, 1, border_radius=8)

        # 選中狀態 - 更加突出
        if selected:
            glow_rect = rect.inflate(8, 8)
            pygame.draw.rect(screen, (*self.COLORS['selected'], 80), glow_rect.move(-4, -4), 0, border_radius=12)
            pygame.draw.rect(screen, self.COLORS['selected'], glow_rect, 4, border_radius=12)

        # 卡牌內容
        color = self._suit_color(card.suit)
        rank_str = self._rank_text(card.rank)

        # 頂部花色 - 改進排版
        rank_small = self.rank_small_font.render(rank_str, True, color)
        screen.blit(rank_small, (x + 6, y + 3))
        self._draw_suit_symbol(screen, card.suit, color, (x + 16, y + 34), 14)

        # 中央和底部花色
        rank_big = self.rank_font.render(rank_str, True, color)
        right_x = x + self.CARD_WIDTH - rank_big.get_width() - 6
        screen.blit(rank_big, (right_x, y + self.CARD_HEIGHT - 50))
        self._draw_suit_symbol(screen, card.suit, color, (x + self.CARD_WIDTH - 15, y + self.CARD_HEIGHT - 14), 14)

    def draw_mini_card(
        self,
        screen,
        rank_text: str,
        suit: int,
        x: int,
        y: int,
        width: int = 46,
        height: int = 64,
    ):
        """繪製說明面板用的小型示意牌。"""
        if width < 20 or height < 28:
            return
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (249, 250, 252), rect, border_radius=6)
        pygame.draw.rect(screen, (170, 181, 193), rect, 1, border_radius=6)

        color = self._suit_color(suit)
        mini_rank_size = max(12, int(height * 0.30))
        mini_rank_font = self._mini_rank_font_cache.get(mini_rank_size)
        if mini_rank_font is None:
            mini_rank_font = self._load_font(mini_rank_size, bold=True, candidates=self.CARD_FONT_CANDIDATES)
            self._mini_rank_font_cache[mini_rank_size] = mini_rank_font
        rank = mini_rank_font.render(rank_text, True, color)
        screen.blit(rank, (x + 4, y + 2))
        self._draw_suit_symbol(screen, suit, color, (x + width // 2, y + (height // 2) + 4), max(12, int(height * 0.22)))

    def draw_card_back(self, screen, x, y, horizontal=True):
        w = self.CARD_WIDTH if horizontal else self.CARD_HEIGHT
        h = self.CARD_HEIGHT if horizontal else self.CARD_WIDTH
        rect = pygame.Rect(x, y, w, h)
        
        # 卡牌背景漸層
        pygame.draw.rect(screen, (238, 244, 249), rect, border_radius=8)
        inner = rect.inflate(-4, -4)
        pygame.draw.rect(screen, self.COLORS['card_back'], inner, border_radius=7)
        pygame.draw.rect(screen, self.COLORS['card_back_dark'], inner, 2, border_radius=7)

        # 卡背圖樣（可切換）
        cx, cy = inner.center
        if self.card_back_style == 'ring':
            corner = (inner.x + 6, inner.y + 6, 10, 10)
            pygame.draw.arc(screen, (200, 230, 255), corner, 0.0, 1.57, 2)
            corner2 = (inner.right - 16, inner.bottom - 16, 10, 10)
            pygame.draw.arc(screen, (200, 230, 255), corner2, 3.14, 4.71, 2)
            for i in range(5):
                radius = 6 + i * 5
                alpha = max(12, 255 - i * 40)
                pygame.draw.circle(screen, (255, 255, 255, alpha)[:3], (cx, cy), radius, 1)
        elif self.card_back_style == 'diamond':
            step = 10
            pattern_color = (215, 235, 250)
            for px in range(inner.x + 6, inner.right - 4, step):
                for py in range(inner.y + 6, inner.bottom - 4, step):
                    diamond = [
                        (px, py - 2),
                        (px + 2, py),
                        (px, py + 2),
                        (px - 2, py),
                    ]
                    pygame.draw.polygon(screen, pattern_color, diamond, 1)
            pygame.draw.rect(screen, (230, 243, 252), inner.inflate(-12, -12), 1, border_radius=6)
        else:  # minimal
            pygame.draw.rect(screen, (230, 243, 252), inner.inflate(-10, -10), 2, border_radius=6)
            pygame.draw.line(screen, (220, 238, 250), (inner.x + 10, cy), (inner.right - 10, cy), 1)
            pygame.draw.line(screen, (220, 238, 250), (cx, inner.y + 10), (cx, inner.bottom - 10), 1)

        # 邊框高亮 - 增加立體感
        pygame.draw.rect(screen, (255, 255, 255, 80), (inner.x, inner.y, inner.width, 2), border_radius=7)

    def draw_icon_button(self, screen, rect, icon_text, mouse_pos, active=False):
        base = (38, 92, 132) if not active else (54, 129, 171)
        hover = (62, 142, 189)
        color = hover if rect.collidepoint(mouse_pos) else base
        pygame.draw.ellipse(screen, color, rect)
        pygame.draw.ellipse(screen, (206, 224, 238), rect, 2)
        label = self.title_font.render(icon_text, True, (238, 246, 252))
        screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2 - 1))

    def draw_hand(self, screen, hand, x, y, selected_indices, spacing=28, cursor_index=None):
        for i, card in enumerate(hand):
            self.draw_card(screen, card, x + i * spacing, y, i in selected_indices)
            if cursor_index is not None and i == cursor_index:
                indicator = pygame.Rect(x + i * spacing + 8, y + self.CARD_HEIGHT + 4, self.CARD_WIDTH - 16, 5)
                pygame.draw.rect(screen, self.COLORS['selected'], indicator, border_radius=2)

    def draw_player(self, screen, player, x, y, is_current, card_count=0, is_top=False, is_side=False):
        panel_w = 204 if player.is_ai else 220
        panel_h = 68
        panel_x = max(10, min(x, self.width - panel_w - 10))
        panel = pygame.Rect(panel_x, y - 52, panel_w, panel_h)
        layer = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
        layer.fill(self.COLORS['panel_bg'])
        screen.blit(layer, panel.topleft)
        border_color = self.COLORS['selected'] if is_current else self.COLORS['panel_border']
        pygame.draw.rect(screen, border_color, panel, 2, border_radius=12)

        name_color = self.COLORS['player'] if not player.is_ai else self.COLORS['ai']
        if is_current:
            name_color = self.COLORS['selected']
        txt = self.font.render(player.name, True, name_color)
        screen.blit(txt, (panel.x + 14, panel.y + 9))

        badge_text = self.small_font.render(f"剩 {card_count} 張", True, self.COLORS['text_primary'])
        badge_w = badge_text.get_width() + 12
        badge_x = max(panel.x + 78, panel.right - badge_w - 12)
        badge = pygame.Rect(badge_x, panel.y + 12, badge_w, 24)
        pygame.draw.rect(screen, (34, 55, 73), badge, border_radius=7)
        pygame.draw.rect(screen, (78, 108, 132), badge, 1, border_radius=7)
        screen.blit(badge_text, (badge.x + 5, badge.y + 2))

        if player.is_ai:
            if is_top:
                spacing = 22
                for i in range(card_count):
                    self.draw_card_back(screen, x + i * spacing, y, horizontal=True)
            else:
                spacing = 17
                for i in range(card_count):
                    self.draw_card_back(screen, x, y + i * spacing, horizontal=False)

    def draw_last_play(self, screen, cards, player_name, x, y, play_type_text=""):
        if not cards:
            return
        title = self.font.render(f"上一手: {player_name}", True, self.COLORS['text_primary'])
        type_label = self.small_font.render(play_type_text, True, self.COLORS['text_muted']) if play_type_text else None
        panel_w = max(280, 36 * len(cards) + 90)
        panel_h = 170
        panel = pygame.Rect(x - 16, y - 52, panel_w, panel_h)
        layer = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
        layer.fill((11, 24, 39, 178))
        screen.blit(layer, panel.topleft)
        pygame.draw.rect(screen, self.COLORS['panel_border'], panel, 2, border_radius=12)

        screen.blit(title, (panel.x + 14, panel.y + 10))
        if type_label:
            screen.blit(type_label, (panel.x + 14, panel.y + 36))

        for i, card in enumerate(cards):
            self.draw_card(screen, card, x + i * 36, y)

    def draw_buttons(self, screen, buttons, mouse_pos, enabled_map=None):
        for name, rect in buttons.items():
            enabled = True if enabled_map is None else enabled_map.get(name, True)
            
            if not enabled:
                color = self.COLORS['button_disabled']
                brightness = 0.6
            else:
                is_hovered = rect.collidepoint(mouse_pos)
                color = self.COLORS['button_hover'] if is_hovered else self.COLORS['button']
                brightness = 1.0 if is_hovered else 0.8
            
            # 陰影效果
            shadow = pygame.Surface((rect.width + 2, rect.height + 2), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0, 0, 0, 40), shadow.get_rect(), border_radius=5)
            screen.blit(shadow, (rect.x, rect.y + 2))
            
            # 漸層按鈕（模擬）
            pygame.draw.rect(screen, color, rect, border_radius=5)
            
            # 頂部高亮 - 增加立體感
            highlight_rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height // 3)
            highlight_color = tuple(min(255, int(c * 1.2)) for c in color)
            pygame.draw.rect(screen, (*highlight_color, 100), highlight_rect, border_radius=5)
            
            # 邊框
            border_color = (227, 237, 246) if enabled else (150, 160, 170)
            pygame.draw.rect(screen, border_color, rect, 2, border_radius=5)
            
            # 文字
            txt_color = (232, 239, 247) if enabled else (180, 190, 200)
            txt = self.font.render(name, True, txt_color)
            txt_rect = txt.get_rect(center=rect.center)
            screen.blit(txt, txt_rect)

    def draw_turn_indicator(self, screen, player_name, is_human):
        message = f"目前回合：{player_name}" if is_human else f"AI 回合：{player_name}"
        text = self.title_font.render(message, True, self.COLORS['text_primary'])
        padding_x = 20
        padding_y = 10
        box = pygame.Rect(0, 0, text.get_width() + padding_x * 2, text.get_height() + padding_y * 2)
        box.center = (self.width // 2, 70)
        overlay = pygame.Surface((box.width, box.height), pygame.SRCALPHA)
        overlay.fill((10, 24, 36, 196))
        screen.blit(overlay, box.topleft)
        pygame.draw.rect(screen, self.COLORS['selected'], box, 2, border_radius=10)
        screen.blit(text, (box.x + padding_x, box.y + padding_y))

    def draw_action_bar(self, screen, rect):
        layer = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        bar_tone = {
            'blue': (10, 24, 36, 200),
            'green': (8, 30, 24, 208),
            'red': (36, 16, 20, 206),
        }
        layer.fill(bar_tone.get(self.table_style, bar_tone['blue']))
        screen.blit(layer, rect.topleft)
        pygame.draw.rect(screen, self.COLORS['panel_border'], rect, 2, border_radius=14)

    def draw_selected_info(self, screen, text, valid, x, y):
        bg = (16, 82, 52, 210) if valid else (98, 42, 44, 210)
        border = (62, 173, 116) if valid else (222, 97, 100)
        fg = (235, 247, 240) if valid else (252, 227, 227)
        label = self.small_font.render(text, True, fg)
        box = pygame.Rect(x, y, label.get_width() + 20, label.get_height() + 10)
        layer = pygame.Surface((box.width, box.height), pygame.SRCALPHA)
        layer.fill(bg)
        screen.blit(layer, box.topleft)
        pygame.draw.rect(screen, border, box, 2, border_radius=8)
        screen.blit(label, (box.x + 10, box.y + 5))

