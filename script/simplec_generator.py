import n_puzzle
import config_generator
import numpy as np
import random

def change_dtype(e):
    if e == -1:
        return '-'
    else: 
        return str(e)

def write_config(config, path):
    for i in range(len(config)):
        config[i] = list(map(change_dtype, config[i]))
    str_config = ['\t'.join(config[i]) for i in range(len(config))]
    str_config = '\n'.join(str_config)
    with config_generator.safe_open_w(path) as f:
        f.write(str_config)

initial_config = n_puzzle.read_config('initial_config.txt')
configs = [initial_config]
for i in range(1, 101):
    configs.extend(np.array(n_puzzle.explore(configs[i-1]), dtype=object)[:, 0])
    folder = 'config/config_'+str(i)+'/'
    write_config(configs[random.randint(0, len(configs)-1)].tolist(), folder+'initial_config.txt')
    write_config(configs[random.randint(0, len(configs)-1)].tolist(), folder+'goal_config.txt')