# Week 07 作業 - 赤壁戰役模擬
# 整合 W02 的 namedtuple/Counter/defaultdict/sorted 和 W07 的檔案 I/O

import os
from collections import Counter, defaultdict, namedtuple

# W02: namedtuple 定義武將資料結構
General = namedtuple("General", ["faction", "name", "hp", "atk", "def_", "spd", "is_leader"])


class ChibiBattle:

    def __init__(self):
        self.generals = {}
        # W02: Counter 統計傷害，defaultdict 追蹤損失
        self.stats = {
            "damage": Counter(),
            "losses": defaultdict(int),
        }

    # W07: 檔案讀取，遇到 EOF 就停
    def load_generals(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "EOF":
                    break
                if not line:
                    continue
                parts = line.split()
                faction, name, hp, atk, def_, spd, is_leader = parts
                g = General(
                    faction=faction,
                    name=name,
                    hp=int(hp),
                    atk=int(atk),
                    def_=int(def_),
                    spd=int(spd),
                    is_leader=(is_leader == "True"),
                )
                self.generals[name] = g

    # W02: sorted 按速度決定出手順序
    def get_battle_order(self):
        return sorted(self.generals.values(), key=lambda g: g.spd, reverse=True)

    def calculate_damage(self, atk_name, def_name):
        a = self.generals[atk_name]
        d = self.generals[def_name]
        dmg = max(1, a.atk - d.def_)
        # W02: Counter 自動累加
        self.stats["damage"][atk_name] += dmg
        self.stats["losses"][def_name] += dmg
        return dmg

    def simulate_wave(self, wave):
        # 蜀吳打魏，魏打蜀吳；軍師有追擊加成
        ally_pool = ["關羽", "黃蓋", "劉備", "孫權", "諸葛亮", "周瑜"]
        for g in self.get_battle_order():
            if g.faction in ("蜀", "吳"):
                target = "夏侯惇" if wave == 1 else "郭嘉"
            else:
                target = ally_pool[(wave + g.spd) % len(ally_pool)]
            if target not in self.generals:
                continue
            dmg = self.calculate_damage(g.name, target)
            if g.is_leader:
                bonus = max(1, dmg // 2)
                self.stats["damage"][g.name] += bonus
                self.stats["losses"][target] += bonus

    def simulate_battle(self):
        for w in range(1, 4):
            self.simulate_wave(w)

    # W02: Counter.most_common()
    def get_damage_ranking(self, top_n=5):
        return self.stats["damage"].most_common(top_n)

    # W02: defaultdict 做勢力統計
    def get_faction_stats(self):
        result = defaultdict(int)
        for name, dmg in self.stats["damage"].items():
            result[self.generals[name].faction] += dmg
        return dict(result)

    def get_defeated_generals(self):
        defeated = []
        for name, loss in self.stats["losses"].items():
            if loss >= self.generals[name].hp:
                defeated.append(name)
        return defeated

    def print_battle_start(self):
        print("+-------------------------------------------------------+")
        print("|       赤壁戰役開始 | 蜀吳聯軍 vs 曹操魏軍              |")
        print("+-------------------------------------------------------+")
        for faction in ["蜀", "吳", "魏"]:
            print(f"\n[{faction}軍]")
            members = [g for g in self.generals.values() if g.faction == faction]
            for g in sorted(members, key=lambda x: x.spd, reverse=True):
                bar = "#" * (g.hp // 10) + "." * (10 - g.hp // 10)
                tag = " (軍師)" if g.is_leader else ""
                print(f"  {g.name:8} {bar} 攻{g.atk} 防{g.def_} 速{g.spd}{tag}")

    def print_damage_report(self):
        print("\n+-------------------------------------------------------+")
        print("|               赤壁戰役 - 傷害統計報告                 |")
        print("+-------------------------------------------------------+")

        print("\n傷害輸出 Top5:")
        for i, (name, dmg) in enumerate(self.get_damage_ranking(), 1):
            bar = "#" * (dmg // 3) + "." * max(0, 24 - dmg // 3)
            print(f"  {i}. {name:8} {bar} {dmg} HP")

        print("\n兵力損失:")
        for name in sorted(self.stats["losses"], key=lambda x: self.stats["losses"][x], reverse=True)[:5]:
            loss = self.stats["losses"][name]
            mark = "[陣亡]" if loss >= self.generals[name].hp else "      "
            print(f"  {mark} {name} 損失 {loss} HP")

        print("\n勢力傷害比較:")
        fs = self.get_faction_stats()
        total = sum(fs.values()) or 1
        for faction in ["蜀", "吳", "魏"]:
            v = fs.get(faction, 0)
            pct = v / total * 100
            bar = "#" * int(pct // 5) + "." * (20 - int(pct // 5))
            print(f"  {faction} {bar} {v} HP ({pct:.1f}%)")

    def run_full_battle(self):
        self.print_battle_start()
        print("\n--- 戰鬥開始 ---")
        self.simulate_battle()
        print("--- 戰鬥結束 ---")
        self.print_damage_report()


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    game = ChibiBattle()
    game.load_generals(os.path.join(base, "generals.txt"))
    game.run_full_battle()
