import pathlib
import random
import copy

from typing import List, Optional, Tuple

Cell = Tuple[int, int]

Cells = List[int]

Grid = List[Cells]


class GameOfLife:

    

    def __init__(

        self,

        size: Tuple[int, int],

        randomize: bool=True,

        max_generations: Optional[float]=float('inf')

    ) -> None:

        # Размер клеточного поля

        self.rows, self.cols = size

        # Предыдущее поколение клеток

        self.prev_generation = self.create_grid()

        # Текущее поколение клеток

        self.curr_generation = self.create_grid(randomize=randomize)

        # Максимальное число поколений

        self.max_generations = max_generations

        # Текущее число поколений

        self.n_generation = 1



    def create_grid(self, randomize: bool=False) -> Grid:
        
        grid = []
        for row in range(self.rows):
            row_values = []
            for col in range(self.cols):
                if randomize:
                     row_values.append(random.randint(0, 1))
                else:
                    row_values.append(0)
            grid.append(row_values)
        return grid 

    def get_neighbours(self, cell: Cell) -> Cells:

        x, y = cell
        cells = []
        if x - 1 >= 0 and y - 1 >= 0:
            cells.append(self.curr_generation[x - 1][y - 1])
        if x - 1 >= 0:
            cells.append(self.curr_generation[x - 1][y])
        if x + 1 <= self.rows - 1 and y + 1 <= self.cols - 1:
            cells.append(self.curr_generation[x + 1][y + 1])
        if y - 1 >= 0:
            cells.append(self.curr_generation[x][y - 1])
        if y + 1 <=  self.cols - 1:
            cells.append(self.curr_generation[x][y + 1])
        if x - 1 >= 0 and y + 1 <= self.cols - 1:
            cells.append(self.curr_generation[x - 1][y + 1])
        if x + 1 <= self.rows - 1:
            cells.append(self.curr_generation[x + 1][y])
        if x + 1 <= self.rows - 1 and y - 1 >= 0:
            cells.append(self.curr_generation[x + 1][y - 1])
        return cells



    def get_next_generation(self) -> Grid:

        b_grid = []
        for row in range(len(self.curr_generation)):
            row_values = []
            for col in range(len(self.curr_generation[row])):
                row_values.append(self.curr_generation[row][col])
            b_grid.append(row_values)
        for row in range(len(b_grid)):
            for col in range(len(b_grid[row])):
                alive_nighbours = sum(self.get_neighbours((row, col)))
                if self.curr_generation[row][col] == 1 and alive_nighbours == 2:
                    b_grid[row][col] = 1
                if alive_nighbours == 3:
                    b_grid[row][col] = 1
                if not (alive_nighbours == 2 or alive_nighbours == 3):
                    b_grid[row][col] = 0
        return b_grid



    def step(self) -> None:

        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.n_generation += 1



    @property

    def is_max_generations_exceed(self) -> bool:
        if self.max_generations is not None:

            return self.max_generations <= self.n_generation 
        return False



    @property

    def is_changing(self) -> bool:

        return self.curr_generation != self.prev_generation



    @staticmethod

    def from_file(filename: pathlib.Path) -> 'GameOfLife':

        str_table = filename.read_text().split('\n')
        game = GameOfLife((len(str_table), len(str_table[0])), False)
        game.curr_generation = []
        for row in str_table:
            sub_Array = []
            for col in row:
                sub_Array.append(int(col))
            game.curr_generation.append(sub_Array)
        return game


    def save(filename: pathlib.Path) -> None:

        for row in self.curr_generation:
            filename.write_text(str(row).replace(',', '').replace('[', '').replace(']', '\n'))
