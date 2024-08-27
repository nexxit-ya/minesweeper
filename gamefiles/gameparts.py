import pygame as pg
from random import randint

SPEED = 100

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

BACKGROUND_COLOR = (153, 153, 153)

CELL_COLOR = (140, 140, 140)

FREE_CELL_COLOR = (255, 255, 255)

BORDER_COLOR = (100, 100, 100)

NUMBERS = {
    1: pg.image.load('gamefiles/sprites/1.png'),
    2: pg.image.load('gamefiles/sprites/2.png'),
    # 3: pg.image.load('gamefiles/sprites/3.png'),
    # 4: pg.image.load('gamefiles/sprites/4.png'),
    # 5: pg.image.load('gamefiles/sprites/5.png'),
    # 6: pg.image.load('gamefiles/sprites/6.png'),
    # 7: pg.image.load('gamefiles/sprites/7.png'),
    # 8: pg.image.load('gamefiles/sprites/8.png')
}

BOMB = pg.image.load('gamefiles/sprites/bomb.png')

FLAG = pg.image.load('gamefiles/sprites/flag.png')

APPLE_COLOR = (255, 0, 0)

GRID_SIZE = 20

FIELD_WIDTH, FIELD_HEIGHT = (SCREEN_WIDTH // GRID_SIZE,
                             SCREEN_HEIGHT // GRID_SIZE)


class Gamefield():
    """Класс игрового поля."""
    def __init__(self):
        pass


class cell():
    """Класс ячейки."""
    def __init__(self, bomb_count=30):
        self.body_color = CELL_COLOR
        self.bomb_color = APPLE_COLOR
        self.bomb_count = bomb_count
        self.bomb_coordinates = []
        self.positions = [(x * GRID_SIZE, y * GRID_SIZE)
                          for x in range(0, FIELD_WIDTH)
                          for y in range(0, FIELD_HEIGHT)]

    def get_near_cells(self, coords, bombs):
        """Получение координат соседних ячеек."""
        x, y = coords
        near_cells = [(x + GRID_SIZE, y),
                      (x - GRID_SIZE, y),
                      (x, y + GRID_SIZE),
                      (x, y - GRID_SIZE),
                      (x + GRID_SIZE, y + GRID_SIZE),
                      (x - GRID_SIZE, y - GRID_SIZE),
                      (x + GRID_SIZE, y - GRID_SIZE),
                      (x - GRID_SIZE, y + GRID_SIZE)]
        self.check_for_bombs(near_cells, bombs)
        return near_cells

    def check_for_bombs(self, coords, bomb):
        bombs_near = []
        print(bomb)
        for coord in coords:
            print(coords)
            if coord in bomb:
                bombs_near.append(coord)
        return bombs_near

    def draw(self, screen):
        for position in self.positions:
            rect = pg.Rect((position[0],
                            position[1]), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Numbers():
    def __init__(self):
        self.positions = []

    def set_position(self, number, coordinates):
        self.positions.append({'coordinates': coordinates, 'color': NUMBERS[number]})
        # position = {'coordinates': (x, y), 'number': NUMBERS[num]}

    def draw(self, screen):
        for coords, color in self.positions:
            pos_x, pos_y = coords
            rect = self.body_color.get_rect(center=(pos_x + (GRID_SIZE // 2),
                                                    pos_y + (GRID_SIZE // 2)))
            screen.blit(color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class free_cell():
    def __init__(self):
        self.positions = []
        self.body_color = FREE_CELL_COLOR

    def draw(self, screen):
        for position in self.positions:
            rect = pg.Rect((position[0],
                            position[1]), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class flag():
    def __init__(self):
        self.positions = []
        self.body_color = FLAG

    def draw(self, screen):
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
        for _ in range(self.count):
            while True:
                coordinates = (randint(0, FIELD_WIDTH - 1) * GRID_SIZE,
                               randint(0, FIELD_HEIGHT - 1) * GRID_SIZE)
                if coordinates not in self.coordinates:
                    self.coordinates.append(coordinates)
                    break

    def get_bomb_coordinates(self):
        return self.coordinates

    def draw(self, screen):
        for coords in self.coordinates:
            pos_x, pos_y = coords
            rect = self.body_color.get_rect(center=(pos_x + (GRID_SIZE // 2),
                                                    pos_y + (GRID_SIZE // 2)))
            screen.blit(self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def event_handler(cover, bomb, flag, free_cell, numbers):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = pg.mouse.get_pos()
            click_coordinates = (pos_x - (pos_x % GRID_SIZE), pos_y - (pos_y % GRID_SIZE))
            if click_coordinates in bomb.coordinates:
                cover.positions.clear()
            elif click_coordinates in flag.positions or click_coordinates in free_cell.positions:
                pass
            else:
                free_cell.positions.append(click_coordinates)
                near_cells = cover.get_near_cells(click_coordinates, bomb.coordinates)
                if len(cover.check_for_bombs(near_cells, bomb.coordinates)) == 0:
                    free_cell.positions.extend(near_cells)
                else:
                    numbers.positions.append(click_coordinates)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            pos_x, pos_y = pg.mouse.get_pos()
            click_coordinates = (pos_x - (pos_x % GRID_SIZE), pos_y - (pos_y % GRID_SIZE))
            if click_coordinates in bomb.coordinates:
                pass
            if click_coordinates not in flag.positions:
                flag.positions.append(click_coordinates)
