
class Face:
    def __init__(self, name, squares):
        self.name = name
        self.squares = squares
        self.grid = [squares[i:i+3] for i in range(0, 9, 3)]

    def get_side(self):
        return self.side

    def get_grid(self):
        self.grid = [self.squares[i:i + 3] for i in range(0, 9, 3)]
        return self.grid

    def set_cell(self, index1, index2, value):
        self.grid[index1][index2] = value

    def rotate(self, clockwise=True):
        if clockwise:
            self.grid = [list(row) for row in zip(*self.grid[::-1])]
            self.squares = [item for row in self.grid for item in row]

        else:
            self.grid = [list(row) for row in zip(*self.grid)][::-1]
            self.squares = [item for row in self.grid for item in row]

