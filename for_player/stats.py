from pygame.image import load
from pygame.font import Font
from pygame import draw


class Heart():
    def __init__(self, screen):
        '''Инициализация жизней'''

        self.max_hp = 5  # Максимальные жизни.
        self.current_hp = self.max_hp  # Стартовые жизни.

        # Получаем экран и сердце.
        self.screen = screen
        self.heart_image = load('sprites/character/heart.png')

        # Получаем прямоугольники экрана и сердец.
        self.screen_rect = screen.get_rect()
        self.heart_rect = self.heart_image.get_rect()

        # Задаём начальные координаты сердец на экране.
        self.heart_rect.top = self.screen_rect.top
        self.heart_rect.left = self.screen_rect.left

        self.is_dead = False  # Флаг смерти.

    def output(self):
        '''Рисует сердца'''

        # Сохраняем исходную позицию первого сердца.
        original_left = self.heart_rect.left

        for hp in range(self.current_hp):
            self.screen.blit(self.heart_image, self.heart_rect)

            # Сдвигаем позицию для следующего сердца.
            self.heart_rect.left = self.heart_rect.right

        # Восстанавливаем исходную позицию для следующего вызова функции.
        self.heart_rect.left = original_left

        if self.is_dead:
            self.show_death_text()

    def decrease_hp(self):
        '''Уменьшает жизни на 1'''

        if self.current_hp > 0:
            self.current_hp -= 1
            if self.current_hp <= 0:
                self.die()  # Если сердец <= 0, то персонаж умирает.

    def increase_hp(self):
        '''Увеличение жизней на 1, но не более чем max_hp'''

        if self.current_hp < self.max_hp:
            self.current_hp += 1  # Увеличение жизней, если они меньше предела.
            # Убирает красный экран и надпись при отхиле после смерти.
            self.is_dead = False

    def die(self):
        '''Изменяет флаг окончания игры'''

        self.is_dead = True

    def show_death_text(self):
        '''Выводит на экран смерти надпись'''

        font = Font(None, 48)  # Создание шрифта.
        # Создание текста.
        text = font.render("GAME OVER!!!", True, (255, 255, 255))
        # Создание прямоугольника для текста.
        text_rect = text.get_rect(
            center=(self.screen_rect.centerx, self.screen_rect.centery))
        # Фон для текста.
        draw.rect(self.screen, (0, 0, 0),
                      (text_rect.x-10, text_rect.y-10,
                       text_rect.width+20, text_rect.height+20))
        self.screen.blit(text, text_rect)  # Вывод текста на экран.


class Mana():
    def __init__(self, screen):
        '''Инициализация маны'''

        self.max_mana = 5  # Максимальная мана.
        self.current_mana = self.max_mana  # Стартовая мана.

        # Получаем экран и ману.
        self.screen = screen
        self.mana_image = load('sprites/character/mana.png')

        # Получаем прямоугольники экрана и маны.
        self.screen_rect = screen.get_rect()
        self.mana_rect = self.mana_image.get_rect()

        # Задаём начальные координаты маны на экране.
        self.mana_rect_coordinates = (0, 33)
        self.mana_rect.x, self.mana_rect.y = self.mana_rect_coordinates

    def output(self):
        '''Рисует ману'''

        # Сохраняем исходную позицию первой маны.
        original_left = self.mana_rect.x

        for mana in range(self.current_mana):
            self.screen.blit(self.mana_image, self.mana_rect)

            # Сдвигаем позицию для следующей маны.
            self.mana_rect.x += 33

        # Восстанавливаем исходную позицию для следующего вызова функции.
        self.mana_rect.x = original_left

    def decrease_mana(self, amount=1):
        '''Уменьшает ману на указанное количество'''

        if self.current_mana > 0:
            self.current_mana = max(0, self.current_mana - amount)

    def increase_mana(self):
        '''Увеличение маны на 1, но не более чем max_mana'''

        if self.current_mana < self.max_mana:
            self.current_mana += 1  # Увеличение маны, если она меньше предела.
