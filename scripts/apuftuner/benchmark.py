
import random, struct, serial, time, json
from settings import Settings
import numpy as np

from os import mkdir
from os.path import exists as fileExists

from utils import info, good, error
from program import program_bitstream, reset_board
from analysis import response_to_bits, compute_bitwise_entropy, compute_total_entropy

def execute_challenge(con, challenge: bytes) -> int | None:
    #payload = challenge + b'\r\n'
    payload = challenge.hex() + '\r\n'
    con.write(payload.encode())
    res = con.readline().decode().strip('\n\r')
    if ':' in res and 'ERROR' not in res:
        res = res.split(' ')[1]

    try:
        resp = int(res, 16)
    except ValueError:
        error('Invalid response from hardware!')
        print('Challenge:', challenge.hex())
        error(res)
        return None

    return resp

PROGBAR_WIDTH = 70

def benchmark(settings, con) -> dict | None:
    info('Executing benchmark')

    if settings.bench_seed is not None:
        random.seed(settings.bench_seed)
    
    crps = {}

    # TODO: Make this batched in the future, for now ill 
    #       keep it slow, it'd be way slower for me to go through
    #       and implement that in libhcm
    for i in range(settings.bench_samples):
        chall = random.randbytes(4) 
        # ew
        resp  = execute_challenge(con, chall)
        
        if i % 64 == 0:
            prog = i / settings.bench_samples
            perc = prog * 100
            bar = ('#'*int(prog * PROGBAR_WIDTH)).ljust(PROGBAR_WIDTH)
            print(f'<{bar}> {perc:.2f}%', end = '\r', flush = True)

        if resp is None: return None

        crps[chall.hex()] = resp
    
    print()
    good('Benchmark complete.')

    return crps

# Kinda dumb to have this func here, but this whole automation
# system is getting thrown together as fast as possible, so itll be fixed later
def analyze_responses(data: dict):
    
    info('Running analysis...')

    responses = list(map(int, data.values()))
    bits = response_to_bits(responses, width = 44)
    
    entropies       = compute_bitwise_entropy(bits)
    total_entropy   = compute_total_entropy(responses)
    avg_entropy     = np.mean(entropies)
    min_entropy     = np.min(entropies)
    max_entropy     = np.max(entropies)

    good(f'Total Entropy: {total_entropy:.2f} bits')
    good(f'Entropies (min/mean/max): {min_entropy:.2f} / {avg_entropy:.2f} / {max_entropy:.2f}')
    
    return entropies#, total_entropy

def test_stream(settings: Settings, stream_name: str, use_cache: bool = False) -> list[float] | None:
    info(f'Testing {stream_name}...')

    # FARTODO: 
    #   Display the progress as a N-line 11 col matrix
    #   of ascii in RED YELLOW or GREEN background,
    #   where the current ideal configuration is displayed
    #   Will just need to clear the term over and over,
    #   and also identify a way to characterize the 
    #   metric as good, ok or horrible

    # execute a full reset, just to be sure
    # not checking result, will proceed either way
    
    cache_file = settings.script_dir / f'cache/{stream_name}.json'

    if use_cache:
        info('Attempting to use cached benchmark results...')

        if fileExists(cache_file):
            # TODO: Error handling
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            good('Using cached result instead')

            return analyze_responses(data['crps'])
        
        error('Cached result data not found. Running benchmark normally')

    reset_board(settings)

    # load the stream & the elf on the board
    if not program_bitstream(settings, stream_name): return

    # connect the serial
    info('Connecting to board')
    try:
        con = serial.Serial(
            port = settings.port,
            baudrate = 115200,
            timeout  = 3
        )
        time.sleep(0.1)
    except BaseException:
        error("Error connecting to board")
        return
    good('Connected.')

    # run benchmarking
    crps = benchmark(settings, con)
    
    # Save to a cache directory, for possible manual analysis
    try:
        mkdir(settings.script_dir / 'cache/')
    except FileExistsError:
        # Will add a directory exists checks in the future
        pass

    with open(settings.script_dir / f'cache/{stream_name}.json', 'w') as f:
        json.dump({
            'timestamp': int(time.time()),
            'crps': crps
        }, f, indent = 4)
        f.write('\n')
    
    # run bitwise entropy analysis
    # return the stats for comparison

    return analyze_responses(crps)

