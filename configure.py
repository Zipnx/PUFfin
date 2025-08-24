
import configparser
from pathlib import Path
from os import name as os_name
from os.path import isdir  as isDirectory
from os.path import exists as fileExists 

try:
    import colorama
    colorama.init()
    COLORAMA = True
except BaseException:
    COLORAMA = False


if os_name == 'nt':
    IS_WIN = True
else:
    IS_WIN = False

VIVADO = 'vivado' if not IS_WIN else 'vivado.bat'
XSCT   = 'xsct'   if not IS_WIN else 'xsct.bat'

COLOR = not IS_WIN or (IS_WIN and COLORAMA)
RED   = '\033[91m' if COLOR else ''
GREEN = '\033[92m' if COLOR else ''
BLUE  = '\033[94m' if COLOR else ''
WHITE = '\033[97m' if COLOR else ''

def info(s):  print(f'{BLUE}[*]{WHITE} {s}')
def good(s):  print(f'{GREEN}[+]{WHITE} {s}')
def error(s): print(f'{RED}[!]{WHITE} {s}')

def main():
    info(f'Platform: {"WINDOWS" if IS_WIN else "UNIX"}')
    info(f'Color Enabled: {COLOR}')

    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        # TODO: Autoresolve then ask the user with a default
        'buildcores': str(input('Enter number of cores to use for vivado jobs: ')),
        # Just so it can be manually set from the config.ini file,
        # once the target autoresolve is made, this can be removed
        'xsct_target': 2
    }
    
    try:
        xil_base = Path(input('Enter the absolute path to your xilinx install: '))
        xil_version = input('Enter your vivado version (default: 2018.3): ') or '2018.3'
    except:
        error('Invalid path')
        return
    
    if not isDirectory(xil_base):
        error('Path does not exist')
        return
    
    config['PATHS'] = {
        'root':   Path(__file__).resolve().parent,
        'vivado': xil_base / f'Vivado/{xil_version}/bin/' / VIVADO,
        'xsct':   xil_base / f'SDK/{xil_version}/bin/' / XSCT
    }

    good('Writing config to file')

    with open('config.ini', 'w') as f:
        config.write(f)

if __name__ == '__main__': main()


