from Face import Face
from Cube import Cube

class CubeSolver:

    def __init__(self):
        self.cube_string = "WWWWWWWWWGGGGGGGGGOOOOOOOOOYYYYYYYYYBBBBBBBBBRRRRRRRRR"

        self.cube = Cube(self.cube_string)


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


if __name__ == "__main__":
    solver = CubeSolver()
    print("Initial state:", solver.cube_string)

    moves = ["R", "U'", "F2"]
    for move in moves:
        print(f"Move {move}:")
        solver.cube.move(move)
        print(f"After move {move}:", solver.get_string())


    