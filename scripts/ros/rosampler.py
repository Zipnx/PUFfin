
import serial, json, argparse, time

def info(s): print(f'[*] {s}')
def error(s): print(f'[!] {s}')
def good(s): print(f'[+] {s}')

# plan rn is to get 1024 samples of each of the 3 selects

def execute(con, select: int) -> list[int]:
    payload = f'{select}\n\r'
    con.write(payload.encode())

    resp = con.readline().decode().strip('\r\n')
    con.readline()
    results = []
    for i in range(16):
        cut = resp[i*6:(i+1) * 6]
        results.append(int(cut, 16))

    return results

PROGBAR_WIDTH = 70

def benchmark(con, select: int, samples: int = 1024) -> list[list[int]]:
    results = []

    for i in range(samples):
        resp = execute(con, select)
        
        if i % 32 == 0:
            prog = i / samples
            perc = prog * 100
            bar = ('#'*int(prog * PROGBAR_WIDTH)).ljust(PROGBAR_WIDTH)
            print(f'<{bar}> {perc:.2f}%', end = '\r', flush = True)

        if len(resp) != 16:
            print()
            error('Invalid response')
            quit()

        results.append(resp)
    print()

    return results  

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=str,
                        help = 'Serial port the board is connected to')
    parser.add_argument('-s', '--samples', type=int, default = 1024,
                        help = 'Count of samples to take for each select (DEFAULT=1024)')
    parser.add_argument('-o', '--output', type=str, default = 'counts.json',
                        help = 'Output file to write to (DEFAULT=./counts.json)')
    args = parser.parse_args()

    info('Connecting to board')
    try:
        con = serial.Serial(
            port = args.port,
            baudrate = 115200,
            timeout  = 3
        )
        time.sleep(0.1)
    except BaseException as e:
        print(e)
        error("Error connecting to board")
        return
    good('Connected.')
    
    info('Sampling for select 0/2')
    sel0 = benchmark(con, 0, samples = args.samples)
    info('Sampling for select 1/2')
    sel1 = benchmark(con, 1, samples = args.samples)
    info('Sampling for select 2/2')
    sel2 = benchmark(con, 2, samples = args.samples)
    
    good('Completed tasks.')

    with open(args.output, 'w') as f:
        json.dump({
            0: sel0,
            1: sel1,
            2: sel2
        }, f, indent = 4)
        f.write('\n')

    good(f'Results written to "{arga.output}"')

if __name__ == '__main__':
    main()
