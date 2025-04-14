from pygame.image import load
from pygame import draw


class Enemy():
    '''Шаблон для создания различных противников'''

    def __init__(self, screen):
        '''Инициализация противника'''

        # Получаем экран.
        self.screen = screen
        # Получаем квадрат экрана.
        self.screen_rect = screen.get_rect()
        # Изначально противник жив.
        self.is_dead = False
        # Координаты квадрата противника.
        self.enemy_rect_coordinates = (200, 0)
        # Будет у конкретных монстров.
        self.enemy_image = None
        self.enemy_rect = None
        # Количество жизней (будет задано в дочерних классах).
        self.max_hp = None
        # Добавляем атрибуты для отрисовки жизней.
        self.heart_image = load('sprites/enemies/heart.png')
        self.heart_rect = self.heart_image.get_rect()
        # Координаты жизней.
        self.heart_rect.topleft = (200, 10)
        # Базовая скорость (будет переопределена в дочерних классах).
        self.attack_speed = None
        self.critical_zone_size = None  # Размер критической зоны.
        self.attack_bar_pos = 0  # Позиция бегунка.
        # Направление движения.
        self.attack_direction = 1

    def output(self):
        '''Рисует противника на экране'''

        if not self.is_dead:
            self.screen.blit(self.enemy_image, self.enemy_rect)

    def decrease_hp(self, amount=1):
        '''Уменьшает жизни противника на указанное количиство'''

        if not self.is_dead:
            self.current_hp -= amount
            if self.current_hp <= 0:
                self.die()

    def die(self):
        '''Меняет флаг живости противника'''

        self.is_dead = True

    def hp_output(self):
        '''Рисует сердца'''

        # Сохраняем исходную позицию первого сердца.
        original_left = self.heart_rect.left

        for hp in range(self.current_hp):
            self.screen.blit(self.heart_image, self.heart_rect)

            # Сдвигаем позицию для следующего сердца.
            self.heart_rect.left = self.heart_rect.right

        # Восстанавливаем исходную позицию для следующего вызова функции.
        self.heart_rect.left = original_left

    def update_attack_bar(self):
        '''Обновление позиции бегунка атаки'''

        if not self.is_dead:
            # Двигаем бегунок.
            self.attack_bar_pos += self.attack_direction * self.attack_speed

            # Если достигли края - меняем направление.
            if self.attack_bar_pos <= 0 or self.attack_bar_pos >= 320:
                self.attack_direction *= -1

    def draw_attack_bar(self):
        '''Отрисовка полосы атаки'''

        if not self.is_dead:
            # Основная полоса.
            draw.rect(self.screen, (0, 0, 0), (160, 320, 320, 20))
            draw.rect(self.screen, (0, 255, 0), (160, 320, 320, 20), 2)

            # Критическая зона (центр полосы).
            center = 320 - self.critical_zone_size // 2
            draw.rect(self.screen, (255, 215, 0),
                      (center, 320, self.critical_zone_size, 20))

            # Бегунок.
            draw.rect(self.screen, (255, 0, 0),
                      (160 + self.attack_bar_pos - 2, 320, 4, 20))

    def is_critical_hit(self):
        '''Проверка, находится ли бегунок в критической зоне'''

        center = 320 - self.critical_zone_size // 2
        return center <= (160 + self.attack_bar_pos) <= center + self.critical_zone_size
