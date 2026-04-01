# -*- coding: utf-8 -*-
"""
視覺增強 - 遊戲整合範例
展示如何在 app.py 中集成所有視覺效果
"""

# ==================== 在 app.py 頂部添加 ====================

from ui.effects import (
    ParticleEffect, CardAnimation, BorderDecorator,
    BackgroundEffect, GlowEffect
)
from ui.themes import get_theme, get_all_themes


# ==================== 在 GameRenderer.__init__() 中添加 ====================

class GameRenderer:
    def __init__(self, width=1280, height=720):
        """... 原有代碼 ..."""
        
        # 視覺效果系統 (新增)
        self.bg_effect = BackgroundEffect(
            width, height,
            color=(100, 150, 200)  # 可根據主題灣調
        )
        self.particle_effects = []
        self.card_animations = []
        self.glow_effects = []
        
        # 主題系統 (新增)
        self.current_theme_name = 'dark_purple'  # 推薦使用新主題
        self.theme = get_theme(self.current_theme_name)


# ==================== 在主遊戲迴圈中添加更新 ====================

def update_visual_effects(self):
    """更新所有視覺效果 (每幀調用一次)"""
    
    # 更新背景粒子
    self.bg_effect.update()
    
    # 清理已完成的粒子效果
    self.particle_effects = [
        e for e in self.particle_effects 
        if e.update()
    ]
    
    # 清理已完成的動畫
    self.card_animations = [
        a for a in self.card_animations
        if a.update()
    ]
    
    # 更新光暈
    for glow in self.glow_effects:
        glow.update()
    
    # 清理已消散的光暈
    self.glow_effects = [
        g for g in self.glow_effects
        if g.intensity > 0.1  # 光暈強度 > 10% 保留
    ]


# ==================== 在卡牌被打出時觸發 ====================

def on_card_played(self, card, player_position):
    """當卡牌被打出時觸發視覺效果"""
    
    # 計算卡牌螢幕位置
    card_x, card_y = self.get_card_screen_position(card)
    
    # 1. 發牌粒子特效
    spark_effect = ParticleEffect(
        card_x, card_y,
        particle_type='spark',
        color=self.theme['glow_color']
    )
    self.particle_effects.append(spark_effect)
    
    # 2. 卡牌翻轉動畫
    card_rect = pygame.Rect(
        card_x - 50, card_y - 70, 100, 140
    )
    flip_anim = CardAnimation(card_rect, animation_type='flip')
    self.card_animations.append(flip_anim)
    
    # 3. 可選：卡牌位置發光
    glow = GlowEffect(
        card_x, card_y,
        radius=60,
        color=self.theme['button_primary'],
        intensity=0.8
    )
    self.glow_effects.append(glow)
    
    print(f"✨ 發牌：{card} 位置 ({card_x}, {card_y})")


# ==================== 在玩家勝利時觸發 ====================

def on_player_victory(self):
    """當玩家勝利時觸發視覺效果"""
    
    center_x = self.WIDTH // 2
    center_y = self.HEIGHT // 2
    
    # 1. 勝利粒子爆炸（3 層）
    for _ in range(3):
        effect = ParticleEffect(
            center_x + ((_ - 1) * 150),
            center_y,
            particle_type='victory',
            color=self.theme['button_primary']
        )
        self.particle_effects.append(effect)
    
    # 2. 大型脈動光暈
    glow = GlowEffect(
        center_x, center_y,
        radius=200,
        color=self.theme['glow_color'],
        intensity=2.0
    )
    self.glow_effects.append(glow)
    
    # 3. 勝利訊息動畫
    victory_rect = pygame.Rect(
        center_x - 150, center_y - 200, 300, 100
    )
    victory_anim = CardAnimation(
        victory_rect, animation_type='glow'
    )
    self.card_animations.append(victory_anim)
    
    print(f"🎉 勝利！粒子爆炸於中央 ({center_x}, {center_y})")


# ==================== 在選牌時可選動畫 ====================

def on_card_selected(self, card_rect):
    """當玩家選擇卡牌時觸發（可選）"""
    
    # 彈跳動畫表示選中
    bounce_anim = CardAnimation(
        card_rect, animation_type='bounce'
    )
    self.card_animations.append(bounce_anim)


# ==================== 主題切換功能 ====================

def switch_theme(self, theme_name):
    """切換遊戲主題"""
    
    if theme_name not in get_all_themes():
        return False
    
    self.current_theme_name = theme_name
    self.theme = get_theme(theme_name)
    
    # 背景顏色隨主題變更
    base_color = self.theme['glow_color']
    self.bg_effect = BackgroundEffect(
        self.WIDTH, self.HEIGHT,
        color=base_color
    )
    
    print(f"🎭 切換主題到：{theme_name}")
    return True


def get_available_themes(self):
    """取得所有可用主題"""
    return get_all_themes()


# ==================== 渲染函數（添加視覺效果繪製層） ====================

def render_game_with_effects(self, screen):
    """完整遊戲渲染（包含視覺效果）"""
    
    # 1. 清屏和背景漸層
    background = pygame.Surface((self.WIDTH, self.HEIGHT))
    color_top = self.theme['bg_top']
    color_bottom = self.theme['bg_bottom']
    
    for y in range(self.HEIGHT):
        ratio = y / self.HEIGHT
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        pygame.draw.line(background, (r, g, b), (0, y), (self.WIDTH, y))
    
    screen.blit(background, (0, 0))
    
    # 2. 背景浮動粒子
    self.bg_effect.draw(screen)
    
    # 3. 棋盤和卡牌（原有遊戲畫面）
    # ... 原有繪製代碼 ...
    
    # 4. 粒子爆炸效果
    for effect in self.particle_effects:
        effect.draw(screen)
    
    # 5. 光暈和脈動
    for glow in self.glow_effects:
        glow.draw(screen)
    
    # 6. 動畫層（卡牌翻轉、彈跳）
    for anim in self.card_animations:
        transform = anim.get_transform()
        # 特定動畫類型的繪製
        if anim.animation_type == 'flip':
            self._render_flip_animation(screen, transform, anim)
        elif anim.animation_type == 'bounce':
            self._render_bounce_animation(screen, transform, anim)
        elif anim.animation_type == 'glow':
            self._render_glow_animation(screen, transform, anim)
    
    # 7. UI 元素和按鈕
    self.render_ui_buttons(screen)
    
    # 8. 按鈕邊框光效
    self._render_button_effects(screen)


# ==================== 按鈕渲染輔助函數 ====================

def render_ui_buttons(self, screen):
    """繪製所有 UI 按鈕並應用發光效果"""
    
    # 示例：Action 按鈕
    action_buttons = [
        {'rect': pygame.Rect(100, 600, 150, 50), 'text': '通過'},
        {'rect': pygame.Rect(300, 600, 150, 50), 'text': '出牌'},
        {'rect': pygame.Rect(500, 600, 150, 50), 'text': '認輸'},
    ]
    
    mouse_pos = pygame.mouse.get_pos()
    
    for btn in action_buttons:
        is_hover = btn['rect'].collidepoint(mouse_pos)
        
        # 使用邊框裝飾器繪製發光按鈕
        BorderDecorator.draw_glowing_button(
            screen, btn['rect'],
            color=self.theme['button_primary'],
            is_hover=is_hover
        )
        
        # 繪製按鈕文本
        font = pygame.font.Font(None, 24)
        text = font.render(btn['text'], True, (255, 255, 255))
        text_rect = text.get_rect(center=btn['rect'].center)
        screen.blit(text, text_rect)


# ==================== 主題選擇器 UI ====================

def render_theme_selector(self, screen):
    """在遊戲中渲染主題選擇器（可選）"""
    
    theme_names = get_all_themes()
    mouse_pos = pygame.mouse.get_pos()
    
    start_x = 20
    start_y = 20
    btn_width = 130
    btn_height = 30
    spacing = 140
    
    for i, theme_name in enumerate(theme_names):
        theme_obj = get_theme(theme_name)
        rect = pygame.Rect(
            start_x + i * spacing,
            start_y,
            btn_width,
            btn_height
        )
        
        # 當前主題高亮
        is_current = (self.current_theme_name == theme_name)
        is_hover = rect.collidepoint(mouse_pos)
        
        # 繪製主題按鈕
        BorderDecorator.draw_glowing_button(
            screen, rect,
            color=theme_obj['button_primary'],
            is_hover=(is_current or is_hover)
        )
        
        # 選中指示
        if is_current:
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)


# ==================== 事件處理中的主題切換 ====================

def handle_mouse_click(self, pos):
    """處理滑鼠點擊事件"""
    
    # 主題按鈕點擊檢測
    theme_names = get_all_themes()
    start_x = 20
    start_y = 20
    spacing = 140
    
    for i, theme_name in enumerate(theme_names):
        rect = pygame.Rect(
            start_x + i * spacing,
            start_y,
            130, 30
        )
        
        if rect.collidepoint(pos):
            self.switch_theme(theme_name)
            print(f"✓ 已切換主題：{theme_name}")


# ==================== 完整使用示例 ====================

"""
【在主遊戲迴圈中的整合】

while game_running:
    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            renderer.handle_mouse_click(event.pos)
        # ... 其他事件 ...
    
    # 遊戲邏輯更新
    # ... game_state.update() ...
    
    # 視覺效果更新 (新增)
    renderer.update_visual_effects()
    
    # 渲染
    renderer.render_game_with_effects(screen)
    
    # 可選：渲染主題選擇器
    renderer.render_theme_selector(screen)
    
    pygame.display.flip()
    clock.tick(60)

【事件觸發集成點】

1. 玩家打出卡牌 →  renderer.on_card_played()
2. 玩家贏得遊戲 →  renderer.on_player_victory()
3. 玩家選擇卡牌 →  renderer.on_card_selected()
4. 點擊主題按鈕 →  renderer.switch_theme()
5. 滑鼠懸停按鈕 →  自動偵測（在渲染中）
"""

# ==================== 配置和調優 ====================

# 粒子效果參數（可調整）
PARTICLE_CONFIG = {
    'spark_count': 8,           # 發牌粒子數
    'spark_life': 30,           # 發牌粒子生命週期
    'victory_count': 20,        # 勝利粒子數
    'victory_life': 60,         # 勝利粒子生命週期
    'bg_particle_count': 15,    # 背景粒子數
}

# 動畫參數
ANIMATION_CONFIG = {
    'flip_duration': 15,        # 翻轉幀數
    'bounce_height': 20,        # 彈跳高度
    'glow_scale': 1.1,         # 發光縮放
}

# 光效參數
GLOW_CONFIG = {
    'card_radius': 60,          # 卡牌光暈半徑
    'victory_radius': 200,      # 勝利光暈半徑
    'max_intensity': 2.0,       # 最大光強度
}
