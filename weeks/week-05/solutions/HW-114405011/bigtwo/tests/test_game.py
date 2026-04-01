# -*- coding: utf-8 -*-
import unittest
from game.game import BigTwoGame
from game.models import Card, Hand

class TestGame(unittest.TestCase):
    """測試遊戲流程"""
    def test_setup(self):
        # 測試初始化
        g = BigTwoGame()
        g.setup()
        self.assertEqual(len(g.players), 4)
        for p in g.players:
            self.assertEqual(len(p.hand), 13)

    def test_pass_lock_and_reset(self):
        g = BigTwoGame()
        g.opening_required = False
        p = g.players[0]

        # 無桌牌時不可 PASS。
        self.assertFalse(g.pass_turn(p))

        g.last_play = [Card(3, 0)]
        self.assertTrue(g.pass_turn(p))
        self.assertTrue(g.is_player_locked(p))

        # 三家 PASS 後清桌，鎖定解除。
        g.pass_count = 3
        g.check_round_reset()
        self.assertIsNone(g.last_play)
        self.assertFalse(g.is_player_locked(p))

    def test_locked_player_cannot_play(self):
        g = BigTwoGame()
        p = g.players[0]
        p.hand = Hand([Card(4, 1)])
        g.last_play = [Card(3, 0)]
        g.passed_players.add(p.name)

        self.assertFalse(g.play(p, [Card(4, 1)]))

    def test_opening_must_contain_3_clubs(self):
        g = BigTwoGame()
        g.current_player = 0
        g.opening_player_index = 0
        g.opening_required = True
        p = g.players[0]
        p.hand = Hand([Card(3, 0), Card(4, 0), Card(5, 1)])

        self.assertFalse(g.play(p, [Card(4, 0)]))
        self.assertTrue(g.play(p, [Card(3, 0)]))

    def test_opening_can_be_any_valid_play_containing_3_clubs(self):
        g = BigTwoGame()
        g.current_player = 0
        g.opening_player_index = 0
        g.opening_required = True
        p = g.players[0]
        p.hand = Hand([Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 1)])

        self.assertTrue(g.play(p, [Card(3, 0), Card(4, 1), Card(5, 2), Card(6, 3), Card(7, 1)]))

    def test_top_guard_forces_largest_play(self):
        g = BigTwoGame()
        g.opening_required = False
        g.current_player = 0
        p = g.players[0]
        down = g.players[1]

        # 下家剩1張，觸發頂大顧牌。
        down.hand = Hand([Card(8, 3)])
        p.hand = Hand([Card(9, 0), Card(10, 0), Card(11, 0)])
        g.last_play = [Card(8, 0)]

        required = g.get_required_top_guard_play(p)
        self.assertIsNotNone(required)
        self.assertEqual(required[0].rank, 11)

        self.assertFalse(g.can_pass(p))
        self.assertFalse(g.play(p, [Card(9, 0)]))
        self.assertTrue(g.play(p, required))

    def test_top_guard_forced_on_non_single_round(self):
        g = BigTwoGame()
        g.opening_required = False
        g.current_player = 0
        p = g.players[0]
        down = g.players[1]

        down.hand = Hand([Card(8, 3)])
        p.hand = Hand([
            Card(9, 0), Card(9, 1), Card(9, 2), Card(4, 0), Card(4, 1),
            Card(10, 0), Card(10, 1), Card(10, 2), Card(5, 0), Card(5, 1),
        ])
        g.last_play = [Card(8, 0), Card(8, 1), Card(8, 2), Card(3, 0), Card(3, 1)]

        self.assertIsNotNone(g.get_required_top_guard_play(p))

    def test_only_current_player_can_act(self):
        g = BigTwoGame()
        g.opening_required = False
        g.current_player = 0
        g.last_play = [Card(3, 0)]

        p0 = g.players[0]
        p1 = g.players[1]
        p0.hand = Hand([Card(4, 1)])
        p1.hand = Hand([Card(5, 1)])

        self.assertFalse(g.play(p1, [Card(5, 1)]))
        self.assertFalse(g.pass_turn(p1))
        self.assertTrue(g.play(p0, [Card(4, 1)]))

    def test_locked_player_cannot_pass_twice(self):
        g = BigTwoGame()
        g.opening_required = False
        g.current_player = 0
        g.last_play = [Card(8, 0)]
        p = g.players[0]

        self.assertTrue(g.pass_turn(p))
        self.assertEqual(g.pass_count, 1)
        self.assertFalse(g.pass_turn(p))
        self.assertEqual(g.pass_count, 1)

    def test_cannot_play_cards_not_in_hand(self):
        g = BigTwoGame()
        g.opening_required = False
        g.current_player = 0
        g.last_play = [Card(3, 0)]
        p = g.players[0]
        p.hand = Hand([Card(4, 1)])

        self.assertFalse(g.play(p, [Card(5, 1)]))

    def test_next_turn_skips_locked_players(self):
        g = BigTwoGame()
        g.opening_required = False
        g.current_player = 3  # AI 3
        g.last_play = [Card(8, 0)]
        g.passed_players = {"Player 1"}

        g.next_turn()
        # 應跳過已鎖定的 Player 1，直接到 AI 1。
        self.assertEqual(g.current_player, 1)

    def test_turn_returns_to_last_player_should_clear_table(self):
        g = BigTwoGame()
        g.opening_required = False
        g.current_player = 0
        g.last_play = [Card(13, 2), Card(13, 1)]
        g.last_player = "Player 1"
        g.passed_players = {"AI 1", "AI 2", "AI 3"}

        g.next_turn()

        self.assertEqual(g.current_player, 0)
        self.assertIsNone(g.last_play)
        self.assertIsNone(g.last_player)
        self.assertEqual(g.pass_count, 0)
        self.assertEqual(len(g.passed_players), 0)

    def test_ai_turn_fallback_avoids_idle_rotation(self):
        g = BigTwoGame()
        g.opening_required = False
        g.current_player = 1

        ai = g.players[1]
        ai.is_ai = True
        ai.hand = Hand([Card(6, 0)])

        # 建立不一致狀態：桌面空但 can_pass 不該成功，且 valid_plays 會先被 mock 成空。
        g.last_play = None

        original_get_valid = g.get_valid_plays_for_player
        state = {"count": 0}

        def fake_get_valid(player):
            state["count"] += 1
            if state["count"] == 1:
                return []
            return original_get_valid(player)

        g.get_valid_plays_for_player = fake_get_valid  # type: ignore[method-assign]

        acted = g.ai_turn()

        self.assertTrue(acted)
        self.assertIsNotNone(g.last_player)

    def test_play_log_uses_ascii_suit_symbols(self):
        g = BigTwoGame()
        cards = [Card(11, 1), Card(11, 3), Card(15, 0), Card(15, 2), Card(15, 3)]

        msg = g._format_play_for_log(cards)

        self.assertIn("（葫蘆）", msg)
        self.assertIn("♢J", msg)
        self.assertIn("♠J", msg)
        self.assertIn("♣2", msg)
        self.assertIn("♥2", msg)
        self.assertIn("♠2", msg)
