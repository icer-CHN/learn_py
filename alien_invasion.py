import sys

import pygame

from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
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

    # 创建一群外星人
    aliens = Group()
    gf.creat_aliens(settings, screen, ship, aliens)

    # 开始游戏主循环
    while True:
        # 监听鼠标键盘事件
        gf.check_event(settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_aliens(settings, aliens)
        gf.update_screen(settings, screen, ship, aliens, bullets)

run_game()
