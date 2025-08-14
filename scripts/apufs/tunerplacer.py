

from dataclasses import dataclass
from typing import List, Tuple

COLOR = True
RED   = '\033[91m' if COLOR else ''
GREEN = '\033[92m' if COLOR else ''
BLUE  = '\033[94m' if COLOR else ''
WHITE = '\033[97m' if COLOR else ''

def info(s):  print(f'{BLUE}[*]{WHITE} {s}')
def good(s):  print(f'{GREEN}[+]{WHITE} {s}')
def error(s): print(f'{RED}[!]{WHITE} {s}')

Location = Tuple[int, int]

OUTPUT = './tuner.xdc'
PREFIX = 'design_1_i/LUT_APUF_Raw_AXI_0/U0/LUT_APUF_Raw_AXI_v1_1_S00_AXI_inst/RAW_APUF_INST/U0/APUF_INST/'
# This goes by puf instance as a whole

PUF_WIDTH  = 2
PUF_HEIGHT = 17 

@dataclass(init = True)
class Sector:
    base: Location
    cols: int
    rows: int

    def get_slots(self) -> List[Location]:
        slots = []
        

        for i in range(self.rows):
            for j in range(self.cols):
                x = self.base[0] + (j * PUF_WIDTH)
                y = self.base[1] - (i * PUF_HEIGHT)

                slots.append((x, y))

        return slots

SECTS = [
    Sector((22, 99), 11, 2),
    Sector((22, 49), 11, 2)
]


def place_lutmux(loc: Location, puf_idx: int, chain_idx: int, down: bool) -> str:

    return f'''
set_property BEL {"C" if down else "D"}6LUT [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/CHAIN_INST/CHAIN_GEN_{"DOWN" if down else "UP"}[{chain_idx}].MUX_INST}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/CHAIN_INST/CHAIN_GEN_{"DOWN" if down else "UP"}[{chain_idx}].MUX_INST}}]
    '''

def place_activator(loc: Location, puf_idx: int, down: bool) -> str:

    return f'''
set_property BEL {"C" if down else "D"}FF [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/STARTER_INST/activator{"1" if down else "0"}}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/STARTER_INST/activator{"1" if down else "0"}}}]'''

def place_arbiter_tapcarry(loc: Location, puf_idx: int, dff: str = 'CFF') -> str:
    return f'''
set_property BEL {dff} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/dff}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/dff}}]
set_property BEL CARRY4 [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/delay}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/delay}}]'''


def index_to_dff(idx: int) -> str:
    return [
        'DFF', 'CFF',
        'BFF', 'AFF'
    ][idx]

@dataclass(init = True)
class PUFPlacement:
    pid:      int
    location: Location
    depth:    int
    carrytap: Tuple[int, int]

    def generate(self):
        output  = ''
        output += place_arbiter_tapcarry(
            loc     = (self.location[0] + 1, self.location[1]),
            puf_idx = self.pid,
            dff     = index_to_dff(self.carrytap[1])
        )

        for i in range(self.depth):
            x = self.location[0] + (0 if i % 2 == 0 else 1)
            y = self.location[1] - ((i - 1) // 2) - 1

            output += place_lutmux((x, y), self.pid, self.depth - i, False)
            output += place_lutmux((x, y), self.pid, self.depth - i, True)
        
        output += place_activator(
            (self.location[0], self.location[1] - self.depth // 2),
            self.pid, False
        )
        output += place_activator(
            (self.location[0], self.location[1] - self.depth // 2),
            self.pid, True
        )

        return output

def fill_sectors(ctconfig: Tuple[int, int]) -> List[PUFPlacement]:

    pufs = []
    idx  = 0

    for sect in SECTS:
        slots = sect.get_slots()

        for slot in slots:
            pufs.append(
                PUFPlacement(pid = idx, location = slot, depth = 32, carrytap = ctconfig)
            )
            idx += 1

    return pufs

def generate_xdc(placements: List[PUFPlacement]) -> str:
    xdc = ''

    for pl in placements:
        xdc += pl.generate()

    return xdc

def main():
    
    info(f"Getting available placements from {len(SECTS)} sectors")
    placements = fill_sectors((0, 0))
    good(f'Got {len(placements)} placements')    
    
    info('Generating XDC...')
    xdc = generate_xdc(placements) 
    
    good('Placement gen complete.')
    info(f'Saving to "{OUTPUT}" ...')

    with open(OUTPUT, 'w') as f:
        f.write(xdc)


    #print(placements)

if __name__ == "__main__":
    main()
