# -*- coding: utf-8 -*-
# game/models.py

import random
from typing import Iterable, List, Optional, Tuple

class Card:
    """撲克牌資料模型"""
    SUITS = ["♣", "♦", "♥", "♠"]  # 梅花 < 方塊 < 紅心 < 黑桃
    RANKS = {3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"10", 11:"J", 12:"Q", 13:"K", 14:"A", 15:"2"}

    def __init__(self, rank: int, suit: int):
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        return f"{self.SUITS[self.suit]}{self.RANKS[self.rank]}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other) -> bool:
        """比較牌的大小（先比rank再比花色）"""
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.suit < other.suit

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    def to_sort_key(self) -> Tuple[int, int]:
        return (self.rank, self.suit)

class Deck:
    """牌組模型"""
    def __init__(self):
        self.cards = self._create_cards()

    def _create_cards(self) -> List[Card]:
        """創建一副完整的撲克牌（52張）：4花色 × 13種點數"""
        cards: List[Card] = []
        for rank in range(3, 16):
            for suit in range(4):
                cards.append(Card(rank, suit))
        return cards

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self, n: int) -> List[Card]:
        """發出指定數量的牌並移除出牌組"""
        dealt = self.cards[:n]
        self.cards = self.cards[n:]
        return dealt

class Hand(list):
    """手牌模型"""
    def __init__(self, cards: Optional[Iterable[Card]] = None):
        super().__init__(cards or [])

    def sort_desc(self):
        """降序排序手牌（由大到小）"""
        self.sort(key=lambda c: (c.rank, c.suit), reverse=True)

    def find_3_clubs(self) -> Optional[Card]:
        """尋找梅花3（遊戲起手牌）"""
        for card in self:
            if card.rank == 3 and card.suit == 0:
                return card
        return None

    def remove(self, cards: Iterable[Card]) -> None:
        """移除指定的牌組，若牌不存在則忽略。"""
        for card in cards:
            if card in self:
                super().remove(card)

class Player:
    """玩家模型"""
    def __init__(self, name: str, is_ai: bool = False):
        self.name = name
        self.is_ai = is_ai
        self.hand = Hand()
        self.score = 0

    def take_cards(self, cards: Iterable[Card]) -> None:
        """從牌組拿入指定的牌並重新排序"""
        self.hand.extend(cards)
        self.hand.sort_desc()

    def play_cards(self, cards: List[Card]) -> List[Card]:
        """出牌（從手牌移除指定牌組）"""
        self.hand.remove(cards)
        return cards
