from ..const import *
from .const import *
from .. import util
from . import asm, const


def prepare_misc_patches(**kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    patch_data = [
        #[TOSS_RING_TEST1, asm.TOSS_RING_TEST1_ASM],
        #[TOSS_RING_TEST0, asm.NEW_TOSS_RING_TEST0_ASM, asm.ORIG_TOSS_RING_TEST0_ASM],
        [FAIRYS_RING_ICON,asm.NEW_FAIRYS_RING_ICON_ASM, asm.ORIG_FAIRYS_RING_ICON_ASM],
        [POTION_CHECK1,   asm.POTION_CHECK1_ASM],
        [POTION_CHECK0,   asm.NEW_POTION_CHECK0_ASM,    asm.ORIG_POTION_CHECK0_ASM],
        [ADVANCE_RING1,   asm.ADVANCE_RING1_ASM],
        [ADVANCE_RING0,   asm.NEW_ADVANCE_RING0_ASM,    asm.ORIG_ADVANCE_RING0_ASM],
        [HASTE_RING_ICON, asm.NEW_HASTE_RING_ICON_ASM,  asm.ORIG_HASTE_RING_ICON_ASM],
        [HASTE_RING1,     asm.HASTE_RING1_ASM],
        [HASTE_RING0,     asm.NEW_HASTE_RING0_ASM,      asm.ORIG_HASTE_RING0_ASM],
        [DISCOVERY_RING1, asm.DISCOVERY_RING1_ASM],
        [DISCOVERY_RING0, asm.NEW_DISCOVERY_RING0_ASM,  asm.ORIG_DISCOVERY_RING0_ASM],
        [FEATHER_SPEED1,  asm.FEATHER_SPEED1_ASM],
        [FEATHER_SPEED0,  asm.NEW_FEATHER_SPEED0_ASM,   asm.ORIG_FEATHER_SPEED0_ASM],
        [STEADFAST_RING1, asm.STEADFAST_RING1_ASM],
        [STEADFAST_RING0, asm.NEW_STEADFAST_RING0_ASM,  asm.ORIG_STEADFAST_RING0_ASM],
        [BOMB_RADIUS2,    asm.NEW_BOMB_RADIUS2_ASM,     asm.ORIG_BOMB_RADIUS2_ASM],
        [BOMB_RADIUS1,    asm.BOMB_RADIUS1_ASM],
        [BOMB_RADIUS0,    asm.NEW_BOMB_RADIUS0_ASM,     asm.ORIG_BOMB_RADIUS0_ASM],
        [PUNCH_WITH_ITEM, asm.NEW_PUNCH_WITH_ITEM_ASM,  asm.ORIG_PUNCH_WITH_ITEM_ASM],
        ]
    kw.get("is_ages") and patch_data.append(
        [SOMARIA_PRIO, asm.NEW_SOMARIA_PRIORITY_ASM, asm.ORIG_SOMARIA_PRIORITY_ASM]
        )
    return [util.alloc_patch(*args, **kw) for args in patch_data]
