from ..const import *
from .const import *
from .. import util
from . import asm, const


def prepare_mystic_seed_ring_patches(**kw):
    patch_data = [
        [MYSTIC_SEED_RING_ICON, asm.NEW_MYSTIC_SEED_RING_ICON_ASM, asm.ORIG_MYSTIC_SEED_RING_ICON_ASM],
        [MYSTIC_SEED_RING9,     asm.MYSTIC_SEED_RING9_ASM],
        [MYSTIC_SEED_RING8,     asm.MYSTIC_SEED_RING8_ASM],
        [MYSTIC_SEED_RING7,     asm.NEW_MYSTIC_SEED_RING7_ASM, asm.ORIG_MYSTIC_SEED_RING7_ASM],
        ]
    if kw.get("is_ages"):
        patch_data.extend([
            [MYSTIC_SEED_RING5, asm.AGES_MYSTIC_SEED_RING5_ASM],
            [MYSTIC_SEED_RING4, asm.AGES_NEW_MYSTIC_SEED_RING4_ASM, asm.AGES_ORIG_MYSTIC_SEED_RING4_ASM],
            [MYSTIC_SEED_RING3, asm.AGES_MYSTIC_SEED_RING3_ASM],
            [MYSTIC_SEED_RING2, asm.AGES_NEW_MYSTIC_SEED_RING2_ASM, asm.AGES_ORIG_MYSTIC_SEED_RING2_ASM],
            [MYSTIC_SEED_RING1, asm.AGES_MYSTIC_SEED_RING1_ASM],
            [MYSTIC_SEED_RING0, asm.AGES_NEW_MYSTIC_SEED_RING0_ASM, asm.AGES_ORIG_MYSTIC_SEED_RING0_ASM],
            ])
    else:
        patch_data.extend([
            [MYSTIC_SEED_RING6, asm.SEAS_NEW_MYSTIC_SEED_RING6_ASM, asm.SEAS_ORIG_MYSTIC_SEED_RING6_ASM],
            [MYSTIC_SEED_RING5, asm.SEAS_MYSTIC_SEED_RING5_ASM],
            [MYSTIC_SEED_RING4, asm.SEAS_NEW_MYSTIC_SEED_RING4_ASM, asm.SEAS_ORIG_MYSTIC_SEED_RING4_ASM],
            [MYSTIC_SEED_RING3, asm.SEAS_MYSTIC_SEED_RING3_ASM],
            [MYSTIC_SEED_RING2, asm.SEAS_NEW_MYSTIC_SEED_RING2_ASM, asm.SEAS_ORIG_MYSTIC_SEED_RING2_ASM],
            [MYSTIC_SEED_RING1, asm.SEAS_MYSTIC_SEED_RING1_ASM],
            [MYSTIC_SEED_RING0, asm.SEAS_NEW_MYSTIC_SEED_RING0_ASM, asm.SEAS_ORIG_MYSTIC_SEED_RING0_ASM],
            ])
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    return [util.alloc_patch(*args, **kw) for args in patch_data]
