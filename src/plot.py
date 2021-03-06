import re
import numpy as np
import matplotlib.pyplot as plt

RESULTS_FILE = 'result.log'
RESULT_LENGTH = 26
RESULT_LINES = [5, 13, 21]
CORES = [1, 2, 4, 6, 8, 12, 16, 24, 32, 40, 48, 56, 64]

def parse_result_line(line):
    return float(re.search('in (\d+(?:\.\d+)?) sec', line).group(1))


def parse_results(lines):
    core_results = [0 for _ in range(len(CORES))]
    for n in range(len(lines) // RESULT_LENGTH):
        results = [parse_result_line(lines[n * RESULT_LENGTH + i]) for i in RESULT_LINES]
        core_results[n] = sum(results) / len(results)
    return core_results


def compute_speedup(results):
    return results[0] / np.asarray(results)


def plot_graph(results):
    x = CORES
    y = compute_speedup(results)
    plt.plot(x, y, 'bo', x, y, 'k')
    plt.title('distributed k-d tree creation performance')
    plt.ylabel('Speedup')
    plt.xlabel('Cores number')
    plt.xticks([1, 4, 8, 16, 24, 32, 40, 48, 56, 64])
    plt.savefig('plot.png')


if __name__ == '__main__':
    x = CORES
    with open(RESULTS_FILE, 'r') as f:
        lines = f.readlines()
    results = parse_results(lines)
    plot_graph(results)
