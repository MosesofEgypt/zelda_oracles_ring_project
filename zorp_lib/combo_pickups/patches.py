from ..const import *
from .const import *
from .. import util
from . import asm, const

def prepare_combo_pickups_patches(
        *, ring_stacking=True, super_stacking=True,**kw
        ):
    new_heart_check_asm   = (
        asm.NEW_HEART_CHECK_SUPER0_ASM  if super_stacking else
        asm.NEW_HEART_CHECK_STACKED_ASM if ring_stacking else
        asm.NEW_HEART_CHECK_ASM
        )
    patch_data = [
        [HEART_CHECK_SUPER1,asm.HEART_CHECK_SUPER1_ASM],
        [HEART_CHECK,       new_heart_check_asm,    asm.ORIG_HEART_CHECK_ASM],
        [JOY_RING3,         asm.JOY_RING3_ASM],
        [JOY_RING1,         asm.JOY_RING1_ASM],
        [JOY_RING2,         asm.NEW_JOY_RING2_ASM,  asm.ORIG_JOY_RING2_ASM],
        [JOY_RING0,         asm.NEW_JOY_RING0_ASM,  asm.ORIG_JOY_RING0_ASM],
        ]
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    return [util.alloc_patch(*args, **kw) for args in patch_data]
