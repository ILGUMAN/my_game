import pygame
import sys


def events(world, heart, mana, abilities, sound_effects=None):
    '''Обработка событий'''

    # Выход из игры, если нажал на крестик.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Действия при нажатии кнопок, если ты жив.
        elif event.type == pygame.KEYDOWN and not heart.is_dead:

            # Проверка наличия живого врага в комнате.
            current_room = world.get_current_room()
            has_live_enemy = (current_room.has_enemy
                              and current_room.enemy
                              and not current_room.enemy.is_dead)

            # Блокировка перемещения из комнаты с врагом.
            if not has_live_enemy and not heart.is_dead:
                if event.key == pygame.K_DOWN:
                    world.move_to_room(0, 1)
                elif event.key == pygame.K_UP:
                    world.move_to_room(0, -1)
                elif event.key == pygame.K_LEFT:
                    world.move_to_room(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    world.move_to_room(1, 0)

            # Нанесение урона врагу на пробел.
            elif event.key == pygame.K_SPACE and has_live_enemy:
                if current_room.enemy.is_critical_hit():
                    current_room.enemy.decrease_hp()
                    if sound_effects:
                        sound_effects['attack'].play()
                else:
                    heart.decrease_hp()
                    if sound_effects:
                        sound_effects['hit'].play()

        # Использование способностей нажатием левой кнопки мыши.
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not heart.is_dead:
            current_room = world.get_current_room()
            has_live_enemy = (current_room.has_enemy
                              and current_room.enemy
                              and not current_room.enemy.is_dead)
            if has_live_enemy:
                abilities.check_click(
                    event.pos, heart, mana, current_room.enemy, sound_effects)
                
        # Перезапуск игры.
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if heart.is_dead and heart.restart_button.collidepoint(event.pos):
                return 'restart'  # Сигнал для перезапуска игры.


def show_text_message(screen, text):
    '''Показывает текстовое сообщение на экране'''

    font = pygame.font.Font(None, 20)

    # Разбиваем текст на строки.
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Рендерим все строки.
    rendered_lines = []
    for line in lines:
        rendered = font.render(line, True, (255, 255, 255))
        rendered_lines.append(rendered)

    # Создаем поверхность для фона.
    bg_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    bg_surface.fill((0, 0, 0))

    # Позиционируем.
    bg_rect = bg_surface.get_rect(
        center=(screen.get_width()//2, screen.get_height()//2))

    # Отрисовываем.
    screen.blit(bg_surface, bg_rect)

    y_offset = 20
    for rendered in rendered_lines:
        text_rect = rendered.get_rect(
            centerx=bg_rect.centerx, top=bg_rect.top + y_offset)
        screen.blit(rendered, text_rect)
        y_offset += rendered.get_height() + 5

    pygame.display.flip()

    # Ждем нажатия клавиши.
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def update_screen(screen, hand, heart, mana, world, abilities, text):
    '''Обновление экрана'''

    # Если персонаж мёртв, то цвет фона меняется на красный.
    if heart.is_dead:
        screen.fill((255, 0, 0))

    current_room = world.get_current_room()

    # Проверяем первый вход в комнату с боссом.
    if (hasattr(current_room, 'is_boss_room')
       and current_room.is_boss_room
       and not current_room.boss_message_shown):
        show_text_message(screen, text)
        current_room.boss_message_shown = True

    # Проверяем условия для спавна босса.
    if not world.boss_spawned:
        world.check_boss_conditions()

    # Проверяем победу над боссом.
    if world.boss_spawned and world.check_boss_defeat():
        world.move_to_new_floor()
        world.boss_spawned = False
        world.boss_defeated = False

    # Проверяем и активируем события при первом посещении комнаты.
    if current_room.visited and not current_room.has_enemy and not current_room.event_triggered:
        current_room.trigger_event(heart, mana)

    # Отрисовываем сообщение о событии.
    current_room.write_event_message()

    # Карта (фон для мини-карты).
    map_rect = pygame.Rect(525, 0, 115, 115)
    world.map_rect = map_rect  # Сохраняем rect для использования в World.
    pygame.draw.rect(screen, (0, 0, 50), map_rect)
    world.draw_map()

    # Показываем/скрываем способности в зависимости от наличия врага.
    has_live_enemy = (current_room.has_enemy
                      and current_room.enemy
                      and not current_room.enemy.is_dead)
    if has_live_enemy:
        abilities.show()
    else:
        abilities.hide()

    # Отрисовка врага и его полосы атаки
    if current_room.has_enemy and current_room.enemy and not current_room.enemy.is_dead:
        current_room.enemy.output()
        current_room.enemy.hp_output()
        current_room.enemy.update_attack_bar()
        current_room.enemy.draw_attack_bar()

    # Отображаем счетчик пройденных этажей.
    font = pygame.font.Font(None, 25)
    boss_counter = font.render(
        f'Циклов пройдено: {world.bosses_defeated}', True, (255, 255, 255))
    screen.blit(boss_counter, (0, 70))

    hand.output()  # Отрисовка рук поверх экрана.
    heart.output()  # Отрисовка сердец поверх экрана.
    mana.output()  # Отрисовка маны поверх экрана.
    # Отрисовка иконок способностей и их эффектов поверх экрана.
    abilities.output()

    pygame.display.flip()  # Обновление отрисовок экрана.
