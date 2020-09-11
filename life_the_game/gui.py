import pygame
from life import GameOfLife
from UI import UI
from pygame.locals import *


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=50, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.height = self.cell_size * self.life.rows
        self.width = self.cell_size * self.life.cols
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                            (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                            (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row in range(0, self.height, self.cell_size):
            for col in range(0, self.width, self.cell_size):
                if self.life.curr_generation[row // self.cell_size][col // self.cell_size] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                    (col, row, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                    (col, row, self.cell_size, self.cell_size))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Life')
        self.life.create_grid(True)
        running = True
        pause = False
        while running and self.life.is_changing
        and not self.life.is_max_generations_exceed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if not pause:
                            pause = True
                        else:
                            pause = False
                if event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    x = x // self.cell_size
                    y = y // self.cell_size
                    if self.life.curr_generation[y][x] == 1:
                        self.life.curr_generation[y][x] = 0
                    else:
                        self.life.curr_generation[y][x] = 1
                    self.draw_grid()
                    pygame.display.flip()

            if pause:
                self.draw_grid()
                pygame.display.flip()
                continue
            self.draw_lines()
            self.draw_grid()
            self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == "__main__":
    life = GameOfLife(size=(10, 8), randomize=True, max_generations=80)
    gui = GUI(life)
    gui.run()
