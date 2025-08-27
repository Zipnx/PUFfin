
from puffinpy import HCMCommander
from os import urandom
import struct, json
import numpy as np

from utils import info, error, good
from analysis import response_to_bits, compute_bitwise_entropy, compute_total_entropy 

PROGBAR_WIDTH = 70

def benchmark(module: HCMCommander, samples: int = 8192):
    info(f'Starting benchmark with {samples} total sampled...')

    crps = {}

    for i in range(samples):
        challenge = bytearray(urandom(4))
        #challenge[0] |= 0x80
        #challenge = bytes(challenge)

        if i % 64 == 0:
            prog = i / samples
            perc = prog * 100
            bar = ('#'*int(prog * PROGBAR_WIDTH)).ljust(PROGBAR_WIDTH)
            print(f'<{bar}> {perc:.2f}%', end = '\r', flush = True) 

        resp = module.rawapuf_single(challenge)

        crps[challenge.hex()] = resp
    
    print()
    good('Collection complete')

    return crps

if __name__ == '__main__':
    hcm = HCMCommander(port = 'COM10')

    crps = benchmark(hcm, samples = 8192)
    
    responses = list(map(int, crps.values()))
    bits = response_to_bits(responses, width = 32)
    entropies = compute_bitwise_entropy(bits)

    print(entropies)
    avg_entropy = np.mean(entropies)
    print(f"\nAverage Bitwise Entropy: {avg_entropy:.4f} bits (of 1.0 max)")

    entropy = compute_total_entropy(responses)
    print('Total entropy:', entropy)

    with open('rawapuf.json', 'w') as f:
        json.dump({
            'crps': crps
        }, f, indent = 4)
        f.write('\n')
