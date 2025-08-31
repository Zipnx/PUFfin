
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

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

def plot_entropies(data: dict, bit_width: int = 32) -> None:
    responses = list(map(int, data.values()))
    bits = response_to_bits(responses, width = bit_width)
    
    entropies = compute_bitwise_entropy(bits)
    total_entropy = compute_total_entropy(responses)

    plt.figure(figsize=(10, 4))
    plt.bar(range(len(entropies)), entropies, color='skyblue')
    plt.xlabel("Bit Index (PUF #)")
    plt.ylabel("Entropy (bits)")
    plt.title("Bitwise Entropy of 32-Bit PUF Responses")
    plt.ylim(0, 1.1)
    plt.grid(True, axis='y')
    plt.tight_layout()

    plt.figtext(0.45, 0.005, f"Total Entropy: {total_entropy:.2f}")

    plt.show()
