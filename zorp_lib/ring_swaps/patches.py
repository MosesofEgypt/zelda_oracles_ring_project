from ..const import *
from .const import *
from .. import util
from . import asm, const

def prepare_ring_swap_patches(**kw):
    patch_data = []
    if kw.get("is_ages"):
        patch_data.extend([
            [RING_DROP_SWAP1, asm.NEW_RING_DROP_SWAP1_ASM, asm.ORIG_RING_DROP_SWAP1_ASM],
            [RING_DROP_SWAP0, asm.NEW_RING_DROP_SWAP0_ASM, asm.ORIG_RING_DROP_SWAP0_ASM],
            ])
    else:
        patch_data.extend([
            [RING_DROP_SWAP2, asm.NEW_RING_DROP_SWAP2_ASM, asm.ORIG_RING_DROP_SWAP2_ASM],
            ])
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    return [util.alloc_patch(*args, **kw) for args in patch_data]
