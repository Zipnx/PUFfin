from puffinpy import HCMCommander
import argparse, json

def info(s): print(f"[*] {s}")
def good(s): print(f'[+] {s}')
def error(s): print(f'[!] {s}')

def get_opts():
    parser = argparse.ArgumentParser(description = 'Sampler for the ROs running on a board with HCM firmware')
    parser.add_argument('port', type=str, help='Serial port to use')
    parser.add_argument('-s', '--samples', type=int, default=512, help="Samples to capture")
    parser.add_argument('-o', '--output', type=str, default='output.json', help='Output file (json)')
    parser.add_argument('--sim', action='store_true', help='Simulate for testing')

    return parser.parse_args()

PROGBAR_WIDTH = 70

def get_resp(hcm: HCMCommander, select: int) -> bytes | None:
    resp = hcm.ropuf(select)

    if len(resp) != 16: return None

    return resp

def benchmark(hcm: HCMCommander, samples: int = 1024):
    results = {
        0: [],
        1: [],
        2: []
    }

    for i in range(samples):
        r0 = get_resp(hcm, 0)
        r1 = get_resp(hcm, 1)
        r2 = get_resp(hcm, 2)
        
        if r0 is None or r1 is None or r2 is None:
            print()
            error('Invalid response')
            quit()

        if i % 32 == 0:
            prog = i / samples
            perc = prog * 100
            bar = ('#'*int(prog * PROGBAR_WIDTH)).ljust(PROGBAR_WIDTH)
            print(f'<{bar}> {perc:.2f}%', end = '\r', flush = True)

        results[0].append(r0.hex())
        results[1].append(r1.hex())
        results[2].append(r2.hex())

    print()

    return results  



def main():
    args = get_opts()
    
    hcm = HCMCommander(port = args.port, simulate = args.sim, debug = args.sim)

    info('Sampling for all selects')
    res = benchmark(hcm, args.samples)

    good('Completed tasks.')

    with open(args.output, 'w') as f:
        json.dump(res, f, indent = 4)
        f.write('\n')

    good(f'Results written to "{args.output}"')

if __name__ == '__main__':
    main()
    
