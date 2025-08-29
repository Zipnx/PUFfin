
import argparse, json
import numpy as np

from os.path import exists as fileExists
from os.path import isdir  as isDirectory

def info(s): print(f'[*] {s}')
def good(s): print(f'[+] {s}')
def error(s): print(f'[!] {s}')

def load_data(path: str) -> dict | None:
    if not fileExists(path) or isDirectory(path):
        error(f'Invalid filepath: {path}')
        return None
    
    with open(path, 'r') as f:
        return json.load(f)

def get_averages(data: dict) -> list[float]:
    results = []

    for i, sel in enumerate(data.keys()):
        if str(i) != sel:
            error('Invalid data file')
            return []

        arr = np.array(data[sel])
        results.append(arr.mean())

    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='JSON Results of sampler from multiple boards')

    args = parser.parse_args()
    
    averages = []

    for file in args.files:
        data = load_data(file)
        if data is None: return

        avg = get_averages(data)
        if len(avg) == 0: return
        
        averages.append(avg)

    for i, avg in enumerate(averages):
        print(f'Board {i}:')
        print(f'\t{avg}')

if __name__ == "__main__":
    main()
