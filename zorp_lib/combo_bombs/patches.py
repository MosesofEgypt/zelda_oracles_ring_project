from ..const import *
from .const import *
from .. import util
from . import asm, const

def prepare_combo_bombs_patches(**kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    patch_data = [
        [MINING_BOMB4, asm.MINING_BOMB4_ASM],
        [MINING_BOMB3, asm.MINING_BOMB3_ASM],
        [MINING_BOMB1, asm.MINING_BOMB1_ASM],
        [REMOTE_BOMB3, asm.REMOTE_BOMB3_ASM],
        [REMOTE_BOMB1, asm.REMOTE_BOMB1_ASM],
        [MINING_BOMB2, asm.NEW_MINING_BOMB2_ASM, asm.ORIG_MINING_BOMB2_ASM],
        [MINING_BOMB0, asm.NEW_MINING_BOMB0_ASM, asm.ORIG_MINING_BOMB0_ASM],
        [REMOTE_BOMB2, asm.NEW_REMOTE_BOMB2_ASM, asm.ORIG_REMOTE_BOMB2_ASM],
        [REMOTE_BOMB0, asm.NEW_REMOTE_BOMB0_ASM, asm.ORIG_REMOTE_BOMB0_ASM],
        ]
    return [util.alloc_patch(*args, **kw) for args in patch_data]
