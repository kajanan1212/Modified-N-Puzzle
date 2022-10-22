import random
import numpy as np
import os, os.path

def generate_config(n):
    config = np.array(list(range(1, (n**2)-1)) + ['-', '-'])
    np.random.shuffle(config)
    config = config.reshape(n, n)
    return config

def safe_open_w(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')

def write_config(config, path):
    str_config = ['\t'.join(config[i]) for i in range(len(config))]
    str_config = '\n'.join(str_config)
    with safe_open_w(path) as f:
        f.write(str_config)

for i in range(1, 101):
    n = random.randint(2, 2)
    initial_config = generate_config(n)
    goal_config = generate_config(n)
    folder = 'config/config_'+str(i)+'/'
    write_config(initial_config, folder+'initial_config.txt')
    write_config(goal_config, folder+'goal_config.txt')