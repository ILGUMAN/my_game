from random import choice, choices
from pygame import draw, font
from for_enemies.slime import Slime
from for_enemies.skeleton import Skeleton
from for_enemies.tentacles import Tentacles


class Room:
    '''Класс комнаты. Генерирует врагов и отрисовывает комнаты поверх карты'''

    def __init__(self, screen, x, y):
        '''Инициализация комнаты'''

        self.screen = screen
        self.x = x  # Координата комнаты на карте.
        self.y = y
        self.visited = False  # Изначально комната не посещена.
        self.has_enemy = choice(
            [True, False])  # 50% шанс на появление врага.
        # Флаг срабатывания события для пустой комнаты.
        self.event_triggered = False
        self.event_message = ""  # Сообщение события.
        self.message_timer = 60  # Время показа сообщения.
        self.enemy = None
        self.generate_enemy()

        self.is_boss_room = False
        self.boss_message_shown = False

    def generate_enemy(self):
        '''Генерация врага в комнате с определённой вероятностью'''

        if self.has_enemy:
            enemy_type = choices(
                ['slime', 'skeleton', 'tentacles'],
                weights=[50, 40, 10],  # 50% слизень, 40% скелет, 10% щупальца.
                k=1
            )[0]

            if enemy_type == 'slime':
                self.enemy = Slime(self.screen)
            elif enemy_type == 'skeleton':
                self.enemy = Skeleton(self.screen)
            else:
                self.enemy = Tentacles(self.screen)

    def trigger_event(self, heart, mana):
        '''Активирует случайное событие в комнате'''

        if self.has_enemy or self.event_triggered:
            return False

        events = [
            self._event_gain_mana,
            self._event_gain_health,
            self._event_lose_resources
        ]

        # Выбираем случайное событие.
        chosen_event = choice(events)
        result = chosen_event(heart, mana)

        if result:
            self.event_triggered = True
            return True
        return False

    def _event_gain_mana(self, heart, mana):
        '''Событие: получение маны'''

        mana.increase_mana()
        self.event_message = 'Получена 1 мана!'
        return True

    def _event_gain_health(self, heart, mana):
        '''Событие: получение здоровья'''

        heart.increase_hp()
        self.event_message = 'Получено 1 здоровье!'
        return True

    def _event_lose_resources(self, heart, mana):
        '''Событие: потеря ресурсов'''

        if heart.current_hp > 1 and mana.current_mana > 0:
            heart.decrease_hp()
            mana.decrease_mana()
            self.event_message = 'Потеряно 1 здоровье и 1 мана!'
            return True
        return False  # Не срабатывает, если это приведет к смерти.

    def write_event_message(self):
        '''Отрисовывает сообщение о событии'''

        if self.message_timer > 0:
            font_obj = font.Font(None, 36)
            text = font_obj.render(self.event_message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width()//2, 50))

            # Фон для текста.
            draw.rect(self.screen, (0, 0, 0),
                      (text_rect.x-10, text_rect.y-10,
                       text_rect.width+20, text_rect.height+20))

            self.screen.blit(text, text_rect)
            self.message_timer -= 1

    def draw_on_map(self, current_room_x, current_room_y, map_rect):
        '''Отрисовка комнаты на мини-карте'''

        room_size = 10  # Размер комнаты.
        padding = 5  # Отступы между комнатами.
        x = map_rect.x + padding + self.x * (room_size + padding)
        y = map_rect.y + padding + self.y * (room_size + padding)

        # Определяем цвет комнаты.
        if self.x == current_room_x and self.y == current_room_y:
            color = (0, 255, 0)  # Текущая комната - всегда зелёная.

        elif self.visited:
            if self.has_enemy and not self.enemy.is_dead:
                color = (255, 0, 0)  # Непобеждённый враг - красный.
            else:
                color = (100, 100, 255)  # Обычная посещённая комната - синий.

        else:
            color = (50, 50, 50)  # Непосещённая комната - тёмно-серый.

        draw.rect(self.screen, color, (x, y, room_size, room_size))
