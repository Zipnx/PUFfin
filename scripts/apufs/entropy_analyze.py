import json
import numpy as np
import argparse
import matplotlib.pyplot as plt
from typing import Mapping
from collections import Counter

def load_data(path: str) -> Mapping[str, int]:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data.get('crps', {})
    except Exception as e:
        print(f"[!] Error loading data: {e}")
        return {}

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

def plot_entropy(entropies: np.ndarray):
    plt.figure(figsize=(10, 4))
    plt.bar(range(len(entropies)), entropies, color='skyblue')
    plt.xlabel("Bit Index (PUF #)")
    plt.ylabel("Entropy (bits)")
    plt.title("Bitwise Entropy of 32-Bit PUF Responses")
    plt.ylim(0, 1.1)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Analyze entropy across 32 PUF bits")
    parser.add_argument("dumpfile", type=str, help="JSON file with CRPs")
    args = parser.parse_args()

    crps = load_data(args.dumpfile)
    if not crps:
        print("[!] No CRPs found")
        return

    responses = list(map(int, crps.values()))
    bits = response_to_bits(responses)
    entropies = compute_bitwise_entropy(bits)

    print("\nBitwise Entropy (max = 1.0):")
    for i, h in enumerate(entropies):
        print(f"PUF Bit {i:02}: {h:.4f} bits")

    avg_entropy = np.mean(entropies)
    print(f"\nAverage Bitwise Entropy: {avg_entropy:.4f} bits (of 1.0 max)")

    print("\nBitwise Entropy (max = 1.0):")
    for i, h in enumerate(entropies):
        print(f"PUF Bit {i:02}: {h:.4f} bits")

    avg_entropy = np.mean(entropies)
    print(f"\nAverage Bitwise Entropy: {avg_entropy:.4f} bits (of 1.0 max)")

    entropy = compute_total_entropy(responses)
    print('Total entropy:', entropy)

    plot_entropy(entropies)

if __name__ == "__main__":
    main()

