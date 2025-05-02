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
        self.edges = [
        ('U', 1, 'B'), ('U', 3, 'L'), ('U', 5, 'R'), ('U', 7, 'F'),
        ('F', 1, 'U'), ('F', 3, 'L'), ('F', 5, 'R'), ('F', 7, 'D'),
        ('R', 1, 'U'), ('R', 3, 'F'), ('R', 5, 'B'), ('R', 7, 'D'),
        ('B', 1, 'U'), ('B', 3, 'R'), ('B', 5, 'L'), ('B', 7, 'D'),
        ('L', 1, 'U'), ('L', 3, 'B'), ('L', 5, 'F'), ('L', 7, 'D'),
        ('D', 1, 'F'), ('D', 3, 'R'), ('D', 5, 'B'), ('D', 7, 'L')
        ]

    def is_cube_solved(self):
        if self.get_string() == "WWWWWWWWWYYYYYYYYYBBBBBBBBBGGGGGGGGGOOOOOOOOORRRRRRRRR":
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
            # Adds the moves to the solution
            self.solution.append(move)

    def solve(self):
        # Checks if the cube is solved
        if self.is_cube_solved():
            return []

        # Solves phase 1 (orienting edges)
        phase1_moves = self.solve_phase1()
        if phase1_moves is None:
            return None
        self.execute_moves(phase1_moves)

        # Solves phase 2 (orienting corners)
        phase2_moves = self.solve_phase2()
        if phase2_moves is None:
            return None
        self.execute_moves(phase2_moves)

        # Solves phase 3 (positioning corners)
        phase3_moves = self.solve_phase3()
        if phase3_moves is None:
            return None
        self.execute_moves(phase3_moves)

        # Solves phase 4 (fully solving the cube)
        phase4_moves = self.solve_phase4()
        if phase4_moves is None:
            return None
        self.execute_moves(phase4_moves)

        return self.solution

    def get_state_phase1(self, cube: Cube):
        edge_orientation = ""

        # Go through each edge location
        for face, index, _ in self.edges:
            edge_orientation += cube.faces[face].squares[index]
        # Sort to make comparing easier
        return tuple(sorted(edge_orientation))

    def solve_phase1(self):
        # Solves the cube to the G1 subgroup (all edges correctly oriented).
        solved_cube = Cube("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
        target_state = self._get_state_phase1(solved_cube)

        current_state = self.get_state_phase1(self.cube)

        if current_state == target_state:
            return []

        # Initialize a queue for BFS, starting with the current cube and an empty path of moves.
        queue = deque([(Cube(self.get_string()), [])])
        visited = {current_state}
        allowed_moves = self.move_set

        while queue:
            # Get the current cube and the path of moves taken to reach it
            current_cube, path = queue.popleft()
            state = self.get_state_phase1(current_cube)
            # If this matches the target state, return the path
            if state == target_state:
                return path

            # Keep iterating through the rest of the allowed moves
            for move in allowed_moves:
                next_cube = Cube(current_cube.get_state_string())
                next_cube.move(move)
                next_state = self.get_state_phase1(next_cube)
                if next_state not in visited:
                    # Mark the state at visited
                    visited.add(next_state)
                    # Create a new path by appending the current move to the existing path
                    new_path = path + [move]
                    # Add the next cube and its path to the queue
                    queue.append((next_cube, new_path))
        return None

    def get_state_phase2(self, cube: Cube):
        corner_orientation = ""
        # List of face and index for corner stickers.
        corners = [
            ('U', 0, 'L', 'B'), ('U', 2, 'B', 'R'), ('U', 6, 'F', 'L'), ('U', 8, 'R', 'F'),
            ('D', 0, 'F', 'L'), ('D', 2, 'R', 'F'), ('D', 6, 'L', 'B'), ('D', 8, 'B', 'R')
        ]
        # Get the color of one square from each corner.
        for face, index, _, _ in corners:
            corner_orientation += cube.faces[face].squares[index]

        edge_positions = ""

        for face, index, _ in self.edges:
            edge_positions += face + str(index)
        # Return a tuple containing the sorted corner orientations and sorted edge positions.
        return tuple(sorted(corner_orientation) + sorted(edge_positions))

    def _solve_phase2(self):
        """
        Solves the cube from the G1 subgroup to the G2 subgroup using BFS.
        The G2 subgroup has all edges correctly positioned and all corners correctly oriented.

        Returns:
            list: A list of moves to reach the G2 state, or None if no solution is found.
        """
        # Get the initial state
        initial_cube = Cube(self.get_string())
        initial_state = self._get_state_phase2(initial_cube)

        # Define the target state for G2.
        solved_cube = Cube("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
        target_state = self._get_state_phase2(solved_cube)

        # If the initial state already matches the target state, return an empty list of moves.
        if initial_state == target_state:
            return []

        # Initialize the BFS queue with the initial cube and an empty path.
        queue = deque([(initial_cube, [])])
        # Initialize a set to keep track of visited states.
        visited = {initial_state}
        # Define the restricted set of moves allowed in this phase (often half-turns of faces).
        allowed_moves = ["U", "U'", "U2", "D", "D'", "D2", "F2", "B2", "L2", "R2"]

        # Begin the BFS loop.
        while queue:
            # Dequeue the current cube and its move path.
            current_cube, path = queue.popleft()
            # Get the simplified state of the current cube for phase 2 comparison.
            state = self._get_state_phase2(current_cube)

            # If the current state matches the target state for G2, return the path.
            if state == target_state:
                return path

            # Iterate through the allowed moves
            for move in allowed_moves:
                # Create a new cube by applying the current move
                next_cube = Cube(current_cube.get_state_string())
                next_cube.move(move)
                # Get the simplified state of the next cube
                next_state = self._get_state_phase2(next_cube)
                # If this state has not been visited
                if next_state not in visited:
                    # Mark the next state as visited
                    visited.add(next_state)
                    # Create a new path by adding the current move
                    new_path = path + [move]
                    # Add the next cube and its path to the queue
                    queue.append((next_cube, new_path))
        # If the queue is empty and the target state is not reached return None
        return None

    def get_state_phase3(self, cube: Cube):
        # String to store the position of each corner piece.
        corner_positions = ""
        # List of face and index for corner stickers.
        corners = [
            ('U', 0), ('U', 2), ('U', 6), ('U', 8),
            ('D', 0), ('D', 2), ('D', 6), ('D', 8)
        ]
        # Create an identifier for each corner based on its face and index.
        for face, index in corners:
            corner_positions += face + str(index)

        # String to store a simplified representation of the edge orientations (already done in Phase 1, but we might track parity).
        edge_orientation = ""

        # Create an identifier for each edge.
        for face, index in self.edges:
            edge_orientation += face + str(index)

        # Return a tuple of sorted corner positions and edge orientations.
        return tuple(sorted(corner_positions) + sorted(edge_orientation))

    def solve_phase3(self):
        """
        Solves the cube from the G2 subgroup to the G3 subgroup using BFS.
        In the G3 subgroup, all corners are correctly positioned.

        Returns:
            list: A list of moves to reach the G3 state, or None if no solution is found.
        """
        initial_cube = Cube(self.get_string())
        initial_state = self._get_state_phase3(initial_cube)

        # Define the target state for G3.
        solved_cube = Cube("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
        target_state = self._get_state_phase3(solved_cube)

        # If the initial state matches the target, return empty list.
        if initial_state == target_state:
            return []

        # Initialize BFS queue.
        queue = deque([(initial_cube, [])])
        # Initialize visited set.
        visited = {initial_state}
        # Define allowed moves for phase 3.
        allowed_moves = ["U2", "D2", "F2", "B2", "L2", "R2"]

        # BFS loop.
        while queue:
            # Dequeue cube and path.
            current_cube, path = queue.popleft()
            # get state
            state = self.get_state_phase3(current_cube)

            # If target state, return path.
            if state == target_state:
                return path

            # Iterate through allowed moves.
            for move in allowed_moves:
                # Create next cube.
                next_cube = Cube(current_cube.get_state_string())
                next_cube.move(move)
                # Get next state
                next_state = self.get_state_phase3(next_cube)

                # If not visited.
                if next_state not in visited:
                    # Mark visited.
                    visited.add(next_state)
                    # create new path
                    new_path = path + [move]
                    # Enqueue.
                    queue.append((next_cube, new_path))
        # No solution.
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


    