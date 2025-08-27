
from os import name as osname

try:
    if osname == 'nt':
        import colorama
        colorama.init()
    COLOR = True
except BaseException:
    COLOR = False

RED   = '\033[91m' if COLOR else ''
GREEN = '\033[92m' if COLOR else ''
BLUE  = '\033[94m' if COLOR else ''
WHITE = '\033[97m' if COLOR else ''

def info(s):  print(f'{BLUE}[*]{WHITE} {s}')
def good(s):  print(f'{GREEN}[+]{WHITE} {s}')
def error(s): print(f'{RED}[!]{WHITE} {s}')
