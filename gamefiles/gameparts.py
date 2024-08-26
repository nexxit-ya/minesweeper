import pygame as pg
from random import randint

SPEED = 100

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

BACKGROUND_COLOR = (153, 153, 153)

CELL_COLOR = (140, 140, 140)

BORDER_COLOR = (100, 100, 100)

BOMB = pg.image.load('gamefiles/sprites/bomb.png')

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
        self.positions = {(x * GRID_SIZE, y * GRID_SIZE): {'bomb': False, 'clicked': False}
                          for x in range(0, FIELD_WIDTH)
                          for y in range(0, FIELD_HEIGHT)}

    def test(self, coords):
        return self.positions[coords]['bomb']

    def draw(self, screen):
        for position in self.positions.keys():
            rect = pg.Rect((position[0],
                            position[1]), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
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


def event_handler(bomb):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos_x, pos_y = pg.mouse.get_pos()
            click_coordinates = (pos_x - (pos_x % GRID_SIZE), pos_y - (pos_y % GRID_SIZE))
            print(click_coordinates)
            if click_coordinates in bomb.coordinates:
                bomb.found += 1
                bomb.coordinates.remove(click_coordinates)
                print('found')
