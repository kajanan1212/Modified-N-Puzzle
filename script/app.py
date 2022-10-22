import sys
import n_puzzle

# may use n_puzzle.total_manhattan_distance or n_puzzle.num_of_misplaced_tiles as the last argument

n_puzzle.write_moves_sequence(sys.argv[1], sys.argv[2], 'moves_sequence.txt', n_puzzle.total_manhattan_distance)