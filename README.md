**Overview**

This program is intended to help the user solve a Rubik’s Cube using Thistlethwaite’s algorithm. Thistlethwaite’s algorithm
has four phases, each of which solve a different aspect of the cube, using a different set of moves.
The program represents the cube using both the Cube and Face classes, and does the actual solving through the CubeSolver class. 
The program begins by taking in the starting state of the cube from the user, then solving it through the program, then
returns the set of moves to solve the cube to the user.

**Time Complexity**

Getting the cube string: time O(1)
* always 6 faces with 9 squares

Rotating a face: time O(1)
* fixed number of square swaps

Phase 1: time O(b^d)
* get_state_phase1: O(1)
* ida_search_phase1(): O(b^d)
  * b = branching factor 
  * d = solution depth (worst case max depth)

Phase 2: time O()

Phase 3: time O()

Phase 4: time O()
