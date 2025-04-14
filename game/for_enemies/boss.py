from pygame.image import load
from for_enemies.enemy_pattern import Enemy

class Boss(Enemy):
    def __init__(self, screen):
        '''Инициализация босса'''

        super().__init__(screen)
        self.enemy_image = load('sprites/enemies/boss.png')
        self.enemy_rect = self.enemy_image.get_rect()
        self.max_hp = 10
        self.current_hp = self.max_hp
        self.enemy_rect.x, self.enemy_rect.y = self.enemy_rect_coordinates
        
        # Боевые показатели.
        self.attack_speed = 5.0
        self.critical_zone_size = 20