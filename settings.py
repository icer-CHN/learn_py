import sys

import pygame


class Settings():
    '''储存游戏的所有设置的类'''

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (214, 222, 224)

        self.ship_limit = 2

        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = 60, 60, 60
        self.bullet_num_limit = 5

        self.alien_drop_speed = 5
        self.alien_points = 50

        self.score_scale = 1.5

        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 5
        self.alien_speed_factor = 1

        # 外星人的移动方向 1:右 -1:左
        self.alien_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.score_scale * self.alien_points)
