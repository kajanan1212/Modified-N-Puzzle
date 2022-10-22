import numpy as np

def change_dtype(e):
    if e == '-':
        return -1
    else: 
        return int(e)

def read_config(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        n_puzzle = [line.strip('\n') for line in lines]
        for i in range(len(n_puzzle)):
            n_puzzle[i] = list(map(change_dtype, n_puzzle[i].split('\t')))
    return np.array(n_puzzle)

def write_output(moves_sequence, file_name):
    with open(file_name, 'w') as f:
        f.write(str(moves_sequence)[1:-1])

def num_of_misplaced_tiles(config_1, config_2):
    num_of_misplaced_tiles = 0
    for row in config_1:
        for e in row:
            if e == -1:
                continue
            current_location = np.array([i_array[0] for i_array in np.where(config_1 == e)])
            goal_location = np.array([i_array[0] for i_array in np.where(config_2 == e)])
            if np.equal(current_location, goal_location).all():
                continue
            num_of_misplaced_tiles += 1
    return num_of_misplaced_tiles

def total_manhattan_distance(config_1, config_2):
    total_manhattan_distance = 0
    for row in config_1:
        for e in row:
            if e == -1:
                continue
            current_location = np.array([i_array[0] for i_array in np.where(config_1 == e)])
            goal_location = np.array([i_array[0] for i_array in np.where(config_2 == e)])
            total_manhattan_distance += np.sum(np.absolute(current_location - goal_location))
    return total_manhattan_distance

def heuristic(heuristic_function, config, goal_config):
    return heuristic_function(config, goal_config)

def move(blank_location, config, row_move, column_move):
    new_config = np.copy(config)
    new_config[blank_location[0], blank_location[1]] = config[blank_location[0]+row_move, blank_location[1]+column_move]
    new_config[blank_location[0]+row_move, blank_location[1]+column_move] = -1
    return new_config

def up(blank_location, config):
    return move(blank_location, config, -1, 0)

def down(blank_location, config):
    return move(blank_location, config, 1, 0)

def left(blank_location, config):
    return move(blank_location, config, 0, -1)

def right(blank_location, config):
    return move(blank_location, config, 0, 1)

def explore(config):
    new_configs_move = []
    row_count, column_count = config.shape
    blank_locations = np.array(np.where(config == -1)).transpose()
    for blank_location in blank_locations:
        blank_row, blank_column = blank_location
        if blank_row != 0:
            new_config = up(blank_location, config)
            moved_tile = new_config[blank_row, blank_column]
            if moved_tile != -1:
                new_configs_move.append([new_config, (moved_tile, 'down')])
        if blank_row != row_count-1:
            new_config = down(blank_location, config)
            moved_tile = new_config[blank_row, blank_column]
            if moved_tile != -1:
                new_configs_move.append([new_config, (moved_tile, 'up')])
        if blank_column != 0:
            new_config = left(blank_location, config)
            moved_tile = new_config[blank_row, blank_column]
            if moved_tile != -1:
                new_configs_move.append([new_config, (moved_tile, 'right')])
        if blank_column != column_count-1:
            new_config = right(blank_location, config)
            moved_tile = new_config[blank_row, blank_column]
            if moved_tile != -1:
                new_configs_move.append([new_config, (moved_tile, 'left')])
    return new_configs_move

def find_min_f_config_index(opened):
    opened_array = np.array(opened, dtype=object)
    f_configs = opened_array[:, 1] + opened_array[:, 2]
    return np.argmin(f_configs)

def find_config_index(config, opened_closed):
    config_index = -1
    for i in range(len(opened_closed)):
        if np.equal(config, opened_closed[i][0]).all():
            return i
    return config_index

def find_moves_sequence(initial_config_path, goal_config_path, heuristic_function):
    initial_config = read_config(initial_config_path)
    goal_config = read_config(goal_config_path)
    cost = 1
    n = initial_config.shape[0]

    g_initial_config = 0
    h_initial_config = heuristic(heuristic_function, initial_config, goal_config)

    opened = [[initial_config, g_initial_config, h_initial_config, list()]]
    closed = []

    min_f_config_index = find_min_f_config_index(opened)
    selected_config = opened.pop(min_f_config_index)
    closed.append(selected_config)

    is_fail = False
    num_step_taken = 0
    while selected_config[2] != 0:
        num_step_taken += 1
        g_selected_config, moves_sequence_selected_config = selected_config[1], selected_config[3]
        new_configs_move = explore(selected_config[0])
        for new_config, moved_action in new_configs_move:
            moves_sequence = moves_sequence_selected_config + [moved_action]
            opened_config_index = find_config_index(new_config, opened)
            closed_config_index = find_config_index(new_config, closed)
            if opened_config_index == -1 and closed_config_index == -1:
                opened.append([new_config, g_selected_config+cost, heuristic(heuristic_function, new_config, goal_config), moves_sequence])
            elif opened_config_index != -1 or closed_config_index != -1:
                if opened_config_index != -1:
                    opened[opened_config_index][1] = np.minimum(opened[opened_config_index][1], g_selected_config+cost)
                    if opened[opened_config_index][1] == g_selected_config+cost:
                        opened[opened_config_index][3] = moves_sequence
                elif closed_config_index != -1:
                    old_f_config = closed[closed_config_index][1] + closed[closed_config_index][2]
                    closed[closed_config_index][1] = np.minimum(closed[closed_config_index][1], g_selected_config+cost)
                    new_f_config = closed[closed_config_index][1] + closed[closed_config_index][2]
                    if new_f_config < old_f_config:
                        closed[closed_config_index][3] = moves_sequence
                        opened.append(closed.pop(closed_config_index))
        if len(opened) == 0:
            is_fail = True
            break
        min_f_config_index = find_min_f_config_index(opened)
        selected_config = opened.pop(min_f_config_index)
        closed.append(selected_config)

    if not is_fail:
        moves_sequence = selected_config[3]
    else:
        moves_sequence = ['FAILED']
    return n, moves_sequence, num_step_taken

def write_moves_sequence(initial_config_path, goal_config_path, moves_sequence_path, heuristic_function):
    n, moves_sequence, num_step_taken = find_moves_sequence(initial_config_path, goal_config_path, heuristic_function)
    write_output(moves_sequence, moves_sequence_path)