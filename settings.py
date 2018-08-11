import sys

import pygame


class Settings():
    '''储存游戏的所有设置的类'''

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (214, 222, 224)

        self.ship_speed_factor = 1.5

        self.bullet_speed_factor = 1
        self.bullet_width = 4
        self.bullet_height = 10
        self.bullet_color = 60, 60, 60
