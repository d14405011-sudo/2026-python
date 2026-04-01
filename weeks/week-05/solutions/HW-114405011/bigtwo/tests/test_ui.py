#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import patch

import pygame

from game.models import Card, Hand
from ui.render import Renderer

class TestUIParts(unittest.TestCase):
    def setUp(self):
        # Allow testing without video driver
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        self.renderer = Renderer(800, 600)
        self.screen = pygame.Surface((800, 600))

    def tearDown(self):
        pygame.quit()
    
    def test_card_render(self):
        card = Card(14, 0)
        self.renderer.draw_card(self.screen, card, 0, 0, False)
        # Verify it runs without error
        self.assertTrue(True)
        
    def test_hand_render(self):
        hand = Hand([Card(3, 0), Card(4, 0)])
        self.renderer.draw_hand(self.screen, hand, 0, 0, [])
        self.assertTrue(True)

    @patch('pygame.display.set_mode')
    def test_game_init(self, mock_set_mode):
        mock_set_mode.return_value = pygame.Surface((800, 600))
        from ui.app import BigTwoApp
        app = BigTwoApp()
        self.assertEqual(len(app.game.players), 4)

if __name__ == '__main__':
    unittest.main()
