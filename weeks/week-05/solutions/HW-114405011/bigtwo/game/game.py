# -*- coding: utf-8 -*-
# game/game.py

from typing import List, Optional
from collections import Counter
from .models import Deck, Player, Card
from .classifier import HandClassifier, CardType
from .finder import HandFinder
from .ai import AIStrategy

class BigTwoGame:
    """大老二遊戲控制類別"""
    def __init__(self, difficulty: str = "hard", mode: str = "casual"):
        self.deck = Deck()
        self.players = [
            Player("Player 1", is_ai=False),
            Player("AI 1", is_ai=True),
            Player("AI 2", is_ai=True),
            Player("AI 3", is_ai=True)
        ]
        self.current_player = 0
        self.last_play: Optional[List[Card]] = None
        self.last_player: Optional[str] = None
        self.pass_count = 0
        self.passed_players: set[str] = set()
        self.turn_id = 0
        self.opening_player_index = 0
        self.opening_required = True
        self.winner: Optional[Player] = None
        self.round_number = 1
        self.is_paused = False
        self.history: List[str] = []
        self.difficulty = difficulty  # "easy", "medium", "hard", or "nightmare"
        self.mode = mode  # "casual" or "ranked"
        # 根據難度設置 AI 隨機性
        self._set_ai_difficulty(difficulty)

    def _log(self, message: str) -> None:
        self.history.append(message)

    def _set_ai_difficulty(self, difficulty: str) -> None:
        """根據難度設置 AI 隨機性參數"""
        difficulty_map = {
            "easy": 0.2,      # 低難度：隨機性強
            "medium": 0.5,    # 中難度：平衡
            "hard": 0.8,      # 高難度：較少隨機
            "nightmare": 1.0, # 困難：幾乎無隨機
        }
        randomness_level = difficulty_map.get(difficulty, 1.0)
        AIStrategy.set_randomness(randomness_level)
        AIStrategy.configure_profile(self.mode, difficulty)

    def get_recent_history(self, limit: int = 8) -> List[str]:
        return self.history[-limit:]

    def toggle_pause(self) -> bool:
        self.is_paused = not self.is_paused
        self._log("遊戲暫停" if self.is_paused else "遊戲繼續")
        return self.is_paused

    def setup(self):
        # 初始設定
        self.deck.shuffle()
        for _ in range(13):
            for p in self.players:
                p.take_cards(self.deck.deal(1))
                
        # 尋找梅花三來決定起手玩家
        for i, p in enumerate(self.players):
            if p.hand.find_3_clubs():
                self.current_player = i
                self.opening_player_index = i
                self.opening_required = True
                self._log(f"開局：{p.name} 持有梅花3先手")
                break

    def _contains_3_clubs(self, cards: List[Card]) -> bool:
        return any(c.rank == 3 and c.suit == 0 for c in cards)

    def _play_sort_key(self, play: List[Card]) -> tuple:
        info = HandClassifier.classify(play)
        if not info:
            return (-1, -1, -1, -1)
        return (int(info[0]), info[1], info[2], len(play))

    def _same_play(self, p1: List[Card], p2: List[Card]) -> bool:
        key1 = sorted((c.rank, c.suit) for c in p1)
        key2 = sorted((c.rank, c.suit) for c in p2)
        return key1 == key2

    def _is_current_player(self, player: Player) -> bool:
        return self.players[self.current_player] is player

    def _format_card_for_log(self, card: Card) -> str:
        """用花色符號輸出，維持直觀牌面顯示。"""
        suit_map = {0: "♣", 1: "♢", 2: "♥", 3: "♠"}
        suit = suit_map.get(card.suit, "?")
        rank = Card.RANKS.get(card.rank, str(card.rank))
        return f"{suit}{rank}"

    def _format_play_for_log(self, cards: List[Card]) -> str:
        """格式化出牌紀錄，避免合法順子顯示成亂序。"""
        info = HandClassifier.classify(cards)
        if not info:
            return "[" + ", ".join(
                self._format_card_for_log(c) if isinstance(c, Card) else str(c)
                for c in cards
            ) + "]"

        ctype = info[0]
        type_name = {
            CardType.SINGLE: "單張",
            CardType.PAIR: "一對",
            CardType.STRAIGHT: "順子",
            CardType.FULL_HOUSE: "葫蘆",
            CardType.FOUR_OF_A_KIND: "鐵支",
            CardType.STRAIGHT_FLUSH: "同花順",
            CardType.DRAGON: "一條龍",
        }.get(ctype, "牌型")

        ordered = list(cards)
        ranks = {c.rank for c in cards}
        if ctype in (CardType.STRAIGHT, CardType.STRAIGHT_FLUSH):
            # 特殊順子顯示為規則文案常見順序，避免被誤認為無效牌。
            if ranks == {3, 4, 5, 14, 15}:      # A2345
                rank_order = {14: 0, 15: 1, 3: 2, 4: 3, 5: 4}
                ordered.sort(key=lambda c: (rank_order[c.rank], c.suit))
            elif ranks == {3, 4, 5, 6, 15}:    # 23456
                rank_order = {15: 0, 3: 1, 4: 2, 5: 3, 6: 4}
                ordered.sort(key=lambda c: (rank_order[c.rank], c.suit))
            else:
                ordered.sort(key=lambda c: c.to_sort_key())
        else:
            ordered.sort(key=lambda c: c.to_sort_key())

        cards_text = "[" + ", ".join(self._format_card_for_log(c) for c in ordered) + "]"
        return f"（{type_name}）{cards_text}"

    def _clear_table(self, log_message: Optional[str] = None) -> None:
        if log_message:
            self._log(log_message)
        self.last_play = None
        self.last_player = None
        self.pass_count = 0
        self.passed_players.clear()

    def _cards_in_hand(self, player: Player, cards: List[Card]) -> bool:
        if not cards:
            return False
        hand_counter = Counter((c.rank, c.suit) for c in player.hand)
        play_counter = Counter((c.rank, c.suit) for c in cards)
        for key, needed in play_counter.items():
            if hand_counter.get(key, 0) < needed:
                return False
        return True

    def get_valid_plays_for_player(self, player: Player) -> List[List[Card]]:
        if self.is_player_locked(player):
            return []
        valid = HandFinder.get_all_valid_plays(player.hand, self.last_play)
        if self.opening_required and player is self.players[self.opening_player_index]:
            valid = [play for play in valid if self._contains_3_clubs(play)]
        return valid

    def is_top_guard_forced(self, player: Player) -> bool:
        player_idx = self.players.index(player)
        next_idx = (player_idx + 1) % len(self.players)
        return len(self.players[next_idx].hand) == 1

    def get_required_top_guard_play(self, player: Player) -> Optional[List[Card]]:
        if not self.is_top_guard_forced(player):
            return None
        valid = self.get_valid_plays_for_player(player)
        if not valid:
            return None
        return max(valid, key=self._play_sort_key)

    def can_play_cards(self, player: Player, cards: List[Card]) -> bool:
        if self.is_paused:
            return False
        if not self._is_current_player(player):
            return False
        if self.is_player_locked(player):
            return False
        if not self._cards_in_hand(player, cards):
            return False
        if not self._is_valid_play(cards):
            return False

        if self.opening_required and player is self.players[self.opening_player_index]:
            if not self._contains_3_clubs(cards):
                return False

        required = self.get_required_top_guard_play(player)
        if required is not None and not self._same_play(cards, required):
            return False

        return True

    def can_pass(self, player: Player) -> bool:
        if self.is_paused:
            return False
        if not self._is_current_player(player):
            return False
        if self.last_play is None:
            return False
        if self.is_player_locked(player):
            return False
        if self.opening_required and player is self.players[self.opening_player_index]:
            return False
        required = self.get_required_top_guard_play(player)
        if required is not None:
            return False
        return True

    def play(self, player: Player, cards: List[Card]) -> bool:
        # 人類或AI出牌
        if self.can_play_cards(player, cards):
            player.play_cards(cards)
            self.last_play = cards
            self.last_player = player.name
            self.pass_count = 0
            if self.opening_required and player is self.players[self.opening_player_index]:
                self.opening_required = False
            self._log(f"{player.name} 出牌 {self._format_play_for_log(cards)}")
            if len(player.hand) == 0:
                self.winner = player
                self._log(f"{player.name} 勝出")
            return True
        return False

    def pass_turn(self, player: Player) -> bool:
        # 過牌
        if not self.can_pass(player):
            return False
        self.passed_players.add(player.name)
        self.pass_count += 1
        self._log(f"{player.name} 過牌")
        return True

    def next_turn(self):
        # 換下一位玩家；本輪已過牌者在清桌前會被自動跳過。
        if self.is_paused:
            return

        player_count = len(self.players)
        for _ in range(player_count):
            self.current_player = (self.current_player + 1) % player_count
            self.turn_id += 1
            self.check_round_reset()

            # 清桌後鎖定會解除，直接停在下一位。
            if self.last_play is None:
                return

            current = self.players[self.current_player]
            if self.last_player == current.name:
                self._clear_table("出牌權回到上一手玩家，清桌重開")
                return

            if not self.is_player_locked(current):
                return

            self._log(f"{current.name} 本輪已過牌，跳過")

        # 保底：若異常出現全員鎖定，強制清桌避免死循環。
        self._clear_table("偵測到回合鎖死，強制清桌")

    def _is_valid_play(self, cards: List[Card]) -> bool:
        # 檢查出牌是否合法
        return HandClassifier.can_play(self.last_play, cards)

    def is_player_locked(self, player: Player) -> bool:
        # 本輪曾過牌者，在清桌前不可再進場。
        return self.last_play is not None and player.name in self.passed_players

    def check_round_reset(self):
        # 若已有3人過牌，重置桌面
        if self.pass_count >= 3:
            self._clear_table("三家過牌，清桌重開")

    def get_current_player(self) -> Player:
        return self.players[self.current_player]

    def ai_turn(self) -> bool:
        # 執行 AI 回合
        if self.is_paused:
            return False
        p = self.get_current_player()
        if not p.is_ai:
            return False

        if self.is_player_locked(p):
            self._log(f"{p.name} 本輪已過牌，略過")
            self.next_turn()
            return True
            
        required = self.get_required_top_guard_play(p)
        if required is not None:
            best = required
        else:
            valid = self.get_valid_plays_for_player(p)
            other_counts = [len(player.hand) for player in self.players if player is not p]
            threat = min(other_counts) if other_counts else 13
            human = self.players[0] if self.players else None
            human_cards = len(human.hand) if human is not None else 13
            if self.mode == "ranked":
                # 挑戰模式：優先按人類剩牌施壓，而非僅看全場最少。
                threat = min(threat, human_cards)
            best = AIStrategy.select_best(
                valid,
                p.hand,
                self.opening_required,
                threat,
                self.last_play,
                human_cards=human_cards,
                last_player=self.last_player,
            )

        acted = False
        if best:
            acted = self.play(p, best)

        if not acted:
            acted = self.pass_turn(p)

        if not acted:
            # 保底機制：避免在特殊狀態下無限輪轉。
            self._clear_table(f"{p.name} 回合無法出牌也無法過牌，強制清桌")
            valid = self.get_valid_plays_for_player(p)
            if valid:
                forced = min(valid, key=self._play_sort_key)
                acted = self.play(p, forced)

        if acted:
            self.next_turn()
        return acted
