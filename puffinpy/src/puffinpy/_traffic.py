
import time
from typing import Deque, Tuple
from collections import deque

class TrafficTracker:
    def __init__(self, window: float = 5.0):
        self.tx: Deque[Tuple[float, int]] = deque()
        self.rx: Deque[Tuple[float, int]] = deque()

        self.tx_total = 0
        self.rx_total = 0

        self.window = window

    def tx_add(self, count: int):
        now = time.time()

        self.tx.append((now, count))
        self.tx_total += count
        self._prune_old(self.tx, now)

    def rx_add(self, count: int):
        now = time.time()

        self.rx.append((now, count))
        self.rx_total += count
        self._prune_old(self.rx, now)
    
    def rx_get_rate(self):
        rx_rate = sum(n for _, n in self.rx) / self.window
        return rx_rate
    
    def tx_get_rate(self):
        tx_rate = sum(n for _, n, in self.tx) / self.window
        return tx_rate

    def _prune_old(self, log, current):
        while log and log[0][0] < current - self.window:
            log.popleft()
