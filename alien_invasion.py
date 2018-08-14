import sys

import pygame
from pygame.sprite import Group

import game_functions as gf
from alien import Alien
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


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

    stats = GameStats(settings)

    play_button = Button(settings, screen, "Play")

    sb = Scoreboard(settings, screen, stats)

    # 开始游戏主循环
    while True:
        # 监听鼠标键盘事件
        gf.check_event(settings, screen, stats, sb, ship,
                       aliens, bullets, play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, stats,
                              sb, ship, aliens, bullets)
            gf.update_aliens(settings, screen, stats,
                             sb, ship, aliens, bullets)
        gf.update_screen(settings, screen, stats, sb, ship,
                         aliens, bullets, play_button)


run_game()
