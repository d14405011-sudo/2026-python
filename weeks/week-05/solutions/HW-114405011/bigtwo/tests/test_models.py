# -*- coding: utf-8 -*-
import unittest
from game.models import Card, Deck, Hand, Player

class TestModels(unittest.TestCase):
    """測試資料模型"""
    def test_card_creation(self):
        # 測試建立卡牌
        c = Card(rank=14, suit=3)
        self.assertEqual(c.rank, 14)
        self.assertEqual(c.suit, 3)

    def test_card_repr_ace(self):
        # 測試黑桃A的字串表示
        c = Card(14, 3)
        self.assertEqual(repr(c), "♠A")

    def test_card_repr_three(self):
        # 測試梅花3的字串表示
        c = Card(3, 0)
        self.assertEqual(repr(c), "♣3")

    def test_card_compare_suit(self):
        # 測試花色比較 (黑桃 > 紅心)
        self.assertTrue(Card(14, 3) > Card(14, 2))

    def test_card_compare_rank(self):
        # 測試數字比較 (2 > A)
        self.assertTrue(Card(15, 0) > Card(14, 3))

    def test_deck_has_52_cards(self):
        # 測試牌組是否剛好52張
        d = Deck()
        self.assertEqual(len(d.cards), 52)
