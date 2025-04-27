from pygame.font import Font
from pygame.image import load


class Abilities():
    def __init__(self, screen):
        '''Инициализация способностей'''

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.abilities = []  # Список имеющихся способностей.
        self.setup_abilities()  # Создание кнопок для способностей.
        # Изначально кнопки невидны. Они появятся во время боя.
        self.visible = False

        self.effect_position = (60, 180)  # Позиция эффекта способности.
        self.effect_image = None  # Текущий эффект для отображения.
        self.effect_timer = 0  # Таймер для отображения эффекта.
        # Длительность отображения эффекта (в кадрах).
        self.effect_duration = 30

        # Флаг, указывающий, что эффект должен отображаться независимо от видимости кнопок.
        self.showing_effect = False

    def setup_abilities(self):
        '''Создание иконок способностей'''

        # Загрузка иконок и эффектов способностей.
        heal_image = load('sprites/abilities/heal.png')
        attack_image = load('sprites/abilities/attack.png')
        kill_image = load('sprites/abilities/kill.png')

        healing_image = load('sprites/abilities/healing.png')
        attacking_image = load('sprites/abilities/attacking.png')
        killing_image = load('sprites/abilities/killing.png')

        # Создаем кнопки способностей.
        self.abilities = [
            {
                'image': heal_image,
                'rect': heal_image.get_rect(),
                'type': 'heal',
                'cost': 1,
                'effect_image': healing_image
            },
            {
                'image': attack_image,
                'rect': attack_image.get_rect(),
                'type': 'attack',
                'cost': 2,
                'effect_image': attacking_image
            },
            {
                'image': kill_image,
                'rect': kill_image.get_rect(),
                'type': 'kill',
                'cost': 5,
                'effect_image': killing_image
            }
        ]

        # Позиционируем кнопки.
        center_x = self.screen_rect.centerx
        start_x = center_x - (len(self.abilities) * 55) // 2

        for i, ability in enumerate(self.abilities):
            ability['rect'].x = start_x + i * 55
            ability['rect'].y = 250  # Позиция выше бегунка атаки.

    def output(self):
        '''Рисует иконки способностей на экране и их эффекты'''

        # Рисуем эффект, если таймер активен (независимо от видимости кнопок).
        if self.effect_timer > 0:
            effect_rect = self.effect_image.get_rect()
            effect_rect.bottomleft = self.effect_position
            self.screen.blit(self.effect_image, effect_rect)
            self.effect_timer -= 1
            self.showing_effect = True
        else:
            self.showing_effect = False

        # Рисуем иконки способностей, если они видимы.
        if self.visible:
            for ability in self.abilities:
                self.screen.blit(ability['image'], ability['rect'])

                # Рисуем стоимость способности.
                font = Font(None, 24)
                cost_text = font.render(
                    str(ability['cost']), True, (255, 255, 255))
                cost_rect = cost_text.get_rect(
                    center=(ability['rect'].centerx, ability['rect'].bottom + 15))
                self.screen.blit(cost_text, cost_rect)

            # Рисуем эффект, если таймер активен.
            if self.effect_timer > 0:
                effect_rect = self.effect_image.get_rect()
                effect_rect.bottomleft = self.effect_position
                self.screen.blit(self.effect_image, effect_rect)
                self.effect_timer -= 1

    def check_click(self, pos, heart, mana, enemy, sound_effects=None):
        '''Проверяем нажатия на иконки'''

        if not self.visible:  # Не работает, если иконка невидима.
            return False

        for ability in self.abilities:
            # Если позиция мыши совпадает с позицией квадрата и маны достаточно, то способность применяется.
            if ability['rect'].collidepoint(pos):
                # Уменьшаем количиство маны.
                if mana.current_mana >= ability['cost']:
                    mana.decrease_mana(ability['cost'])
                    self.use_ability(
                        ability['type'], heart, enemy, ability['effect_image'], sound_effects)
                    return True
        return False

    def use_ability(self, ability_type, heart, enemy, effect_image, sound_effects=None):
        '''Использование способности'''

        self.effect_image = effect_image
        self.effect_timer = self.effect_duration

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
        '''Скрывает иконки способностей и их эффекты'''

        self.visible = False
