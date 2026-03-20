import time
from solve import *

# Initialize Ccbe
cube = State(
    [0, 1, 2, 3, 4, 5, 6, 7], # cp
    [0, 0, 0, 0, 0, 0, 0, 0], # co
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], #ep
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # eo
)

if __name__ == "__main__":
    # Generate scramble
    scramble = cube.scramble(30)
    print(scramble)
    print(cube.cp,cube.co,cube.ep,cube.eo)
    search = Search(cube)
    start = time.time()
    # Start searching
    # solution = search.start_search(cube)
    solution = search.start_search_kociemba()
    print(f"Finished! ({time.time() - start:.5f} sec)")
    if solution:
        print(f"Solution: {solution}")
    else:
        print("Solution was not found")