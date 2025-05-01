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

    def is_cube_solved(self):
        if self.get_string() == "WWWWWWWWWGGGGGGGGGOOOOOOOOOYYYYYYYYYBBBBBBBBBRRRRRRRRR":
            return True
        return False

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
        if self.is_cube_solved():
            return []

        phase1_moves = self._solve_phase1()
        if phase1_moves is None:
            return None
        self.execute_moves(phase1_moves)

        phase2_moves = self._solve_phase2()
        if phase2_moves is None:
            return None
        self.execute_moves(phase2_moves)

        phase3_moves = self._solve_phase3()
        if phase3_moves is None:
            return None
        self.execute_moves(phase3_moves)

        phase4_moves = self._solve_phase4()
        if phase4_moves is None:
            return None
        self.execute_moves(phase4_moves)

        return self.solution



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


    