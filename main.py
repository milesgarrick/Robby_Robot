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
    state = "00000"
    can_val = str(grid[curr_y][curr_x])
    state = state[:4] + can_val
    # If at y extreme
    if curr_y == 0 or curr_y == 9:
        # Setting walls for y extremes
        if curr_y == 0:
            state = '2' + state[:1]
            state = state[:2] + str(grid[curr_y + 1][curr_x]) + state[3:]
        elif curr_y == 9:
            state = str(grid[curr_y - 1][curr_x]) + state[1:]
            state = state[:2] + '2' + state[3:]

        # Setting walls for x extremes
        if curr_x == 0:
            state = state[:3] + '2' + state[4:]
            # Square to the right is 1 or 0
            state = state[:1] + str(grid[curr_y][curr_x + 1]) + state[2:]
        elif curr_x == 9:
            state = state[:1] + '2' + state[2:]
            # Square to the left is 1 or 0
            state = state[:3] + str(grid[curr_y][curr_x - 1]) + state[4:]
        # Setting 1 or 0 for squares to the left and right
        else:
            state = state[:1] + str(grid[curr_y][curr_x + 1]) + state[2:]
            state = state[:3] + str(grid[curr_y][curr_x - 1]) + state[4:]
    # Not at y extreme
    else:
        if curr_x == 0:
            state = state[:1] + str(grid[curr_y][curr_x + 1]) + state[2:]
            state = state[:3] + '2' + state[4:]
        elif curr_x == 9:
            state = state[:1] + '2' + state[2:]
            state = state[:3] + str(grid[curr_y][curr_x - 1]) + state[4:]
        else:
            state = state[:1] + str(grid[curr_y][curr_x + 1]) + state[2:]
            state = state[:3] + str(grid[curr_y][curr_x - 1]) + state[4:]
        state = str(grid[curr_y - 1][curr_x]) + state[1:]
        state = state[:2] + str(grid[curr_y + 1][curr_x]) + state[3:]
    return state


def pick_action(q_matrix, curr_state):
    epsilon = 0.1
    x = random.random(0, 1)
    if x < epsilon:
        # pick randomly
        return str(random.randint(0, 4))
    else:
        # pick greedily
        action = '0'
        max_reward = q_matrix.get(curr_state + action)
        for i in range(1, 5):
            i = str(i)
            if q_matrix.get(curr_state + i) > max_reward:
                max_reward = q_matrix.get(curr_state + i)
                action = i
        return action


def get_reward(grid, curr_y, curr_x, curr_state, action) -> int:
    if action == '4':
        if grid[curr_y][curr_x] == 1:
            return 1
        else:
            return 0, curr_state
    else:
        if action == '0':
            x = curr_x
            y = curr_y - 1
        elif action == '1':
            x = curr_x + 1
            y = curr_y
        elif action == '2':
            x = curr_x
            y = curr_y + 1
        else:
            x = curr_x - 1
            y = curr_y
        if grid[y][x] == 2:
            return -1, curr_state
        else:
            new_state = build_state(y, x, grid)
            return 0, new_state


def get_q_value(q_matrix, curr_state, action, reward, next_state):
    q = q_matrix.get(curr_state + action)
    q_prime = max(q_matrix.get(next_state + '0'),
                  q_matrix.get(next_state + '1'),
                  q_matrix.get(next_state + '2'),
                  q_matrix.get(next_state + '3'),
                  q_matrix.get(next_state + '4'))
    eta = 0.2
    gamma = 0.9
    q_value = q + (eta * (reward + (gamma * q_prime) - q))
    return q_value


def learn(q_matrix, grid):
    total_reward = 0

    # Robby's current coordinates
    curr_y, curr_x = (random.randint(0, 9), random.randint(0, 9))
    print("Starting location: (%d, %d)" % (curr_y, curr_x))

    # Encoding the location state
    curr_state = build_state(curr_y, curr_x, grid)

    for m in range(200):
        # 5 possible actions per state.
        # 0 = up
        # 1 = right
        # 2 = down
        # 3 = left
        # 4 = pick up can
        for i in range(5):
            # Adds the state-action encoding to the Q Matrix.  If state-action pair already exists, does nothing.
            q_matrix.setdefault(curr_state + str(i), 0)

        action = pick_action(q_matrix, curr_state)
        reward, next_state = get_reward(grid, curr_y, curr_x, action)
        q_value = get_q_value(q_matrix, curr_state, action, reward, next_state)
        q_matrix.update({(curr_state + action): q_value})
        curr_state = next_state
        total_reward += reward
    return total_reward


def main():
    print("Main")
    q_matrix = dict()
    n = 5000
    total_reward = 0
    for i in range(n):
        grid = build_grid()
        print_grid(grid)
        total_reward += learn(q_matrix, grid)
    avg_reward = total_reward / n
    print("Learning avg reward: ", avg_reward)

    grid = build_grid()
    test_reward = learn(q_matrix, grid)
    print("Test reward: ", test_reward)



if __name__ == '__main__':
    main()
