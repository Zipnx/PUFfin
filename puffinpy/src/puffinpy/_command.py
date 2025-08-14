
from dataclasses import dataclass, field
from typing import Optional
from enum import IntEnum
import threading, struct

class Opcode(IntEnum):
    HALT            = 0
    APUF_SINGLE     = 1
    PUFKY_READ      = 2
    READ_TEMP       = 3
    APUF_BATCH      = 4
    AES_ENCRYPT     = 5
    AES_DECRYPT     = 6
    
    # Debug operations
    RAWAPUF_BATCH   = 254
    RAWAPUF_SINGLE  = 255

class ResponseFlags(IntEnum):
    ERROR       = 0x01
    RESERVED1   = 0x02
    RESERVED2   = 0x04
    RESERVED3   = 0x08
    RESERVED4   = 0x10
    RESERVED5   = 0x20
    RESERVED6   = 0x40
    RESERVED7   = 0x80

@dataclass(init = True)
class Command:
    opcode: Opcode
    data: Optional[bytes] = None
    
    # Will use raw bytes for this protocol instead of ascii, as in
    # the current ps handler, better perf, will make the PS parser later
    def pack(self) -> bytes:
        output  = struct.pack('B', self.opcode)
        output += struct.pack('>H', len(self.data) if self.data is not None else 0)
        
        if self.data:
            output += self.data

        return output

@dataclass(init = True)
class Response:
    flags: int
    size:  int
    data:  Optional[bytes]
    error: Optional[bytes]

@dataclass(init = True)
class CommandRequest:
    command: Command
    event: threading.Event = field(default_factory=threading.Event)
    response: Optional[bytes] = None
    error: Optional[bytes] = None
    size:  int = 0
    flags: int = 0
