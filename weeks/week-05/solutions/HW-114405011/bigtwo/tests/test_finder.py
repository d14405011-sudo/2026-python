# -*- coding: utf-8 -*-
import unittest
from game.finder import HandFinder
from game.models import Card, Hand
from game.classifier import HandClassifier, CardType

class TestFinder(unittest.TestCase):
    """測試牌型搜尋"""

    def test_find_singles(self):
        h = Hand([Card(3,0), Card(4,1)])
        res = HandFinder.find_singles(h)
        self.assertEqual(len(res), 2)

    def test_find_five_card_plays_excludes_plain_flush(self):
        # 同一花色但不連續，在此規則下不屬於合法五張牌型。
        h = Hand([Card(3, 2), Card(6, 2), Card(9, 2), Card(12, 2), Card(15, 2)])
        plays = HandFinder.find_five_card_plays(h)
        self.assertEqual(len(plays), 0)

    def test_find_five_card_plays_contains_straight_flush(self):
        h = Hand([Card(7, 1), Card(8, 1), Card(9, 1), Card(10, 1), Card(11, 1)])
        plays = HandFinder.find_five_card_plays(h)
        self.assertEqual(len(plays), 1)
        self.assertEqual(HandClassifier.classify(plays[0])[0], CardType.STRAIGHT_FLUSH)

    def test_find_dragons(self):
        h = Hand([Card(rank, 0) for rank in range(3, 16)])
        plays = HandFinder.find_dragons(h)
        self.assertEqual(len(plays), 1)
        self.assertEqual(HandClassifier.classify(plays[0])[0], CardType.DRAGON)

    def test_get_all_valid_plays_excludes_triples(self):
        h = Hand([Card(8, 0), Card(8, 1), Card(8, 2), Card(4, 0)])
        plays = HandFinder.get_all_valid_plays(h, None)
        self.assertFalse(any(len(p) == 3 for p in plays))
