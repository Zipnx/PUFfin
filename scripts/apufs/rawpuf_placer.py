
from typing import Tuple
import argparse

Location = Tuple[int, int]

# used when not specified by args
TOPLEFT: Location = (120, 60)
DIMENSIONS = (32, 32)
#PREFIX = 'APUF_INST/'
PREFIX = 'design_1_i/LUT_APUF_Raw_AXI_0/U0/LUT_APUF_Raw_AXI_v1_1_S00_AXI_inst/RAW_APUF_INST/U0/APUF_INST/'

def place_lutmux(loc: Location, puf_idx: int, chain_idx: int, down: bool) -> str:

    return f'''
set_property BEL {"C" if down else "D"}6LUT [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/CHAIN_INST/CHAIN_GEN_{"DOWN" if down else "UP"}[{chain_idx}].MUX_INST}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/CHAIN_INST/CHAIN_GEN_{"DOWN" if down else "UP"}[{chain_idx}].MUX_INST}}]
    '''

def place_activator(loc: Location, puf_idx: int, down: bool) -> str:

    return f'''
set_property BEL {"C" if down else "D"}FF [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/STARTER_INST/activator{"1" if down else "0"}}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/STARTER_INST/activator{"1" if down else "0"}}}]'''

def place_arbiter(loc: Location, puf_idx: int) -> str:
    # Change: put it on AFF instead of A5FF
    return f'''
set_property BEL BFF [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/dff}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/dff}}]'''

def place_arbiter_lutdelay(loc: Location, puf_idx: int) -> str:
    # Change: put it on AFF instead of A5FF
    return f'''
set_property BEL BFF [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/dff}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/dff}}]
set_property BEL A5LUT [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/delay}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/delay}}]'''

def place_arbiter_tapcarry(loc: Location, puf_idx: int) -> str:
    # Change: put it on AFF instead of A5FF
    return f'''
set_property BEL CFF [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/dff}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/dff}}]
set_property BEL CARRY4 [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/delay}}]
set_property LOC SLICE_X{loc[0]}Y{loc[1]} [get_cells {{{PREFIX}N_APUF_GEN[{puf_idx}].N_APUF_INST/ARBITER_INST/delay}}]'''

def place_puf(args, loc: Location, puf_idx: int) -> str:
    output = ''
    
    output += place_arbiter_tapcarry((loc[0] + 1, loc[1]), puf_idx)
    
    '''
    for i in range(args.d):
        
        x = loc[0] + (1 if i % 2 == 0 else 0)
        y = loc[1] - (i // 2) - 1

        output += place_lutmux( (x,y), puf_idx, args.d - i, False)
        output += place_lutmux( (x,y), puf_idx, args.d - i, True)
    '''

    for i in range(args.d):
        x = loc[0] + (0 if i % 2 == 0 else 1)
        y = loc[1] - ((i - 1) // 2) - 1

        output += place_lutmux( (x,y), puf_idx, args.d - i, False)
        output += place_lutmux( (x,y), puf_idx, args.d - i, True)
        

    output += place_activator( (loc[0], loc[1] - args.d // 2), puf_idx, False )
    output += place_activator( (loc[0], loc[1] - args.d // 2), puf_idx, True )

    return output

def place_pufs(args) -> str:
    
    # note: i made the activators and dffs share a CLB when stacked
    puf_height = (args.d // 2) + 1

    output = ''
    loc = (args.x, args.y)

    for i in range(args.w):

        placement_loc = (loc[0] + (i % args.s) * 2, loc[1] - (i // args.s) * puf_height)

        output += place_puf(args, placement_loc, i)
    
    return output

def ila_debug(args) -> str:

    output = '''create_debug_core u_ila_0 ila
set_property ALL_PROBE_SAME_MU true [get_debug_cores u_ila_0]
set_property ALL_PROBE_SAME_MU_CNT 1 [get_debug_cores u_ila_0]
set_property C_ADV_TRIGGER false [get_debug_cores u_ila_0]
set_property C_DATA_DEPTH 4096 [get_debug_cores u_ila_0]
set_property C_EN_STRG_QUAL false [get_debug_cores u_ila_0]
set_property C_INPUT_PIPE_STAGES 0 [get_debug_cores u_ila_0]
set_property C_TRIGIN_EN false [get_debug_cores u_ila_0]
set_property C_TRIGOUT_EN false [get_debug_cores u_ila_0]
set_property port_width 1 [get_debug_ports u_ila_0/clk]
connect_debug_port u_ila_0/clk [get_nets [list CLK_WIZ_INST/inst/ila_clk]]'''
    
    for i in range(args.w):
        output += f'''set_property PROBE_TYPE DATA [get_debug_ports u_ila_0/probe{i}]
set_property port_width 2 [get_debug_ports u_ila_0/probe{i}]
connect_debug_port u_ila_0/probe{i} [get_nets [list {{{PREFIX}N_APUF_GEN[{i}].N_APUF_INST/chain_out_sig[0]}} {{{PREFIX}N_APUF_GEN[{i}].N_APUF_INST/chain_out_sig[1]}}]]
create_debug_port u_ila_0 probe'''
    
    output += f'''set_property PROBE_TYPE TRIGGER [get_debug_ports u_ila_0/probe{args.w}]
set_property port_width 1 [get_debug_ports u_ila_0/probe{args.w}]
connect_debug_port u_ila_0/probe{args.w} [get_nets [list ipulse_IBUF]]
set_property C_CLK_INPUT_FREQ_HZ {int(args.ila * 1_000_000)} [get_debug_cores dbg_hub]
set_property C_ENABLE_CLK_DIVIDER false [get_debug_cores dbg_hub]
set_property C_USER_SCAN_CHAIN 1 [get_debug_cores dbg_hub]
connect_debug_port dbg_hub/clk [get_nets u_ila_0_ila_clk]'''
    
    return output

def main():
    parser = argparse.ArgumentParser(description = 'Placer for a custom CARRY4 APUF design')
    parser.add_argument('-x', type=int, help = 'Top left X coordinate of placement', default = TOPLEFT[0])
    parser.add_argument('-y', type=int, help = 'Top left Y coordinate of placement', default = TOPLEFT[1])
    parser.add_argument('-w', type=int, help = 'Response bit width', default = DIMENSIONS[0])
    parser.add_argument('-d', type=int, help = 'Challenge bit width', default = DIMENSIONS[1])
    parser.add_argument('-s', type=int, help = 'Stack width (DEFAULT=11 to fit on a zybo clock region)', default = 11)
    parser.add_argument('-o', type=str, help = 'Filepath to save the placement')
    parser.add_argument('--ila', type=int, help = 'Used to add ILA to the xdc (Parameter is the sample freq in MHz)')

    args = parser.parse_args()
    
    print(f'[*] Placing at topleft: X={args.x} Y={args.y}')
    print(f'[*] Generating for CHALL={args.d} and WIDTH={args.w}\n')
    print('='*30)
    print()
    
    placement = place_pufs(args).replace('\n    \n', '\n')

    if args.ila:
        placement += ila_debug(args)
    
    if not args.o:
        print(placement)
    
    if not args.o: return
    
    with open(args.o, 'w') as f:
        f.write(placement + '\n')

    print(f'[+] Saved the placement to "{args.o}"')

if __name__ == "__main__":
    main()
