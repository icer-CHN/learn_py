import sys

import pygame

from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    '''初始化游戏主界面'''
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))

    # 设置游戏窗体标题
    pygame.display.set_caption('Alien Invasion')

    # 创建一艘飞船
    ship = Ship(settings, screen)
    bullets = Group()

    # 开始游戏主循环
    while True:
        # 监听鼠标键盘事件
        gf.check_event(settings, screen, ship, bullets)
        ship.update()
        bullets.update()

        for bullet in bullets:
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        # print(len(bullets))

        gf.update_screen(settings, screen, ship, bullets)


run_game()
