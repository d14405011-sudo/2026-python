# -*- coding: utf-8 -*-
"""
視覺增強整合示例
展示如何在遊戲中使用各種視覺效果
"""

from ui.effects import (
    ParticleEffect, CardAnimation, BorderDecorator, 
    BackgroundEffect, GlowEffect
)
from ui.themes import get_theme, get_all_themes

class VisualEnhancementExample:
    """視覺增強使用範例"""
    
    def __init__(self, screen_width=1280, screen_height=720):
        self.width = screen_width
        self.height = screen_height
        
        # 所有活躍效果
        self.particle_effects = []
        self.card_animations = []
        self.glow_effects = []
        
        # 背景特效
        self.bg_effect = BackgroundEffect(
            screen_width, screen_height,
            color=(100, 150, 200)
        )
        
        # 當前主題
        self.current_theme = 'dark_purple'
        self.theme = get_theme(self.current_theme)
    
    def on_card_played(self, card_x, card_y):
        """卡牌被打出時觸發"""
        # 1. 發牌粒子效果
        effect = ParticleEffect(
            card_x, card_y, 
            particle_type='spark',
            color=self.theme['glow_color']
        )
        self.particle_effects.append(effect)
        
        # 2. 卡牌翻轉動畫
        card_rect = pygame.Rect(card_x - 50, card_y - 70, 100, 140)
        anim = CardAnimation(card_rect, animation_type='flip')
        self.card_animations.append(anim)
        
        print(f"✨ 發牌特效：({card_x}, {card_y})")
    
    def on_player_victory(self, win_x, win_y):
        """玩家勝利時觸發"""
        # 1. 勝利粒子爆炸
        effect = ParticleEffect(
            win_x, win_y,
            particle_type='victory',
            color=self.theme['button_primary']
        )
        self.particle_effects.append(effect)
        
        # 2. 發光脈動
        glow = GlowEffect(
            win_x, win_y,
            radius=100,
            color=self.theme['glow_color'],
            intensity=1.5
        )
        self.glow_effects.append(glow)
        
        print(f"🎉 勝利！粒子爆炸於 ({win_x}, {win_y})")
    
    def on_button_hover(self, button_rect, is_hovered):
        """按鈕懸停時觸發"""
        if is_hovered:
            # 添加按鈕彈跳動畫
            anim = CardAnimation(button_rect, animation_type='bounce')
            self.card_animations.append(anim)
            print(f"🔘 按鈕懸停")
    
    def switch_theme(self, theme_name):
        """切換主題"""
        if theme_name in get_all_themes():
            self.current_theme = theme_name
            self.theme = get_theme(theme_name)
            
            # 背景顏色跟著主題變
            base_color = self.theme['glow_color']
            self.bg_effect = BackgroundEffect(
                self.width, self.height,
                color=base_color
            )
            
            print(f"🎭 切換到主題：{theme_name}")
            return True
        return False
    
    def update(self):
        """更新所有視覺效果"""
        # 更新背景
        self.bg_effect.update()
        
        # 更新粒子效果
        dead_particles = []
        for i, effect in enumerate(self.particle_effects):
            if not effect.update():
                dead_particles.append(i)
        
        for i in reversed(dead_particles):
            self.particle_effects.pop(i)
        
        # 更新卡牌動畫
        dead_anims = []
        for i, anim in enumerate(self.card_animations):
            if not anim.update():
                dead_anims.append(i)
        
        for i in reversed(dead_anims):
            self.card_animations.pop(i)
        
        # 更新光暈
        for glow in self.glow_effects:
            glow.update()
    
    def render(self, screen):
        """渲染所有視覺效果（層級順序）"""
        # 1. 背景
        screen.fill((0, 0, 0))
        
        # 2. 背景浮動粒子
        self.bg_effect.draw(screen)
        
        # 3. 遊戲區域（模擬）
        game_rect = pygame.Rect(100, 100, 800, 600)
        pygame.draw.rect(screen, self.theme['bg_top'], game_rect)
        
        # 4. 粒子爆炸
        for effect in self.particle_effects:
            effect.draw(screen)
        
        # 5. 光暈脈動
        for glow in self.glow_effects:
            glow.draw(screen)
        
        # 6. 卡牌（示例）
        card_rect = pygame.Rect(400, 300, 100, 140)
        pygame.draw.rect(screen, self.theme['card_back'], card_rect)
        pygame.draw.rect(screen, self.theme['glow_color'], card_rect, 2)
        
        # 7. 卡牌動畫
        for anim in self.card_animations:
            transform = anim.get_transform()
            pygame.draw.rect(screen, self.theme['button_primary'], 
                           transform['rect'])
        
        # 8. 按鈕
        btn_rect = pygame.Rect(500, 550, 200, 50)
        is_hovered = btn_rect.collidepoint(pygame.mouse.get_pos())
        BorderDecorator.draw_glowing_button(
            screen, btn_rect,
            color=self.theme['button_primary'],
            is_hover=is_hovered
        )
        
        # 9. 主題選擇器
        theme_names = get_all_themes()
        for i, theme_name in enumerate(theme_names):
            theme_btn_rect = pygame.Rect(
                20 + i * 140, 20, 130, 30
            )
            
            # 當前主題高亮
            highlight = (self.current_theme == theme_name)
            theme_obj = get_theme(theme_name)
            
            BorderDecorator.draw_glowing_button(
                screen, theme_btn_rect,
                color=theme_obj['button_primary'],
                is_hover=highlight
            )
            
            # 文字（簡化版）
            if highlight:
                pygame.draw.rect(screen, (255, 255, 0), theme_btn_rect, 2)


# ================== 互動演示 ==================

DEMO_INSTRUCTIONS = """
【視覺增強互動演示】

按鍵說明：
  1-7: 切換主題 (1=冬季, 2=霓光, 3=夏日, 4=經典, 5=黑紫, 6=綠幕, 7=皇金)
  SPACE: 發牌特效演示
  V: 勝利特效演示
  R: 重置所有效果
  Q: 退出

滑鼠：
  懸停按鈕時有互動效果

視覺效果層級（從下到上）：
  背景 → 浮動粒子 → 遊戲區 → 爆炸粒子 → 光暈 → 卡牌 → 動畫 → 按鈕 → UI
"""

if __name__ == '__main__':
    import pygame
    import sys
    
    pygame.init()
    
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("大老二 - 視覺增強演示")
    
    clock = pygame.time.Clock()
    running = True
    
    # 初始化視覺系統
    visual = VisualEnhancementExample(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    print(DEMO_INSTRUCTIONS)
    
    while running:
        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # 主題切換 (1-7)
                if event.key == pygame.K_1:
                    visual.switch_theme('winter')
                elif event.key == pygame.K_2:
                    visual.switch_theme('neon')
                elif event.key == pygame.K_3:
                    visual.switch_theme('summer')
                elif event.key == pygame.K_4:
                    visual.switch_theme('default')
                elif event.key == pygame.K_5:
                    visual.switch_theme('dark_purple')
                elif event.key == pygame.K_6:
                    visual.switch_theme('tech_green')
                elif event.key == pygame.K_7:
                    visual.switch_theme('royal_gold')
                
                # 特效演示
                elif event.key == pygame.K_SPACE:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    visual.on_card_played(mouse_x, mouse_y)
                
                elif event.key == pygame.K_v:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    visual.on_player_victory(mouse_x, mouse_y)
                
                elif event.key == pygame.K_r:
                    visual.particle_effects.clear()
                    visual.card_animations.clear()
                    visual.glow_effects.clear()
                    print("✓ 重置所有效果")
                
                elif event.key == pygame.K_q:
                    running = False
        
        # 更新
        visual.update()
        
        # 渲染
        visual.render(screen)
        
        # 顯示說明文字
        font = pygame.font.Font(None, 24)
        text_lines = [
            f"主題: {visual.current_theme}",
            f"粒子: {len(visual.particle_effects)} 活躍",
            f"動畫: {len(visual.card_animations)} 活躍",
            "按 1-7 切換主題 | SPACE 發牌 | V 勝利 | R 重置 | Q 退出"
        ]
        
        for i, line in enumerate(text_lines):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (20, SCREEN_HEIGHT - 100 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()
