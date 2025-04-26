from for_game_work.room import Room
from random import choice, shuffle, randint
from for_enemies.boss import Boss


class World:
    '''Класс ответственный за генерацию карты, её отрисовку и передвижение по комнатам'''

    def __init__(self, screen, map_width=7, map_height=7):
        '''Инициализация мира'''

        self.screen = screen
        self.map_width = map_width  # Количество вмещаемых комнат по х.
        self.map_height = map_height  # Количество вмещаемых комнат по у.
        # Матрица с пустыми комнатами.
        self.rooms = [[None for i in range(map_height)]
                      for j in range(map_width)]
        self.current_room_x = map_width // 2  # Начальные координаты.
        self.current_room_y = map_height // 2
        self.map_rect = None  # Будет установлено при инициализации.
        self.generate_world()
        # Запоминаем стартовую комнату.
        self.start_room_x = self.current_room_x
        self.start_room_y = self.current_room_y
        self.boss_spawned = False  # Изначально на этаже нет босса.
        self.boss_defeated = False  # Изначально босс не побеждён.
        self.bosses_defeated = 0  # Счётчик пройденных этажей.

    def generate_world(self):
        '''Генерация мира и начальных комнат'''

        # Создаем стартовую комнату.
        start_x, start_y = self.current_room_x, self.current_room_y
        self.rooms[start_x][start_y] = Room(self.screen, start_x, start_y)
        # Стартовая комната посещена.
        self.rooms[start_x][start_y].visited = True
        # Стартовая комната всегда без монстра.
        self.rooms[start_x][start_y].has_enemy = False

        # Создаем 3 начальные соседние комнаты.
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        shuffle(directions)  # Перемешиваем направления.

        # Выбираем только 3 случайных направления.
        for dx, dy in directions[:3]:
            nx, ny = start_x + dx, start_y + dy
            # Не даём комнатам выйти за пределы карты.
            if 0 <= nx < self.map_width and 0 <= ny < self.map_height:
                self.rooms[nx][ny] = Room(self.screen, nx, ny)
                # У начальных комнат создаём соседние, количество которых от 3 до 6.
                self.generate_path(nx, ny, (dx, dy), depth=randint(3, 6))

    def generate_path(self, x, y, from_direction, depth):
        '''Генерация всего этажа'''

        if depth <= 0:  # Прирывает создание комнат, если вся глубина исчерпана.
            return

        # Вверх, вправо, вниз, влево.
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        # Направление "назад".
        opposite_dir = (-from_direction[0], -from_direction[1])

        # Удаляем обратное направление и уже занятые направления.
        valid_directions = [d for d in directions if d != opposite_dir]

        # Ограничиваем количество новых путей.
        if len(valid_directions) > 0:
            dx, dy = choice(valid_directions)  # Выбор нового направления.
            nx, ny = x + dx, y + dy

            if (0 <= nx < self.map_width and 0 <= ny < self.map_height
                    # Проверяет, что новые координаты в пределах карты.
                    and self.rooms[nx][ny] is None):
                self.rooms[nx][ny] = Room(self.screen, nx, ny)
                # Создаёт новую комнату и продолжает генерацию с уменьшенной глубиной.
                self.generate_path(nx, ny, (dx, dy), depth-1)

    def move_to_room(self, dx, dy):
        '''Передвижение между комнатами'''

        # Координаты новых комнат.
        new_x, new_y = self.current_room_x + dx, self.current_room_y + dy

        if 0 <= new_x < self.map_width and 0 <= new_y < self.map_height:
            # Не выходим за пределы экрана.
            if self.rooms[new_x][new_y] is None:
                return False  # Не создаем новые комнаты при движении.

            self.current_room_x, self.current_room_y = new_x, new_y
            self.rooms[new_x][new_y].visited = True  # Посещаем комнату.
            return True  # Успешное перемещение.
        return False  # На пути есть преграда, перемещение невозможно.

    def get_current_room(self):
        '''Получение координат текущей комнаты'''

        return self.rooms[self.current_room_x][self.current_room_y]

    def draw_map(self):
        '''Отрисовка всей карты'''

        for x in range(self.map_width):
            for y in range(self.map_height):
                # Если комната существует, то её рисуют на мини-карте.
                if self.rooms[x][y] is not None:
                    self.rooms[x][y].draw_on_map(
                        self.current_room_x,
                        self.current_room_y,
                        self.map_rect
                    )

    def check_boss_conditions(self):
        '''Проверяет условия для спавна босса: все враги убиты и все комнаты посещены'''

        if self.boss_spawned:
            return False

        # Проверяем, что все комнаты с врагами очищены.
        all_enemies_defeated = True
        all_rooms_visited = True

        for x in range(self.map_width):
            for y in range(self.map_height):
                room = self.rooms[x][y]
                if room is not None:
                    # Проверка на непобежденных врагов.
                    if room.has_enemy and room.enemy and not room.enemy.is_dead:
                        all_enemies_defeated = False

                    # Проверка на непосещенные комнаты.
                    if not room.visited:
                        all_rooms_visited = False

        # Если оба условия выполнены - спавним босса.
        if all_enemies_defeated and all_rooms_visited:
            self.spawn_boss()
            return True

        return False

    def spawn_boss(self):
        '''Создает босса в стартовой комнате'''

        start_room = self.rooms[self.start_room_x][self.start_room_y]
        start_room.has_enemy = True
        start_room.enemy = Boss(self.screen)  # Создаем босса.
        self.boss_spawned = True

    def move_to_new_floor(self):
        '''Генерация нового этажа с сохранением прогресса'''

        # Запоминаем текущие показатели игрока.
        old_hp = self.player_hp if hasattr(self, 'player_hp') else None
        old_mana = self.player_mana if hasattr(self, 'player_mana') else None

        # Очищаем этаж.
        for x in range(self.map_width):
            for y in range(self.map_height):
                self.rooms[x][y] = None

        # Генерируем новый этаж.
        self.generate_world()

        # Восстанавливаем показатели.
        if old_hp is not None:
            self.player_hp = old_hp
        if old_mana is not None:
            self.player_mana = old_mana

    def check_boss_defeat(self):
        '''Проверяет убит ли босс'''

        if self.boss_spawned and not self.boss_defeated:
            start_room = self.rooms[self.start_room_x][self.start_room_y]
            if start_room.has_enemy and start_room.enemy and start_room.enemy.is_dead:
                self.boss_defeated = True
                # Увеличиваем счетчик пройденных этажей.
                self.bosses_defeated += 1
                return True
        return False
