# -*- coding: utf-8 -*-
# game/finder.py

import itertools
from typing import Dict, Iterable, List, Optional
from .models import Hand, Card
from .classifier import HandClassifier

class HandFinder:
    """牌型搜尋器"""

    @staticmethod
    def _group_by_rank(hand: Hand) -> Dict[int, List[Card]]:
        grouped: Dict[int, List[Card]] = {}
        for card in hand:
            grouped.setdefault(card.rank, []).append(card)
        return grouped

    @staticmethod
    def _iter_five_card_combos(hand: Hand) -> Iterable[List[Card]]:
        for combo in itertools.combinations(hand, 5):
            yield list(combo)
    
    @staticmethod
    def find_singles(hand: Hand) -> List[List[Card]]:
        """找出所有單張出牌方案
        
        返回：[單張牌] 的列表
        """
        return [[c] for c in hand]

    @staticmethod
    def find_pairs(hand: Hand) -> List[List[Card]]:
        """找出所有對子出牌方案
        
        對子：2張同rank不同花的牌
        返回：[牌1, 牌2] 的列表
        """
        res: List[List[Card]] = []
        grouped = HandFinder._group_by_rank(hand)
        for cards in grouped.values():
            if len(cards) >= 2:
                for pair in itertools.combinations(cards, 2):
                    res.append(list(pair))
        return res

    @staticmethod
    def find_five_card_plays(hand: Hand) -> List[List[Card]]:
        """找出所有合法的五張牌組合
        
        遍歷手牌的所有5張組合，篩選出合法牌型：
        - 順子（Straight）
        - 葫蘆（Full House）
        - 四條（Four of a Kind）
        - 同花順（Straight Flush）
        
        返回：[5張牌組合] 的列表
        """
        res: List[List[Card]] = []
        for cards in HandFinder._iter_five_card_combos(hand):
            if HandClassifier.classify(cards):
                res.append(cards)
        return res

    @staticmethod
    def find_dragons(hand: Hand) -> List[List[Card]]:
        """找出所有一條龍（13 張連續）的組合。"""
        res: List[List[Card]] = []
        if len(hand) < 13:
            return res
        for cards in itertools.combinations(hand, 13):
            combo = list(cards)
            info = HandClassifier.classify(combo)
            if info and info[0].name == "DRAGON":
                res.append(combo)
        return res

    @staticmethod
    def get_all_valid_plays(hand: Hand, last_play: Optional[List[Card]]) -> List[List[Card]]:
        """取得所有可出的合法牌組（基於當前桌面狀態）
        
        邏輯：
        1. 桌上無牌（last_play=None）：返回所有可能的牌型
        2. 桌上有牌：根據其張數和牌型，搜尋相符的出牌
        
        返回：所有可合法出牌的牌組列表
        """
        candidates: List[List[Card]] = []
        candidates.extend(HandFinder.find_singles(hand))
        candidates.extend(HandFinder.find_pairs(hand))
        candidates.extend(HandFinder.find_five_card_plays(hand))
        candidates.extend(HandFinder.find_dragons(hand))

        # 以 can_play 統一過濾。
        valid: List[List[Card]] = []
        for c in candidates:
            if HandClassifier.can_play(last_play, c):
                valid.append(c)
        return valid
