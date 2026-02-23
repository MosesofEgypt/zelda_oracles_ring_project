from ..const import *
from .const import *
from .. import util
from . import asm, const

def prepare_combo_swimming_patches(**kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    patch_data = [
        [LINK_DIVING_CHECK, asm.LINK_DIVING_CHECK_ASM],
        [SWIMMING_CHECK0,   asm.NEW_SWIMMING_CHECK0_ASM,   asm.ORIG_SWIMMING_CHECK0_ASM],
        [SWIMMING_CHECK1,   asm.NEW_SWIMMING_CHECK1_ASM,   asm.ORIG_SWIMMING_CHECK1_ASM],
        ]
    kw["is_ages"] and patch_data.extend([
        [UNDERWATER_ITEM_B1, asm.UNDERWATER_ITEM_B1_ASM],
        [UNDERWATER_ITEM_B0, asm.NEW_UNDERWATER_ITEM_B0_ASM, asm.ORIG_UNDERWATER_ITEM_B0_ASM],
        [SWIM_CHECK,         asm.NEW_SWIM_CHECK_ASM,         asm.ORIG_SWIM_CHECK_ASM],
        ])

    return [util.alloc_patch(*args, **kw) for args in patch_data]
