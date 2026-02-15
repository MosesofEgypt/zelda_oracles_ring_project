from ..const import *
from .const import *
from .. import util
from . import asm, const


def prepare_hikers_ring_patches(**kw):
    patch_data = [
        [HIKERS_RING_ICON, asm.NEW_HIKERS_RING_ICON_ASM, asm.ORIG_HIKERS_RING_ICON_ASM],
        [HIKERS_RING3, asm.HIKERS_RING3_ASM],
        [HIKERS_RING2, asm.NEW_HIKERS_RING2_ASM, asm.ORIG_HIKERS_RING2_ASM],
        [HIKERS_RING1, asm.NEW_HIKERS_RING1_ASM, asm.ORIG_HIKERS_RING1_ASM],
        [HIKERS_RING0, asm.NEW_HIKERS_RING0_ASM, asm.ORIG_HIKERS_RING0_ASM]
        ]
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    return [util.alloc_patch(*args, **kw) for args in patch_data]
