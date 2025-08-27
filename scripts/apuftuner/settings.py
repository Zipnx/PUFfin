
from utils import info, good, error
from dataclasses import dataclass
from pathlib import Path
from os.path import exists as fileExists
import configparser

@dataclass(init = True)
class Settings:
    port: str
    script_dir:   str  = Path(__file__).resolve().parent # mistyped this
    stream_dir:   str  = ''
    force_bitgen: bool = False
    bench_samples: int = 4096
    bench_seed: int | None = None

    gconfig: configparser.ConfigParser | None = None 

    def __post_init__(self):

        self.stream_dir = self.script_dir / 'streams/'

        info('Loading puffin general config...')
        config_path = self.script_dir / '../../config.ini'
        
        if not fileExists(config_path):
            error('Config file "config.ini" does not exist!')
            error('Make sure you have run the configure.py script')
        
        self.gconfig = configparser.ConfigParser()
        self.gconfig.read(config_path)

        good('Config loaded.')
