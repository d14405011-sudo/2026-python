# -*- coding: utf-8 -*-
# game/classifier.py

from enum import IntEnum
from typing import Dict, List, Optional, Tuple
from .models import Card

class CardType(IntEnum):
    """牌型列舉（此版本不支援三條）"""
    SINGLE = 1        # 單張
    PAIR = 2          # 對子
    STRAIGHT = 3      # 順子
    FLUSH = 4         # 同花（此版本禁用，僅保留相容列舉）
    FULL_HOUSE = 5    # 葫蘆
    FOUR_OF_A_KIND = 6 # 四條
    STRAIGHT_FLUSH = 7 # 同花順
    DRAGON = 8        # 一條龍（13張連續）

class HandClassifier:
    """牌型分類器"""

    # 依截圖規則：鐵支可壓葫蘆/順子/一對/單張；同花順可壓鐵支以下；一條龍可壓所有牌型。
    FOUR_OF_A_KIND_BEATS = {
        CardType.SINGLE,
        CardType.PAIR,
        CardType.STRAIGHT,
        CardType.FULL_HOUSE,
        CardType.FOUR_OF_A_KIND,
    }
    STRAIGHT_FLUSH_BEATS = {
        CardType.SINGLE,
        CardType.PAIR,
        CardType.STRAIGHT,
        CardType.FULL_HOUSE,
        CardType.FOUR_OF_A_KIND,
        CardType.STRAIGHT_FLUSH,
    }

    @staticmethod
    def _count_ranks(ranks: List[int]) -> Dict[int, int]:
        """統計各點數出現次數。"""
        count_map: Dict[int, int] = {}
        for rank in ranks:
            count_map[rank] = count_map.get(rank, 0) + 1
        return count_map
    
    @staticmethod
    def _is_straight(ranks: List[int]) -> bool:
        """判斷是否為順子（5 張連續點數）"""
        if len(ranks) != 5:
            return False
        sr = sorted(ranks)
        if len(set(sr)) != 5:
            return False
        straight_sets = (
            {3, 4, 5, 14, 15},  # A2345
            {3, 4, 5, 6, 15},   # 23456
        )
        s = set(sr)
        if s in straight_sets:
            return True
        # 含 2 的順子只接受兩種特例，避免 JQKA2 被視為合法。
        if 15 in s:
            return False
        return all(sr[i] + 1 == sr[i + 1] for i in range(4))

    @staticmethod
    def _is_flush(suits: List[int]) -> bool:
        return len(set(suits)) == 1

    @staticmethod
    def _is_dragon(ranks: List[int]) -> bool:
        """判斷是否為一條龍（3..2 共 13 個點數各一張）。"""
        if len(ranks) != 13:
            return False
        return set(ranks) == set(range(3, 16))

    @staticmethod
    def _straight_key(scards: List[Card]) -> Tuple[int, int]:
        """順子比較鍵：23456 最大，A2345 次大，其餘依一般順序。"""
        ranks = {c.rank for c in scards}

        if ranks == {3, 4, 5, 6, 15}:  # 23456
            high_suit = max(c.suit for c in scards if c.rank == 15)
            return (200, high_suit)

        if ranks == {3, 4, 5, 14, 15}:  # A2345
            high_suit = max(c.suit for c in scards if c.rank == 15)
            return (199, high_suit)

        max_rank = max(c.rank for c in scards)
        high_suit = max(c.suit for c in scards if c.rank == max_rank)
        return (max_rank, high_suit)

    @staticmethod
    def _flush_key(scards: List[Card]) -> Tuple[int, int]:
        """同花比較鍵：依最大、次大...逐張比較。"""
        ranks_desc = sorted((c.rank for c in scards), reverse=True)
        signature = 0
        for rank in ranks_desc:
            signature = signature * 16 + rank
        top_rank = ranks_desc[0]
        top_suit = max(c.suit for c in scards if c.rank == top_rank)
        return (signature, top_suit)

    @staticmethod
    def classify(cards: List[Card]) -> Optional[Tuple[CardType, int, int]]:
        """分類牌型，回傳 (牌型, 最大數字, 最大花色)
        
        對於多張牌組合，通常以最大點數和花色來判斷大小。
        """
        if not cards:
            return None
        n = len(cards)
        scards = sorted(cards, key=lambda c: c.to_sort_key())
        ranks = [c.rank for c in scards]
        suits = [c.suit for c in scards]
        max_rank = scards[-1].rank
        max_suit = scards[-1].suit
        
        # 單張
        if n == 1:
            return (CardType.SINGLE, max_rank, max_suit)
        # 對子（2張同 rank）
        elif n == 2:
            if ranks[0] == ranks[1]:
                return (CardType.PAIR, max_rank, max_suit)
        # 三條規則禁用：3 張牌不構成合法出牌。
        elif n == 3:
            return None
        # 5張牌（順子、同花、葫蘆、四條、同花順）
        elif n == 5:
            is_straight = HandClassifier._is_straight(ranks)
            is_flush = HandClassifier._is_flush(suits)
            count_map = HandClassifier._count_ranks(ranks)
            frequencies = sorted(count_map.values())
            straight_rank, straight_suit = HandClassifier._straight_key(scards)
            
            # 同花順（最強）
            if is_straight and is_flush:
                return (CardType.STRAIGHT_FLUSH, straight_rank, straight_suit)
            # 四條（4+1）
            if 4 in frequencies:
                four_rank = [k for k, v in count_map.items() if v == 4][0]
                return (CardType.FOUR_OF_A_KIND, four_rank, max_suit)
            # 葫蘆（3+2）
            if frequencies == [2, 3]:
                triple_rank = [k for k, v in count_map.items() if v == 3][0]
                return (CardType.FULL_HOUSE, triple_rank, max_suit)
            # 順子（5 種連續 rank）
            if is_straight:
                return (CardType.STRAIGHT, straight_rank, straight_suit)

        # 13張牌（一條龍）
        elif n == 13:
            if HandClassifier._is_dragon(ranks):
                # rank欄位用來標示類型：同花一條龍(1) > 雜花一條龍(0)
                dragon_kind = 1 if HandClassifier._is_flush(suits) else 0
                return (CardType.DRAGON, dragon_kind, max_suit)
        return None

    @staticmethod
    def compare(play1: List[Card], play2: List[Card]) -> int:
        """比較兩手牌大小
        
        返回值：1 (play1 > play2), -1 (play1 < play2), 0 (相同或無法比較)
        
        比較順序：
        1. 牌型（牌型值越大越強）
        2. 主要點數（通常是最高點數或組合點數）
        3. 最高花色
        """
        c1 = HandClassifier.classify(play1)
        c2 = HandClassifier.classify(play2)
        if not c1 or not c2: 
            return 0
        # 不同牌型：牌型強度決定勝負
        if c1[0] != c2[0]:
            return 1 if c1[0] > c2[0] else -1
        # 同牌型比點數
        if c1[1] != c2[1]:
            return 1 if c1[1] > c2[1] else -1
        # 同點數比花色
        if c1[2] != c2[2]:
            return 1 if c1[2] > c2[2] else -1
        return 0

    @staticmethod
    def can_play(last_play: Optional[List[Card]], cards: List[Card]) -> bool:
        """檢查是否可以出牌
        
        條件：
        1. 出牌必須是合法的牌型
        2. 如果桌上有牌，出牌張數必須相同，且必須比桌上的牌強
        """
        new_type = HandClassifier.classify(cards)
        if not new_type: 
            return False
        # 桌上無牌，任何合法牌型都能出
        if not last_play: 
            return True

        last_type = HandClassifier.classify(last_play)
        if not last_type:
            return False

        # 五張牌回應規則：除指定特例外，需同牌型比較，避免順子被葫蘆直接壓制。
        if len(cards) == len(last_play) == 5 and new_type[0] != last_type[0]:
            if new_type[0] == CardType.STRAIGHT_FLUSH:
                return last_type[0] in HandClassifier.STRAIGHT_FLUSH_BEATS
            if new_type[0] == CardType.FOUR_OF_A_KIND:
                return last_type[0] in HandClassifier.FOUR_OF_A_KIND_BEATS
            return False

        # 一般情況：同張數直接比大小。
        if len(cards) == len(last_play):
            return HandClassifier.compare(cards, last_play) > 0

        # 特例 1：一條龍可壓所有非一條龍牌型。
        if new_type[0] == CardType.DRAGON:
            return last_type[0] != CardType.DRAGON

        # 特例 2：同花順可跨張數壓鐵支以下指定牌型。
        if new_type[0] == CardType.STRAIGHT_FLUSH:
            return last_type[0] in HandClassifier.STRAIGHT_FLUSH_BEATS

        # 特例 3：鐵支可跨張數壓葫蘆/順子/一對/單張。
        if new_type[0] == CardType.FOUR_OF_A_KIND:
            return last_type[0] in HandClassifier.FOUR_OF_A_KIND_BEATS

        return False
