import pygame
from pygame.locals import *
import random
from typing import List, Tuple

from pprint import pprint as pp



Cell = Tuple[int, int]

Cells = List[int]

Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        self.create_grid(randomize = True)
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            b_grid = self.get_next_generation()
            self.grid = []
            for row in range(len(b_grid)):
                row_values = []
                for col in range(len(b_grid[row])):
                    row_values.append(b_grid[row][col])
                self.grid.append(row_values)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        self.grid = []
        for row in range(self.cell_height):
            row_values = []
            for col in range(self.cell_width):
                if randomize:
                     row_values.append(random.randint(0, 1))
                else:
                    row_values.append(0)
            self.grid.append(row_values)
        return self.grid 


    def draw_grid(self) -> None:

        """

        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.

        """

        for row in range(0, self.height, self.cell_size):
            for col in range(0, self.width, self.cell_size):
                if self.grid[row // self.cell_size][col // self.cell_size] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (col, row, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (col, row, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x, y = cell
        cells = []
        if x - 1 >= 0 and y - 1 >= 0:
            cells.append(self.grid[x - 1][y - 1])
        if x - 1 >= 0:
            cells.append(self.grid[x - 1][y])
        if x + 1 <= self.cell_height - 1 and y + 1 <= self.cell_width - 1:
            cells.append(self.grid[x + 1][y + 1])
        if y - 1 >= 0:
            cells.append(self.grid[x][y - 1])
        if y + 1 <=  self.cell_width - 1:
            cells.append(self.grid[x][y + 1])
        if x - 1 >= 0 and y + 1 <= self.cell_width - 1:
            cells.append(self.grid[x - 1][y + 1])
        if x + 1 <= self.cell_height - 1:
            cells.append(self.grid[x + 1][y])
        if x + 1 <= self.cell_height - 1 and y - 1 >= 0:
            cells.append(self.grid[x + 1][y - 1])
        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        b_grid = []
        for row in range(len(self.grid)):
            row_values = []
            for col in range(len(self.grid[row])):
                row_values.append(self.grid[row][col])
            b_grid.append(row_values)
        for row in range(len(b_grid)):
            for col in range(len(b_grid[row])):
                alive_nighbours = sum(self.get_neighbours((row, col)))
                if self.grid[row][col] == 1 and alive_nighbours == 2:
                    b_grid[row][col] = 1
                if alive_nighbours == 3:
                    b_grid[row][col] = 1
                if not (alive_nighbours == 2 or alive_nighbours == 3):
                    b_grid[row][col] = 0
        return b_grid




if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()


