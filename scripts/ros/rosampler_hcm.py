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

# Checking for the 49 bits that we use right now, this is temporary
def get_used_bits(resp: bytes) -> str:
    lsb = int.from_bytes(resp[0:4], byteorder='big')
    msb = int.from_bytes(resp[4:8], byteorder='big') & 0x1ffff

    value = (msb << 32) | lsb

    return f'{value:049b}'

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

        results[0].append(get_used_bits(r0))
        results[1].append(get_used_bits(r1))
        results[2].append(get_used_bits(r2))

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
    
