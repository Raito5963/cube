import time
from cube import *

NUM_CORNERS = 8
NUM_EDGES = 12

NUM_CO = 2187  # 3 ** 7
NUM_EO = 2048  # 2 ** 11
NUM_E_COMBINATIONS = 495  # 12C4

NUM_CP = 40320  # 8!
# NUM_EP = 479001600  # 12! # usless
NUM_UD_EP = 40320  # 8!
NUM_E_EP = 24  # 4!

# --- phase1 indexing ---
# co > index
def co_to_index(co):
    index = 0
    for co_i in co[:-1]:
        index *= 3
        index += co_i
    return index

# index > co
def index_to_co(index):
    co = [0] * 8
    sum_co = 0
    for i in range(6, -1, -1):
        co[i] = index % 3
        index //= 3
        sum_co += co[i]
    co[-1] = (3 - sum_co % 3) % 3
    return co

# eo > index
def eo_to_index(eo):
    index = 0
    for eo_i in eo[:-1]:
        index *= 2
        index += eo_i
    return index

# index > eo
def index_to_eo(index):
    eo = [0] * 12
    sum_eo = 0
    for i in range(10, -1, -1):
        eo[i] = index % 2
        index //= 2
        sum_eo += eo[i]
    eo[-1] = (2 - sum_eo % 2) % 2
    return eo

# Calculate nCr
def calc_combination(n, r):
    ret = 1
    for i in range(r):
        ret *= n - i
    for i in range(r):
        ret //= r - i
    return ret

# e combination > index
# E line edge parts 
# Calculate the combinations of E line edge parts that fit into the E line.
def e_combination_to_index(comb):
    index = 0
    r = 4
    for i in range(12 - 1, -1, -1):
        if comb[i]:
            index += calc_combination(i, r)
            r -= 1
    return index

# combination > index
def index_to_e_combination(index):
    combination = [0] * 12
    r = 4
    for i in range(12 - 1, -1, -1):
        if index >= calc_combination(i, r):
            combination[i] = 1
            index -= calc_combination(i, r)
            r -= 1
    return combination

# --- phase2 indexing ---
# cp > index
def cp_to_index(cp):
    index = 0
    for i, cp_i in enumerate(cp):
        index *= 8 - i
        for j in range(i + 1, 8):
            if cp[i] > cp[j]:
                index += 1
    return index

# index > cp
def index_to_cp(index):
    cp = [0] * 8
    for i in range(6, -1, -1):
        cp[i] = index % (8 - i)
        index //= 8 - i
        for j in range(i + 1, 8):
            if cp[j] >= cp[i]:
                cp[j] += 1
    return cp

# U,D face ep > index
def ud_ep_to_index(ep):
    index = 0
    for i, ep_i in enumerate(ep):
        index *= 8 - i
        for j in range(i + 1, 8):
            if ep[i] > ep[j]:
                index += 1
    return index

# index > U,D face ep
def index_to_ud_ep(index):
    ep = [0] * 8
    for i in range(6, -1, -1):
        ep[i] = index % (8 - i)
        index //= 8 - i
        for j in range(i + 1, 8):
            if ep[j] >= ep[i]:
                ep[j] += 1
    return ep

# E line ep > index
def e_ep_to_index(eep):
    index = 0
    for i, eep_i in enumerate(eep):
        index *= 4 - i
        for j in range(i + 1, 4):
            if eep[i] > eep[j]:
                index += 1
    return index

# index > E line ep
def index_to_e_ep(index):
    eep = [0] * 4
    for i in range(4 - 2, -1, -1):
        eep[i] = index % (4 - i)
        index //= 4 - i
        for j in range(i + 1, 4):
            if eep[j] >= eep[i]:
                eep[j] += 1
    return eep

# Transition tables are almost the same code, 
# but variable name and place of storing are different.
# The operation of these functions is explained in the comments below.
'''
print("computing ANY_table")
start = time.time()
# Create a two-dimensional array of the number of moves multiplied by ANY.
ANY_table = [[0] * len(move_names or move_names_ph2) for _ in range(NUM_ANY)]
for i in range(NUM_ANY): # Repeat ANY times
    state = State(
        # The value returned from the index is placed in the State that is related to ANY. 
        # Empty the values for all other states.
        index_to_ANY(i), # cp
        index_to_ANY(i), # co
        index_to_ANY(i), # ep
        index_to_ANY(i), # eo
    )
    for i_move, move_name in enumerate(move_names):
        # For each move, compute the next state from the current indexed state.
        new_state = state.apply_move(moves[move_name])
        # Store the indexed result in the transition table.
        ANY_table[i][i_move] = ANY_to_index(new_state.ANY)
print(f"Finished! ({time.time() - start:2.f} sec.)")
'''

# --- phase1 transition tables ---
# co transition table
print("Computing co_move_table")
start = time.time()
co_move_table = [[0] * len(move_names) for _ in range(NUM_CO)]
for i in range(NUM_CO):
    state = State(
        [0] * 8,
        index_to_co(i),
        [0] * 12,
        [0] * 12
    )
    for i_move, move_name in enumerate(move_names):
        new_state = state.apply_move(moves[move_name])
        co_move_table[i][i_move] = co_to_index(new_state.co)
print(f"Finished! ({time.time() - start:.5f} sec.)")

# eo transition table
print("Computing eo_move_table")
start = time.time()
eo_move_table = [[0] * len(move_names) for _ in range(NUM_EO)]
for i in range(NUM_EO):
    state = State(
        [0] * 8,
        [0] * 8,
        [0] * 12,
        index_to_eo(i)
    )
    for i_move, move_name in enumerate(move_names):
        new_state = state.apply_move(moves[move_name])
        eo_move_table[i][i_move] = eo_to_index(new_state.eo)
print(f"Finished! ({time.time() - start:.5f} sec.)")

# E line edge combination transition table
print("Computing e_combination_table")
start = time.time()
e_combination_table = [[0] * len(move_names) for _ in range(NUM_E_COMBINATIONS)]
for i in range(NUM_E_COMBINATIONS):
    state = State(
        [0] * 8,
        [0] * 8,
        index_to_e_combination(i),
        [0] * 12,
    )
    for i_move, move_name in enumerate(move_names):
        new_state = state.apply_move(moves[move_name])
        e_combination_table[i][i_move] = e_combination_to_index(new_state.ep)
print(f"Finished! ({time.time() - start:.5f} sec.)")

# --- phase2 transition tables ---
# In phase 2, It is limited some moves
move_names_ph2 = ["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]

# cp transition table
print("Computing cp_move_table")
cp_move_table = [[0] * len(move_names_ph2) for _ in range(NUM_CP)]
start = time.time()
for i in range(NUM_CP):
    state = State(
        index_to_cp(i),
        [0] * 8,
        [0] * 12,
        [0] * 12
    )
    for i_move, move_name in enumerate(move_names_ph2):
        new_state = state.apply_move(moves[move_name])
        cp_move_table[i][i_move] = cp_to_index(new_state.cp)
print(f"Finished! ({time.time() - start:.5f} sec.)")

# U,D face ep transition table
print("Computing ud_ep_move_table")
ud_ep_move_table = [[0] * len(move_names_ph2) for _ in range(NUM_UD_EP)]
start = time.time()
for i in range(NUM_UD_EP):
    state = State(
        [0] * 8,
        [0] * 8,
        [0] * 4 + index_to_ud_ep(i),
        [0] * 12
    )
    for i_move, move_name in enumerate(move_names_ph2):
        new_state = state.apply_move(moves[move_name])
        ud_ep_move_table[i][i_move] = ud_ep_to_index(new_state.ep[4:])
print(f"Finished! ({time.time() - start:.5f} sec.)")

# E line ep transition table
print("Computing e_edge_permutation_move_table")
e_ep_move_table = [[0] * len(move_names_ph2) for _ in range(NUM_E_EP)]
start = time.time()
for i in range(NUM_E_EP):
    state = State(
        [0] * 8,
        [0] * 8,
        index_to_e_ep(i) + [0] * 8,
        [0] * 12,
    )
    for i_move, move_name in enumerate(move_names_ph2):
        new_state = state.apply_move(moves[move_name])
        e_ep_move_table[i][i_move] = e_ep_to_index(new_state.ep[:4])
print(f"Finished! ({time.time() - start:.5f} sec.)")

# Prune tables are almost the same code, 
# but variable name and place of storing are different.
# The operation of these functions is explained in the comments below.
'''
# Ignore ANY_A and consider ANY_B and ANY_C
print("Computing B_C_prune_table")
start = time.time()
# Initialize all entries as unvisited (-1).
B_C_prune_table = [[-1] * NUM_C for _ in range(NUM_B)]
# Set the solved pair (0, 0) to distance 0.
B_C_prune_table[0][0] = 0
distance = 0
num_filled = 1
# Expand states in BFS layers so each newly reached state gets the minimum distance.
while num_filled != NUM_B * NUM_C: # Stop when every (B, C) pair has been assigned a distance.
    print(f"distance = {distance}")
    print(f"num_filled = {num_filled}")
    # Iterate through all possible state pairs of B and C.
    for i_B in range(NUM_B):
        for i_C in range(NUM_C):
            # Currently only unfold the layer with distance "distance".
            if B_C_prune_table[i_B][i_C] == distance:
                for i_move in range(len(move_names)):
                    # Both of B and C enduring with the same move i_move to create the next state.
                    next_B = B_move_table[i_B][i_move]
                    next_C = C_move_table[i_C][i_move]
                    # By updating only the unvisited cells, 
                    # the first distance reached can be fixed as the shortest distance.
                    if B_C_prune_table[next_B][next_C] == -1:
                        B_C_prune_table[next_B][next_C] = distance + 1
                        num_filled += 1 # Completed BFS.
    distance += 1
print(f"Finished! ({time.time() - start:.5f} sec.)") 
'''

# --- phase1 prune tables ---
# Ignore EO and consider CO and E line
print("Computing co_eec_prune_table")
start = time.time()
co_eec_prune_table = [[-1] * NUM_E_COMBINATIONS for _ in range(NUM_CO)]
co_eec_prune_table[0][0] = 0
distance = 0
num_filled = 1
while num_filled != NUM_CO * NUM_E_COMBINATIONS:
    print(f"distance = {distance}")
    print(f"num_filled = {num_filled}")
    for i_co in range(NUM_CO):
        for i_eec in range(NUM_E_COMBINATIONS):
            if co_eec_prune_table[i_co][i_eec] == distance:
                for i_move in range(len(move_names)):
                    next_co = co_move_table[i_co][i_move]
                    next_eec = e_combination_table[i_eec][i_move]
                    if co_eec_prune_table[next_co][next_eec] == -1:
                        co_eec_prune_table[next_co][next_eec] = distance + 1
                        num_filled += 1
    distance += 1
print(f"Finished! ({time.time() - start:.5f} sec.)") 

# Ignore CO and consider EO and E line
print("Computing eo_eec_prune_table")
start = time.time()
eo_eec_prune_table = [[-1] * NUM_E_COMBINATIONS for _ in range(NUM_EO)]
eo_eec_prune_table[0][0] = 0
distance = 0
num_filled = 1
while num_filled != NUM_EO * NUM_E_COMBINATIONS:
    print(f"distance = {distance}")
    print(f"num_filled = {num_filled}")
    for i_eo in range(NUM_EO):
        for i_eec in range(NUM_E_COMBINATIONS):
            if eo_eec_prune_table[i_eo][i_eec] == distance:
                for i_move in range(len(move_names)):
                    next_eo = eo_move_table[i_eo][i_move]
                    next_eec = e_combination_table[i_eec][i_move]
                    if eo_eec_prune_table[next_eo][next_eec] == -1:
                        eo_eec_prune_table[next_eo][next_eec] = distance + 1
                        num_filled += 1
    distance += 1
print(f"Finished! ({time.time() - start:.5f} sec.)")

# --- phase2 prune tables ---
# Ignore U,D faces and consider CP and E line edges
print("Computing cp_eep_prune_table")
start = time.time()
cp_eep_prune_table = [[-1] * NUM_E_EP for _ in range(NUM_CP)]
cp_eep_prune_table[0][0] = 0
distance = 0
num_filled = 1
while num_filled != NUM_CP * NUM_E_EP:
    print(f"distance = {distance}")
    print(f"num_filled = {num_filled}")
    for i_cp in range(NUM_CP):
        for i_eep in range(NUM_E_EP):
            if cp_eep_prune_table[i_cp][i_eep] == distance:
                for i_move in range(len(move_names_ph2)):
                    next_cp = cp_move_table[i_cp][i_move]
                    next_eep = e_ep_move_table[i_eep][i_move]
                    if cp_eep_prune_table[next_cp][next_eep] == -1:
                        cp_eep_prune_table[next_cp][next_eep] = distance + 1
                        num_filled += 1
    distance += 1
print(f"Finished! ({time.time() - start:.5f} sec.)")

# Ignore CP and consider U,D faces and E line edges
print("Computing udep_eep_prune_table")
start = time.time()
udep_eep_prune_table = [[-1] * NUM_E_EP for _ in range(NUM_UD_EP)]
udep_eep_prune_table[0][0] = 0
distance = 0
num_filled = 1
while num_filled != NUM_UD_EP * NUM_E_EP:
    print(f"distance = {distance}")
    print(f"num_filled = {num_filled}")
    for i_udep in range(NUM_UD_EP):
        for i_eep in range(NUM_E_EP):
            if udep_eep_prune_table[i_udep][i_eep] == distance:
                for i_move in range(len(move_names_ph2)):
                    next_udep = ud_ep_move_table[i_udep][i_move]
                    next_eep = e_ep_move_table[i_eep][i_move]
                    if udep_eep_prune_table[next_udep][next_eep] == -1:
                        udep_eep_prune_table[next_udep][next_eep] = distance + 1
                        num_filled += 1
    distance += 1
print(f"Finished! ({time.time() - start:.5f} sec.)") 

# These are dictionaries that retrieve the operation index from the operation name.
move_names_to_index_ph1 = {move_name: i for i, move_name in enumerate(move_names)}
move_names_to_index_ph2 = {move_name: i for i, move_name in enumerate(move_names_ph2)}
