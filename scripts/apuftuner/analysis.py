
from collections import Counter
import numpy as np


def response_to_bits(responses: list[int], width: int = 32) -> np.ndarray:
    bits = [list(map(int, format(r, f'0{width}b'))) for r in responses]
    return np.array(bits)

def compute_bitwise_entropy(bit_array: np.ndarray) -> np.ndarray:
    entropies = []
    for i in range(bit_array.shape[1]):
        col = bit_array[:, i]
        counts = np.bincount(col, minlength=2) / len(col)
        entropy = -np.sum(p * np.log2(p) for p in counts if p > 0)
        entropies.append(entropy)
    return np.array(entropies)

def compute_total_entropy(responses: list[int]) -> float:
    counts = Counter(responses)
    total = len(responses)
    probs = [c / total for c in counts.values()]
    return -sum(p * np.log2(p) for p in probs if p > 0)

if __name__ == '__main__':
    # Just doin this for checking against test.json
    import json, sys
    
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <RESULT_FILE>')
        sys.exit(-1)

    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    crps = data['crps']
    responses = list(map(int, crps.values()))
    bits = response_to_bits(responses, width = 44)
    entropies = compute_bitwise_entropy(bits)

    print(entropies)
    avg_entropy = np.mean(entropies)
    print(f"\nAverage Bitwise Entropy: {avg_entropy:.4f} bits (of 1.0 max)")

    entropy = compute_total_entropy(responses)
    print('Total entropy:', entropy)
