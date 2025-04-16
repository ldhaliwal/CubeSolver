class Cube:
    def __init__(self):
        self.neighbors = {
            'U': ['L', 'B', 'R', 'F'],
            'D': ['L', 'B', 'R', 'F'],
            'F': ['L', 'U', 'R', 'D'],
            'B': ['L', 'U', 'R', 'D'],
            'L': ['U', 'F', 'D', 'B'],
            'R': ['U', 'F', 'D', 'B']
        }

        # Initialize a blank cube: each face is a 3x3 list filled with '-'
        self.faces = {
            'U': Face('U', neighbors),
            'D': Face('D', neighbors),
            'F': Face('F', neighbors),
            'B': Face('B', neighbors),
            'L': Face('L', neighbors),
            'R': Face('R', neighbors)
        }

        self.affected_neighbors = {
            'U': {faces['L'][0], faces['B'][0], faces['R'][0], faces['F'][0]},
            'D': {faces['L'][2], faces['B'][2], faces['R'][2], faces['F'][2]},
            'F': {faces['L'][0][2]+faces['L'][1][2]+faces['L'][2][2], faces['U'][2], faces['R'][0][0]+faces['R'][1][0]+faces['R'][2][0], faces['D'][0]},
            'B': {faces['L'][0][0]+faces['L'][1][0]+faces['L'][2][0], faces['U'][0], faces['R'][0][2]+faces['R'][1][2]+faces['R'][2][2], faces['D'][2]},
            'L': {faces['U'][0][0]+faces['U'][1][0]+faces['U'][2][0],
                  faces['F'][0][0]+faces['F'][1][0]+faces['F'][2][0],
                  faces['D'][0][0]+faces['D'][1][0]+faces['D'][2][0],
                  faces['B'][0][2]+faces['B'][1][2]+faces['B'][2][2]},
            'R': {faces['U'][0][2] + faces['U'][1][2] + faces['U'][2][2],
                  faces['F'][0][2] + faces['F'][1][2] + faces['F'][2][2],
                  faces['D'][0][2] + faces['D'][1][2] + faces['D'][2][2],
                  faces['B'][0][0] + faces['B'][1][0] + faces['B'][2][0]}
        }

    def get_face(self, face):
        return self.faces[face]

    def get_affected_faces(self, face):
        return [self.faces[n] for n in self.neighbors[face]]

    def is_valid_cube(self) -> bool:
        from collections import Counter
        flat = [c for face in self.faces.values() for row in face for c in row]
        count = Counter(flat)
        return all(i == 9 for i in count.values()) and len(count) == 6