import kociemba

class CubeSolver:

    def __init__(self):
        self.cube = new Cube()

        solution =



    ## Sets up the cube based on a given string
    def set_cube(self, cube_string: str):
        if is_valid_cube(cube_string):
            for i, face in enumerate(['U', 'R', 'F', 'D', 'L', 'B']):
                for j, color in enumerate(['U', 'R', 'F']):
                    self.faces[face][i // 9][j] = color
                for j, color in enumerate(['D', 'L', 'B']):
                    self.faces[face][(i + 27) // 9][j] = color
                for j, color in enumerate(cube_string[i * 3:(i + 1) * 3]):
                    self.faces[face][i % 9][j] = color

    def get_string(self) -> str:
        face_order = ['U', 'R', 'F', 'D', 'L', 'B']
        return ''.join(self.faces[face][i][j] for face in face_order for i in range(3) for j in range(3))



    def rotate_face(self, face, clockwise=True):
        face.rotate(clockwise)
    ## need to change the other adjancent faces accordingly

    def solve(self):

