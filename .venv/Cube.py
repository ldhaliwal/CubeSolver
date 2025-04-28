from Face import Face

class Cube:
    def __init__(self, state):

        if len(state) != 54:
            print(len(state))
            raise ValueError("wrong input")

        # face_mapping = {
        #     'U': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],  # Up face
        #     'R': [(0, 2), (1, 2), (2, 2), (3, 5), (4, 5), (5, 5), (6, 2), (7, 2), (8, 2)],  # Right face
        #     'F': [(2, 0), (2, 1), (2, 2), (5, 3), (5, 4), (5, 5), (8, 0), (8, 1), (8, 2)],  # Front face
        #     'D': [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)],  # Down face
        #     'L': [(0, 0), (1, 0), (2, 0), (3, 3), (4, 3), (5, 3), (6, 0), (7, 0), (8, 0)],  # Left face
        #     'B': [(0, 2), (0, 1), (0, 0), (3, 0), (3, 1), (3, 2), (6, 2), (6, 1), (6, 0)],  # Back face
        # }

        face_names = ['U', 'R', 'F', 'D', 'L', 'B']
        self.faces = {}
        color_index = 0
        for face_name in face_names:
            squares = []
            for _ in range(9):
                squares.append(state[color_index])
                color_index += 1
            self.faces[face_name] = Face(face_name, squares)

    def get_face(self, face):
        return self.faces[face].get_grid()

    def get_affected_faces(self, face):
        return [self.faces[n] for n in self.neighbors[face]]

    def is_valid_cube(self) -> bool:
        from collections import Counter
        flat = [c for face in self.faces.values() for row in face for c in row]
        count = Counter(flat)
        return all(i == 9 for i in count.values()) and len(count) == 6

    def move(self, move_str):
        face_name = move_str[0]

        # 1 = clockwise, -1 = counterclockwise
        direction = 1
        turns = 1

        if len(move_str) > 1:
            if move_str[1] == "'":
                direction = -1
            elif move_str[1] == "2":
                turns = 2

        # Get the face
        face = self.faces.get(face_name)
        if face is None:
            raise ValueError(f"Invalid move")

        # Rotate the face
        for _ in range(turns):
            face.rotate(clockwise=(direction == 1))

        self.update_adjacent_faces(face_name, direction, turns)

    def update_adjacent_faces(self, face_name, direction, turns):
        if face_name == 'F':
            if direction == 1:
                for _ in range(turns):
                    u_squares = self.faces['U'].squares[6:9]
                    r_squares = self.faces['R'].squares[0:7:3]
                    d_squares = self.faces['D'].squares[0:3]
                    l_squares = self.faces['L'].squares[2:9:3]
                    self.faces['U'].squares[6:9] = l_squares
                    self.faces['R'].squares[0:7:3] = u_squares
                    self.faces['D'].squares[0:3] = r_squares
                    self.faces['L'].squares[2:9:3] = d_squares
            elif direction == -1:
                for _ in range(turns):
                    u_squares = self.faces['U'].squares[6:9]
                    r_squares = self.faces['R'].squares[0:7:3]
                    d_squares = self.faces['D'].squares[0:3]
                    l_squares = self.faces['L'].squares[2:9:3]
                    self.faces['U'].squares[6:9] = r_squares
                    self.faces['R'].squares[0:7:3] = d_squares
                    self.faces['D'].squares[0:3] = l_squares
                    self.faces['L'].squares[2:9:3] = u_squares
        elif face_name == 'B':
            if direction == 1:
                for _ in range(turns):
                    u_squares = self.faces['U'].squares[0:3]
                    r_squares = self.faces['R'].squares[2:9:3]
                    d_squares = self.faces['D'].squares[6:9]
                    l_squares = self.faces['L'].squares[0:7:3]
                    self.faces['U'].squares[0:3] = r_squares
                    self.faces['R'].squares[2:9:3] = d_squares
                    self.faces['D'].squares[6:9] = l_squares
                    self.faces['L'].squares[0:7:3] = u_squares
            elif direction == -1:
                for _ in range(turns):
                    u_squares = self.faces['U'].squares[0:3]
                    r_squares = self.faces['R'].squares[2:9:3]
                    d_squares = self.faces['D'].squares[6:9]
                    l_squares = self.faces['L'].squares[0:7:3]
                    self.faces['U'].squares[0:3] = l_squares
                    self.faces['L'].squares[0:7:3] = d_squares
                    self.faces['D'].squares[6:9] = r_squares
                    self.faces['R'].squares[2:9:3] = u_squares
        elif face_name == 'U':
            if direction == 1:
                for _ in range(turns):
                    f_squares = self.faces['F'].squares[0:3]
                    r_squares = self.faces['R'].squares[0:3]
                    b_squares = self.faces['B'].squares[0:3]
                    l_squares = self.faces['L'].squares[0:3]
                    self.faces['F'].squares[0:3] = r_squares
                    self.faces['R'].squares[0:3] = b_squares
                    self.faces['B'].squares[0:3] = l_squares
                    self.faces['L'].squares[0:3] = f_squares
            elif direction == -1:
                for _ in range(turns):
                    f_squares = self.faces['F'].squares[0:3]
                    r_squares = self.faces['R'].squares[0:3]
                    b_squares = self.faces['B'].squares[0:3]
                    l_squares = self.faces['L'].squares[0:3]
                    self.faces['F'].squares[0:3] = l_squares
                    self.faces['L'].squares[0:3] = b_squares
                    self.faces['B'].squares[0:3] = r_squares
                    self.faces['R'].squares[0:3] = f_squares
        elif face_name == 'D':
            if direction == 1:
                for _ in range(turns):
                    f_squares = self.faces['F'].squares[6:9]
                    r_squares = self.faces['R'].squares[6:9]
                    b_squares = self.faces['B'].squares[6:9]
                    l_squares = self.faces['L'].squares[6:9]
                    self.faces['F'].squares[6:9] = l_squares
                    self.faces['L'].squares[6:9] = b_squares
                    self.faces['B'].squares[6:9] = r_squares
                    self.faces['R'].squares[6:9] = f_squares
            elif direction == -1:
                for _ in range(turns):
                    f_squares = self.faces['F'].squares[6:9]
                    r_squares = self.faces['R'].squares[6:9]
                    b_squares = self.faces['B'].squares[6:9]
                    l_squares = self.faces['L'].squares[6:9]
                    self.faces['F'].squares[6:9] = r_squares
                    self.faces['R'].squares[6:9] = b_squares
                    self.faces['B'].squares[6:9] = l_squares
                    self.faces['L'].squares[6:9] = f_squares
        elif face_name == 'R':
            if direction == 1:
                for _ in range(turns):
                    u_squares = self.faces['U'].squares[2:9:3]
                    f_squares = self.faces['F'].squares[2:9:3]
                    d_squares = self.faces['D'].squares[2:9:3]
                    b_squares = self.faces['B'].squares[0:7:3]
                    self.faces['U'].squares[2:9:3] = f_squares
                    self.faces['F'].squares[2:9:3] = d_squares
                    self.faces['D'].squares[2:9:3] = b_squares
                    self.faces['B'].squares[0:7:3] = u_squares
            elif direction == -1:
                for _ in range(turns):
                    u_squares = self.faces['U'].squares[2:9:3]
                    f_squares = self.faces['F'].squares[2:9:3]
                    d_squares = self.faces['D'].squares[2:9:3]
                    b_squares = self.faces['B'].squares[0:7:3]
                    self.faces['U'].squares[2:9:3] = b_squares
                    self.faces['B'].squares[0:7:3] = d_squares
                    self.faces['D'].squares[2:9:3] = f_squares
                    self.faces['F'].squares[2:9:3] = u_squares
        elif face_name == 'L':
            if direction == 1:
                for _ in range(turns):
                    u_squares = self.faces['U'].squares[0:7:3]
                    f_squares = self.faces['F'].squares[0:7:3]
                    d_squares = self.faces['D'].squares[0:7:3]
                    b_squares = self.faces['B'].squares[2:9:3]
                    self.faces['U'].squares[0:7:3] = b_squares
                    self.faces['B'].squares[2:9:3] = d_squares
                    self.faces['D'].squares[0:7:3] = f_squares
                    self.faces['F'].squares[0:7:3] = u_squares
            elif direction == -1:
                for _ in range(turns):
                    u_squares = self.faces['U'].squares[0:7:3]
                    f_squares = self.faces['F'].squares[0:7:3]
                    d_squares = self.faces['D'].squares[0:7:3]
                    b_squares = self.faces['B'].squares[2:9:3]
                    self.faces['U'].squares[0:7:3] = f_squares
                    self.faces['F'].squares[0:7:3] = d_squares
                    self.faces['D'].squares[0:7:3] = b_squares
                    self.faces['B'].squares[2:9:3] = u_squares

