from Face import Face
from Cube import Cube
from collections import deque

class CubeSolver:



    def __init__(self):
        # Test Case
        self.cube_string = "WRWGWROBWYGWRYOBOYOYYYBYRBBGYRRGWGBGGWOBOWOORBGBGRORWY"
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

        self.corners = [
            ('U', 0, 'L', 'B'), ('U', 2, 'B', 'R'), ('U', 6, 'F', 'L'), ('U', 8, 'R', 'F'),
            ('D', 0, 'F', 'L'), ('D', 2, 'R', 'F'), ('D', 6, 'L', 'B'), ('D', 8, 'B', 'R')
        ]

        self.phase1_moves = ["U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2", "L", "L'", "L2", "R",
                             "R'", "R2"]
        self.phase2_moves = ["U", "U'", "U2", "D", "D'", "D2", "F2", "B2", "L2", "R2"]
        self.phase3_moves = ["U2", "D2", "F2", "B2", "L2", "R2"]
        self.phase4_moves = ["U2", "D2", "L2", "R2"]

        self.move_pruning = {
            # Avoid applying the same move twice, or doing inverse moves back-to-back
            'U': ['U', 'U2'], 'U2': ['U', 'U2', "U'"], 'U\'': ['U\'', 'U2'],
            'D': ['D', 'D2'], 'D2': ['D', 'D2', "D'"], 'D\'': ['D\'', 'D2'],
            'F': ['F', 'F2'], 'F2': ['F', 'F2', "F'"], 'F\'': ['F\'', 'F2'],
            'B': ['B', 'B2'], 'B2': ['B', 'B2', "B'"], 'B\'': ['B\'', 'B2'],
            'L': ['L', 'L2'], 'L2': ['L', 'L2', "L'"], 'L\'': ['L\'', 'L2'],
            'R': ['R', 'R2'], 'R2': ['R', 'R2', "R'"], 'R\'': ['R\'', 'R2']
        }

        # Pattern databases for heuristics
        self.edge_orientation_db = {}

        self.states_checked = 0

        self.solved_state = "WWWWWWWWWYYYYYYYYYBBBBBBBBBGGGGGGGGGOOOOOOOOORRRRRRRRR"

    def is_cube_solved(self):
        if self.get_string() == self.solved_state:
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

    def optimize_move_sequence(self, moves):
        if not moves:
            return []

        # Replace sequences like U U with U2
        i = 0
        optimized = []
        while i < len(moves):
            if i + 1 < len(moves) and moves[i] == moves[i + 1]:
                if moves[i][-1] == '2':  # If already U2 + U2, they cancel out
                    i += 2
                    continue
                elif moves[i][-1] == "'":  # U' + U' = U2
                    optimized.append(moves[i][0] + '2')
                    i += 2
                else:  # U + U = U2
                    optimized.append(moves[i] + '2')
                    i += 2
            elif (i + 1 < len(moves) and
                  ((moves[i] == moves[i + 1][0] and moves[i + 1][-1] == "'") or
                   (moves[i][-1] == "'" and moves[i][0] == moves[i + 1]))):
                # U + U' or U' + U cancel out
                i += 2
            else:
                optimized.append(moves[i])
                i += 1

        return optimized

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
        # phase2_moves = self.solve_phase2()
        # if phase2_moves is None:
        #     return None
        # self.execute_moves(phase2_moves)

        # Solves phase 3 (positioning corners)
        # phase3_moves = self.solve_phase3()
        # if phase3_moves is None:
        #     return None
        # self.execute_moves(phase3_moves)
        #
        # # Solves phase 4 (fully solving the cube)
        # phase4_moves = self.solve_phase4()
        # if phase4_moves is None:
        #     return None
        # self.execute_moves(phase4_moves)

        optimized_solution = self.optimize_move_sequence(self.solution)

        return optimized_solution


    # Written with help from Claude AI (specifically with the bit representation part)
    def get_state_phase1(self, cube):
        orientation = 0

        # Only need to check 12 edges (not all 24 positions since each edge has 2 colors)
        for i, (face, index, _) in enumerate(self.edges[:12]):

            # Get the square color
            color = cube.faces[face].squares[index]

            # Find the correct face of this color (where it should be in solved state)
            home_face = None
            for f in ['U', 'D', 'F', 'B', 'L', 'R']:
                if cube.faces[f].squares[4] == color:
                    home_face = f
                    break

            # Checks edge orientation based on Thistlethwaite rules
            is_flipped = False
            if home_face in ['U', 'D']:
                # U or D color should be on U or D face
                is_flipped = face not in ['U', 'D']
            elif home_face in ['F', 'B']:
                # F or B color should be on F or B face
                is_flipped = face not in ['F', 'B']

            # Set the bit if flipped
            if is_flipped:
                orientation |= (1 << i)

        return orientation


    def solve_phase1(self):
        initial_cube = Cube(self.get_string())
        initial_state = self.get_state_phase1(initial_cube)

        # Target state is that all edges correctly oriented (state method will return 0)
        target_state = 0

        if initial_state == target_state:
            return []

        # Use IDA DFS with a heuristic for efficiency
        def edge_orientation_heuristic(state):
            # Count number of flipped edges
            count = bin(state).count('1')

            # Return the minimum moves to fix flipped edges
            return (count + 3) // 4

        max_depth = edge_orientation_heuristic(initial_state)

        while max_depth <= 20:
            ## Find the shortest bath between the initial cube and its target state
            path = self.ida_search_phase1(initial_cube, target_state, max_depth)
            if path:
                return path
            max_depth += 1

        return None

    # Written with help from Claude AI (specifically with the heuristic)
    def ida_search_phase1(self, cube, target_state, max_depth):
        # Stack DFS implementation
        stack = [(cube, [], 0)]

        moves_to_try = self.phase1_moves.copy()

        while stack:
            current_cube, path, depth = stack.pop()
            self.states_checked += 1

            # Get current state
            current_state = self.get_state_phase1(current_cube)

            # If solution is found, return the path
            if current_state == target_state:
                return path

            # Reached depth limit
            if depth >= max_depth:
                continue

            # Get the heuristic based on remaining edge orientation distance
            h = bin(current_state).count('1')
            h = (h + 3) // 4  # Ceiling division

            # If current depth + heuristic > max_depth, prune the path
            if depth + h > max_depth:
                continue

            # Go through each move
            last_move = path[-1] if path else None

            for move in reversed(moves_to_try):
                # Get rid of redundant moves
                if last_move and move in self.move_pruning.get(last_move, []):
                    continue

                # Create a new cube and do the move
                next_cube = Cube(current_cube.get_state_string())
                next_cube.move(move)

                # Add to stack
                stack.append((next_cube, path + [move], depth + 1))

        return None

## Oldest

    # def get_state_phase1(self, cube: Cube):
    #     edge_orientation = ""
    #
    #     # Go through each edge location
    #     for face, index, _ in self.edges:
    #         edge_orientation += cube.faces[face].squares[index]
    #     # Sort to make comparing easier
    #     return tuple(sorted(edge_orientation))
    #
    # def solve_phase1(self):
    #     initial_state = self._get_state_phase1(self.cube)
    #
    #     # Solves the cube to the G1 subgroup (all edges correctly oriented).
    #     target_state = tuple(sorted("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"))[:12]
    #
    #     if current_state == target_state:
    #         return []
    #
    #     # Initialize a queue for BFS, starting with the current cube and an empty path of moves.
    #     queue = deque([(Cube(self.get_string()), [])])
    #     visited = {current_state}
    #     allowed_moves = self.move_set
    #
    #     while queue:
    #         # Get the current cube and the path of moves taken to reach it
    #         current_cube, path = queue.popleft()
    #         state = self.get_state_phase1(current_cube)
    #         # If this matches the target state, return the path
    #         if state == target_state:
    #             return path
    #
    #         # Keep iterating through the rest of the allowed moves
    #         for move in allowed_moves:
    #             next_cube = Cube(current_cube.get_state_string())
    #             next_cube.move(move)
    #             next_state = self.get_state_phase1(next_cube)
    #             if next_state not in visited:
    #                 # Mark the state at visited
    #                 visited.add(next_state)
    #                 # Create a new path by appending the current move to the existing path
    #                 new_path = path + [move]
    #                 # Add the next cube and its path to the queue
    #                 queue.append((next_cube, new_path))
    #     return None

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
        # Get the initial state
        initial_cube = Cube(self.get_string())
        initial_state = self.get_state_phase2(initial_cube)

        # Define the target state for G2.
        solved_cube = Cube("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
        target_state = self.get_state_phase2(solved_cube)

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
            state = self.get_state_phase2(current_cube)

            # If the current state matches the target state for G2, return the path.
            if state == target_state:
                return path

            # Iterate through the allowed moves
            for move in allowed_moves:
                # Create a new cube by applying the current move
                next_cube = Cube(current_cube.get_state_string())
                next_cube.move(move)
                # Get the simplified state of the next cube
                next_state = self.get_state_phase2(next_cube)
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
        initial_cube = Cube(self.get_string())
        initial_state = self.get_state_phase3(initial_cube)

        # Define the target state for G3.
        solved_cube = Cube("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
        target_state = self.get_state_phase3(solved_cube)

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

    def get_state_phase4(self, cube: Cube):
        """
        Returns the full cube state for Phase 4 (G4 - solved).

        Args:
            cube (Cube): The current state of the cube.

        Returns:
            tuple: A tuple representing the complete cube state.
        """
        # The most detailed state representation: the entire cube string.
        return tuple(cube.get_state_string())

    def solve_phase4(self):

        # Define the target state as the solved cube string.
        target_state = tuple("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
        # Get the initial cube
        initial_cube = Cube(self.get_string())
        # get initial state.
        initial_state = self.get_state_phase4(initial_cube)
        # If already solved, return empty list
        if initial_state == target_state:
            return []

        # Initialize queue for BFS.
        queue = deque([(initial_cube, [])])
        # Initialize visited set.
        visited = {initial_state}
        # All moves are allowed in the final phase.
        restricted_moves = self.move_set

        # BFS
        while queue:
            # Get current cube and path.
            current_cube, path = queue.popleft()
            # Get current state
            state = self.get_state_phase4(current_cube)

            # If solved, return path.
            if state == target_state:
                return path

            # Iterate through allowed moves
            for move in restricted_moves:
                # Create the next cube
                next_cube = Cube(current_cube.get_state_string())
                next_cube.move(move)
                # Get the next state
                next_state = self.get_state_phase4(next_cube)

                # If not visited
                if next_state not in visited:
                    # Mark visited
                    visited.add(next_state)
                    # Create new path
                    new_path = path + [move]
                    # Enqueue
                    queue.append((next_cube, new_path))
        # No solution
        return None

if __name__ == "__main__":
    solver = CubeSolver()
    print("Initial state:", solver.cube_string)
    print("face order: U D L R F B")

    solution = solver.solve()

    print(solution)

    # Test Case
    # moves = ["R", "L", "F'", "R2"]
    # for move in moves:
    #     print(f"Move {move}")
    #     solver.cube.move(move)
    #     print(f"After move {move}:", solver.get_grid())


    