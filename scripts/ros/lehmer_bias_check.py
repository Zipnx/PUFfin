import numpy as np
import random
from tqdm import tqdm 

M = 16     #   
BIT_WIDTH = 24 
N = 100000     

# Lehmer encoder
def lehmer_encode(perm):
    n = len(perm)
    code = []
    for i in range(n-1):  
        smaller = sum(1 for x in perm[:i] if perm[i] > x)
        code.append(smaller)
    return code  


def gray_encode(n):
    return n ^ (n >> 1)


max_bits_per_L = [1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4]  


total_bits = sum(max_bits_per_L)
bits_matrix = np.zeros((N, total_bits), dtype=int)

# generate random permutations and encode
for i in tqdm(range(N), desc="Generating permutations"):
    perm = list(range(1, M+1))
    random.shuffle(perm)
    L = lehmer_encode(perm) 
    bit_idx = 0
    for coeff, bits_needed in zip(L, max_bits_per_L):
        g = gray_encode(coeff)
        for k in range(bits_needed):
            bits_matrix[i, bit_idx] = (g >> k) & 1
            bit_idx += 1

bias_per_bit = np.abs(bits_matrix.mean(axis=0) - 0.5)

 
threshold = 0.15
problematic_bits = np.where(bias_per_bit > threshold)[0]

print("Bias per bit:", bias_per_bit)
print("Problematic bit positions:", problematic_bits)
