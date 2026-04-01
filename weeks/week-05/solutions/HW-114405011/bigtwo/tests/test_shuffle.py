#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""測試洗牌位置隨機性"""

from game.models import Deck

print("測試梅花3 在洗牌後的位置（20 次）")
print("=" * 50)

positions = []
for game_num in range(1, 21):
    deck = Deck()
    deck.shuffle()
    
    # 找梅花3 的位置
    for pos, card in enumerate(deck.cards):
        if card.rank == 3 and card.suit == 0:
            positions.append(pos)
            print(f"遊戲 {game_num:2d}: 梅花3 在第 {pos+1:2d} 位")
            break

print("\n" + "=" * 50)
print(f"梅花3 位置分佈: {sorted(positions)}")
print(f"平均位置: {sum(positions) / len(positions):.1f}")
if len(set(positions)) == 1:
    print("⚠️  警告: 梅花3 總在同一位置！這表示洗牌有問題")
else:
    print(f"✓ 正常: 梅花3 出現在 {len(set(positions))} 個不同位置")
