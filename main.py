import pygame
from for_player.hands import Hand
from for_player.stats import Heart, Mana
from for_game_work import controls
from for_game_work.world import World
from for_player.abilities import Abilities


# Главная рабочая функция.
def run():
    pygame.init()  # Инициализация игровой системы.
    pygame.mixer.init()  # Инициализация звуковой системы.
    clock = pygame.time.Clock()  # Используется для настройки FPS.

    screen = pygame.display.set_mode((640, 360))  # Размер экрана.
    pygame.display.set_caption('Infinity_dungeon')  # Название экрана.

    # Загрузка фонового изображения.
    background = pygame.image.load('sprites/background/background.png')

    hand = Hand(screen)  # Объект класса, взаимодействующего с руками.
    heart = Heart(screen)  # Объект класса, взаимодействующего с сердцами.
    mana = Mana(screen)  # Объект класса, взаимодействующего с маной.
    world = World(screen)  # Объект класса, взаимодействующего с картой.
    # Объект класса, взаимодействующего со способностями.
    abilities = Abilities(screen)

    # Фоновая музыка.
    pygame.mixer.music.load('sounds/background_music.mp3')
    pygame.mixer.music.set_volume(1.0)  # 100% от максимальной громкости.

    # Звуковые эффекты.
    hit_sound = pygame.mixer.Sound('sounds/hit_sound.ogg')
    attack_sound = pygame.mixer.Sound('sounds/attack_sound.ogg')
    heal_sound = pygame.mixer.Sound('sounds/heal_sound.ogg')

    # Устанавливаем громкость для всех звуковых эффектов.
    for sound in [hit_sound, attack_sound, heal_sound]:
        sound.set_volume(0.15)  # 15% от максимальной громкости.

    pygame.mixer.music.play(-1)  # Зацикливание музыки.

    # Передаем звуки в controls.
    sound_effects = {
        'hit': hit_sound,
        'attack': attack_sound,
        'heal': heal_sound
    }

    # Сюжетные тексты.
    INTRO_TEXT = '''Ходят легенды, что в древнем подземелье обитает безумный волшебник, 
    который смог подчинить само время, с помощью волшебного посоха невероятной силы.
    Ты намерен одолеть чародея и заполучить контроль над временем, чтобы ввести мир в эру 
    спокойствия и процветания. 
    Вот только такое чувство, что всё это ты уже слышишь не в первый раз...'''

    BOSS_TEXT = '''Тебе меня не одолеть! Жалкий смертный!
    Я управляю самим временем, даже если ты победишь меня, то я просто верну всё обратно!
    Ты обрёк себя на вечные попытки в тот момент, когда переступил порог моего подземелья!
    Интересно, сколько раз до этого ты уже слышал мои млова!?
    АХАХА-ХАХА-ХА!!!'''

    # Показываем вступительный текст.
    controls.show_text_message(screen, text=INTRO_TEXT)

    # Главный цикл исполнения игровых действий.
    while True:
        screen.blit(background, (0, 0))
        controls.events(world, heart, mana, abilities, sound_effects)
        controls.update_screen(screen, hand, heart, mana,
                               world, abilities, text=BOSS_TEXT)

        clock.tick(60)  # 60 кадров в секунду.


if __name__ == '__main__':
    run()
