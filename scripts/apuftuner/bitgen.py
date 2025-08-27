from settings import Settings

from utils import info, good, error
from os.path import exists as fileExists
from os.path import isdir  as isDirectory

def bitstream_names() -> list[str]:
    names = []

    for ff in ['aff', 'bff', 'cff', 'dff']:
        for i in range(4):
            names += [f'{ff}_{i:02b}.bit']

    return names

def streams_exist(stream_dir: str) -> bool:
    # TODO: Make this result in only the missing ones being
    #       marked for generation
    for stream in bitstream_names():
        path = stream_dir / stream

        if isDirectory(path): return False
        if not fileExists(path): return False

    return True

def generate_bitstreams(settings: Settings) -> bool:
    info('Checking for existing streams...')
    
    if streams_exist(settings.stream_dir) and not settings.force_bitgen:
        good('Found existing streams, skipping generation')
        return True

    raise ValueError('Fully automated bitstream gen is unimplemented')


