import os
import unittest
from collections import Counter

from chibi_battle import ChibiBattle

# generals.txt 在上一層資料夾
GENERALS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "generals.txt"
)


class TestStage1DataLoading(unittest.TestCase):
    # Stage 1: 讀檔測試

    def test_load_generals_from_file(self):
        game = ChibiBattle()
        game.load_generals(GENERALS_FILE)
        self.assertEqual(len(game.generals), 9)
        self.assertIn("劉備", game.generals)
        self.assertIn("曹操", game.generals)

    def test_parse_general_attributes(self):
        game = ChibiBattle()
        game.load_generals(GENERALS_FILE)
        g = game.generals["關羽"]
        self.assertEqual(g.faction, "蜀")
        self.assertEqual(g.atk, 28)
        self.assertEqual(g.def_, 14)
        self.assertEqual(g.spd, 85)

    def test_faction_distribution(self):
        game = ChibiBattle()
        game.load_generals(GENERALS_FILE)
        factions = Counter(g.faction for g in game.generals.values())
        self.assertEqual(factions["蜀"], 3)
        self.assertEqual(factions["吳"], 3)
        self.assertEqual(factions["魏"], 3)

    def test_eof_stops_reading(self):
        # EOF 後不應該繼續讀
        game = ChibiBattle()
        game.load_generals(GENERALS_FILE)
        self.assertEqual(len(game.generals), 9)


class TestStage2BattleLogic(unittest.TestCase):
    # Stage 2: 戰鬥邏輯測試

    def setUp(self):
        self.game = ChibiBattle()
        self.game.load_generals(GENERALS_FILE)

    def test_battle_order_by_speed(self):
        order = self.game.get_battle_order()
        # 最快速度是 85，最慢是 60
        self.assertEqual(order[0].spd, 85)
        self.assertEqual(order[-1].spd, 60)

    def test_calculate_damage(self):
        # 關羽 atk=28, 夏侯惇 def=14 -> 傷害 14
        dmg = self.game.calculate_damage("關羽", "夏侯惇")
        self.assertEqual(dmg, 14)

    def test_damage_accumulation(self):
        # 同一個人打兩次，Counter 要累加
        self.game.calculate_damage("關羽", "夏侯惇")  # 28-14=14
        self.game.calculate_damage("關羽", "曹操")    # 28-16=12
        self.assertEqual(self.game.stats["damage"]["關羽"], 26)

    def test_simulate_wave(self):
        self.game.simulate_wave(1)
        total = sum(self.game.stats["damage"].values())
        self.assertGreater(total, 0)

    def test_simulate_three_waves(self):
        self.game.simulate_battle()
        fs = self.game.get_faction_stats()
        shu_wu = fs.get("蜀", 0) + fs.get("吳", 0)
        wei = fs.get("魏", 0)
        self.assertGreater(shu_wu, wei)

    def test_loss_tracking(self):
        self.game.simulate_battle()
        self.assertGreater(self.game.stats["losses"]["夏侯惇"], 0)

    def test_damage_ranking_sorted(self):
        self.game.simulate_battle()
        ranking = self.game.get_damage_ranking()
        dmgs = [d for _, d in ranking]
        self.assertEqual(dmgs, sorted(dmgs, reverse=True))

    def test_faction_stats_all_positive(self):
        self.game.simulate_battle()
        fs = self.game.get_faction_stats()
        self.assertGreater(fs["蜀"], 0)
        self.assertGreater(fs["吳"], 0)
        self.assertGreater(fs["魏"], 0)

    def test_defeated_generals_exist(self):
        self.game.simulate_battle()
        defeated = self.game.get_defeated_generals()
        self.assertGreater(len(defeated), 0)


class TestStage3Refactor(unittest.TestCase):
    # Stage 3: 確認報告輸出不會改到統計數字

    def setUp(self):
        self.game = ChibiBattle()
        self.game.load_generals(GENERALS_FILE)

    def test_report_does_not_change_stats(self):
        self.game.simulate_battle()
        dmg_snap = dict(self.game.stats["damage"])
        loss_snap = dict(self.game.stats["losses"])
        self.game.print_damage_report()
        self.assertEqual(dict(self.game.stats["damage"]), dmg_snap)
        self.assertEqual(dict(self.game.stats["losses"]), loss_snap)

    def test_generals_count_still_nine(self):
        self.assertEqual(len(self.game.generals), 9)

    def test_ranking_has_enough_entries(self):
        self.game.simulate_battle()
        self.assertGreaterEqual(len(self.game.get_damage_ranking()), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
