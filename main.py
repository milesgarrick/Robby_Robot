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


def learn(q_matrix, grid):
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
