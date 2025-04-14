from pygame.font import Font
from pygame.image import load
from pygame.transform import scale


class Abilities():
    def __init__(self, screen):
        '''Инициализация способностей'''

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.abilities = []  # Список имеющихся способностей.
        self.setup_abilities()  # Создание кнопок для способностей.
        # Изначально кнопки невидны. Они появятся во время боя.
        self.visible = False

    def setup_abilities(self):
        '''Создание иконок способностей'''

        # Загрузка и масштабирование иконок.
        heal_image = scale(load('sprites/abilities/heal.png'), (50, 50))
        attack_image = scale(load('sprites/abilities/attack.png'), (50, 50))
        escape_image = scale(load('sprites/abilities/kill.png'), (50, 50))

        # Создаем кнопки способностей.
        self.abilities = [
            {
                'image': heal_image,
                'rect': heal_image.get_rect(),
                'type': 'heal',
                'cost': 1
            },
            {
                'image': attack_image,
                'rect': attack_image.get_rect(),
                'type': 'attack',
                'cost': 2
            },
            {
                'image': escape_image,
                'rect': escape_image.get_rect(),
                'type': 'kill',
                'cost': 5
            }
        ]

        # Позиционируем кнопки.
        center_x = self.screen_rect.centerx
        start_x = center_x - (len(self.abilities) * 55) // 2

        for i, ability in enumerate(self.abilities):
            ability['rect'].x = start_x + i * 55
            ability['rect'].y = 250  # Позиция выше бегунка атаки.

    def output(self):
        '''Рисует иконки способностей на экране'''

        if not self.visible:  # Ничего не делаем, если они невидимые.
            return

        # Рисуем иконки способностей.
        for ability in self.abilities:
            self.screen.blit(ability['image'], ability['rect'])

            # Рисуем стоимость способности.
            font = Font(None, 24)
            cost_text = font.render(
                str(ability['cost']), True, (255, 255, 255))
            cost_rect = cost_text.get_rect(
                center=(ability['rect'].centerx, ability['rect'].bottom + 15))
            self.screen.blit(cost_text, cost_rect)

    def check_click(self, pos, heart, mana, enemy, world, sound_effects=None):
        '''Проверяем нажатия на иконки'''

        if not self.visible:  # Не работает, если иконка невидима.
            return False

        for ability in self.abilities:
            # Если позиция мыши совпадает с позицией квадрата и маны достаточно, то способность применяется.
            if ability['rect'].collidepoint(pos):
                # Уменьшаем количиство маны.
                if mana.current_mana >= ability['cost']:
                    mana.decrease_mana(ability['cost'])
                    self.use_ability(ability['type'], heart, enemy, world, sound_effects)
                    return True
        return False

    def use_ability(self, ability_type, heart, enemy, world, sound_effects=None):
        '''Использование способности'''

        if ability_type == 'heal':
            heart.increase_hp()
            if sound_effects:
                sound_effects['heal'].play()
        elif ability_type == 'attack':
            if enemy and not enemy.is_dead:
                enemy.decrease_hp()
                if sound_effects:
                    sound_effects['attack'].play()
        elif ability_type == 'kill':
            enemy.decrease_hp(enemy.current_hp)
            if sound_effects:
                sound_effects['attack'].play()

    def show(self):
        '''Показывает иконки способностей'''

        self.visible = True

    def hide(self):
        '''Скрывает иконки способностей'''

        self.visible = False
