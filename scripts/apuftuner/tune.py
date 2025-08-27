
from pathlib import Path
import argparse

from dataclasses import replace
from utils import info, good, error
from settings import Settings
from bitgen import generate_bitstreams, bitstream_names
from benchmark import test_stream
from place import Sector, Slot, QUAD_SECTORS, CarryTap

def get_all_slots() -> list[Slot]:
    slots = []

    for sector in QUAD_SECTORS:
        slots += sector.get_slots(start_index = len(slots))

    return slots

def streamname_to_carrytap(stream: str) -> CarryTap:
    ff = ['aff', 'bff', 'cff', 'dff'].index(stream[:3])
    tap = int(stream[4:6], 2)

    return (tap, ff)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('serial', type = str,
                        help = 'Interaction serial port (the one the board usually gets assigned to)')

    parser.add_argument('--usecache', action = 'store_true',
                        help = 'Use cached benchmark results if they exist')

    args = parser.parse_args()
    config = Settings(port = args.serial)

    info('Running tuner...')
    if args.usecache:
        info('Using cached benchmark results if possible')

    if not generate_bitstreams(config): return
    
    opts = {}

    for slot in get_all_slots():
        opts[slot] = 0

    # Result of the tests will be a configuration,
    # will write out to a carrytap bit string config and xdc for the dffs
    
    streams = bitstream_names()

    info(f'Running tuner automation on {streams}')

    for stream in streams:
        res = test_stream(config, stream, args.usecache)

        if res is None:
            return
        
        incr_count = 0

        # Get the new best from the results
        for slot, entropy in zip(opts.keys(), res):
            if entropy > opts[slot]:
                slot.carrytap = streamname_to_carrytap(stream)
                opts[slot] = entropy
                incr_count += 1

        good(f'Total Entropy Upgrades: {incr_count}')

    # take the keys from opt and sort them by the value in a list
    sorted_slots = sorted(opts.keys(), key = lambda k: opts[k], reverse = True)

    # pick the top 32
    picked = sorted_slots[:32]
    
    # DEBUG JUST PRINTING OUT TO SEE IF IT GETS APPLIED PROPERLY
    for pick in picked:
        info(f'{pick.location=} & {pick.puf_index=}: {pick.carrytap=} {float(opts[pick])=}')

    # Replace the puf_index for each
    remapped = [replace(k, puf_index=remap) for remap, k in enumerate(picked)]
    print(remapped)

    # Print out the rawapuf config & write the XDC to file
    xdc  = ''
    taps = ''

    for slot in remapped:
        xdc += slot.place()
        taps = f'{slot.carrytap[0]:02b}' + taps

    with open('./tuned.xdc', 'w') as f:
        f.write(xdc)
    
    good('Tuned XDC written to ./tuned.xdc')
    good(f'CarryTap Tap Config: {taps}')

if __name__ == '__main__':
    main()
