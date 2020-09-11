import curses
from UI import UI
from life import GameOfLife
import time


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border('|', '|', '_', '_', '*', '*', '*', '*')

    def draw_grid(self, screen) -> None:
        y, x = screen.getmaxyx()
        x = x // 2
        y = y // 2
        centerrows = self.life.rows // 2
        centercols = self.life.cols // 2
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    screen.addstr(col + y - centercols,
                                  row + x - centerrows, 'O')
                else:
                    screen.addstr(col + y - centercols,
                                  row + x - centerrows, ' ')

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        pause = False
        screen.keypad(True)
        self.life.create_grid(True)
        self.draw_borders(screen)
        screen.nodelay(True)
        while self.life.is_changing and not self.life.is_max_generations_exceed:
            if screen.getch() == ord('p'):
                if not pause:
                    pause = True
                else:
                    pause = False
            if screen.getch() == 27:
                break
            if pause:
                continue
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(3)
        curses.endwin()

if __name__ == '__main__':
    life = GameOfLife(size=(10, 8), randomize=True, max_generations=80)
    CLI = Console(life)
    CLI.run()