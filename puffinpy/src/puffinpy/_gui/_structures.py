
from enum import Enum

class WinType(Enum):
    STATS           = 'winstats'
    APUF_INTERACT   = 'winapuf'
    APUF_SAMPLER    = 'winapufsample'
    APUF_ANALYSIS   = 'winapufanalysis'
    KEYGEN          = 'winkeygen'
    CONSOLE         = 'winconsole'
    DEBUGCON        = 'windebugcon'
    
