# -*- coding: utf-8 -*-
import unittest
from game.classifier import HandClassifier, CardType
from game.models import Card

class TestClassifier(unittest.TestCase):
    """測試牌型分類"""

    def test_single_card(self):
        self.assertEqual(HandClassifier.classify([Card(3, 0)])[0], CardType.SINGLE)

    def test_pair(self):
        self.assertEqual(HandClassifier.classify([Card(3, 0), Card(3, 1)])[0], CardType.PAIR)

    def test_triple_is_invalid(self):
        cards = [Card(8, 0), Card(8, 1), Card(8, 2)]
        self.assertIsNone(HandClassifier.classify(cards))

    def test_straight(self):
        cards = [Card(8, 0), Card(9, 1), Card(10, 2), Card(11, 0), Card(12, 3)]
        info = HandClassifier.classify(cards)
        self.assertEqual(info[0], CardType.STRAIGHT)
        self.assertEqual(info[1], 12)

    def test_plain_flush_is_invalid(self):
        cards = [Card(3, 2), Card(6, 2), Card(9, 2), Card(12, 2), Card(15, 2)]
        info = HandClassifier.classify(cards)
        self.assertIsNone(info)

    def test_full_house(self):
        cards = [Card(10, 0), Card(10, 1), Card(10, 2), Card(4, 0), Card(4, 1)]
        info = HandClassifier.classify(cards)
        self.assertEqual(info[0], CardType.FULL_HOUSE)
        self.assertEqual(info[1], 10)

    def test_four_of_a_kind(self):
        cards = [Card(13, 0), Card(13, 1), Card(13, 2), Card(13, 3), Card(5, 0)]
        info = HandClassifier.classify(cards)
        self.assertEqual(info[0], CardType.FOUR_OF_A_KIND)
        self.assertEqual(info[1], 13)

    def test_straight_flush(self):
        cards = [Card(7, 3), Card(8, 3), Card(9, 3), Card(10, 3), Card(11, 3)]
        info = HandClassifier.classify(cards)
        self.assertEqual(info[0], CardType.STRAIGHT_FLUSH)
        self.assertEqual(info[1], 11)

    def test_compare_five_card_type_strength(self):
        straight = [Card(8, 0), Card(9, 1), Card(10, 2), Card(11, 0), Card(12, 3)]
        full_house = [Card(9, 0), Card(9, 1), Card(9, 2), Card(4, 0), Card(4, 1)]
        self.assertEqual(HandClassifier.compare(full_house, straight), 1)

    def test_can_not_play_plain_flush_on_straight(self):
        last_play = [Card(5, 0), Card(6, 1), Card(7, 2), Card(8, 0), Card(9, 1)]
        plain_flush = [Card(3, 2), Card(6, 2), Card(9, 2), Card(12, 2), Card(15, 2)]
        self.assertFalse(HandClassifier.can_play(last_play, plain_flush))

    def test_full_house_cannot_beat_straight(self):
        straight = [Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0)]
        full_house = [Card(11, 1), Card(11, 2), Card(11, 3), Card(15, 0), Card(15, 2)]
        self.assertFalse(HandClassifier.can_play(straight, full_house))

    def test_straight_special_a2345(self):
        cards = [Card(14, 0), Card(15, 1), Card(3, 2), Card(4, 0), Card(5, 3)]
        info = HandClassifier.classify(cards)
        self.assertEqual(info[0], CardType.STRAIGHT)

    def test_straight_special_23456_is_highest(self):
        high = [Card(15, 3), Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 0)]
        second = [Card(14, 1), Card(15, 0), Card(3, 1), Card(4, 2), Card(5, 0)]
        self.assertEqual(HandClassifier.compare(high, second), 1)

    def test_jqka2_is_not_straight(self):
        cards = [Card(11, 0), Card(12, 1), Card(13, 2), Card(14, 3), Card(15, 0)]
        self.assertIsNone(HandClassifier.classify(cards))

    def test_dragon(self):
        cards = [
            Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0),
            Card(8, 1), Card(9, 2), Card(10, 3), Card(11, 0), Card(12, 1),
            Card(13, 2), Card(14, 3), Card(15, 0),
        ]
        info = HandClassifier.classify(cards)
        self.assertEqual(info[0], CardType.DRAGON)

    def test_same_suit_dragon_beats_mixed_dragon(self):
        mixed = [
            Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0),
            Card(8, 1), Card(9, 2), Card(10, 3), Card(11, 0), Card(12, 1),
            Card(13, 2), Card(14, 3), Card(15, 0),
        ]
        same_suit = [Card(rank, 3) for rank in range(3, 16)]
        self.assertTrue(HandClassifier.can_play(mixed, same_suit))

    def test_four_of_a_kind_can_beat_pair(self):
        last_play = [Card(10, 0), Card(10, 1)]
        four = [Card(6, 0), Card(6, 1), Card(6, 2), Card(6, 3), Card(14, 0)]
        self.assertTrue(HandClassifier.can_play(last_play, four))

    def test_straight_flush_can_beat_single(self):
        last_play = [Card(15, 0)]
        sf = [Card(7, 2), Card(8, 2), Card(9, 2), Card(10, 2), Card(11, 2)]
        self.assertTrue(HandClassifier.can_play(last_play, sf))

    def test_dragon_can_beat_single(self):
        last_play = [Card(15, 3)]
        dragon = [
            Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 0),
            Card(8, 1), Card(9, 2), Card(10, 3), Card(11, 0), Card(12, 1),
            Card(13, 2), Card(14, 3), Card(15, 0),
        ]
        self.assertTrue(HandClassifier.can_play(last_play, dragon))
