import n_puzzle
import pandas as pd

df = pd.DataFrame(columns=['n', 'num_step_taken(h_misplaced)', 'num_step_taken(h_manhattan)'])
for i in range(1, 101):
    print(str(i)+' started...')
    initial_config_path = 'config/config_'+str(i)+'/initial_config.txt'
    goal_config_path = 'config/config_'+str(i)+'/goal_config.txt'
    n, h_misplaced, num_step_taken_misplaced = n_puzzle.find_moves_sequence(initial_config_path, goal_config_path, n_puzzle.num_of_misplaced_tiles)
    n, h_manhattan, num_step_taken_manhattan = n_puzzle.find_moves_sequence(initial_config_path, goal_config_path, n_puzzle.total_manhattan_distance)
    df = df.append({'n': n, 'num_step_taken(h_misplaced)': num_step_taken_misplaced, 'num_step_taken(h_manhattan)': num_step_taken_manhattan}, ignore_index=True)
    print(str(i)+' finished...')

df['num_step_taken(h_misplaced-h_manhattan)'] = df['num_step_taken(h_misplaced)'] - df['num_step_taken(h_manhattan)']
df.to_csv('experiment_result.csv', index=False)
print('DONE')
