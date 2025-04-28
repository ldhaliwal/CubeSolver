from Face import Face
from Cube import Cube

class CubeSolver:

    def __init__(self):
        # Test Case
        self.cube_string = "BWWWWWRWOGBRYGRGOWYOYROBRGRBOWYYYGBBORGGBBWGYBGYYRROOO"
        self.cube = Cube(self.cube_string)
        self.solution = []


    # Sets up the cube based on the given string
    def set_cube(self, cube_string: str):
        if is_valid_cube(cube_string):
            for i, face in enumerate(['U', 'R', 'F', 'D', 'L', 'B']):
                for j, color in enumerate(['U', 'R', 'F']):
                    self.cube.faces[face][i // 9][j] = color
                for j, color in enumerate(['D', 'L', 'B']):
                    self.cube.faces[face][(i + 27) // 9][j] = color
                for j, color in enumerate(cube_string[i * 3:(i + 1) * 3]):
                    self.cube.faces[face][i % 9][j] = color

    def get_string(self) -> str:
        face_order = ['U', 'R', 'F', 'D', 'L', 'B']
        string = ""
        for face in face_order:
            for i in range(3):
                for j in range(3):
                    string += self.cube.get_face(face)[i][j]

        return string

    def get_grid(self):
        string = self.get_string()

        grid = [list(string[i * 9:(i + 1) * 9]) for i in range(6)]
        grid = [[face[i:i + 3] for i in range(0, 9, 3)] for face in grid]
        return grid

    def execute_moves(self, moves):
        for move in moves:
            self.cube.move(move)
            self.solution.append(move)

    def solve(self):
        self.solve_white_cross()
        self.solve_white_corners()
        self.solve_second_layer()
        self.solve_yellow_cross()
        self.solve_yellow_edges()
        self.solve_yellow_corners()
        self.orient_yellow_corners()
        return self.solution

    def solve_white_cross(self):
        white_edges = [
            ('U', 1, 'B'), ('U', 3, 'L'), ('U', 5, 'R'), ('U', 7, 'F'),
            ('F', 1, 'U'), ('F', 3, 'L'), ('F', 5, 'R'), ('F', 7, 'D'),
            ('R', 1, 'U'), ('R', 3, 'F'), ('R', 5, 'B'), ('R', 7, 'D'),
            ('B', 1, 'U'), ('B', 3, 'R'), ('B', 5, 'L'), ('B', 7, 'D'),
            ('L', 1, 'U'), ('L', 3, 'B'), ('L', 5, 'F'), ('L', 7, 'D'),
            ('D', 1, 'F'), ('D', 3, 'R'), ('D', 5, 'B'), ('D', 7, 'L')
        ]



    def solve_white_corners(self):
        pass

    def solve_second_layer(self):
        pass

    def solve_yellow_cross(self):
        pass

    def solve_yellow_edges(self):
        pass

    def solve_yellow_corners(self):
        pass

    def orient_yellow_corners(self):
        pass


if __name__ == "__main__":
    solver = CubeSolver()
    print("Initial state:", solver.cube_string)
    print("face order: U R F D L B")

    solver.solve_white_cross()
    print("Final state:", solver.cube_string)

    # Test Case
    # moves = ["R", "L", "F'", "R2"]
    # for move in moves:
    #     print(f"Move {move}")
    #     solver.cube.move(move)
    #     print(f"After move {move}:", solver.get_grid())


    