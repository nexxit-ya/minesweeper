import pygame as pg
from gamefiles import gameparts as game


screen = pg.display.set_mode((game.SCREEN_WIDTH, game.SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Сапёр. Найдено бомб: 0 из 0')

clock = pg.time.Clock()


def main():
    pg.init()

    board = game.cell()
    bombs = game.bomb(30)
    flags = game.flag()
    number_cells = game.near_1()
    free_cells = game.free_cell()
    screen.fill(game.BACKGROUND_COLOR)
    while True:
        clock.tick(game.SPEED)
        game.event_handler(board, bombs, flags, free_cells, number_cells)
        bombs.draw(screen)
        board.draw(screen)
        flags.draw(screen)
        free_cells.draw(screen)
        number_cells.draw(screen)
        pg.display.set_caption(f'Сапёр. Найдено бомб: {bombs.found} из {bombs.count}')
        pg.display.update()


if __name__ == '__main__':
    main()
