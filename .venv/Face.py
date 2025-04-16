import Storage

class Face:
    def __init__(self, name, squares):
        self.name = name
        self.squares = squares
        self.grid = [squares[i:i+3] for i in range(0, 9, 3)]
        self.neighbors = neighbors[name]

    def get_side(self):
        return self.side

    def rotate(self, clockwise=True):
        if clockwise:
            self.grid = [list(row) for row in zip(*self.grid[::-1])]
            self.squares = [item for row in self.grid for item in row]

        else:
            self.grid = [list(row) for row in zip(*self.grid)][::-1]
            self.squares = [item for row in self.grid for item in row]


