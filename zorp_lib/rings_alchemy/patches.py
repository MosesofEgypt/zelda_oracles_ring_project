from ..const import *
from .const import *
from .. import util
from . import asm, const


def prepare_alchemy_ring_patches(
        alchemy_seed_cost=RUPEEVAL_002,
        alchemy_bomb_cost=RUPEEVAL_005,
        alchemy_bombchu_cost=RUPEEVAL_050, **kw
        ):
    kw["replace_map"].update(
        ALCHEMY_COST_SEED       = util.to_bytes(alchemy_seed_cost),
        ALCHEMY_COST_BOMB       = util.to_bytes(alchemy_bomb_cost),
        ALCHEMY_COST_BOMBCHU    = util.to_bytes(alchemy_bombchu_cost),
        )
    patch_data = [
        [ALCHEMY_RING_ICON, asm.NEW_ALCHEMY_RING_ICON_ASM, asm.ORIG_ALCHEMY_RING_ICON_ASM],
        [ALCHEMY_RING8,     asm.ALCHEMY_RING8_ASM],
        [ALCHEMY_RING7,     asm.ALCHEMY_RING7_ASM],
        [ALCHEMY_RING6,     asm.ALCHEMY_RING6_ASM],
        [ALCHEMY_RING5,     asm.ALCHEMY_RING5_ASM],
        [ALCHEMY_RING4,     asm.NEW_ALCHEMY_RING4_ASM, asm.ORIG_ALCHEMY_RING4_ASM],
        [ALCHEMY_RING3,     asm.NEW_ALCHEMY_RING3_ASM, asm.ORIG_ALCHEMY_RING3_ASM],
        [ALCHEMY_RING2,     asm.NEW_ALCHEMY_RING2_ASM, asm.ORIG_ALCHEMY_RING2_ASM],
        [ALCHEMY_RING1,     asm.NEW_ALCHEMY_RING1_ASM, asm.ORIG_ALCHEMY_RING1_ASM],
        [ALCHEMY_RING0,     asm.NEW_ALCHEMY_RING0_ASM, asm.ORIG_ALCHEMY_RING0_ASM],
        ]
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    return [util.alloc_patch(*args, **kw) for args in patch_data]
