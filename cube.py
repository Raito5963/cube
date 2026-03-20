import random

'''
    Rubik's Cube has 8 corners and 12 edges.
    To make it easier to manage the status of the parts, I number them.

    # Definition
    U face: center color is white
    F face: center color is green
    R face: center color is red
    B face: center color is blue
    L face: center color is orange
    D face: center color is yellow

    # corner numbers
    ## U face corners
    0: UBL
    1: UBR
    2: UFR
    3: UFL
    ## D face corners
    4: DBL
    5: DBR
    6: DFR
    7: DFL

    # edge numbers
    ## E line edges
    0: BR
    1: FR
    2: FL
    3: FB
    ## UD face edges
    4: UB
    5: UR
    6: UF
    7: UL
    8: DB
    9: DR
    10: DF
    11: DL
'''

# This is a class that represents the state of a Rubik's Cube.
class State:
    
    def __init__(self, cp, co, ep, eo):
        self.cp = cp # corner position [0,1,2,3,4,5,6,7]
        self.co = co # corner orientation [0 or 1 or 2] * 8
        self.ep = ep # edge position [0,1,2,3,4,5,6,7,8,9,10,11]
        self.eo = eo # edge orientation [0 or 1] * 12
    
    def apply_solved(self):
        self.cp = [0, 1, 2, 3, 4, 5, 6, 7], # cp
        self.co = [0, 0, 0, 0, 0, 0, 0, 0], # co
        self.ep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], #ep
        self.eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # eo

    def apply_move(self, move):
        # Apply move, and return new status.
        # "move" is a instance that represents move.
        # Subscript 'p' means permutation.
        new_cp = [self.cp[p] for p in move.cp]
        new_co = [(self.co[p] + move.co[i]) % 3 for i, p in enumerate(move.cp)]
        new_ep = [self.ep[p] for p in move.ep]
        new_eo = [(self.eo[p] + move.eo[i]) % 2 for i, p in enumerate(move.ep)]
        return State(new_cp, new_co, new_ep, new_eo)
    
    def scramble(self, length):
        # Scramble the cube the specified number of times.
        scr = []
        last_face = None
        state = self
        while len(scr) < length:
            face = random.choice(move_names)
            if last_face is None or face[0] != last_face:
                scr.append(face)
                state = state.apply_move(moves[face])
                last_face = face[0]
        self.cp, self.co, self.ep, self.eo = state.cp, state.co, state.ep, state.eo
        return " ".join(scr)
    
    def is_solved(self):
        return (
            self.co == [0] * 8 # all CO are correct
            and self.eo == [0] * 12 # all EO are correct
            and self.cp == list(range(8)) # all CP are correct
            and self.ep == list(range(12)) # all EP are correct
        )
    
    def is_movable(self, prev_move, next_move):
        # Determine if next move is able to move.
        # Don't move the same face continuously.
        # If move inverce face, fix the order to lexicographical order.
        if prev_move is None:
            return True # When it is first move, it can move any faces.
        prev_face = prev_move[0]
        if prev_face == next_move[0]: # When these are the same face,
                return False
        if inverce_face[prev_face] == next_move[0]: # When it is inverce face,
            return prev_face < next_move[0] # if the order is lexicographical, return True, else False.
        return True

# --- Setup ---

# Define 18 moves
moves = {
    'U': State(
        [3, 0, 1, 2, 4, 5, 6, 7], # cp
        [0, 0, 0, 0, 0, 0, 0, 0], # co: U move doesn't change orientation.
        [0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11], # ep
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # eo: U move doesn't change orientation.
    ),
    'D': State(
        [0, 1, 2, 3, 5, 6, 7, 4], # cp
        [0, 0, 0, 0, 0, 0, 0, 0], # co: D move doesn't change orientation.
        [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8], # ep
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # eo: D move doesn't change orientation.
    ),
    'R': State(
        [0, 2, 6, 3, 4, 1, 5, 7], # cp
        [0, 1, 2, 0, 0, 2, 1, 0], # co
        [0, 5, 9, 3, 4, 2, 6, 7, 8, 1, 10, 11], # ep
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # eo: R move doesn't change edge orientation.
    ),
    'L': State(
        [4, 1, 2, 0, 7, 5, 6, 3], # cp
        [2, 0, 0, 1, 1, 0, 0, 2], # co
        [11, 1, 2, 7, 4, 5, 6, 0, 8, 9, 10, 3], # ep
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # eo: L move doesn't change edge orientation.
    ),
    'F': State(
        [0, 1, 3, 7, 4, 5, 2, 6], # cp
        [0, 0, 1, 2, 0, 0, 2, 1], # co
        [0, 1, 6, 10, 4, 5, 3, 7, 8, 9, 2, 11], # ep
        [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0], # eo
    ),
    'B': State(
        [1, 5, 2, 3, 0, 4, 6, 7], # cp
        [1, 2, 0, 0, 2, 1, 0, 0], # co
        [4, 8, 2, 3, 1, 5, 6, 7, 0, 9, 10, 11], # ep
        [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], # eo
    ),
}

inverce_face = {
    'U': 'D',
    'D': 'U',
    'R': 'L',
    'L': 'R',
    'F': 'B',
    'B': 'F',
}

# This is an array that store all moves including double moves and prime moves.
move_names = []
faces = list(moves.keys()) # keys are 'U', 'D', 'R', 'L', 'F', 'B,
for face in faces:
    move_names += [face, face + '2', face + '\'']
    # double moves
    moves[face + '2'] = moves[face].apply_move(moves[face])
    # prime moves are equivalent to turning face three times.
    moves[face + '\''] = moves[face].apply_move(moves[face]).apply_move(moves[face])
# print(move_names) # for debug