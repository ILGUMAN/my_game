from pygame.image import load
from for_enemies.enemy_pattern import Enemy


class Tentacles(Enemy):
    '''Противник'''

    def __init__(self, screen):
        '''Инициализируем противника'''

        # Наследуем квадраты экрана и противника, и флаг смерти.
        super().__init__(screen)

        # Получаем картинку противника.
        self.enemy_image = load('sprites/enemies/tentacles.png')
        # Получаем квадрат противника.
        self.enemy_rect = self.enemy_image.get_rect()
        # Получаем жизни противника.
        self.max_hp = 5
        self.current_hp = self.max_hp
        # Устанавливаем координаты противника.
        self.enemy_rect.x, self.enemy_rect.y = self.enemy_rect_coordinates
        
        # Боевые показатели.
        self.attack_speed = 3.0
        self.critical_zone_size = 30
