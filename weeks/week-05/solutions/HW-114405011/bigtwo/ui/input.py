# -*- coding: utf-8 -*-
import pygame

class InputHandler:
    def __init__(self, renderer):
        self.renderer = renderer
        self.selected_indices = []
        self.cursor_index = 0
        self.buttons = {}
        self.hand_x = 140
        self.hand_y = 450
        self.hand_spacing = 25
        self.selected_lift = 15

    def set_layout(self, hand_x, hand_y, hand_spacing=25, selected_lift=15):
        self.hand_x = hand_x
        self.hand_y = hand_y
        self.hand_spacing = hand_spacing
        self.selected_lift = selected_lift

    def handle_event(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.handle_click(event.pos, game)
        elif event.type == pygame.KEYDOWN:
            return self.handle_key(event.key, game)
        return False

    def handle_click(self, pos, game):
        current_p = game.players[game.current_player]
        if current_p.is_ai:
            return False

        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if name == "出牌 (Enter)":
                    return self.try_play(game)
                elif name == "過牌 (P)":
                    current = game.players[game.current_player]
                    if game.can_pass(current) and game.pass_turn(current):
                        game.next_turn()
                        self.selected_indices.clear()
                        return True
                return False

        if not current_p.is_ai:
            for i in range(len(current_p.hand)-1, -1, -1):
                x = self.hand_x + i * self.hand_spacing
                y = self.hand_y - (self.selected_lift if i in self.selected_indices else 0)
                card_rect = pygame.Rect(x, y, self.renderer.CARD_WIDTH, self.renderer.CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    self.cursor_index = i
                    if i in self.selected_indices:
                        self.selected_indices.remove(i)
                    else:
                        self.selected_indices.append(i)
                    return True
        return False

    def handle_key(self, key, game):
        current_p = game.players[game.current_player]
        if current_p.is_ai:
            return False

        hand_size = len(current_p.hand)

        if key == pygame.K_RETURN:
            return self.try_play(game)
        elif key == pygame.K_p:
            current = game.players[game.current_player]
            if game.can_pass(current) and game.pass_turn(current):
                game.next_turn()
                self.selected_indices.clear()
                return True
        elif key in (pygame.K_LEFT, pygame.K_a):
            if hand_size > 0:
                self.cursor_index = (self.cursor_index - 1) % hand_size
                return True
        elif key in (pygame.K_RIGHT, pygame.K_d):
            if hand_size > 0:
                self.cursor_index = (self.cursor_index + 1) % hand_size
                return True
        elif key in (pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE):
            if hand_size > 0:
                idx = max(0, min(self.cursor_index, hand_size - 1))
                if idx in self.selected_indices:
                    self.selected_indices.remove(idx)
                else:
                    self.selected_indices.append(idx)
                return True
        elif key == pygame.K_HOME:
            if hand_size > 0:
                self.cursor_index = 0
                return True
        elif key == pygame.K_END:
            if hand_size > 0:
                self.cursor_index = hand_size - 1
                return True
        return False

    def try_play(self, game):
        if not self.selected_indices: return False
        current_p = game.players[game.current_player]
        if current_p.is_ai: return False
        
        selected_cards = [current_p.hand[i] for i in sorted(self.selected_indices, reverse=True)]
        selected_cards.reverse()

        success = game.play(current_p, selected_cards)
        if success:
            game.next_turn()
            self.selected_indices.clear()
            return True
        return False
