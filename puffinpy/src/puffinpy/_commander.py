
import queue, serial
import struct
import threading
from typing import List, Optional, Tuple
from puffinpy._command import CommandRequest, Command, Opcode, Response, ResponseFlags
from puffinpy._settings import HCMConfig
from puffinpy._sim import sim_apuf_batch, sim_apuf_single, sim_ropuf, sim_temperature

class HCMCommander:
    def __init__(self, port: str, debug = False, simulate = False):
        
        self.port     = port
        self.is_debug = debug
        self.is_sim   = simulate
        self.config   = HCMConfig()

        if debug:
            print(f'[DEBUG] Starting HCM commander at {port=}, {debug=} {simulate=}')

        try:
            self.conn = serial.Serial(
                port     = self.port,
                baudrate = self.config.BAUD_RATE,
                timeout  = self.config.TIMEOUT
            ) if not simulate else None
        except serial.SerialException:
            raise ValueError(f'Specified port "{port}" is unavailable')

        self.command_queue = queue.Queue()
        
        self.worker_thr = threading.Thread(target = self._worker, args = ())
        self.worker_thr.daemon = True
        self.worker_thr.start()

    def push_command(self, cmd: Command) -> Response:
        req = CommandRequest(cmd)
        self.command_queue.put(req)

        completed = req.event.wait()

        if not completed:
            raise ValueError('Unable to process command')

        return Response(
            flags = req.flags,
            size  = req.size,
            data  = req.response,
            error = req.error
        )
    
    def _receive_packet(self) -> Tuple[int, int, Optional[bytes]]:
        if self.is_sim or self.conn is None:
            return (-1, 0, None)
        
        header = self.conn.read(size = 3)
        
        if len(header) == 0:
            return 24, 0x1, b'[CORE] Peer unresponsive'

        if len(header) != 3:
            return 21, 0x1, b'[CORE] Invalid header'

        # My plan rn is the response to always have a size and 1 byte of flags
        
        packet_size = struct.unpack(">H", header[:2])[0]
        flags       = header[2]

        data = self.conn.read(size = packet_size) if packet_size > 0 else None
        
        if data is not None and len(data) != packet_size:
            return 0, 0x1, b'[CORE] Received invalid data count'

        return packet_size, flags, data

    def _dispatch_command(self, req: CommandRequest):
        if self.is_sim or self.conn is None:
            if self.is_debug: print('[DEBUG] Cannot use _dispatch_command during sim')
            return

        data = req.command.pack()
        
        self.conn.write(data)

        rsize, rflags, rdata = self._receive_packet()
        
        if rsize < 0:
            req.response = b'Error dispatching command'
            return

        if (rflags & ResponseFlags.ERROR) != 0:
            req.error = rdata
            req.flags = rflags
            return
        
        req.flags = rflags
        req.response = rdata
        req.size = rsize

    def _worker(self) -> None:
        while True:
            
            cmd_req: CommandRequest = self.command_queue.get()

            try:
                self._dispatch_command(cmd_req)
            # Will handle the exceptions better later
            except BaseException as e:
                cmd_req.error = b'Unable to submit task'
                print(e)

            finally:
                cmd_req.event.set()
                self.command_queue.task_done()
    
    # TODO: Handle errors better on the builtins
    def get_temperature(self) -> float:

        if self.is_sim:
            return sim_temperature()

        cmd = Command(Opcode.READ_TEMP)
        result = self.push_command(cmd)

        if result.error is not None or result.data is None or result.size != 4: return -1

        temp = struct.unpack('<f', result.data[0:4])[0]

        return temp
    
    def rawapuf_single(self, challenge: int) -> int:

        if self.is_sim:
            return struct.unpack('>I', sim_apuf_single(challenge))[0]
        
        try:
            chall = struct.pack('>I', challenge)
        except BaseException:
            raise ValueError(f'Value {challenge} is not a valid uint32 challenge')

        cmd = Command(Opcode.RAWAPUF_SINGLE, data = chall)
        result = self.push_command(cmd)

        if result.error is not None or result.data is None or result.size != 4: return -1

        return struct.unpack('>I', result.data[0:4])[0]
    
    def rawapuf_batch(self, challenges: List[int]) -> List[int]:
        
        if len(challenges) > self.config.MAX_APUF_BATCH:
            raise ValueError(f'Cannot batch more than {self.config.MAX_APUF_BATCH} challenges')

        if self.is_sim:
            return sim_apuf_batch(challenges)

        payload = b''

        for chall in challenges:
            try:
                enc = struct.pack('>I', chall)
            except BaseException:
                raise ValueError(f'Value {chall} is not a valid uint32 challenge')
            
            payload += enc
        
        payload_len = len(payload)

        # To be sure yknow
        if payload_len + 3 > self.config.RX_BUFFER:
            raise ValueError(f'Provider cannot receive {len(payload)} bytes')
        
        cmd = Command(Opcode.RAWAPUF_BATCH, data = payload)
        res = self.push_command(cmd)

        if res.error is not None or res.data is None or res.size != payload_len:
            return []
        
        responses = []

        for i in range(0, res.size, 4):
            responses += [struct.unpack('>I', res.data[i:i+4])]

        return responses

    def ropuf(self, select: int) -> bytes:
        if select < 0 or select > self.config.MAX_ROPUF_SELECT:
            raise ValueError(f'Select "{select}" is not valid')

        if self.is_sim:
            return sim_ropuf(select)

        raise ValueError('UNIMPLEMENTED')
