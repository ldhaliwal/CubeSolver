from Face import Face
from Cube import Cube

class CubeSolver:

    def __init__(self):
        # Test Case
        self.cube_string = "BWWWWWRWOGBRYGRGOWYOYROBRGRBOWYYYGBBORGGBBWGYBGYYRROOO"
        self.cube = Cube(self.cube_string)
        self.solution = []
        self.move_set = ["U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2", "L", "L'", "L2", "R", "R'",
                         "R2"]

    def is_cube_solved(self):
        if self.get_string() == "WWWWWWWWWGGGGGGGGGOOOOOOOOOYYYYYYYYYBBBBBBBBBRRRRRRRRR":
            return True
        return False

    def get_string(self) -> str:
        face_order = ['U', 'D', 'L', 'R', 'F', 'B']
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

        phase1_moves = self.solve_phase1()
        if phase1_moves is None:
            return None
        self.execute_moves(phase1_moves)

        phase2_moves = self.solve_phase2()
        if phase2_moves is None:
            return None
        self.execute_moves(phase2_moves)

        phase3_moves = self.solve_phase3()
        if phase3_moves is None:
            return None
        self.execute_moves(phase3_moves)

        phase4_moves = self.solve_phase4()
        if phase4_moves is None:
            return None
        self.execute_moves(phase4_moves)

        return self.solution

    def get_state_phase1(self, cube: Cube):
        edge_orientation = ""
        edges = [
            ('U', 1, 'B'), ('U', 3, 'L'), ('U', 5, 'R'), ('U', 7, 'F'),
            ('F', 1, 'U'), ('F', 3, 'L'), ('F', 5, 'R'), ('F', 7, 'D'),
            ('R', 1, 'U'), ('R', 3, 'F'), ('R', 5, 'B'), ('R', 7, 'D'),
            ('B', 1, 'U'), ('B', 3, 'R'), ('B', 5, 'L'), ('B', 7, 'D'),
            ('L', 1, 'U'), ('L', 3, 'B'), ('L', 5, 'F'), ('L', 7, 'D'),
            ('D', 1, 'F'), ('D', 3, 'R'), ('D', 5, 'B'), ('D', 7, 'L')
        ]
        for face, index, _ in edges:
            edge_orientation += cube.faces[face].squares[index]
        # Sort to handle different permutations
        return tuple(sorted(edge_orientation))

    def solve_phase1(self):
        # Solves the cube to the G1 subgroup (all edges correctly oriented).
        target_state = tuple(sorted("UUUUUUUUUDDDDDDDDDRRRRRRRRRLLLLLLLLLFFFFFFFFFBBBBBBBBB"))[:12]
        current_state = self.get_state_phase1(self.cube)
        if all(c in 'UDLRFB' for c in current_state):
            return []

        queue = deque([(Cube(self.get_string()), [])])
        visited = {current_state}
        allowed_moves = self.move_set

        while queue:
            current_cube, path = queue.popleft()
            state = self.get_state_phase1(current_cube)
            if all(c in 'UDLRFB' for c in state):
                return path

            for move in allowed_moves:
                next_cube = Cube(current_cube.get_state_string())
                next_cube.move(move)
                next_state = self.get_state_phase1(next_cube)
                if next_state not in visited:
                    visited.add(next_state)
                    new_path = path + [move]
                    queue.append((next_cube, new_path))
        return None


if __name__ == "__main__":
    solver = CubeSolver()
    print("Initial state:", solver.cube_string)
    print("face order: U D L R F B")

    solver.solve_white_cross()
    print("Final state:", solver.cube_string)

    # Test Case
    # moves = ["R", "L", "F'", "R2"]
    # for move in moves:
    #     print(f"Move {move}")
    #     solver.cube.move(move)
    #     print(f"After move {move}:", solver.get_grid())


    