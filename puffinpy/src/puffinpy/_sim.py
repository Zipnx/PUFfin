import random, struct
import hashlib

def sim_temperature() -> float:
    return 50 + random.uniform(-2.5, 2.5)

def sim_apuf_single(chall: int) -> bytes:
    return hashlib.sha256(chall.to_bytes(4)).digest()[:4]

def sim_apuf_batch(challenges: list[int]) -> list[int]:
    res = b''

    for chall in challenges:
        res += sim_apuf_single(chall)

    ret = []

    for i in range(0, len(challenges)*4, 4):
        ret.append(struct.unpack('>I', res[i:i+4])[0])

    return ret

def sim_ropuf(select: int) -> bytes:
    mixer = f'all your base belong to us {select}'
    return hashlib.sha256(mixer.encode()).digest()[:16]
