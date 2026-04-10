# -*- coding: utf-8 -*-
import unittest
from game.ai import AIStrategy
from game.models import Hand, Card
from game.classifier import CardType

class TestAI(unittest.TestCase):
    """測試 AI 策略"""
    def test_score_play(self):
        # 測試出牌評分
        hand = Hand([Card(3, 0), Card(4, 1)])
        score = AIStrategy.score_play([Card(3, 0)], hand)
        self.assertGreater(score, 0)

    def test_select_best_first_turn_prefers_low_cost_play(self):
        hand = Hand([
            Card(3, 0), Card(5, 0), Card(7, 0), Card(9, 0), Card(11, 0),
            Card(6, 1), Card(6, 2), Card(12, 3),
        ])
        valid_plays = [
            [Card(3, 0)],
            [Card(3, 0), Card(5, 0), Card(7, 0), Card(9, 0), Card(11, 0)],
        ]

        best = AIStrategy.select_best(valid_plays, hand, is_first=True, threat_level=13)
        self.assertEqual(best, [Card(3, 0)])

    def test_select_best_single_response_uses_smallest_winner(self):
        hand = Hand([Card(5, 0), Card(6, 1), Card(15, 3)])
        valid_plays = [[Card(5, 0)], [Card(6, 1)], [Card(15, 3)]]
        last_play = [Card(4, 2)]

        best = AIStrategy.select_best(valid_plays, hand, is_first=False, threat_level=13, last_play=last_play)
        self.assertEqual(best, [Card(5, 0)])

    def test_select_best_single_response_under_threat_uses_strongest(self):
        hand = Hand([Card(5, 0), Card(6, 1), Card(15, 3)])
        valid_plays = [[Card(5, 0)], [Card(6, 1)], [Card(15, 3)]]
        last_play = [Card(4, 2)]

        best = AIStrategy.select_best(valid_plays, hand, is_first=False, threat_level=1, last_play=last_play)
        self.assertEqual(best, [Card(15, 3)])

    def test_select_best_prefers_multi_when_leading_non_opening(self):
        hand = Hand([Card(4, 0), Card(9, 0), Card(9, 2), Card(12, 1)])
        valid_plays = [[Card(4, 0)], [Card(9, 0)], [Card(12, 1)], [Card(9, 0), Card(9, 2)]]

        best = AIStrategy.select_best(valid_plays, hand, is_first=False, threat_level=13, last_play=None)
        self.assertEqual(best, [Card(9, 0), Card(9, 2)])

    def test_select_best_full_house_avoids_two_as_pair_when_not_urgent(self):
        hand = Hand([
            Card(10, 0), Card(10, 1), Card(10, 2),
            Card(15, 0), Card(15, 2),
            Card(9, 0), Card(9, 1),
        ])
        full_house_with_twos = [Card(10, 0), Card(10, 1), Card(10, 2), Card(15, 0), Card(15, 2)]
        full_house_with_nines = [Card(10, 0), Card(10, 1), Card(10, 2), Card(9, 0), Card(9, 1)]

        best = AIStrategy.select_best(
            [full_house_with_twos, full_house_with_nines],
            hand,
            is_first=False,
            threat_level=13,
            last_play=None,
        )

        self.assertEqual(best, full_house_with_nines)
