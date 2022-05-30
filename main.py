import random
import statistics as st


def build_grid():
    grid = []
    # ratio = random.randint(1, 3)
    ratio = 5
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


def pick_action(q_matrix, curr_state, epsilon):
    x = random.random()
    action = str(random.randint(0, 4))
    if x < epsilon:
        # pick randomly
        return str(random.randint(0, 4))
    else:
        # pick greedily
        max_reward = q_matrix.get(curr_state + action)
        for i in range(5):
            i = str(i)
            if q_matrix.get(curr_state + i) > max_reward:
                max_reward = q_matrix.get(curr_state + i)
                action = i
        return action


def get_reward(grid, curr_y, curr_x, curr_state, action) -> tuple[int, str, int, int]:
    if action == '4':
        if grid[curr_y][curr_x] == 1:
            grid[curr_y][curr_x] = 0
            return 10, curr_state, curr_y, curr_x
        else:
            return -1, curr_state, curr_y, curr_x
    else:
        if curr_state[int(action)] == '2':
            return -5, curr_state, curr_y, curr_x
        elif action == '0':
            y = curr_y - 1
            x = curr_x
        elif action == '1':
            x = curr_x + 1
            y = curr_y
        elif action == '2':
            x = curr_x
            y = curr_y + 1
        elif action == '3':
            x = curr_x - 1
            y = curr_y
        new_state = build_state(y, x, grid)
        return 0, new_state, y, x


def get_q_value(q_matrix, curr_state, action, reward, next_state):
    q = q_matrix.get(curr_state + action)
    q_prime = max(int(q_matrix.get(next_state + '0')),
                  int(q_matrix.get(next_state + '1')),
                  int(q_matrix.get(next_state + '2')),
                  int(q_matrix.get(next_state + '3')),
                  int(q_matrix.get(next_state + '4')))
    eta = 0.2
    gamma = 0.9
    q_value = q + (eta * (reward + (gamma * q_prime) - q))
    return q_value


def learn(q_matrix, grid, epsilon_flag):
    data_set = []
    total_reward = 0

    # Robby's current coordinates
    curr_y, curr_x = (random.randint(0, 9), random.randint(0, 9))

    # Encoding the location state
    curr_state = build_state(curr_y, curr_x, grid)
    # 5 possible actions per state.
    # 0 = up
    # 1 = right
    # 2 = down
    # 3 = left
    # 4 = pick up can
    for i in range(5):
        # Adds the state-action encoding to the Q Matrix.  If state-action pair already exists, does nothing.
        q_matrix.setdefault(curr_state + str(i), 0)

    epsilon = 0.1

    for m in range(200):
        # reduce epsilon ever 50 epochs
        if epsilon_flag:
            if (m + 1) % 50 == 0:
                epsilon -= 0.025

        action = pick_action(q_matrix, curr_state, epsilon)
        reward, next_state, curr_y, curr_x = get_reward(grid, curr_y, curr_x, curr_state, action)
        for i in range(5):
            q_matrix.setdefault(next_state + str(i), 0)
        q_value = get_q_value(q_matrix, curr_state, action, reward, next_state)
        q_matrix.update({(curr_state + action): q_value})
        curr_state = next_state
        total_reward += reward
    return total_reward


def main():
    f = open("data.txt", 'w')
    q_matrix = dict()
    n = 5000
    total_reward = 0
    episode_reward = 0
    data_set = []
    for i in range(n):
        # print()
        # print("Episode ", i)
        grid = build_grid()
        episode_reward = learn(q_matrix, grid, True)
        total_reward += episode_reward
        # print("Episode reward: ", episode_reward)
        print(episode_reward)
        f.write(str(episode_reward) + "\n")
    avg_reward = total_reward / n
    total_reward = 0
    print("Learning avg reward: ", avg_reward)
    print("==================================")
    f.write("Learning avg reward: " + str(avg_reward) + "\n")

    for i in range(n):
        grid = build_grid()
        episode_reward = learn(q_matrix, grid, False)
        data_set.append(episode_reward)
        total_reward += episode_reward

    print("Testing standard deviation: ", st.stdev(data_set))
    print("Average testing reward: ", total_reward / n)
    f.write("Testing standard deviation: " + str(st.stdev(data_set)) + "\n")
    f.write("Average testing reward: " + str(total_reward / n))
    f.close()


if __name__ == '__main__':
    main()
