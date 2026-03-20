import timeout_decorator
from kociemba import *

class Search:
    def __init__(self, state: State):
        self.initial_state = state
        self.solution = [] # This is an array that store the solution searching.
        self.solution_ph1 = [] # This is an array that store the solution untill phase 1.
        self.solution_ph2 = [] # This is an array that store the solution untill phase 2.
        self.max_solution_length = 9999
        self.best_solution = None
        self.start = 0

    def count_solved_corners(self,state: State):
        return sum([state.cp[i] == i and state.co[i] == 0 for i in range(8)])

    def count_solved_edges(self,state: State):
        return sum([state.ep[i] == i and state.eo[i] == 0 for i in range(12)])

    def prune(self,state: State, depth):
        # If further searching is pointless, return True.
        if depth == 1 and (self.count_solved_corners(state) < 4 or self.count_solved_edges(state) < 8):
            return True
        if depth == 2 and self.count_solved_edges(state) < 4:
            return True
        if depth == 3 and self.count_solved_edges(state) < 2:
            return True
        return False

    def depth_limited_search(self, state: State, depth):
        if depth == 0 and state.is_solved():
            return True
        if depth == 0:
            return False
        
        # pruning (IDA* algorithm)
        if self.prune(state, depth):
            return False

        # searching untill depth = 0
        prev_move = self.solution[-1] if self.solution else None
        for move_name in move_names:
            if not state.is_movable(prev_move,move_name):
                continue
            self.solution.append(move_name)
            if self.depth_limited_search(state.apply_move(moves[move_name]), depth - 1):
                return True
            self.solution.pop()
        return False

    def depth_limited_search_ph1(self, co_index, eo_index, e_comb_index, depth):
        if depth == 0 and co_index == 0 and eo_index == 0 and e_comb_index == 0:
            last_move = self.solution_ph1[-1] if self.solution_ph1 else None
            if last_move is None or last_move in ("R", "L", "F", "B", "R'", "L'", "F'", "B'"):
                state = self.initial_state
                for move_name in self.solution_ph1:
                    state = state.apply_move(moves[move_name])
                return self.start_search_kociemba_ph2(state)
        if depth == 0:
            return False

        # pruning (IDA* algorithm)
        if max(co_eec_prune_table[co_index][e_comb_index], eo_eec_prune_table[eo_index][e_comb_index]) > depth:
            return False
        
        # searching untill depth = 0
        prev_move = self.solution_ph1[-1] if self.solution_ph1 else None
        for move_name in move_names:
            if not self.initial_state.is_movable(prev_move, move_name):
                continue
            self.solution_ph1.append(move_name)
            move_index = move_names_to_index_ph1[move_name]
            next_co_index = co_move_table[co_index][move_index]
            next_eo_index = eo_move_table[eo_index][move_index]
            next_e_comb_index = e_combination_table[e_comb_index][move_index]
            
            if self.depth_limited_search_ph1(next_co_index, next_eo_index, next_e_comb_index, depth - 1):
                return True
            self.solution_ph1.pop()
        return False
    
    def depth_limited_search_ph2(self, cp_index, udep_index, eep_index, depth):
        if depth == 0 and cp_index == 0 and udep_index == 0 and eep_index == 0:
            solution = " ".join(self.solution_ph1) + " . " + " ".join(self.solution_ph2)
            print(
                f"Solution: {solution} "
                f"({len(self.solution_ph1) + len(self.solution_ph2)} moves) "
                f"in {time.time() - self.start:.5f} sec.")
            self.max_solution_length = len(self.solution_ph1) + len(self.solution_ph2) - 1
            self.best_solution = solution
            return True
        if depth == 0:
            return False
        
        # pruning (IDA* algorithm)
        if max(cp_eep_prune_table[cp_index][eep_index], udep_eep_prune_table[udep_index][eep_index]) > depth:
            return False
        
        # searching untill depth = 0
        if self.solution_ph2:
            prev_move = self.solution_ph2[-1]
        elif self.solution_ph1:
            prev_move = self.solution_ph1[-1]
        else:
            prev_move = None

        for move_name in move_names_ph2:
            if not self.initial_state.is_movable(prev_move, move_name):
                continue
            self.solution_ph2.append(move_name)
            move_index = move_names_to_index_ph2[move_name]
            next_cp_index = cp_move_table[cp_index][move_index]
            next_udep_index = ud_ep_move_table[udep_index][move_index]
            next_eep_index = e_ep_move_table[eep_index][move_index]
            found = self.depth_limited_search_ph2(next_cp_index, next_udep_index, next_eep_index, depth - 1)
            self.solution_ph2.pop()
            if found:
                return True
        return False

    def start_search(self, max_length=20):
        for depth in range(0, max_length):
            print(f"# Start searching: length {depth}")
            if self.depth_limited_search(self.initial_state, depth):
                # if it finds solution, return it then.
                return ' '.join(self.solution)
        return None
    
    def start_search_kociemba(self, max_length=20, timeout=30):
        self.best_solution = None
        self.start_search_kociemba_ph1(max_length=max_length, timeout=timeout)
        return self.best_solution

    def start_search_kociemba_ph1(self, max_length, timeout):
        self.start = time.time()
        self.max_solution_length = max_length
        co_index = co_to_index(self.initial_state.co)
        eo_index = eo_to_index(self.initial_state.eo)
        e_combination = [1 if e in (0, 1, 2, 3) else 0 for e in self.initial_state.ep]
        e_comb_index = e_combination_to_index(e_combination)

        depth = 0
        while depth <= self.max_solution_length:
            if time.time() - self.start >= timeout:
                return self.best_solution
            if self.depth_limited_search_ph1(co_index, eo_index, e_comb_index, depth):
                pass
            depth += 1
        return None
    
    def start_search_kociemba_ph2(self, state: State):
        cp_index = cp_to_index(state.cp)
        udep_index = ud_ep_to_index(state.ep[4:])
        eep_index = e_ep_to_index(state.ep[:4])
        depth = 0
        while depth <= self.max_solution_length - len(self.solution_ph1):
            if self.depth_limited_search_ph2(cp_index, udep_index, eep_index, depth):
                return True
            depth += 1
        return False