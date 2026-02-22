from ..const import *
from .const import *
from .. import util
from . import asm, const


def prepare_wallet_size_patches(**kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    patch_data = [
        [DRAW_DIGIT,   asm.DRAW_DIGIT_ASM],
        [WALLET_SIZE1, asm.NEW_WALLET_SIZE1_ASM, asm.ORIG_WALLET_SIZE1_ASM],
        [WALLET_SIZE0, asm.NEW_WALLET_SIZE0_ASM, asm.ORIG_WALLET_SIZE0_ASM],
        ]
    return [util.alloc_patch(*args, **kw) for args in patch_data]
