# 簡化版 - 只看結果用
import os
from chibi_battle import ChibiBattle

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

game = ChibiBattle()
game.load_generals(os.path.join(base, "generals.txt"))
game.simulate_battle()

print("=== 赤壁戰役 結果 ===")
print("\n傷害排名:")
for i, (name, dmg) in enumerate(game.get_damage_ranking(), 1):
    print(f"  {i}. {name}: {dmg} HP")

print("\n各勢力傷害:")
for faction, dmg in game.get_faction_stats().items():
    print(f"  {faction}: {dmg} HP")

print("\n陣亡武將:", game.get_defeated_generals())
