
from pathlib import Path
from settings import Settings

import re
from utils import info, good, error
from os import name as osname
from os.path import exists as fileExists
import subprocess

# TODO: Rn using the script_dir in fmt strings, fix later to use pathlib
#       In general once im back all this horrible python code needs to be cleaned up
#       and the errors handled properly

def exec_xsct_script(xsct_path: str, tcl_path: str) -> bool:
    try:
        proc = subprocess.run(
            [xsct_path, tcl_path],
            capture_output  = True,
            text            = True,
            check           = False
        )
    except FileNotFoundError:
        error('TCL_EXEC: Path not found')
        return False

    output = proc.stdout + proc.stderr
    
    # NOTE: These were not reliable, i was doing some regex but i assume
    #       it has subtly changed over versions
    #if not stream_loaded:
    #    error('Error loading bitstream')
    #    return False
    
    #good('Bitstream loaded.')

    #if not elf_loaded:
    #    error('Error loading firmware')
    #    return False
    
    
    if proc.returncode != 0:
        error(f'Invalid exit code: {proc.returncode}')
        return False
    
    return True

def reset_board(settings: Settings) -> bool:
    script = f'''# Might also hardcode the program script but for now it works
    connect
    targets {settings.gconfig.get("DEFAULT", "xsct_target")}
    rst -srst
    '''
    
    tcl_path = f'{settings.script_dir}/tcl/reset.tmp.tcl'

    with open(tcl_path, 'w') as f:
        f.write(script)
    
    info('Reseting board...')
    result = exec_xsct_script(settings.gconfig.get('PATHS', 'xsct'), tcl_path)
    
    if result:
        good('Board reset.')
    else:
        error('Unable to reset board!')
        error('This might affect results, possibly, idk')

    return result

def program_bitstream(settings: Settings, stream_name: str) -> bool:
    # load the template
    
    info('Preparing FPGA program script...')
    
    try:
        with open(f'{settings.script_dir}/tcl/program.template.tcl', 'r') as f:
            prog_template = f.read()
    except BaseException as e:
        error('Error loading template for prog script')
        return False

    ps7_init_script = Path(settings.gconfig.get('PATHS', 'root')) / 'standalone/ps_apuftune/firmware/toplevel_wrapper_hw_platform_0/ps7_init.tcl'
    
    elf = Path(settings.gconfig.get('PATHS', 'root')) /  'standalone/ps_apuftune/firmware/tune_sampler/Debug/tune_sampler.elf'
    
    if not fileExists(elf):
        error('Firmware ELF file not found! Make sure you have generated it')
        return False

    stream = Path(settings.script_dir) / f'streams/{stream_name}'

    # format it
    prog = prog_template.format(
        str(ps7_init_script).replace('\\', '\\\\'),
        str(stream).replace('\\', '\\\\'),
        str(elf).replace('\\', '\\\\')
    )
    
    # save it temporarily
    try:
        with open(f'{settings.script_dir}/tcl/prog.tmp.tcl', 'w') as f:
            f.write(prog)
    except BaseException:
        error('Error writting program script.')
        return False

    good('Script written.')

    # execute in xsct and parse result to check if it worked
    info("Executing program script...")
    result = exec_xsct_script(settings.gconfig.get('PATHS', 'xsct'), f'{settings.script_dir}/tcl/prog.tmp.tcl')

    if result:
        good('Stream & Firmware loaded.')

    return result



