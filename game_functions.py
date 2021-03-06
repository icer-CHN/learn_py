import json
import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from scoreboard import Scoreboard


def close_game(stats):
    high_score = stats.high_score
    filename = 'high_score.json'
    with open(filename, 'w') as f:
        json.dump(high_score, f)
    sys.exit()


def check_keydown_event(event, settings, stats, screen, ship, bullets):
    if event.key == pygame.K_ESCAPE:
        close_game(stats)
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


def check_event(settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''监听鼠标键盘事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game(stats)

        elif event.type == pygame.KEYDOWN:
            if event.key != pygame.K_p:
                check_keydown_event(event, settings, stats,
                                    screen, ship, bullets)
            else:
                check_play_button(settings, screen, stats, sb, ship,
                                  aliens, bullets, play_button, 0, 0, True)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, ship,
                              aliens, bullets, play_button, mouse_x, mouse_y, False)


def check_play_button(settings, screen, stats, sb, ship, aliens, bullets, play_button, mouse_x, mouse_y, enter):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if enter:
        button_clicked = True

    if button_clicked and not stats.game_active:
        settings.initialize_dynamic_settings()

        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        creat_aliens(settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''更新屏幕上的图像，并切换到新屏幕'''
    # 每次循环都重绘屏幕背景色
    screen.fill(settings.bg_color)

    for bullet in bullets:
        bullet.draw_bullet()

    # 绘制飞船
    ship.blitme()
    # 绘制外星人
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()

    for bullet in bullets:
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for collisions_each_bullet in collisions.values():
            stats.score += settings.alien_points * len(collisions_each_bullet)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        creat_aliens(settings, screen, ship, aliens)


def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullet_num_limit:
        bullet = Bullet(settings, screen, ship)
        bullets.add(bullet)


def creat_aliens(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(settings, alien_width)
    number_rows = get_number_rows(
        settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows + 1):
        for alien_number in range(number_aliens_x + 1):
            create_alien(settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(settings, alien_width):
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (1.5 * alien_width))
    return number_aliens_x


def create_alien(settings, screen, aliens, alien_number, row_number):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 2 * alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(settings, ship_height, alien_height):
    available_space_y = settings.screen_height - \
        (5 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(settings, screen, stats, sb, ship, aliens, bullets):
    check_aliens_edges(settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, screen, stats, sb, ship, aliens, bullets)
    else:
        check_aliens_bottom(settings, screen, stats, sb, ship, aliens, bullets)


def check_aliens_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_aliens_direction(settings, aliens)
            break


def change_aliens_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.alien_drop_speed
    settings.alien_direction *= -1


def ship_hit(settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        creat_aliens(settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
