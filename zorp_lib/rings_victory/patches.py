from ..const import *
from .const import *
from .. import util
from . import asm, const


def prepare_victory_ring_patches(**kw):
    patch_data = [
        [VICTORY_RING8,     asm.VICTORY_RING8_ASM],
        [VICTORY_RING5,     asm.VICTORY_RING5_ASM],
        [VICTORY_RING3,     asm.VICTORY_RING3_ASM],
        [VICTORY_RING1,     asm.VICTORY_RING1_ASM],
        [VICTORY_RING7,     asm.NEW_VICTORY_RING7_ASM,     asm.ORIG_VICTORY_RING7_ASM],
        [VICTORY_RING6,     asm.NEW_VICTORY_RING6_ASM,     asm.ORIG_VICTORY_RING6_ASM],
        [VICTORY_RING4,     asm.NEW_VICTORY_RING4_ASM,     asm.ORIG_VICTORY_RING4_ASM],
        [VICTORY_RING2,     asm.NEW_VICTORY_RING2_ASM,     asm.ORIG_VICTORY_RING2_ASM],
        [VICTORY_RING0,     asm.NEW_VICTORY_RING0_ASM,     asm.ORIG_VICTORY_RING0_ASM],
        [VICTORY_RING_ICON, asm.NEW_VICTORY_RING_ICON_ASM, asm.ORIG_VICTORY_RING_ICON_ASM],
        ]
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    return [util.alloc_patch(*args, **kw) for args in patch_data]
