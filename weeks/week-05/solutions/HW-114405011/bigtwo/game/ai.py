# -*- coding: utf-8 -*-
# game/ai.py

import random
from typing import List, Optional
from .models import Hand, Card
from .classifier import CardType, HandClassifier

class AIStrategy:
    """AI策略"""

    INVALID_STRENGTH = (999, 999, 999, 999)
    INVALID_SCORE = -1e9
    BASE_SCORE = 1000.0
    TYPE_WEIGHT = 70
    RANK_WEIGHT = 8
    FIRST_TURN_SIZE_PREF = {1: 200.0, 2: 160.0, 3: 130.0, 5: 40.0}
    FIRST_TURN_STRONG_FIVE_PENALTY = 220.0
    FIRST_TURN_HIGH_CARD_PENALTY = 160.0
    FIRST_TURN_TWO_PENALTY = 320.0
    FULL_HOUSE_TWO_PAIR_PENALTY = 180.0
    FINISHING_BONUS = 1200.0
    THREAT_HIGH_CARD_BONUS = 80.0
    PAIR_BREAK_PENALTY = 45.0
    TRIPLE_BREAK_PENALTY = 75.0
    RANDOM_NOISE = 0.0
    LOOKAHEAD_WEIGHT = 0.85
    CARD_REMAIN_PENALTY = 32.0
    HIGH_CARD_REMAIN_PENALTY = 7.0
    THREAT_DEFENSE_THRESHOLD = 2
    AGGRESSIVE_MODE = False
    BOMB_HOLD_HUMAN_THRESHOLD = 6
    ROUND_POWER = 0.0
    ROUND_POWER_BASE = 0.35

    _rng = random.Random()

    @staticmethod
    def set_randomness(level: float = 1.0, seed: Optional[int] = None) -> None:
        """設定 AI 隨機性強度與種子，方便重現與調整難度。"""
        AIStrategy.RANDOM_NOISE = max(0.0, float(level) * 12.0)
        if seed is not None:
            AIStrategy._rng.seed(seed)

    @staticmethod
    def configure_profile(mode: str = "casual", difficulty: str = "hard") -> None:
        """根據模式配置 AI 決策風格。"""
        if mode == "ranked":
            AIStrategy.AGGRESSIVE_MODE = True
            AIStrategy.THREAT_DEFENSE_THRESHOLD = 4
            AIStrategy.BOMB_HOLD_HUMAN_THRESHOLD = 6
            AIStrategy.FINISHING_BONUS = 1450.0
            AIStrategy.LOOKAHEAD_WEIGHT = 1.0
            AIStrategy.CARD_REMAIN_PENALTY = 38.0
            AIStrategy.HIGH_CARD_REMAIN_PENALTY = 5.0
        else:
            AIStrategy.AGGRESSIVE_MODE = False
            AIStrategy.THREAT_DEFENSE_THRESHOLD = 2
            AIStrategy.BOMB_HOLD_HUMAN_THRESHOLD = 99
            AIStrategy.FINISHING_BONUS = 1200.0
            AIStrategy.LOOKAHEAD_WEIGHT = 0.85
            AIStrategy.CARD_REMAIN_PENALTY = 32.0
            AIStrategy.HIGH_CARD_REMAIN_PENALTY = 7.0
        AIStrategy.ROUND_POWER = 0.0

    @staticmethod
    def set_round_progress(current_round: int, total_rounds: int, mode: str, difficulty: str = "hard") -> None:
        """設定局數進度，僅在挑戰模式 nightmare：開局即最難並持續進步。"""
        if mode != "ranked" or difficulty != "nightmare":
            AIStrategy.ROUND_POWER = 0.0
            return
        if total_rounds <= 1:
            AIStrategy.ROUND_POWER = AIStrategy.ROUND_POWER_BASE
            return
        # 第1局即高難基線，最後一局到滿值。
        progress = max(0.0, min(1.0, (current_round - 1) / (total_rounds - 1)))
        base = AIStrategy.ROUND_POWER_BASE
        AIStrategy.ROUND_POWER = min(1.0, base + (1.0 - base) * progress)

    @staticmethod
    def _is_bomb_like(play: List[Card]) -> bool:
        info = HandClassifier.classify(play)
        if not info:
            return False
        return info[0] in (CardType.FOUR_OF_A_KIND, CardType.STRAIGHT_FLUSH, CardType.DRAGON)

    @staticmethod
    def _rank_frequencies(hand: Hand) -> dict:
        freq = {}
        for card in hand:
            freq[card.rank] = freq.get(card.rank, 0) + 1
        return freq

    @staticmethod
    def _remaining_hand_value(cards: List[Card]) -> float:
        """評估出牌後手牌品質：越高越好。"""
        if not cards:
            return 9999.0

        rank_freq = {}
        for card in cards:
            rank_freq[card.rank] = rank_freq.get(card.rank, 0) + 1

        pair_count = sum(1 for v in rank_freq.values() if v >= 2)
        triple_count = sum(1 for v in rank_freq.values() if v >= 3)
        high_cards = sum(1 for c in cards if c.rank >= 14)

        value = 0.0
        value += pair_count * 42.0
        value += triple_count * 65.0
        value -= len(cards) * AIStrategy.CARD_REMAIN_PENALTY
        value -= high_cards * AIStrategy.HIGH_CARD_REMAIN_PENALTY
        return value

    @staticmethod
    def _remaining_after_play(hand: Hand, play: List[Card]) -> List[Card]:
        play_set = {(c.rank, c.suit) for c in play}
        return [c for c in hand if (c.rank, c.suit) not in play_set]

    @staticmethod
    def _lookahead_score(
        play: List[Card],
        hand: Hand,
        is_first: bool,
        threat_level: int,
    ) -> float:
        immediate = AIStrategy.score_play(play, hand, is_first)
        remaining = AIStrategy._remaining_after_play(hand, play)
        future = AIStrategy._remaining_hand_value(remaining)

        # 對手接近收尾時，提高即時壓制權重；其餘情況平衡即時與後續。
        if threat_level <= 2:
            return immediate * (1.25 + 0.15 * AIStrategy.ROUND_POWER) + future * max(0.3, 0.45 - 0.1 * AIStrategy.ROUND_POWER)
        return immediate + future * AIStrategy.LOOKAHEAD_WEIGHT

    @staticmethod
    def _response_overkill_cost(play: List[Card], last_play: Optional[List[Card]]) -> float:
        """估算為了壓住上一手而付出的超額成本，越低代表越精準。"""
        if not last_play:
            return 0.0
        now = HandClassifier.classify(play)
        prev = HandClassifier.classify(last_play)
        if not now or not prev:
            return 0.0

        now_type, now_rank, now_suit = now
        prev_type, prev_rank, prev_suit = prev
        cost = 0.0

        # 跨張數壓牌通常是高價值資源，除非必要不應濫用。
        if len(play) != len(last_play):
            if AIStrategy._is_bomb_like(play):
                cost += 320.0
            else:
                cost += 140.0

        type_gap = max(0, int(now_type) - int(prev_type))
        rank_gap = max(0, now_rank - prev_rank)
        suit_gap = max(0, now_suit - prev_suit)

        cost += type_gap * 34.0
        cost += rank_gap * 4.5
        cost += suit_gap * 1.5

        # 黑桃2是關鍵防守牌，非必要情況盡量保留。
        if len(play) == 1 and play[0].rank == 15 and play[0].suit == 3:
            cost += 90.0

        return cost

    @staticmethod
    def _play_strength(cards: List[Card]) -> tuple:
        """評估單手出牌的強度（用於排序和比較）
        
        返回 (張數, 牌型強度, 點數, 花色)
        優先級：張數 > 牌型 > 點數 > 花色
        """
        info = HandClassifier.classify(cards)
        if not info:
            return AIStrategy.INVALID_STRENGTH
        c_type, rank, suit = info
        return (len(cards), int(c_type), rank, suit)

    @staticmethod
    def _uses_two_as_full_house_pair(cards: List[Card]) -> bool:
        """判斷是否為「葫蘆把 2 當胚（對子）」的出法。"""
        info = HandClassifier.classify(cards)
        if not info or info[0] != CardType.FULL_HOUSE:
            return False
        two_count = sum(1 for c in cards if c.rank == 15)
        return two_count == 2

    
    @staticmethod
    def score_play(cards: List[Card], hand: Hand, is_first: bool = False) -> float:
        """計算單手出牌的戰略評分
        
        評分考量因素：
        - 起手回合（is_first=True）：保守策略，優先單張/對子，避免高牌
        - 車尾回合（手牌1-2張）：激進策略，優先出牌清手
        - 中盤回合：平衡策略，用適當強度的牌
        
        起手牌型價值: 單張:200 > 對子:160 > 三條:130 > 順葫四:40
        高牌懲罰: 大王:320 > 小王:160 > A/K:160
        """
        c_type = HandClassifier.classify(cards)
        if not c_type:
            return AIStrategy.INVALID_SCORE
        
        base_score = AIStrategy.BASE_SCORE
        base_score -= float(
            int(c_type[0]) * AIStrategy.TYPE_WEIGHT
            + c_type[1] * AIStrategy.RANK_WEIGHT
            + c_type[2]
        )
        
        penalty = 0.0
        rank_freq = AIStrategy._rank_frequencies(hand)

        # 優先保留可形成對子/三條的資源，避免過早拆組。
        if len(cards) == 1:
            card_rank = cards[0].rank
            if rank_freq.get(card_rank, 0) >= 3:
                penalty += AIStrategy.TRIPLE_BREAK_PENALTY
            elif rank_freq.get(card_rank, 0) == 2:
                penalty += AIStrategy.PAIR_BREAK_PENALTY

        if is_first:
            # 起手應保守：避免浪費高牌和強五張組合
            base_score += AIStrategy.FIRST_TURN_SIZE_PREF.get(len(cards), 0.0)
            
            if c_type[0] in (CardType.STRAIGHT, CardType.FULL_HOUSE, CardType.FOUR_OF_A_KIND, CardType.STRAIGHT_FLUSH):
                penalty += AIStrategy.FIRST_TURN_STRONG_FIVE_PENALTY
            if any(c.rank >= 14 for c in cards):
                penalty += AIStrategy.FIRST_TURN_HIGH_CARD_PENALTY
            if any(c.rank == 15 for c in cards):
                penalty += AIStrategy.FIRST_TURN_TWO_PENALTY

        # 中盤策略：合法但通常不建議把 2 拿去當葫蘆胚，盡量保留 2 的防守價值。
        if AIStrategy._uses_two_as_full_house_pair(cards):
            penalty += AIStrategy.FULL_HOUSE_TWO_PAIR_PENALTY
        
        # 車尾應果斷：優先清出所有牌
        if len(hand) - len(cards) <= 1:
            base_score += AIStrategy.FINISHING_BONUS
        
        return float(base_score - penalty)

    @staticmethod
    def select_best(
        valid_plays: List[List[Card]],
        hand: Hand,
        is_first: bool = False,
        threat_level: int = 13,
        last_play: Optional[List[Card]] = None,
        human_cards: int = 13,
        last_player: Optional[str] = None,
    ) -> Optional[List[Card]]:
        """選擇最佳出牌方案
        
        決策優先級：
        1. 對手只剩1張牌（threat <= 1） → 必須出單張，優先最大點數【頂大強制性】
        2. 能直接出完 → 最強牌
        3. 對手快出完（threat == 2） → 用強牌壓制
        4. 起手回合（is_first=True） → 優先多張組合清牌
        5. 手牌充足 (> 5張) → 用最弱可壓的牌保留高牌
        6. 其他 → 綜合評分最高的牌
        """
        if not valid_plays:
            return None

        candidates = list(valid_plays)
        dynamic_threat = AIStrategy.THREAT_DEFENSE_THRESHOLD + (1 if AIStrategy.ROUND_POWER >= 0.55 else 0)

        def tiebreak_small(play: List[Card]) -> tuple:
            size, ptype, rank, suit = AIStrategy._play_strength(play)
            return (-size, -ptype, -rank, -suit)
        
        # 【優先級最高】對手只剩1張牌：絕對必須頂大（執行頂大強制性）
        if threat_level <= 1:
            single_candidates = [p for p in valid_plays if len(p) == 1]
            if single_candidates:
                # 強制出最大點數的單張以壓制對手
                return max(single_candidates, key=lambda p: (p[0].rank, p[0].suit))
            # 如果無單張可出，視為無法出牌的特殊狀況（此時應無有效牌）
            return None
        
        # 能直接收尾就直接收尾（一手出完所有牌）
        finishing = [p for p in candidates if len(hand) - len(p) == 0]
        if finishing:
            return max(finishing, key=AIStrategy._play_strength)

        # 挑戰模式：在安全區間先保留炸彈牌，必要時再釋放。
        if AIStrategy.AGGRESSIVE_MODE:
            hold_bombs = (
                human_cards > AIStrategy.BOMB_HOLD_HUMAN_THRESHOLD
                and threat_level > dynamic_threat
            )
            if hold_bombs:
                non_bomb = [p for p in candidates if not AIStrategy._is_bomb_like(p)]
                if non_bomb:
                    candidates = non_bomb

        if AIStrategy.AGGRESSIVE_MODE and human_cards <= 5:
            # 挑戰模式：人類進入收尾時，優先高壓策略搶主導權。
            if last_play is not None and last_player == "Player 1":
                return max(
                    candidates,
                    key=lambda p: (
                        AIStrategy._play_strength(p),
                        AIStrategy._lookahead_score(p, hand, is_first, threat_level),
                    ),
                )
            if human_cards <= 3:
                return max(
                    candidates,
                    key=lambda p: (
                        AIStrategy._play_strength(p),
                        len(p),
                        AIStrategy._lookahead_score(p, hand, is_first, threat_level),
                    ),
                )

        # 非首輪且桌面清空時，主動領牌優先考慮多張組合，避免過度單張化。
        if last_play is None and not is_first:
            multi = [p for p in candidates if len(p) >= 2]
            if multi:
                return max(
                    multi,
                    key=lambda p: (
                        AIStrategy._lookahead_score(p, hand, is_first, threat_level),
                        len(p),
                        -AIStrategy._play_strength(p)[2],
                    ),
                )

        # 單張對局：平時用最小可壓，高威脅時才用最大壓制。
        if last_play and len(last_play) == 1:
            single_candidates = [p for p in candidates if len(p) == 1]
            if single_candidates:
                # 高威脅（threat_level == 2）：對手剩2張牌，用強牌壓制
                if threat_level <= dynamic_threat:
                    return max(single_candidates, key=lambda p: (p[0].rank, p[0].suit))
                # 平時出單張：用最弱的牌以保留更強牌
                # 盡量保留黑桃2作為最後壓制牌。
                safe = [p for p in single_candidates if not (p[0].rank == 15 and p[0].suit == 3)]
                pool = safe or single_candidates
                return min(pool, key=lambda p: (p[0].rank, p[0].suit))
        
        # 對手即將出完時，優先用強牌壓制
        if threat_level <= dynamic_threat:
            # 末段防守：在高強度中優先帶高點數，搶奪回合主導權。
            return max(
                candidates,
                key=lambda p: (
                    AIStrategy._play_strength(p),
                    AIStrategy.score_play(p, hand, is_first) + AIStrategy.THREAT_HIGH_CARD_BONUS * (1.0 + 0.35 * AIStrategy.ROUND_POWER),
                ),
            )

        if AIStrategy.AGGRESSIVE_MODE and last_play is not None:
            # 挑戰模式：對人類收尾時強攻，其餘回合以「精準壓牌」降低亂出感。
            pressure_mode = (
                threat_level <= dynamic_threat
                or (last_player == "Player 1" and human_cards <= 5)
            )

            if pressure_mode:
                return max(
                    candidates,
                    key=lambda p: (
                        AIStrategy._play_strength(p),
                        AIStrategy._lookahead_score(p, hand, is_first, threat_level),
                    ),
                )

            overkill_weight = 0.58 + 0.22 * AIStrategy.ROUND_POWER
            return max(
                candidates,
                key=lambda p: (
                    AIStrategy._lookahead_score(p, hand, is_first, threat_level)
                    - AIStrategy._response_overkill_cost(p, last_play) * overkill_weight,
                    -float(AIStrategy._is_bomb_like(p)),
                    -AIStrategy._play_strength(p)[2],
                    -AIStrategy._play_strength(p)[3],
                ),
            )
        
        if is_first:
            # 起手回合：保留高價值組合，優先低成本起手。
            return max(
                candidates,
                key=lambda p: (AIStrategy.score_play(p, hand, True),) + tiebreak_small(p),
            )
        
        if len(hand) > 5:
            return max(
                candidates,
                key=lambda p: (AIStrategy._lookahead_score(p, hand, is_first, threat_level),) + tiebreak_small(p),
            )
        
        return max(
            candidates,
            key=lambda p: (AIStrategy._lookahead_score(p, hand, is_first, threat_level),) + tiebreak_small(p),
        )
