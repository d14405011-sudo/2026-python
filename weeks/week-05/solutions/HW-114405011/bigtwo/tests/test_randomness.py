#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""測試發牌隨機性"""

from game.models import Deck, Player

print("測試發牌隨機性（20 次遊戲）")
print("=" * 50)

distribution = {0: 0, 1: 0, 2: 0, 3: 0}

for game_num in range(1, 21):
    deck = Deck()
    deck.shuffle()
    
    players = [Player(f"Player {i+1}", is_ai=(i > 0)) for i in range(4)]
    
    # 發牌
    for _ in range(13):
        for p in players:
            p.take_cards(deck.deal(1))
    
    # 找梅花3
    for i, p in enumerate(players):
        if p.hand.find_3_clubs():
            distribution[i] += 1
            print(f"遊戲 {game_num:2d}: 梅花3 給 Player {i+1}")
            break

print("\n" + "=" * 50)
print("梅花3 分配統計：")
for i in range(4):
    print(f"  Player {i+1}: {distribution[i]} 次")
