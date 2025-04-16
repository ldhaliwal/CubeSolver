import Storage

class Face:
    def __init__(self, side, neighbors):
        self.side = side
        self.grid = [[color for _ in range(3)] for _ in range(3)]

        self.neighbors = neighbors[side]


    def get_side(self):
        return self.side

    def rotate(self, clockwise=True):
        if clockwise:
            self.faces[face] = [list(row) for row in zip(*self.faces[face][::-1])]

            affected_neighbors = super().get_affected_neighbors()

            for neighbor in affected_neighbors:




        else:
            self.faces[face] = [list(row) for row in zip(*self.faces[face])][::-1]


