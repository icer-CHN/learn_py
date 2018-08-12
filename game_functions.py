import sys

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_event(event, settings, screen, ship, bullets):
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)


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


def update_screen(settings, screen, ship, aliens, bullets):
    '''更新屏幕上的图像，并切换到新屏幕'''
    # 每次循环都重绘屏幕背景色
    screen.fill(settings.bg_color)

    for bullet in bullets:
        bullet.draw_bullet()

    # 绘制飞船
    ship.blitme()
    # 绘制外星人
    aliens.draw(screen)

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets):
    bullets.update()

    for bullet in bullets:
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)


def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullet_num_limit:
        bullet = Bullet(settings, screen, ship)
        bullets.add(bullet)


def creat_aliens(settings, screen, aliens):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (1.5 * alien_width))

    for alien_number in range(number_aliens_x + 1):
        alien = Alien(settings, screen)
        alien.x = alien_width + 1.5 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)
