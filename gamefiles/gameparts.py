import pygame as pg
from random import randint

# Текущая скорость игры в тиках/сек
SPEED = 100

# Размер экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

# Цвет для заднего фона
BACKGROUND_COLOR = (153, 153, 153)

# Цвет для ячеек
CELL_COLOR = (140, 140, 140)

# Цвет для отмеченных ячеек, в которых нет бомб
FREE_CELL_COLOR = (255, 255, 255)

# Цвет границ вокруг ячеек
BORDER_COLOR = (100, 100, 100)

# Состояние игры. Если True - то нажатия не регистрируются
CLICK_FORBID = False

# Список спрайтов для номеров
NUMBERS = {
    1: pg.image.load('gamefiles/sprites/1.png'),
    2: pg.image.load('gamefiles/sprites/2.png'),
    3: pg.image.load('gamefiles/sprites/3.png'),
    4: pg.image.load('gamefiles/sprites/4.png'),
    5: pg.image.load('gamefiles/sprites/5.png'),
    6: pg.image.load('gamefiles/sprites/6.png'),
    7: pg.image.load('gamefiles/sprites/7.png'),
    8: pg.image.load('gamefiles/sprites/8.png')
}

# Спрайт бомбы
BOMB = pg.image.load('gamefiles/sprites/bomb.png')

# Спрайт флага
FLAG = pg.image.load('gamefiles/sprites/flag.png')

# Размер ячейки
GRID_SIZE = 20

# Размер игрового поля
FIELD_WIDTH, FIELD_HEIGHT = (SCREEN_WIDTH // GRID_SIZE,
                             SCREEN_HEIGHT // GRID_SIZE)


class cell():
    """Класс ячейки. По умолчанию ячейка 'Накрывает' все клетки игрового поля"""
    def __init__(self):
        self.body_color = CELL_COLOR
        self.positions = [(x * GRID_SIZE, y * GRID_SIZE)
                          for x in range(0, FIELD_WIDTH)
                          for y in range(0, FIELD_HEIGHT)]

    def get_near_cells(self, coords, bombs):
        """Получение координат соседних ячеек и проверка на бомбы"""
        x, y = coords
        near_cells = [(x + GRID_SIZE, y),
                      (x - GRID_SIZE, y),
                      (x, y + GRID_SIZE),
                      (x, y - GRID_SIZE),
                      (x + GRID_SIZE, y + GRID_SIZE),
                      (x - GRID_SIZE, y - GRID_SIZE),
                      (x + GRID_SIZE, y - GRID_SIZE),
                      (x - GRID_SIZE, y + GRID_SIZE)]
        num_of_bombs = self.check_for_bombs(near_cells, bombs)
        return near_cells, num_of_bombs

    def check_for_bombs(self, coords, bomb) -> int:
        """Проверка на наличие бомб в соседних ячейках. Возвращает количество бомб"""
        bombs_near = 0
        for coord in coords:
            if coord in bomb:
                bombs_near += 1
        return bombs_near

    def draw(self, screen):
        """Отрисовка ячеек"""
        for position in self.positions:
            rect = pg.Rect((position[0],
                            position[1]), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Numbers():
    """Класс для отображения чисел"""
    def __init__(self):
        self.positions = []

    def set_position(self, number, coordinates):
        """Устанавливает координаты и цвет ячейки"""
        self.positions.append({'coordinates': coordinates, 'color': NUMBERS[number]})
        self.body_color = NUMBERS[number]

    def draw(self, screen):
        """Отрисовка чисел"""
        for entry in self.positions:
            pos_x, pos_y = entry['coordinates']
            rect = entry['color'].get_rect(center=(pos_x + (GRID_SIZE // 2),
                                                   pos_y + (GRID_SIZE // 2)))
            screen.blit(entry['color'], rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stopwatch():
    """Класс таймера для отображения времени"""
    def __init__(self, speed):
        self.speed = speed  # speed - number of ticks in 1 sec
        self.ticks = 0  # num. of ticks from last second
        self.time = 1  # num. of seconds from start
        self.display_time = '00:01'

    def update_time(self):
        """Обновление времени 1 раз в тик"""
        self.ticks += 1
        if self.ticks == self.speed:
            self.time += 1
            self.ticks = 0
        minutes = str(self.time // 60)
        seconds = str(self.time % 60)
        if int(seconds) < 10:
            seconds = '0' + seconds
        if int(minutes) < 10:
            minutes = '0' + minutes
        self.display_time = minutes + ':' + seconds


class free_cell():
    """Класс для отображения свободных ячеек без бомб"""
    def __init__(self):
        self.positions = []
        self.body_color = FREE_CELL_COLOR

    def draw(self, screen):
        """Отрисовка свободных ячеек"""
        for position in self.positions:
            rect = pg.Rect((position[0],
                            position[1]), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class flag():
    """Класс флага, которым помечают бомбу"""
    def __init__(self):
        self.positions = []
        self.body_color = FLAG
        self.placed = 0

    def draw(self, screen):
        """Отрисовка флага"""
        for coords in self.positions:
            pos_x, pos_y = coords
            rect = self.body_color.get_rect(center=(pos_x + (GRID_SIZE // 2),
                                                    pos_y + (GRID_SIZE // 2)))
            screen.blit(self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class bomb():
    """Класс бомбы."""
    def __init__(self, count):
        self.coordinates = []
        self.body_color = BOMB
        self.count = count
        self.found = 0
        self.generate_bombs()

    def generate_bombs(self):
        """Случайная генерация координат бомб"""
        for _ in range(self.count):
            while True:
                coordinates = (randint(0, FIELD_WIDTH - 1) * GRID_SIZE,
                               randint(0, FIELD_HEIGHT - 1) * GRID_SIZE)
                if coordinates not in self.coordinates:
                    self.coordinates.append(coordinates)
                    break

    def get_bomb_coordinates(self):
        """Возвращает координаты бомб"""
        return self.coordinates

    def draw(self, screen):
        """Отрисовка бомб"""
        for coords in self.coordinates:
            pos_x, pos_y = coords
            rect = self.body_color.get_rect(center=(pos_x + (GRID_SIZE // 2),
                                                    pos_y + (GRID_SIZE // 2)))
            screen.blit(self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def click_check(click_coords, cells, bombs, flags, free_cells, numbers):
    """Проверка условий после нажатия на клетку"""
    if (click_coords in bombs.coordinates) and (click_coords not in flags.positions):
        cells.positions.clear()
        pg.display.set_caption('Game Over!')
        global CLICK_FORBID
        CLICK_FORBID = True
    elif (click_coords in flags.positions) or (click_coords in free_cells.positions):
        pass
    else:
        free_cells.positions.append(click_coords)
        near_cells, num_of_bombs = cells.get_near_cells(click_coords, bombs.coordinates)

        if num_of_bombs == 0:
            for cell in near_cells:
                more_near_cells, near_bombs = cells.get_near_cells(cell, bombs.coordinates)
                free_cells.positions.append(cell)
                if near_bombs > 0:
                    numbers.set_position(near_bombs, cell)
        else:
            numbers.set_position(num_of_bombs, click_coords)


def event_handler(cells, bomb, flag, free_cell, numbers):
    """Обработка типов нажатий"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not CLICK_FORBID:
            pos_x, pos_y = pg.mouse.get_pos()
            click_coordinates = (pos_x - (pos_x % GRID_SIZE), pos_y - (pos_y % GRID_SIZE))
            click_check(click_coordinates, cells, bomb, flag, free_cell, numbers)

        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and not CLICK_FORBID:
            pos_x, pos_y = pg.mouse.get_pos()
            click_coordinates = (pos_x - (pos_x % GRID_SIZE), pos_y - (pos_y % GRID_SIZE))
            if click_coordinates in bomb.coordinates:
                pass

            if click_coordinates not in flag.positions:
                flag.positions.append(click_coordinates)
                flag.placed += 1
            else:
                flag.positions.remove(click_coordinates)
                flag.placed -= 1

            if len(list(set(cells.coordinates) - set(bomb.positions))) == 0:
                pg.display.set_caption('You win!')
                global CLICK_FORBID
                CLICK_FORBID = True
