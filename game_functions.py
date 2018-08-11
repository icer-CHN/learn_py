import sys

import pygame

from bullet import Bullet


def check_keydown_event(event, settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        bullet = Bullet(settings, screen, ship)
        bullets.add(bullet)


def check_keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_event(settings, screen, ship, bullets):
    '''监听鼠标键盘事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


def update_screen(settings, screen, ship, bullets):
    '''更新屏幕上的图像，并切换到新屏幕'''
    # 每次循环都重绘屏幕背景色
    screen.fill(settings.bg_color)

    for bullet in bullets:
        bullet.draw_bullet()

    # 绘制飞船
    ship.blitme()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
