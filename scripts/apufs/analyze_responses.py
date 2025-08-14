
from collections import Counter
import json, argparse
from typing import Mapping
import numpy as np
from os.path import exists as fileExists
from os.path import isdir as isDirectory
from itertools import combinations

def load_data(path: str) -> dict:

    try:
        with open(path, 'rb') as f:
            return json.load(f)
    except BaseException:
        print('[!] Invalid JSON data')
        return {}

def analyze(crps: Mapping[str, int]) -> None:
    responses = [list(map(int, format(resp, '032b'))) for resp in crps.values()]
    responses = np.array(responses)
    
    chall_count, puf_count = responses.shape

    uniformity  = np.mean(responses, axis=0) * 100
    avg_uniform = np.mean(uniformity)
    
    hamming_distances = []

    for i, j in combinations(range(puf_count), 2):
        hamming_distance = np.mean(responses[:, i] != responses[:, j]) * 100
        hamming_distances.append(hamming_distance)
    
    avg_uniqueness = np.mean(hamming_distances)
    
    responses_ints = list(map(int, crps.values()))
    counts = Counter(responses_ints)
    
    entropy     = -sum((c / chall_count) * np.log2(c / chall_count) for c in counts.values())
    
    entropy_perc = (entropy / puf_count) * 100

    print('\n======= Metrics =======')
    print(f'Uniformity: {uniformity}')
    print(f'Avg Uniformity: {avg_uniform:.2f}%')
    print(f'Avg Uniqueness: {avg_uniqueness:.2f}%')
    print(f'Response Entropy: {entropy:.2f} bits out of {puf_count}')
    print(f'Entropy % of ideal: {entropy_perc:.2f}%')
    print(f'Number of unique {puf_count}-bit responses: {len(counts)}/{len(crps)}')

def main():
    parser = argparse.ArgumentParser(description = 'Script that runs tests on results from arbiter pufs')
    parser.add_argument('dumpfile', type=str, help = 'JSON file with CRPs')
    args = parser.parse_args()

    if not fileExists(args.dumpfile) or isDirectory(args.dumpfile):
        print('[!] Invalid dumpfile path')
        return

    data = load_data(args.dumpfile)

    if len(data) == 0: return
    
    # Format [CHALLENGE INT] -> [RESPONSE INT]
    crps = data.get('crps', None)

    if crps is None:
        print('[!] Invalid JSON format')
        return
    
    analyze(crps)


if __name__ == "__main__":
    main()
