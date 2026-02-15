from ..const import *
from .const import *
from .. import util
from . import asm, const

def prepare_combo_collision_patches(**kw):
    patch_data = [
        [COLLISION_BOUNCE0, asm.COLLISION_BOUNCE0_ASM],
        [COLLISION_BOUNCE1, asm.COLLISION_BOUNCE1_ASM],
        [COLLISION_CHECK1,  asm.COLLISION_CHECK1_ASM],
        [COLLISION_CHECK0,  asm.NEW_COLLISION_CHECK0_ASM, asm.ORIG_COLLISION_CHECK0_ASM],
        ]

    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    return [util.alloc_patch(*args, **kw) for args in patch_data]
