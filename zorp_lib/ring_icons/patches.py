from .const import *
from .. import util
from . import asm, const


def prepare_ring_icon_patches(**kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    patch_data = [
        [FRIENDSHIP_RING_ICON,  asm.NEW_FRIENDSHIP_RING_ICON_ASM,  asm.ORIG_FRIENDSHIP_RING_ICON_ASM],
        [STEADFAST_RING_ICON,   asm.NEW_STEADFAST_RING_ICON_ASM,   asm.ORIG_STEADFAST_RING_ICON_ASM],
        [GREEN_JOY_RING_ICON,   asm.NEW_GREEN_JOY_RING_ICON_ASM,   asm.ORIG_GREEN_JOY_RING_ICON_ASM],
        [GOLD_JOY_RING_ICON,    asm.NEW_GOLD_JOY_RING_ICON_ASM,    asm.ORIG_GOLD_JOY_RING_ICON_ASM],
        [GASHA_RING_ICON,       asm.NEW_GASHA_RING_ICON_ASM,       asm.ORIG_GASHA_RING_ICON_ASM],
        [ENERGY_RING_ICON,      asm.NEW_ENERGY_RING_ICON_ASM,      asm.ORIG_ENERGY_RING_ICON_ASM],
        [BOMBERS_RING_ICON,     asm.NEW_BOMBERS_RING_ICON_ASM,     asm.ORIG_BOMBERS_RING_ICON_ASM],
        ]
    return [util.alloc_patch(*args, **kw) for args in patch_data]
