from ..const import *
from .const import *
from .. import util
from . import asm, const

def prepare_combo_feather_patches(**kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    patch_data = [
        [LINK_DIVING_CHECK, asm.LINK_DIVING_CHECK_ASM],
        [FEATHER_CHECK0,    asm.NEW_FEATHER_CHECK0_ASM,   asm.ORIG_FEATHER_CHECK0_ASM],
        [FEATHER_CHECK1,    asm.NEW_FEATHER_CHECK1_ASM,   asm.ORIG_FEATHER_CHECK1_ASM],
        ]
    kw["is_ages"] and patch_data.extend([
        [SWIM_CHECK, asm.NEW_SWIM_CHECK_ASM, asm.ORIG_SWIM_CHECK_ASM],
        ])

    return [util.alloc_patch(*args, **kw) for args in patch_data]
