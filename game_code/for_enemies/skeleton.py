from pygame.image import load
from for_enemies.enemy_pattern import Enemy


class Skeleton(Enemy):
    '''Противник'''

    def __init__(self, screen):
        '''Инициализируем противника'''

        # Наследуем квадраты экрана и противника, и флаг смерти.
        super().__init__(screen)

        # Получаем картинку противника.
        self.enemy_image = load('sprites/enemies/skeleton.png')
        # Получаем квадрат противника.
        self.enemy_rect = self.enemy_image.get_rect()
        # Получаем жизни противника.
        self.max_hp = 3
        self.current_hp = self.max_hp
        # Устанавливаем координаты противника.
        self.enemy_rect.x, self.enemy_rect.y = self.enemy_rect_coordinates

        # Боевые показатели.
        self.attack_speed = 2.0
        self.critical_zone_size = 40
