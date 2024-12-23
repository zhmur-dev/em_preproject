from random import sample


class Cell:
    def __init__(self, around_mines=0, mine=False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False


class GamePole:
    def __init__(self, n: int, m: int):
        self.N = n
        self.M = m
        self.pole = []
        self.init()

    def set_new_pole(self):
        self.pole = [
            [Cell() for x in range(self.N)] for y in range(self.N)
        ]

    def set_mines(self):
        for mine in sample(range(self.N * self.N), self.M):
            self.pole[mine // self.N][mine % self.N].mine = True

    def set_around_mines(self, x, y):
        self.pole[x][y].around_mines = 0
        for around_x in range(x-1, x+2):
            for around_y in range(y-1, y+2):
                if (self.N > around_x >= 0 and self.N > around_y >= 0
                        and self.pole[around_x][around_y].mine
                        and not (around_x == x and around_y == y)):
                    self.pole[x][y].around_mines += 1

    def init(self):
        self.set_new_pole()
        self.set_mines()
        for x in range(self.N):
            for y in range(self.N):
                self.set_around_mines(x, y)

    def show(self):
        for x in range(self.N):
            row = ''
            for y in range(self.N):
                if not self.pole[x][y].fl_open:
                    row += '# '
                elif self.pole[x][y].mine:
                    row += '* '
                else:
                    row += f'{str(self.pole[x][y].around_mines)} '
            print(row)


if __name__ == '__main__':
    pole_game = GamePole(10, 12)
