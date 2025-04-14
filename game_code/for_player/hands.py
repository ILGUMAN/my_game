from pygame.image import load
from pygame.transform import flip


class Hand():
    def __init__(self, screen):
        '''Инициализация рук игрока'''

        # Получаем экран и руки.
        self.screen = screen
        self.leftf_hand_image = load('sprites/character/hand.png')
        self.right_hand_image = flip(
            self.leftf_hand_image, True, False)

        # Получили прямоугольники экрана и рук.
        self.screen_rect = screen.get_rect()
        self.left_hand_rect = self.leftf_hand_image.get_rect()
        self.right_hand_rect = self.right_hand_image.get_rect()

        # Задаём координаты рук на экране.
        self.left_hand_rect.bottom = self.screen_rect.bottom  # Для левой руки.
        self.left_hand_rect.left = self.screen_rect.left

        # Для правой руки.
        self.right_hand_rect.bottom = self.screen_rect.bottom
        self.right_hand_rect.right = self.screen_rect.right

    def output(self):
        '''Рисует руки'''

        self.screen.blit(self.leftf_hand_image, self.left_hand_rect)
        self.screen.blit(self.right_hand_image, self.right_hand_rect)
