
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
        'buildcores': str(input('Enter number of cores to use for vivado jobs: '))
    }
    
    try:
        vivado_base = Path(input('Enter the absolute path to your vivado install: '))
    except:
        error('Invalid path')
        return
    
    if not isDirectory(vivado_base):
        error('Path does not exist')
        return

    config['PATHS'] = {
        'vivado': vivado_base / VIVADO,
        'xsct':   vivado_base / XSCT
    }
    
    good('Writing config to file')

    with open('config.ini', 'w') as f:
        config.write(f)

if __name__ == '__main__': main()


