
from dataclasses import dataclass

@dataclass(init = True)
class HCMConfig:
    BAUD_RATE: int = 115200
    TIMEOUT:   int = 2
    TX_BUFFER: int = 0x10000
    RX_BUFFER: int = 0x10000
    DEBUG_ENABLED: bool = True

    MAX_APUF_BATCH: int     = 256
    MAX_ROPUF_SELECT: int   = 3
