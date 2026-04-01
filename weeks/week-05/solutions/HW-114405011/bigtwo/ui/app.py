# -*- coding: utf-8 -*-
import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui.render import Renderer
from ui.input import InputHandler
from ui.effects import BackgroundEffect, ParticleEffect, GlowEffect
from ui.sound import get_sound_manager
from game.game import BigTwoGame
from game.classifier import HandClassifier, CardType
from game.finder import HandFinder
from game.ai import AIStrategy


class BigTwoApp:
    def __init__(self):
        pygame.init()
        self.width = 1000
        self.height = 700
        self.min_width = 900
        self.min_height = 620
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("大老二 (Big Two)")

        # 初始化渲染器 - 支持主題
        self.current_theme = 'default'  # 可選: winter, neon, summer, default
        self.renderer = Renderer(self.width, self.height, theme=self.current_theme)
        self.input_handler = InputHandler(self.renderer)
        
        # 初始化音效管理器
        self.sound_manager = get_sound_manager()

        # Visual effects runtime state
        self.bg_effect = BackgroundEffect(self.width, self.height, color=self.renderer.glow_color)
        self.particle_effects = []
        self.glow_effects = []
        self.last_history_len = 0

        self.scene = "lobby"  # lobby | playing | result
        self.game = BigTwoGame()
        # Defer expensive setup until user clicks "開始遊玩".

        self.action_bar = pygame.Rect(0, 0, 0, 0)
        self.human_hand_x = 140
        self.human_hand_y = 450
        self.human_hand_spacing = 44

        self.menu_buttons = {}
        self.result_buttons = {}
        self.round_buttons = {}
        self.mode_buttons = {}
        self.difficulty_buttons = {}
        self.round_adjust_buttons = {}
        self.background_buttons = {}
        self.table_style_buttons = {}
        self.card_back_buttons = {}

        self.round_options = [3, 5, 10]
        self.selected_rounds = 5
        self.mode_options = {
            "casual": "休閒模式",
            "ranked": "挑戰模式",
        }
        self.selected_mode = "casual"
        
        # 難度選擇（只在休閒模式可見）
        self.difficulty_options = {
            "easy": "低難度",
            "medium": "中難度", 
            "hard": "高難度",
        }
        self.selected_difficulty = "hard"  # 預設高難度

        self.background_options = {
            "diagonal": "斜紋背景",
            "grid": "網格背景",
            "clean": "純淨背景",
        }
        self.table_style_options = {
            "blue": "深藍桌布",
            "green": "綠絨桌布",
            "red": "酒紅桌布",
        }
        self.card_back_options = {
            "ring": "同心圓牌背",
            "diamond": "菱紋牌背",
            "minimal": "極簡牌背",
        }
        self.selected_background = "diagonal"
        self.selected_table_style = "blue"
        self.selected_card_back = "ring"

        self.renderer.set_background_style(self.selected_background)
        self.renderer.set_table_style(self.selected_table_style)
        self.renderer.set_card_back_style(self.selected_card_back)

        self.current_round = 1
        self.total_rounds = self.selected_rounds
        self.ai_delay_ms = 720
        self.next_auto_action_ms = 0
        self.auto_play_human = False
        self.turn_timeout_ms = 15000
        self.full_auto_grace_ms = 1400
        self.turn_deadline_ms = 0
        self.idle_human_turns = 0
        self.pending_full_auto = False
        self.full_auto_mode = False
        self.human_interacted_this_turn = False
        self.observed_turn_id = -1
        self.show_help = False
        self.help_tab = "操作"
        self.help_button = pygame.Rect(0, 0, 0, 0)
        self.help_tab_buttons = {}
        self.help_close_button = pygame.Rect(0, 0, 0, 0)

        self.session_points = {
            "Player 1": 0,
            "AI 1": 0,
            "AI 2": 0,
            "AI 3": 0,
        }
        self.last_settlement = []
        self.result_prepared = False

        self.update_layout(self.width, self.height)

    def _refresh_effect_palette(self):
        self.bg_effect.color = self.renderer.glow_color

    def _reset_effects_for_scene(self):
        """重置場景效果，並清理粒子計數"""
        self.bg_effect = BackgroundEffect(self.width, self.height, color=self.renderer.glow_color)
        self.particle_effects.clear()
        self.glow_effects.clear()

    def _emit_center_play_effect(self):
        # 已停用：中間動態特效會影響流暢度
        return

    def _emit_victory_effect(self):
        # 已停用：中間動態特效會影響流暢度
        return

    def _update_effects(self):
        self.bg_effect.update()

        alive_particles = []
        for effect in self.particle_effects:
            if effect.update():
                alive_particles.append(effect)
        self.particle_effects = alive_particles

        alive_glows = []
        for glow in self.glow_effects:
            glow.update()
            if glow.is_alive():
                alive_glows.append(glow)
        self.glow_effects = alive_glows[-6:]

    def _process_history_effects(self):
        if not self.game:
            return
        if self.last_history_len > len(self.game.history):
            self.last_history_len = 0

        new_logs = self.game.history[self.last_history_len:]
        self.last_history_len = len(self.game.history)

        for line in new_logs:
            if " 出牌 " in line:
                self._emit_center_play_effect()
            elif " 勝出" in line:
                self._emit_victory_effect()

    def _update_hand_layout_for_count(self, human_hand_count):
        hand_left = self.action_bar.x + 22
        hand_right = self.input_handler.buttons["出牌 (Enter)"].x - 24
        hand_area_width = max(320, hand_right - hand_left)
        if human_hand_count > 1:
            min_spacing = 34
            max_spacing = 62
            fit_spacing = (hand_area_width - self.renderer.CARD_WIDTH) // (human_hand_count - 1)
            self.human_hand_spacing = max(min_spacing, min(max_spacing, fit_spacing))
        else:
            self.human_hand_spacing = 0

        total_hand_width = max(0, (human_hand_count - 1) * self.human_hand_spacing + self.renderer.CARD_WIDTH)
        self.human_hand_x = hand_left + max(0, (hand_area_width - total_hand_width) // 2)
        self.human_hand_y = self.height - 145
        self.input_handler.set_layout(self.human_hand_x, self.human_hand_y, self.human_hand_spacing)

        if human_hand_count > 0:
            self.input_handler.cursor_index = max(0, min(self.input_handler.cursor_index, human_hand_count - 1))
        else:
            self.input_handler.cursor_index = 0

    def _reset_session_points(self):
        for k in self.session_points:
            self.session_points[k] = 0

    def start_new_game(self, new_session=False):
        if new_session:
            self._reset_session_points()
            self.current_round = 1
            self.total_rounds = self.selected_rounds

        # 如果是挑戰賽，難度固定為困難
        difficulty = "nightmare" if self.selected_mode == "ranked" else self.selected_difficulty
        self.game = BigTwoGame(difficulty=difficulty, mode=self.selected_mode)
        self.game.setup()
        AIStrategy.set_round_progress(self.current_round, self.total_rounds, self.selected_mode, difficulty)
        if self.selected_mode == "ranked" and difficulty == "nightmare":
            ai_level = int(round(AIStrategy.ROUND_POWER * 100))
            self.game._log(f"挑戰AI進化等級: {ai_level}%")
        
        # 根據遊戲模式應用主題
        # 挑戰模式：冬季（深沉風格），休閒模式：夏日（明亮風格）
        theme = 'winter' if self.selected_mode == 'ranked' else 'summer'
        if self.current_theme != theme:
            self.current_theme = theme
            self.renderer.set_theme(theme)
            self._refresh_effect_palette()
        
        self.input_handler.selected_indices.clear()
        self.input_handler.cursor_index = 0
        self.show_help = False
        self.help_tab = "操作"
        self.auto_play_human = False
        self.turn_deadline_ms = 0
        self.idle_human_turns = 0
        self.pending_full_auto = False
        self.full_auto_mode = False
        self.human_interacted_this_turn = False
        self.observed_turn_id = -1
        self.next_auto_action_ms = 0
        self.result_prepared = False
        self.scene = "playing"
        self.last_history_len = len(self.game.history)
        self._reset_effects_for_scene()
        self.update_layout(self.width, self.height)

    def _run_human_autoplay_turn(self):
        if not self.game or self.game.winner or self.game.is_paused:
            return False
        p = self.game.get_current_player()
        if p.is_ai:
            return False

        valid = HandFinder.get_all_valid_plays(p.hand, self.game.last_play)
        other_counts = [len(player.hand) for player in self.game.players if player is not p]
        threat = min(other_counts) if other_counts else 13
        best = AIStrategy.select_best(valid, p.hand, self.game.last_play is None, threat)

        if best:
            self.game.play(p, best)
        else:
            self.game.pass_turn(p)
        self.game.next_turn()
        return True

    def _begin_human_turn(self):
        now = pygame.time.get_ticks()
        self.turn_deadline_ms = now + self.turn_timeout_ms
        self.human_interacted_this_turn = False
        if self.pending_full_auto:
            self.pending_full_auto = False
            self.full_auto_mode = True
            self.game._log("連續2輪未操作，整手自動代打已啟動")
        if self.full_auto_mode:
            self.turn_deadline_ms = now + self.full_auto_grace_ms

    def _mark_human_activity(self):
        if not self.game:
            return
        p = self.game.get_current_player()
        if p.is_ai:
            return
        if self.full_auto_mode:
            self.full_auto_mode = False
            self.pending_full_auto = False
            self.game._log("偵測玩家操作，已取消整手自動代打")
        self.human_interacted_this_turn = True
        self.idle_human_turns = 0

    def _select_smallest_single(self, hand, last_play):
        valid = HandFinder.get_all_valid_plays(hand, last_play)
        singles = [play for play in valid if len(play) == 1]
        if not singles:
            return None
        return min(singles, key=lambda play: play[0].to_sort_key())

    def _run_timeout_autoplay_turn(self):
        if not self.game or self.game.winner or self.game.is_paused:
            return False
        p = self.game.get_current_player()
        if p.is_ai:
            return False

        required = self.game.get_required_top_guard_play(p)
        if required:
            self.game.play(p, required)
            self.game._log(f"{p.name} 頂大顧牌，自動出最大牌 {required}")
            self.idle_human_turns += 1
            self.game.next_turn()
            return True

        best_single = self._select_smallest_single(p.hand, self.game.last_play)
        if best_single:
            self.game.play(p, best_single)
            self.game._log(f"{p.name} 逾時，自動出最小單張 {best_single}")
        else:
            self.game.pass_turn(p)
            self.game._log(f"{p.name} 逾時，無單張可壓，自動PASS")

        self.idle_human_turns += 1
        if self.idle_human_turns >= 2 and (not self.full_auto_mode):
            self.pending_full_auto = True
            self.game._log("再下一輪將啟動整手自動代打")

        self.game.next_turn()
        return True

    def _run_full_auto_turn(self):
        if not self.game or self.game.winner or self.game.is_paused:
            return False
        p = self.game.get_current_player()
        if p.is_ai:
            return False

        required = self.game.get_required_top_guard_play(p)
        if required:
            self.game.play(p, required)
            self.game._log(f"{p.name} 整手代打（頂大顧牌）：出最大牌 {required}")
            self.game.next_turn()
            return True

        if self.game.last_play is None or len(self.game.last_play) == 1:
            best_single = self._select_smallest_single(p.hand, self.game.last_play)
            if best_single:
                self.game.play(p, best_single)
                self.game._log(f"{p.name} 整手代打：出最小單張 {best_single}")
            else:
                self.game.pass_turn(p)
                self.game._log(f"{p.name} 整手代打：無單張可壓，自動PASS")
        else:
            self.game.pass_turn(p)
            self.game._log(f"{p.name} 整手代打：非單張局面，自動PASS")

        self.game.next_turn()
        return True

    def _format_card_type(self, cards):
        info = HandClassifier.classify(cards)
        if not info:
            return "非法牌型"
        mapping = {
            CardType.SINGLE: "單張",
            CardType.PAIR: "對子",
            CardType.STRAIGHT: "順子",
            CardType.FULL_HOUSE: "葫蘆",
            CardType.FOUR_OF_A_KIND: "四條",
            CardType.STRAIGHT_FLUSH: "同花順",
            CardType.DRAGON: "一條龍",
        }
        return mapping.get(info[0], "未知牌型")

    def _selected_cards(self):
        if not self.game:
            return []
        current_p = self.game.players[self.game.current_player]
        if current_p.is_ai:
            return []
        if not self.input_handler.selected_indices:
            return []
        cards = [current_p.hand[i] for i in sorted(self.input_handler.selected_indices, reverse=True)]
        cards.reverse()
        return cards

    def _can_play_selected(self):
        cards = self._selected_cards()
        if not cards:
            return False
        p = self.game.players[self.game.current_player]
        return self.game.can_play_cards(p, cards)

    def _calc_penalty(self, player):
        """根據模式計算扣分。
        
        休閒模式：簡單計分，不使用老 2 加倍
        挑戰賽：複雜計分，參考賽制規則
        """
        cards_left = len(player.hand)
        
        if self.selected_mode == "casual":
            # 休閒模式：簡單計分（不用計分）
            return 0
        
        # 挑戰賽模式：複雜計分
        # 基礎分數：剩餘每張 1 分
        base = cards_left
        
        # 加倍 1：剩餘 >= 9 張時加倍
        multiplier = 2 if cards_left >= 9 else 1
        
        # 加倍 2：統計老 2 的數量（2♠ 即 rank=15, suit=3）
        num_twos = sum(1 for card in player.hand if card.rank == 15)
        
        # 老 2 每張加倍一次（2^num_twos）
        multiplier *= (2 ** num_twos)
        
        penalty = base * multiplier
        return penalty

    def _prepare_settlement(self):
        if not self.game or not self.game.winner:
            return

        winner_name = self.game.winner.name
        settlement = []
        winner_gain = 0

        for p in self.game.players:
            left = len(p.hand)
            penalty = 0 if p.name == winner_name else self._calc_penalty(p)
            settlement.append({"name": p.name, "left": left, "penalty": penalty})

            if p.name != winner_name:
                winner_gain += penalty
                self.session_points[p.name] -= penalty

        self.session_points[winner_name] += winner_gain
        self.last_settlement = settlement
        self.result_prepared = True

    def update_layout(self, width, height):
        self.width = max(self.min_width, width)
        self.height = max(self.min_height, height)
        self.renderer.update_size(self.width, self.height)
        self._reset_effects_for_scene()

        self.action_bar = pygame.Rect(20, self.height - 154, self.width - 40, 130)

        btn_w, btn_h = 210, 50
        btn_x = self.action_bar.right - btn_w - 22
        btn_y = self.action_bar.y + 16
        self.input_handler.buttons = {
            "出牌 (Enter)": pygame.Rect(btn_x, btn_y, btn_w, btn_h),
            "過牌 (P)": pygame.Rect(btn_x, btn_y + btn_h + 14, btn_w, btn_h),
        }

        if self.game:
            human_hand_count = len(self.game.players[0].hand)
        else:
            human_hand_count = 13

        hand_left = self.action_bar.x + 22
        hand_right = self.input_handler.buttons["出牌 (Enter)"].x - 24
        hand_area_width = max(320, hand_right - hand_left)
        if human_hand_count > 1:
            min_spacing = 34
            max_spacing = 62
            fit_spacing = (hand_area_width - self.renderer.CARD_WIDTH) // (human_hand_count - 1)
            self.human_hand_spacing = max(min_spacing, min(max_spacing, fit_spacing))
        else:
            self.human_hand_spacing = 0

        total_hand_width = max(0, (human_hand_count - 1) * self.human_hand_spacing + self.renderer.CARD_WIDTH)
        self.human_hand_x = hand_left + max(0, (hand_area_width - total_hand_width) // 2)
        self.human_hand_y = self.height - 145
        self.input_handler.set_layout(self.human_hand_x, self.human_hand_y, self.human_hand_spacing)

        cx = self.width // 2
        self.menu_buttons = {
            "開始遊玩": pygame.Rect(cx - 120, self.height // 2 + 180, 240, 58),
            "離開遊戲": pygame.Rect(cx - 120, self.height // 2 + 255, 240, 58),
        }

        self.result_buttons = {
            "action1": pygame.Rect(cx - 260, self.height - 126, 220, 56),
            "回到大廳": pygame.Rect(cx - 20, self.height - 126, 220, 56),
            "離開遊戲": pygame.Rect(cx + 220, self.height - 126, 220, 56),
        }

        self.help_button = pygame.Rect(self.width - 58, 16, 42, 42)

        # 大廳佈局：左邊模式選擇，右邊局數選擇（充分利用寬度）
        left_x = 60
        right_x = self.width - 220
        mode_y = self.height // 2 - 80
        
        # 模式選擇（左邊頂部）
        self.mode_buttons = {
            "casual": pygame.Rect(left_x, mode_y, 160, 48),
            "ranked": pygame.Rect(left_x, mode_y + 62, 160, 48),
        }

        # 難度選擇（左邊模式下方，只在休閒模式顯示）
        difficulty_y = mode_y + 140
        self.difficulty_buttons = {
            "easy": pygame.Rect(left_x, difficulty_y, 48, 48),
            "medium": pygame.Rect(left_x + 56, difficulty_y, 48, 48),
            "hard": pygame.Rect(left_x + 112, difficulty_y, 48, 48),
        }

        # 局數選擇（右邊）
        round_y = mode_y
        self.round_buttons = {
            3: pygame.Rect(right_x, round_y, 150, 46),
            5: pygame.Rect(right_x, round_y + 56, 150, 46),
            10: pygame.Rect(right_x, round_y + 112, 150, 46),
        }

        # 自訂局數（左下方）
        custom_y = difficulty_y + 70
        self.round_adjust_buttons = {
            "-": pygame.Rect(left_x, custom_y, 48, 48),
            "+": pygame.Rect(left_x + 128, custom_y, 48, 48),
            "display": pygame.Rect(left_x + 56, custom_y, 72, 48),
        }

        # 中央：外觀設定（背景、桌布、牌背）
        style_x = self.width // 2 - 180
        style_y = self.height // 2 - 60
        chip_w = 116
        chip_h = 36
        chip_gap = 10

        self.background_buttons = {
            "diagonal": pygame.Rect(style_x, style_y, chip_w, chip_h),
            "grid": pygame.Rect(style_x + chip_w + chip_gap, style_y, chip_w, chip_h),
            "clean": pygame.Rect(style_x + (chip_w + chip_gap) * 2, style_y, chip_w, chip_h),
        }
        self.table_style_buttons = {
            "blue": pygame.Rect(style_x, style_y + 54, chip_w, chip_h),
            "green": pygame.Rect(style_x + chip_w + chip_gap, style_y + 54, chip_w, chip_h),
            "red": pygame.Rect(style_x + (chip_w + chip_gap) * 2, style_y + 54, chip_w, chip_h),
        }
        self.card_back_buttons = {
            "ring": pygame.Rect(style_x, style_y + 108, chip_w, chip_h),
            "diamond": pygame.Rect(style_x + chip_w + chip_gap, style_y + 108, chip_w, chip_h),
            "minimal": pygame.Rect(style_x + (chip_w + chip_gap) * 2, style_y + 108, chip_w, chip_h),
        }

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            now = pygame.time.get_ticks()
            self._update_effects()

            if self.scene == "playing" and self.game and not self.game.winner:
                if self.observed_turn_id != self.game.turn_id:
                    self.observed_turn_id = self.game.turn_id
                    if not self.game.players[self.game.current_player].is_ai:
                        self._begin_human_turn()

                if (not self.game.is_paused) and self.game.players[self.game.current_player].is_ai:
                    if now >= self.next_auto_action_ms:
                        if self.game.ai_turn():
                            self.next_auto_action_ms = now + self.ai_delay_ms
                elif (not self.game.is_paused) and (not self.show_help):
                    if self.full_auto_mode:
                        if self.turn_deadline_ms and now >= self.turn_deadline_ms and now >= self.next_auto_action_ms and self._run_full_auto_turn():
                            self.next_auto_action_ms = now + max(300, self.ai_delay_ms - 220)
                    elif self.auto_play_human:
                        if now >= self.next_auto_action_ms and self._run_human_autoplay_turn():
                            self.next_auto_action_ms = now + max(360, self.ai_delay_ms - 180)
                    elif self.turn_deadline_ms and now >= self.turn_deadline_ms:
                        if now >= self.next_auto_action_ms and self._run_timeout_autoplay_turn():
                            self.next_auto_action_ms = now + max(300, self.ai_delay_ms - 220)

                self._process_history_effects()

            running = self.handle_events()

            if self.scene == "playing" and self.game and self.game.winner and not self.result_prepared:
                self._emit_victory_effect()
                self._prepare_settlement()
                self.scene = "result"

            self.render()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def _handle_lobby_click(self, pos):
        for rounds, rect in self.round_buttons.items():
            if rect.collidepoint(pos):
                self.selected_rounds = rounds
                return True

        if self.round_adjust_buttons["-"].collidepoint(pos):
            self.selected_rounds = max(1, self.selected_rounds - 1)
            return True

        if self.round_adjust_buttons["+"].collidepoint(pos):
            self.selected_rounds = min(30, self.selected_rounds + 1)
            return True

        for style_name, rect in self.background_buttons.items():
            if rect.collidepoint(pos):
                self.selected_background = style_name
                self.renderer.set_background_style(style_name)
                return True

        for style_name, rect in self.table_style_buttons.items():
            if rect.collidepoint(pos):
                self.selected_table_style = style_name
                self.renderer.set_table_style(style_name)
                return True

        for style_name, rect in self.card_back_buttons.items():
            if rect.collidepoint(pos):
                self.selected_card_back = style_name
                self.renderer.set_card_back_style(style_name)
                return True

        # 難度選擇（只在休閒模式有效）
        if self.selected_mode == "casual":
            for difficulty, rect in self.difficulty_buttons.items():
                if rect.collidepoint(pos):
                    self.selected_difficulty = difficulty
                    return True

        for mode, rect in self.mode_buttons.items():
            if rect.collidepoint(pos):
                self.selected_mode = mode
                return True

        if self.menu_buttons["開始遊玩"].collidepoint(pos):
            self.start_new_game(new_session=True)
        elif self.menu_buttons["離開遊戲"].collidepoint(pos):
            return False
        return True

    def _result_action1_label(self):
        if self.current_round < self.total_rounds:
            return "下一局"
        return "再玩一輪"

    def _handle_result_click(self, pos):
        if self.result_buttons["action1"].collidepoint(pos):
            if self.current_round < self.total_rounds:
                self.current_round += 1
                self.start_new_game(new_session=False)
            else:
                self.start_new_game(new_session=True)
        elif self.result_buttons["回到大廳"].collidepoint(pos):
            self.scene = "lobby"
            self.game = None
            self.input_handler.selected_indices.clear()
        elif self.result_buttons["離開遊戲"].collidepoint(pos):
            return False
        return True

    def _handle_help_click(self, pos):
        if self.help_close_button.collidepoint(pos):
            self.show_help = False
            return True
        for tab, rect in self.help_tab_buttons.items():
            if rect.collidepoint(pos):
                self.help_tab = tab
                return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if (
                self.scene == "playing"
                and self.game
                and not self.game.players[self.game.current_player].is_ai
                and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN)
            ):
                self._mark_human_activity()

            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                    (max(self.min_width, event.w), max(self.min_height, event.h)),
                    pygame.RESIZABLE,
                )
                self.update_layout(event.w, event.h)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.scene == "lobby":
                    return self._handle_lobby_click(event.pos)
                if self.scene == "result":
                    return self._handle_result_click(event.pos)
                if self.scene == "playing" and self.game:
                    if self.help_button.collidepoint(event.pos):
                        self.show_help = not self.show_help
                        return True
                    if self.show_help:
                        if self._handle_help_click(event.pos):
                            return True
                        self.show_help = False
                        return True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.scene == "playing":
                    if self.show_help:
                        self.show_help = False
                        return True
                    self.scene = "lobby"
                    self.game = None
                    self.input_handler.selected_indices.clear()
                    return True
                if self.scene == "result":
                    self.scene = "lobby"
                    self.game = None
                    self.input_handler.selected_indices.clear()
                    return True

            if event.type == pygame.KEYDOWN and self.scene == "playing" and self.game:
                if event.key == pygame.K_SPACE and self.game.players[self.game.current_player].is_ai:
                    self.game.toggle_pause()
                    return True
                if event.key == pygame.K_t:
                    self.auto_play_human = not self.auto_play_human
                    if self.auto_play_human:
                        # 手動代打開啟時，清掉逾時連鎖狀態，避免與整手代打混淆。
                        self.full_auto_mode = False
                        self.pending_full_auto = False
                        self.idle_human_turns = 0
                    self.game._log("人類自動代打：開啟" if self.auto_play_human else "人類自動代打：關閉")
                    return True
                if event.key in (pygame.K_h, pygame.K_SLASH):
                    self.show_help = not self.show_help
                    return True
                if self.show_help:
                    if event.key == pygame.K_1:
                        self.help_tab = "操作"
                        return True
                    if event.key == pygame.K_2:
                        self.help_tab = "牌型"
                        return True
                    if event.key == pygame.K_3:
                        self.help_tab = "規則"
                        return True

            if self.scene == "playing" and self.game and (not self.game.winner) and (not self.game.is_paused) and (not self.show_help):
                handled = self.input_handler.handle_event(event, self.game)
                if handled:
                    self._mark_human_activity()

        return True

    def _draw_chip(self, rect, text, selected):
        bg = (33, 116, 161) if selected else (23, 48, 72)
        border = (96, 194, 247) if selected else (84, 116, 140)
        pygame.draw.rect(self.screen, bg, rect, border_radius=10)
        pygame.draw.rect(self.screen, border, rect, 2, border_radius=10)
        txt = self.renderer.small_font.render(text, True, self.renderer.COLORS['text_primary'])
        self.screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))

    def _draw_lobby(self):
        self.renderer.draw_table_background(self.screen)

        moon = pygame.Surface((240, 240), pygame.SRCALPHA)
        pygame.draw.circle(moon, (220, 238, 255, 35), (120, 120), 120)
        self.screen.blit(moon, (72, 58))
        moon2 = pygame.Surface((180, 180), pygame.SRCALPHA)
        pygame.draw.circle(moon2, (255, 206, 170, 24), (90, 90), 90)
        self.screen.blit(moon2, (self.width - 290, 110))

        title = self.renderer.title_font.render("大老二 Big Two", True, self.renderer.COLORS['text_primary'])
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 80))
        subtitle = self.renderer.small_font.render("Classic Big Two Table", True, self.renderer.COLORS['text_muted'])
        self.screen.blit(subtitle, (self.width // 2 - subtitle.get_width() // 2, 128))

        # 左邊：模式選擇
        left_x = 60
        mode_y = self.height // 2 - 80
        
        mode_title = self.renderer.font.render("模式選擇", True, self.renderer.COLORS['text_primary'])
        self.screen.blit(mode_title, (left_x, mode_y - 40))
        self._draw_chip(self.mode_buttons["casual"], "休閒模式", self.selected_mode == "casual")
        self._draw_chip(self.mode_buttons["ranked"], "挑戰模式", self.selected_mode == "ranked")
        
        # 難度選擇（只在休閒模式顯示）
        if self.selected_mode == "casual":
            difficulty_y = mode_y + 140
            difficulty_title = self.renderer.small_font.render("AI 難度", True, self.renderer.COLORS['text_muted'])
            self.screen.blit(difficulty_title, (left_x, difficulty_y - 32))
            self._draw_chip(self.difficulty_buttons["easy"], "低", self.selected_difficulty == "easy")
            self._draw_chip(self.difficulty_buttons["medium"], "中", self.selected_difficulty == "medium")
            self._draw_chip(self.difficulty_buttons["hard"], "高", self.selected_difficulty == "hard")
            custom_y = difficulty_y + 70
        else:
            custom_y = mode_y + 140
        
        # 自訂局數
        custom_title = self.renderer.small_font.render("自訂局數", True, self.renderer.COLORS['text_muted'])
        self.screen.blit(custom_title, (left_x, custom_y - 32))
        self._draw_chip(self.round_adjust_buttons["-"], "-", False)
        self._draw_chip(self.round_adjust_buttons["display"], f"{self.selected_rounds} 局", False)
        self._draw_chip(self.round_adjust_buttons["+"], "+", False)

        # 右邊：局數快選
        right_x = self.width - 220
        rounds_title = self.renderer.font.render("局數選擇", True, self.renderer.COLORS['text_primary'])
        self.screen.blit(rounds_title, (right_x, mode_y - 40))
        
        for rounds, rect in self.round_buttons.items():
            self._draw_chip(rect, f"{rounds} 局", self.selected_rounds == rounds)

        # 中央：外觀設定
        style_x = self.width // 2 - 180
        style_title = self.renderer.font.render("外觀設定", True, self.renderer.COLORS['text_primary'])
        self.screen.blit(style_title, (style_x, mode_y - 40))

        bg_label = self.renderer.small_font.render("背景", True, self.renderer.COLORS['text_muted'])
        self.screen.blit(bg_label, (style_x, mode_y - 10))
        self._draw_chip(self.background_buttons["diagonal"], "斜紋", self.selected_background == "diagonal")
        self._draw_chip(self.background_buttons["grid"], "網格", self.selected_background == "grid")
        self._draw_chip(self.background_buttons["clean"], "純淨", self.selected_background == "clean")

        table_label = self.renderer.small_font.render("桌布", True, self.renderer.COLORS['text_muted'])
        self.screen.blit(table_label, (style_x, mode_y + 44))
        self._draw_chip(self.table_style_buttons["blue"], "深藍", self.selected_table_style == "blue")
        self._draw_chip(self.table_style_buttons["green"], "綠絨", self.selected_table_style == "green")
        self._draw_chip(self.table_style_buttons["red"], "酒紅", self.selected_table_style == "red")

        back_label = self.renderer.small_font.render("牌背", True, self.renderer.COLORS['text_muted'])
        self.screen.blit(back_label, (style_x, mode_y + 98))
        self._draw_chip(self.card_back_buttons["ring"], "同心圓", self.selected_card_back == "ring")
        self._draw_chip(self.card_back_buttons["diamond"], "菱紋", self.selected_card_back == "diamond")
        self._draw_chip(self.card_back_buttons["minimal"], "極簡", self.selected_card_back == "minimal")

        mouse_pos = pygame.mouse.get_pos()
        self.renderer.draw_buttons(self.screen, self.menu_buttons, mouse_pos)

        # lobby ambient effects
        self.bg_effect.draw(self.screen)
        for glow in self.glow_effects[-3:]:
            glow.draw(self.screen)

    def _draw_playing(self):
        self.renderer.draw_table_background(self.screen)
        self.bg_effect.draw(self.screen)
        self.renderer.draw_action_bar(self.screen, self.action_bar)
        self._update_hand_layout_for_count(len(self.game.players[0].hand))

        left_x = 26
        right_x = self.width - 230
        top_x = (self.width // 2) - 170
        top_y = 162
        side_y = max(195, (self.height // 2) - 92)

        self.renderer.draw_turn_indicator(
            self.screen,
            self.game.players[self.game.current_player].name,
            not self.game.players[self.game.current_player].is_ai,
        )

        self.renderer.draw_player(self.screen, self.game.players[1], left_x, side_y,
                                  self.game.current_player == 1, len(self.game.players[1].hand), is_side=True)
        self.renderer.draw_player(self.screen, self.game.players[2], top_x, top_y,
                                  self.game.current_player == 2, len(self.game.players[2].hand), is_top=True)
        self.renderer.draw_player(self.screen, self.game.players[3], right_x, side_y,
                                  self.game.current_player == 3, len(self.game.players[3].hand), is_side=True)

        self.renderer.draw_player(self.screen, self.game.players[0], self.human_hand_x, self.human_hand_y - 40,
                                  self.game.current_player == 0, len(self.game.players[0].hand))
        self.renderer.draw_hand(
            self.screen,
            self.game.players[0].hand,
            self.human_hand_x,
            self.human_hand_y,
            self.input_handler.selected_indices,
            self.human_hand_spacing,
            self.input_handler.cursor_index,
        )

        selected_cards = self._selected_cards()
        if selected_cards:
            type_name = self._format_card_type(selected_cards)
            can_play = self._can_play_selected()
            msg = f"已選 {len(selected_cards)} 張 - {type_name}"
            self.renderer.draw_selected_info(
                self.screen,
                msg,
                can_play,
                self.action_bar.x + 18,
                self.action_bar.y + 18,
            )

        # foreground visual effects disabled for smoother gameplay

        if self.game.last_play:
            play_type_text = self._format_card_type(self.game.last_play)
            self.renderer.draw_last_play(
                self.screen,
                self.game.last_play,
                self.game.last_player,
                (self.width // 2) - 120,
                (self.height // 2) - 35,
                play_type_text,
            )

        mouse_pos = pygame.mouse.get_pos()
        button_enabled = {
            "出牌 (Enter)": (not self.game.players[self.game.current_player].is_ai) and self._can_play_selected(),
            "過牌 (P)": (not self.game.players[self.game.current_player].is_ai)
            and self.game.can_pass(self.game.players[self.game.current_player]),
        }
        self.renderer.draw_buttons(self.screen, self.input_handler.buttons, mouse_pos, button_enabled)
        self.renderer.draw_icon_button(self.screen, self.help_button, "?", mouse_pos, self.show_help)
        auto_text = self.renderer.small_font.render(
            f"手動代打(T): {'ON' if self.auto_play_human else 'OFF'}",
            True,
            self.renderer.COLORS['text_muted'],
        )
        self.screen.blit(auto_text, (self.help_button.x - auto_text.get_width() - 10, self.help_button.y + 12))

        # 只在挑戰賽模式顯示計時器
        if self.selected_mode == "ranked":
            timer_text = self.renderer.small_font.render(
                f"逾時計時: {max(0, (self.turn_deadline_ms - pygame.time.get_ticks()) // 1000)}s",
                True,
                self.renderer.COLORS['text_muted'],
            )
            self.screen.blit(timer_text, (self.help_button.x - timer_text.get_width() - 10, self.help_button.y + 34))

        if self.game.is_paused:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((5, 12, 20, 140))
            self.screen.blit(overlay, (0, 0))
            msg = self.renderer.title_font.render("已暫停 (Space 繼續)", True, self.renderer.COLORS['selected'])
            self.screen.blit(msg, (self.width // 2 - msg.get_width() // 2, self.height // 2 - msg.get_height() // 2))

        if self.show_help:
            self._draw_help_overlay()

    def _draw_help_overlay(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((4, 10, 18, 188))
        self.screen.blit(overlay, (0, 0))

        panel_w = min(self.width - 80, 980)
        panel_h = min(self.height - 70, 640)
        panel = pygame.Rect(self.width // 2 - panel_w // 2, self.height // 2 - panel_h // 2, panel_w, panel_h)
        layer = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
        layer.fill((12, 24, 39, 235))
        self.screen.blit(layer, panel.topleft)
        pygame.draw.rect(self.screen, self.renderer.COLORS['selected'], panel, 2, border_radius=14)

        self.help_close_button = pygame.Rect(panel.right - 44, panel.y + 10, 32, 32)
        pygame.draw.rect(self.screen, (44, 70, 97), self.help_close_button, border_radius=6)
        pygame.draw.rect(self.screen, (158, 189, 214), self.help_close_button, 1, border_radius=6)
        close_txt = self.renderer.font.render("X", True, self.renderer.COLORS['text_primary'])
        self.screen.blit(close_txt, (self.help_close_button.centerx - close_txt.get_width() // 2, self.help_close_button.centery - close_txt.get_height() // 2))

        title = self.renderer.title_font.render("規則與操作說明", True, self.renderer.COLORS['text_primary'])
        self.screen.blit(title, (panel.x + 24, panel.y + 18))

        tabs = ["操作", "牌型", "規則"]
        self.help_tab_buttons = {}
        tab_y = panel.y + 72
        tab_w = 120
        for i, tab in enumerate(tabs):
            rect = pygame.Rect(panel.x + 24 + i * (tab_w + 12), tab_y, tab_w, 36)
            self.help_tab_buttons[tab] = rect
            active = (tab == self.help_tab)
            bg = (50, 121, 162) if active else (29, 58, 86)
            bd = (133, 203, 246) if active else (97, 132, 160)
            pygame.draw.rect(self.screen, bg, rect, border_radius=8)
            pygame.draw.rect(self.screen, bd, rect, 2, border_radius=8)
            txt = self.renderer.small_font.render(tab, True, self.renderer.COLORS['text_primary'])
            self.screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))

        body_rect = pygame.Rect(panel.x + 24, panel.y + 122, panel.width - 48, panel.height - 150)
        body_layer = pygame.Surface((body_rect.width, body_rect.height), pygame.SRCALPHA)
        body_layer.fill((8, 20, 33, 170))
        self.screen.blit(body_layer, body_rect.topleft)
        pygame.draw.rect(self.screen, (86, 119, 147), body_rect, 1, border_radius=10)
        content_clip = body_rect.inflate(-12, -12)

        def draw_section_header(y, text):
            bar = pygame.Rect(body_rect.x + 8, y, body_rect.width - 16, 36)
            pygame.draw.rect(self.screen, (239, 128, 25), bar, border_radius=7)
            t = self.renderer.font.render(text, True, (250, 250, 250))
            self.screen.blit(t, (bar.x + 14, bar.centery - t.get_height() // 2))
            return bar.bottom + 10

        def draw_wrapped_text(y, text, color=None, max_width=None, line_h=22):
            if color is None:
                color = self.renderer.COLORS['text_muted']
            if max_width is None:
                max_width = body_rect.width - 28

            line = ""
            for ch in text:
                test = line + ch
                if self.renderer.small_font.size(test)[0] <= max_width:
                    line = test
                else:
                    txt = self.renderer.small_font.render(line, True, color)
                    self.screen.blit(txt, (body_rect.x + 16, y))
                    y += line_h
                    line = ch
            if line:
                txt = self.renderer.small_font.render(line, True, color)
                self.screen.blit(txt, (body_rect.x + 16, y))
                y += line_h
            return y

        self.screen.set_clip(content_clip)

        if self.help_tab == "操作":
            y = draw_section_header(body_rect.y + 10, "基本玩法")
            lines = [
                "1. 手持梅花3者擁有首出權，但不一定要先出梅花3。",
                "2. 一般需同張數比牌；但鐵支/同花順/一條龍可跨張數壓制。",
                "3. 出牌順序為逆時鐘；若不出或無法壓過可選擇本輪 PASS。",
                "4. 本輪 PASS 後直到清桌前不可再出牌。",
                "5. 玩家逾時未出牌：系統自動出最小可出單張，否則 PASS。",
                "6. 連續2輪未操作，第3輪啟動整手自動代打，玩家可中途取消。",
                "7. 整手代打規則：單張局自動出最小單張，非單張局自動 PASS。",
                "8. 滑鼠選牌、Enter 出牌、P 過牌、? 開關說明、T 手動代打。",
            ]
            for line in lines:
                txt = self.renderer.small_font.render(line, True, self.renderer.COLORS['text_muted'])
                self.screen.blit(txt, (body_rect.x + 16, y))
                y += 24

            y += 6
            y = draw_section_header(y, "對局記錄")
            logs = self.game.get_recent_history(8)
            if not logs:
                hint = self.renderer.small_font.render("目前尚無記錄。", True, self.renderer.COLORS['text_muted'])
                self.screen.blit(hint, (body_rect.x + 16, y))
            else:
                for line in logs:
                    txt = self.renderer.small_font.render(line, True, self.renderer.COLORS['text_muted'])
                    self.screen.blit(txt, (body_rect.x + 16, y))
                    y += 24

        elif self.help_tab == "牌型":
            y = draw_section_header(body_rect.y + 10, "手牌大小比較")
            line1 = "先比點數：2 > A > K > Q > J > 10 > 9 > 8 > 7 > 6 > 5 > 4 > 3"
            txt1 = self.renderer.small_font.render(line1, True, self.renderer.COLORS['text_primary'])
            self.screen.blit(txt1, (body_rect.x + 16, y))

            suit_bar = pygame.Rect(body_rect.x + 14, y + 30, body_rect.width - 28, 40)
            pygame.draw.rect(self.screen, (232, 235, 239), suit_bar, border_radius=10)
            pygame.draw.rect(self.screen, (198, 204, 212), suit_bar, 1, border_radius=10)

            suit_items = [
                ("♠", "黑桃", (33, 26, 28)),
                ("♥", "紅心", (219, 77, 68)),
                ("♦", "方塊", (219, 77, 68)),
                ("♣", "梅花", (33, 26, 28)),
            ]
            sx = suit_bar.x + 12
            sy = suit_bar.y + 5
            for idx, (glyph, label, color) in enumerate(suit_items):
                g = self.renderer.rank_small_font.render(glyph, True, color)
                t = self.renderer.font.render(label, True, (18, 22, 30))
                self.screen.blit(g, (sx, sy + 1))
                self.screen.blit(t, (sx + 30, sy + 6))
                sx += 110
                if idx < len(suit_items) - 1:
                    gt = self.renderer.font.render(">", True, (22, 28, 36))
                    self.screen.blit(gt, (sx, sy + 8))
                    sx += 26

            y = draw_section_header(y + 66, "牌組說明")
            headers = ["牌型", "牌型說明", "示例"]
            col1 = body_rect.x + 16
            col2 = body_rect.x + 122
            col3 = body_rect.x + 452
            h1 = self.renderer.small_font.render(headers[0], True, self.renderer.COLORS['text_primary'])
            h2 = self.renderer.small_font.render(headers[1], True, self.renderer.COLORS['text_primary'])
            h3 = self.renderer.small_font.render(headers[2], True, self.renderer.COLORS['text_primary'])
            self.screen.blit(h1, (col1, y))
            self.screen.blit(h2, (col2, y))
            self.screen.blit(h3, (col3, y))
            y += 24

            rows = [
                ("單張", "任意一張牌", [("A", 3)]),
                ("一對", "兩張同數字的牌", [("9", 0), ("9", 2)]),
                ("順子", "5 張連續數字（含 A2345、23456 特例）", [("7", 0), ("8", 1), ("9", 2), ("10", 3), ("J", 0)]),
                ("葫蘆", "3 張相同 + 2 張相同", [("Q", 0), ("Q", 1), ("Q", 3), ("4", 0), ("4", 2)]),
                ("鐵支", "4 張相同 + 任一單張（可壓葫蘆、順子、一對、單張）", [("5", 0), ("5", 1), ("5", 2), ("5", 3), ("K", 0)]),
                ("同花順", "5 張同花色且連續（可壓鐵支以下牌型）", [("6", 3), ("7", 3), ("8", 3), ("9", 3), ("10", 3)]),
                ("一條龍", "13 種點數各一張（可壓所有牌型）", []),
            ]
            row_h = 34
            for name, desc, sample in rows:
                row_bg = pygame.Rect(body_rect.x + 10, y - 2, body_rect.width - 20, row_h)
                pygame.draw.rect(self.screen, (20, 37, 56, 120), row_bg, border_radius=4)
                n = self.renderer.small_font.render(name, True, self.renderer.COLORS['text_muted'])
                d = self.renderer.small_font.render(desc, True, self.renderer.COLORS['text_muted'])
                self.screen.blit(n, (col1, y + 2))
                self.screen.blit(d, (col2, y + 2))
                if sample:
                    sample_x = col3
                    for rank_text, suit in sample:
                        self.renderer.draw_mini_card(self.screen, rank_text, suit, sample_x, y - 1, width=20, height=30)
                        sample_x += 14
                else:
                    dragon_ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
                    dragon_suits = [3, 2, 1, 0, 3, 1, 0, 2, 3, 2, 1, 0, 3]
                    sample_x = col3
                    for i, rank_text in enumerate(dragon_ranks):
                        self.renderer.draw_mini_card(
                            self.screen,
                            rank_text,
                            dragon_suits[i],
                            sample_x,
                            y,
                            width=16,
                            height=24,
                        )
                        sample_x += 10
                y += row_h + 2

        else:
            y = draw_section_header(body_rect.y + 10, "規則設定")
            paragraphs = [
                "手持「梅花3」的玩家先手，首輪第一手必須包含梅花3（可為單張、順子、葫蘆、鐵支、同花順等合法牌型）。其他三家必須依照首家牌型出牌，且大於上家。",
                "四位玩家逆時鐘順序出牌；一般需以同張數且更大的牌壓上家。特例：鐵支、同花順、一條龍可跨張數壓牌。",
                "若選擇 PASS 不出，該輪牌型結束前都不能再出牌（正統賽制）。當所有玩家都 PASS 後，視為該輪結束；最後出牌者可重新選擇出牌方式，不受上一輪牌型限制。上一輪 PASS 的玩家也可在新一輪重新回應。",
                "防串謀規則（頂大）：當下家只剩一張手牌時，具有出牌權的上家需優先以最大牌／牌型壓制，阻礙對手勝出。若上家因本輪 PASS 無法出牌，則依序往上上家遞補。",
                "代打規則：玩家逾時時，系統只會自動嘗試最小可出單張；若局面為非單張或無單張可壓，則自動 PASS。連續2輪逾時後，第3輪啟動整手代打，玩家可隨時操作取消。",
                "牌型強度：同花順 > 鐵支 > 葫蘆 > 順子；其中鐵支可壓葫蘆/順子/一對/單張，同花順可壓鐵支以下，一條龍可壓所有牌型。",
                "先比點數：2 > A > K > Q > J > 10 > 9 > 8 > 7 > 6 > 5 > 4 > 3；後比花色：黑桃 > 紅心 > 方塊 > 梅花。",
            ]
            for idx, p in enumerate(paragraphs, start=1):
                y = draw_wrapped_text(y, f"{idx}. {p}", color=self.renderer.COLORS['text_muted'])
                y += 6

        self.screen.set_clip(None)

    def _draw_result(self):
        self.renderer.draw_table_background(self.screen)

        panel = pygame.Rect(self.width // 2 - 360, 92, 720, self.height - 220)
        layer = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
        layer.fill((10, 24, 36, 210))
        self.screen.blit(layer, panel.topleft)
        pygame.draw.rect(self.screen, self.renderer.COLORS['panel_border'], panel, 2, border_radius=16)

        winner = self.game.winner.name if self.game and self.game.winner else "-"
        title = self.renderer.title_font.render("本局結算", True, self.renderer.COLORS['text_primary'])
        winner_text = self.renderer.font.render(
            f"第 {self.current_round}/{self.total_rounds} 局  勝利者: {winner}",
            True,
            self.renderer.COLORS['selected'],
        )
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 114))
        self.screen.blit(winner_text, (self.width // 2 - winner_text.get_width() // 2, 168))

        y = 224
        for row in self.last_settlement:
            name = row["name"]
            left = row["left"]
            penalty = row["penalty"]
            total = self.session_points.get(name, 0)
            line = self.renderer.font.render(
                f"{name:<8} 剩牌 {left:>2} 張   本局分數 {-penalty:+d}   累計 {total:+d}",
                True,
                self.renderer.COLORS['text_primary'],
            )
            self.screen.blit(line, (panel.x + 50, y))
            y += 46

        mouse_pos = pygame.mouse.get_pos()
        bottom_y = panel.bottom - 86
        btn_w = self.result_buttons["action1"].width
        gap = 20
        total_w = btn_w * 3 + gap * 2
        start_x = panel.centerx - total_w // 2

        self.result_buttons["action1"].x = start_x
        self.result_buttons["回到大廳"].x = start_x + btn_w + gap
        self.result_buttons["離開遊戲"].x = start_x + (btn_w + gap) * 2

        self.result_buttons["action1"].y = bottom_y
        self.result_buttons["回到大廳"].y = bottom_y
        self.result_buttons["離開遊戲"].y = bottom_y
        action_buttons = {
            self._result_action1_label(): self.result_buttons["action1"],
            "回到大廳": self.result_buttons["回到大廳"],
            "離開遊戲": self.result_buttons["離開遊戲"],
        }
        self.renderer.draw_buttons(self.screen, action_buttons, mouse_pos)

    def render(self):
        if self.scene == "lobby":
            self._draw_lobby()
        elif self.scene == "playing" and self.game:
            self._draw_playing()
        elif self.scene == "result" and self.game:
            self._draw_result()


if __name__ == '__main__':
    app = BigTwoApp()
    app.run()
