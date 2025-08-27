
import json
import matplotlib.pyplot as plt
import numpy as np

from analysis import response_to_bits, compute_bitwise_entropy

# quick script to just plot out the cached data

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

def load_crps(path: str) -> dict:
    with open(path, 'r') as f:
        data = json.load(f)

    return data.get('crps', None)

def main():
    crps = load_crps('./cache/bff_01.bit.json')

    if crps is None: return

    responses = list(map(int, crps.values()))
    bits = response_to_bits(responses, width = 44)
    entropies = compute_bitwise_entropy(bits)
    
    plot_entropy(entropies) 


if __name__ == '__main__': main()
