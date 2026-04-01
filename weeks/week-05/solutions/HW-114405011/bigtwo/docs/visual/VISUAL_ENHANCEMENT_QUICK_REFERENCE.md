# 🎨 視覺增強 - 快速參考卡

## 📦 新增文件

| 檔案 | 說明 | 用途 |
|------|------|------|
| `ui/effects.py` | 視覺效果核心模組 | 粒子、動畫、邊框、背景 |
| `VISUAL_ENHANCEMENT.md` | 詳細整合指南 | 實作和調優參考 |
| `ui/visual_demo.py` | 互動演示程式 | 測試和預览所有效果 |

## 🎭 主題總結（7 個）

```
原有 4 個:
  winter      🔵 深藍 + 金光 (冬季夜晚)
  neon        🟣 紫藍 + 青光 (霓光未來)
  summer      🔷 亮藍 + 黃光 (夏日明朗)
  default     🔵 深藍 + 標準 (經典深藍)

新增 3 個: ✨
  dark_purple 🟣 黑紫 + 粉光 (黑紫帝王) ← 最高級
  tech_green  🟢 綠黑 + 亮綠 (科技綠幕) ← 最酷
  royal_gold  🟡 棕金 + 皇金 (皇金璀璨) ← 最華麗
  sunset      🟠 橙紅 + 火光 (夕陽火燒) ← 最溫暖
```

## ⚡ 核心效果（一句話說明）

| 效果 | 類別 | 說明 | 觸發時機 |
|------|------|------|---------|
| `ParticleEffect('spark')` | 粒子 | 8 個粒子向四方散炸 | 發牌 |
| `ParticleEffect('victory')` | 粒子 | 20 個彩色粒子向上漂 | 勝利 |
| `CardAnimation('flip')` | 動畫 | 卡牌 3D 翻轉 | 出牌 |
| `CardAnimation('bounce')` | 動畫 | 卡牌彈跳 | 選牌 |
| `CardAnimation('glow')` | 動畫 | 卡牌脈動發光 | 特選 |
| `BackgroundEffect` | 背景 | 15 個浮動粒子 | 持續 |
| `BorderDecorator` | UI | 立體邊框和按鈕光澤 | UI 繪製 |
| `GlowEffect` | 光效 | 圓形脈動光暈 | 特殊事件 |

## 🚀 最小整合（3 步快速上手）

### 步驟 1：導入模組
```python
from ui.effects import ParticleEffect, BackgroundEffect, BorderDecorator
```

### 步驟 2：初始化背景（在遊戲初始化）
```python
self.bg_effect = BackgroundEffect(width, height, color=(100, 200, 150))
```

### 步驟 3：每幀更新和繪製
```python
# 更新
self.bg_effect.update()

# 繪製（在背景之後）
self.bg_effect.draw(screen)
```

✓ 完成！已有動畫背景

## 📝 常見用法

### 發牌特效
```python
effect = ParticleEffect(card_x, card_y, 'spark', color=(255,200,80))
effects.append(effect)
```

### 勝利爆炸
```python
effect = ParticleEffect(center_x, center_y, 'victory', color=(200,150,60))
effects.append(effect)
```

### 卡牌動畫
```python
anim = CardAnimation(card_rect, 'flip')  # 或 'bounce' 或 'glow'
animations.append(anim)
```

### 更新和清理
```python
# 更新
animations = [a for a in animations if a.update()]
effects = [e for e in effects if e.update()]

# 繪製
for effect in effects:
    effect.draw(screen)
```

### 切換主題
```python
from ui.themes import get_theme
theme = get_theme('dark_purple')
glow_color = theme['glow_color']
```

### 繪製發光按鈕
```python
from ui.effects import BorderDecorator
BorderDecorator.draw_glowing_button(
    screen, button_rect, 
    color=theme['button_primary'],
    is_hover=mouse_over
)
```

## 🎬 層級順序（重要！）

```
背景
  ↓
浮動粒子 (BackgroundEffect)
  ↓
遊戲區域 (棋盤)
  ↓
卡牌
  ↓
粒子爆炸 (ParticleEffect)
  ↓
動畫 (CardAnimation)
  ↓
UI 面板
  ↓
按鈕 (BorderDecorator)
  ↓
光效層
```

## 🧪 測試方法

### 方法 1：運行演示程式
```bash
python ui/visual_demo.py
```
- 按 1-7 切換主題
- SPACE 發牌特效
- V 勝利特效
- R 重置
- Q 退出

### 方法 2：在遊戲中整合後測試
1. 發牌時檢查粒子效果
2. 勝利時檢查爆炸效果
3. 按鈕懸停時檢查發光
4. 在設定選單切換主題

## ⚙️ 性能考量

| 項目 | 影響 | 建議 |
|------|------|------|
| 同時粒子數 | 中 | 限制 ≤100 個 |
| 同時動畫數 | 低 | 可容納 ≤50 個 |
| 背景粒子 | 低 | 預設 15 個足夠 |
| 效果更新 | 低 | 每幀更新無壓力 |

## 📊 視覺層級完成度

```
基礎背景繪製       ✓ 完成
主題色彩系統       ✓ 完成（新增 3 主題）
粒子效果系統       ✓ 完成（2 種）
卡牌動畫系統       ✓ 完成（3 種）
邊框和按鈕裝飾    ✓ 完成
背景浮動特效       ✓ 完成
光暈和脈動效果    ✓ 完成
演示程式          ✓ 完成
完整文檔          ✓ 完成
```

## 🎯 下一步建議

### 優先級 1（推薦先做）
- [ ] 在 `ui/app.py` 導入 `effects.py`
- [ ] 初始化 `BackgroundEffect`
- [ ] 集成到遊戲主迴圈

### 優先級 2（視覺提升）
- [ ] 發牌時觸發粒子效果
- [ ] 勝利時觸發爆炸效果
- [ ] 測試所有 7 个主題

### 優先級 3（專業感）
- [ ] 卡牌翻轉動畫
- [ ] 按鈕邊框光效
- [ ] 細調動畫速度

### 優先級 4（加分項）
- [ ] 背景音樂配合視覺節奏
- [ ] 自訂主題編輯器
- [ ] 高分時特殊效果

## 📞 故障排除

### 問題：粒子沒有出現
**解決**：確保 `update()` 和 `draw()` 在遊戲迴圈中被調用

### 問題：背景粒子太多/太少
**解決**：修改 `BackgroundEffect.__init__()` 中的粒子數量

### 問題：動畫太快/太慢
**解決**：調整 `CardAnimation.duration` 值（15 = 0.25 秒 @ 60FPS）

### 問題：按鈕不發光
**解決**：確保 `is_hover` 參數根據滑鼠位置正確設定

## 🎉 完成檢查

- [x] 創建視覺效果模組 (`effects.py`)
- [x] 添加新的帥氣主題（黑紫、綠幕、皇金、夕陽）
- [x] 編寫完整整合指南 (`VISUAL_ENHANCEMENT.md`)
- [x] 創建互動演示程式 (`visual_demo.py`)
- [x] 編寫快速參考卡（本檔案）

**目標達成**：美術設計增加多個帥氣好看的東西 ✓

---

📌 **相關檔案位置**：
- 效果代碼：`ui/effects.py`
- 主題配置：`ui/themes.py`
- 演示程式：`ui/visual_demo.py`
- 詳細指南：`VISUAL_ENHANCEMENT.md`
- 此快速卡：`VISUAL_ENHANCEMENT_QUICK_REFERENCE.md`
