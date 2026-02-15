from .const import *
from ..const import *
from ..shared.const import *

ORIG_RING_DROP_SWAP0_ASM = [
    # gold joy ring
    b'\x38', # flags
    b'\x26', # ring id
    b'\x54', # text id
    b'\x0e', # sfx
    ]
NEW_RING_DROP_SWAP0_ASM = list(ORIG_RING_DROP_SWAP0_ASM)
NEW_RING_DROP_SWAP0_ASM[1] = HEART_RING_L1

ORIG_RING_DROP_SWAP1_ASM = [
    # gold luck ring
    b'\x38', # flags
    b'\x1c', # ring id
    b'\x54', # text id
    b'\x0e', # sfx
    ]
NEW_RING_DROP_SWAP1_ASM = list(ORIG_RING_DROP_SWAP1_ASM)
NEW_RING_DROP_SWAP1_ASM[1] = FAIRYS_RING

ORIG_RING_DROP_SWAP2_ASM = [
    b'\xf6',    # wait 30
    # asm15 scriptHelp.linkedScript_giveRing, HEART_RING_L1
    b'\xe1', b'\xc1\x63', HEART_RING_L1,
    b'\xf6',    # wait 30
    ]
NEW_RING_DROP_SWAP2_ASM = list(ORIG_RING_DROP_SWAP2_ASM)
NEW_RING_DROP_SWAP2_ASM[3] = GOLD_JOY_RING
