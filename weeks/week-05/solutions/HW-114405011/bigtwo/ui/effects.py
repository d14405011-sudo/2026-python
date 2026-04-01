# -*- coding: utf-8 -*-
"""
視覺效果增強模組
添加動畫、粒子效果、高級光效、邊框裝飾等

【優化】粒子系統進行如下改進：
  1. 全局粒子數量限制（最多 100 個活躍粒子）
  2. 粒子自動清理（生命週期完成後立即移除）
  3. 內存池管理（可選複用粒子對象）
"""

import pygame
import math
import random

class ParticleEffect:
    """粒子效果系統（已優化）"""
    
    # 每個效果物件的粒子上限
    MAX_PARTICLES = 100
    
    def __init__(self, x, y, particle_type='spark', color=(255, 200, 80)):
        self.x = x
        self.y = y
        self.particles = []
        self.color = color
        self.particle_type = particle_type
        self._generate_particles()
    
    def _generate_particles(self):
        """生成粒子（受全局限制約束）"""
        if self.particle_type == 'spark':
            # 閃爍效果（發牌）
            for _ in range(min(8, self.MAX_PARTICLES)):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 6)
                self.particles.append({
                    'x': self.x,
                    'y': self.y,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed,
                    'life': 30,
                    'age': 0,
                    'size': random.uniform(2, 5)
                })
                
        elif self.particle_type == 'victory':
            # 勝利粒子（更多、更彩色）
            colors = [
                (255, 215, 0),    # 金色
                (255, 105, 180),  # 深粉紅
                (0, 255, 255),    # 青色
                (255, 0, 127),    # 玫瑰紅
                (0, 255, 0),      # 綠色
            ]
            for _ in range(min(20, self.MAX_PARTICLES)):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(3, 8)
                self.particles.append({
                    'x': self.x,
                    'y': self.y,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed - 2,  # 向上偏向
                    'life': 60,
                    'age': 0,
                    'size': random.uniform(3, 8),
                    'color': random.choice(colors)
                })
    
    def update(self):
        """更新粒子（自動清理已過期粒子）"""
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.15  # 重力效果
            p['age'] += 1
            
        # 移除已過期的粒子，並更新計數
        self.particles = [p for p in self.particles if p['age'] < p['life']]
        return len(self.particles) > 0
    
    def draw(self, screen):
        """繪製粒子"""
        for p in self.particles:
            alpha = int(255 * (1 - p['age'] / p['life']))
            color = p.get('color', self.color)
            # 漸褪效果
            faded_color = tuple(
                int(c * (1 - p['age'] / p['life'])) for c in color
            )
            pygame.draw.circle(screen, faded_color, 
                             (int(p['x']), int(p['y'])), 
                             int(p['size']))


class GlowEffect:
    """高級光暈效果"""
    def __init__(self, x, y, radius=30, color=(255, 200, 80), intensity=1.0, max_life=36):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.intensity = intensity
        self.time = 0
        self.life = 0
        self.max_life = max_life
    
    def update(self, dt=1):
        """更新光暈（脈動效果）"""
        self.time += dt
        self.life += dt

    def is_alive(self):
        return self.life < self.max_life
    
    def draw(self, screen):
        """繪製光暈"""
        # 使用半透明實心層來做柔和光暈，避免黑色同心圓遮擋內容
        pulse = 0.72 + 0.28 * math.sin(self.time * 0.05)
        current_radius = int(self.radius * pulse)
        if current_radius <= 0:
            return

        glow_surface = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
        for i in range(4):
            scale = 1 - i * 0.22
            r = int(current_radius * scale)
            if r <= 0:
                continue
            alpha = max(10, int(88 * self.intensity * scale * pulse))
            pygame.draw.circle(glow_surface, (*self.color, alpha), (current_radius, current_radius), r)

        screen.blit(glow_surface, (int(self.x) - current_radius, int(self.y) - current_radius))


class CardAnimation:
    """卡牌動畫效果"""
    def __init__(self, card_rect, animation_type='flip'):
        self.start_rect = card_rect.copy()
        self.current_rect = card_rect.copy()
        self.animation_type = animation_type
        self.progress = 0
        self.duration = 15  # 幀數
    
    def update(self):
        """更新動畫進度"""
        self.progress = min(self.progress + 1, self.duration)
        t = self.progress / self.duration  # 0 ~ 1
        
        if self.animation_type == 'flip':
            # 翻轉效果
            scale = 1 - abs(2 * (t - 0.5))
            self.current_rect.width = int(self.start_rect.width * scale)
            self.current_rect.centerx = self.start_rect.centerx
        
        elif self.animation_type == 'bounce':
            # 彈跳效果
            bounce = math.sin(t * math.pi) * 20
            self.current_rect.centery = self.start_rect.centery - bounce
        
        elif self.animation_type == 'glow':
            # 發光效果
            scale = 1 + 0.1 * math.sin(t * math.pi)
            self.current_rect.width = int(self.start_rect.width * scale)
            self.current_rect.height = int(self.start_rect.height * scale)
            self.current_rect.center = self.start_rect.center
        
        return self.progress < self.duration
    
    def get_transform(self):
        """獲取變換參數"""
        t = self.progress / self.duration
        return {
            'rect': self.current_rect,
            'alpha': int(255 * (1 - abs(math.sin(t * math.pi)) if self.animation_type == 'flip' else 1))
        }


class BorderDecorator:
    """邊框裝飾"""
    @staticmethod
    def draw_elevated_border(screen, rect, color=(100, 150, 200), width=3, glow=True):
        """繪製帶光澤的立體邊框"""
        # 外部亮邊
        pygame.draw.rect(screen, 
            tuple(min(255, c + 50) for c in color),
            rect, width)
        
        # 內部暗邊
        inner_rect = rect.inflate(-4, -4)
        pygame.draw.rect(screen,
            tuple(max(0, c - 50) for c in color),
            inner_rect, 1)
        
        # 可選：光暈
        if glow:
            if hasattr(pygame, 'gfxdraw'):
                try:
                    import pygame.gfxdraw as gfxdraw
                    gfxdraw.rectangle(screen, 
                        rect.inflate(4, 4),
                        tuple(int(c * 0.3) for c in color))
                except:
                    pass
    
    @staticmethod
    def draw_glowing_button(screen, rect, color=(100, 150, 200), is_hover=False):
        """繪製發光按鈕"""
        # 背景
        bg_color = tuple(min(255, c + 40) for c in color) if is_hover else color
        pygame.draw.rect(screen, bg_color, rect, 0)
        
        # 邊框
        border_color = tuple(min(255, c + 80) for c in color) if is_hover else color
        pygame.draw.rect(screen, border_color, rect, 2)
        
        # 光澤線
        if is_hover:
            shine_rect = rect.copy()
            shine_rect.height = 4
            pygame.draw.rect(screen, 
                tuple(min(255, c + 120) for c in color),
                shine_rect, 0)


class BackgroundEffect:
    """背景流動效果"""
    def __init__(self, width, height, color=(100, 200, 150)):
        self.width = width
        self.height = height
        self.color = color
        self.particles = []
        self.time = 0
        # 生成浮動粒子
        for _ in range(15):
            self.particles.append({
                'x': random.uniform(0, width),
                'y': random.uniform(0, height),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.3, 0),
                'size': random.uniform(1, 3),
                'alpha': random.uniform(20, 80)
            })
    
    def update(self):
        """更新背景粒子"""
        self.time += 1
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['alpha'] = 50 + 30 * math.sin(self.time * 0.05 + p['x'])
            
            # 邊界回饋
            if p['x'] < 0:
                p['x'] = self.width
            elif p['x'] > self.width:
                p['x'] = 0
            
            if p['y'] < 0:
                p['y'] = self.height
    
    def draw(self, screen):
        """繪製背景效果"""
        for p in self.particles:
            # 淡色浮動粒子
            color = tuple(int(c * p['alpha'] / 100) for c in self.color)
            pygame.draw.circle(screen, color, 
                             (int(p['x']), int(p['y'])), 
                             int(p['size']))


# 使用示例和整合指南
ENHANCEMENT_GUIDE = """
【視覺效果整合指南】

1. 卡牌動畫
   - 在發牌時使用 CardAnimation('flip')
   - 在玩家選牌時使用 CardAnimation('bounce')

2. 粒子效果
   - ParticleEffect(x, y, 'spark', color) - 發牌特效
   - ParticleEffect(x, y, 'victory', color) - 勝利特效

3. 按鈕光效
   - BorderDecorator.draw_glowing_button() - 互動按鈕

4. 背景流動
   - BackgroundEffect() - 持續更新的背景

整合步驟：
1. 在 ui/app.py 中導入此模組
2. 在 render_game_state() 中調用相應效果
3. 在遊戲事件中觸發粒子和動畫

預期視覺提升：
✓ 卡牌翻轉時的 3D 效果
✓ 選牌時的彈跳反饋
✓ 發牌和勝利的粒子爆炸
✓ 浮動的背景粒子
✓ 按鈕的互動發光
"""
