import random


def build_grid():
    grid = []
    ratio = random.randint(1, 3)
    for i in range(10):
        cols = []
        for j in range(10):
            x = random.randint(1, 10)
            if x <= ratio:
                cols.append(1)
            else:
                cols.append(0)
        grid.append(cols)
    return grid


def print_grid(grid):
    for i in grid:
        print(i)


def build_state(curr_y, curr_x, grid):
    state = [0, 0, 0, 0, 0]
    state[4] = grid[curr_y][curr_x]
    # If at y extreme
    if curr_y == 0 or curr_y == 9:
        # Setting walls for y extremes
        if curr_y == 0:
            state[0] = 2
            state[2] = grid[curr_y + 1][curr_x]
        elif curr_y == 9:
            state[0] = grid[curr_y - 1][curr_x]
            state[2] = 2

        # Setting walls for x extremes
        if curr_x == 0:
            state[3] = 2
            # Square to the right is 1 or 0
            state[1] = grid[curr_y][curr_x + 1]
        elif curr_x == 9:
            state[1] = 2
            # Square to the left is 1 or 0
            state[3] = grid[curr_y][curr_x - 1]
        # Setting 1 or 0 for squares to the left and right
        else:
            state[1] = grid[curr_y][curr_x + 1]
            state[3] = grid[curr_y][curr_x - 1]
    # Not at y extreme
    else:
        if curr_x == 0:
            state[1] = grid[curr_y][curr_x + 1]
            state[3] = 2
        elif curr_x == 9:
            state[1] = 2
            state[3] = grid[curr_y][curr_x - 1]
        else:
            state[1] = grid[curr_y][curr_x + 1]
            state[3] = grid[curr_y][curr_x - 1]
        state[0] = grid[curr_y - 1][curr_x]
        state[2] = grid[curr_y + 1][curr_x]
    return state


def learn(q_matrix, grid):
    curr_y, curr_x = (random.randint(0, 9), random.randint(0, 9))
    print("Starting location: (%d, %d)" % (curr_y, curr_x))
    curr_state = build_state(curr_y, curr_x, grid)
    print("First state: ", curr_state)
    return


def main():
    print("Main")
    q_matrix = dict()
    n = 1
    for i in range(n):
        grid = build_grid()
        print_grid(grid)
        learn(q_matrix, grid)


if __name__ == '__main__':
    main()
