
from dataclasses import dataclass
from typing import Tuple, List, Self

CarryTap = Tuple[int, int]

# TODO: Unhardcode this, multiple ps projects
#PREFIX = 'design_1_i/LUT_APUF_Raw_AXI_0/U0/LUT_APUF_Raw_AXI_v1_1_S00_AXI_inst/RAW_APUF_INST/U0/APUF_INST/'
PREFIX = 'toplevel_i/APUF_Raw_AXI_v1_0_0/U0/APUF_Raw_AXI_v1_1_S00_AXI_inst/RAW_APUF_INST/U0/APUF_INST/'

@dataclass(init = True)
class Location:
    x: int
    y: int

    def __iadd__(self, other):
        if isinstance(other, tuple) and len(other) >= 2:
            self.x += other[0] if other[0] is not None else 0
            self.y += other[1] if other[1] is not None else 0
            return

        if isinstance(other, type(self)):
            self.x += other.x
            self.y += other.y
            return

        raise BaseException('Invalid operation')

    def __add__(self, other):
        if isinstance(other, tuple) and len(other) >= 2:
            return Location(
                self.x + other[0] if other[0] is not None else 0, 
                self.y + other[1] if other[1] is not None else 0
            )

        if isinstance(other, type(self)):
            return Location(self.x + other.x, self.y + other.y)

        raise BaseException('Invalid operation')


SLOT_WIDTH = 2
SLOT_HEIGHT = 17

@dataclass(init = True)
class Slot:
    puf_index:  str
    location:   Location
    carrytap:   CarryTap
    depth:      int = 32
    
    def __hash__(self): return hash(self.puf_index)

    def place(self):
        output = ''
        output += place_arbiter_tapcarry(
            loc     = self.location + Location(1, 0),
            puf_idx = self.puf_index,
            dff     = ['AFF', 'BFF', 'CFF', 'DFF'][self.carrytap[1]]
        )

        for i in range(self.depth):
            loc = self.location + (
                (0 if i % 2 == 0 else 1),
                -((i - 1) // 2) - 1
            )
            
            output += place_lutmux(loc, self.puf_index, self.depth - i, False)
            output += place_lutmux(loc, self.puf_index, self.depth - i, True)

        output += place_activator(
            loc     = self.location + Location(0, -(self.depth // 2)),
            puf_idx = self.puf_index,
            down    = False
        )

        output += place_activator(
            loc     = self.location + Location(0, -(self.depth // 2)),
            puf_idx = self.puf_index,
            down    = True
        )

        return output

@dataclass(init = True)
class Sector:
    base: Location
    cols: int
    rows: int

    def get_slot_locations(self) -> List[Location]:
        slots = []

        for i in range(self.rows):
            for j in range(self.cols):
                slots.append(self.base + (
                    (j * SLOT_WIDTH),
                    (i * SLOT_HEIGHT)
                ))
        
        return slots

    def get_slots(self, depth: int = 32, carrytap: CarryTap = (0, 0), start_index: int = 0) -> List[Slot]:
        
        locs = self.get_slot_locations()
        slots = []

        for i, loc in enumerate(locs):
            slots.append(
                Slot(
                    puf_index = start_index + i,
                    location  = loc,
                    carrytap  = carrytap,
                    depth     = depth
                )
            )

        return slots

QUAD_SECTORS = [
    Sector(Location(0, 99), 11, 1),
    Sector(Location(22, 99), 11, 1),
    Sector(Location(0, 16), 11, 1),
    Sector(Location(22, 16), 11, 1)
]



def place_lutmux(loc: Location, puf_idx: int, chain_idx: int, down: bool) -> str:
    return f'''
set_property BEL {"C" if down else "D"}6LUT [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/CHAIN_INST/CHAIN_GEN_{"DOWN" if down else "UP"}[{chain_idx}].MUX_INST}}]
set_property LOC SLICE_X{loc.x}Y{loc.y} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/CHAIN_INST/CHAIN_GEN_{"DOWN" if down else "UP"}[{chain_idx}].MUX_INST}}]'''

def place_activator(loc: Location, puf_idx: int, down: bool) -> str:
    return f'''
set_property BEL {"C" if down else "D"}FF [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/STARTER_INST/activator{"1" if down else "0"}}}]
set_property LOC SLICE_X{loc.x}Y{loc.y} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/STARTER_INST/activator{"1" if down else "0"}}}]'''

def place_arbiter_tapcarry(loc: Location, puf_idx: int, dff: str = 'CFF') -> str:
    return f'''
set_property BEL {dff} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/dff}}]
set_property LOC SLICE_X{loc.x}Y{loc.y} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/dff}}]
set_property BEL CARRY4 [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/delay}}]
set_property LOC SLICE_X{loc.x}Y{loc.y} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/delay}}]'''


