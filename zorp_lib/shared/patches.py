from ..const import *
from .const import *
from .. import util
from . import asm, const


def prepare_shared_patches(*, ring_stacking=True, atk_def_stacking=2, **kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    new_active_ring1_asm = (
        asm.NEW_CP_ACTIVE_RING1_BUFFED1_ASM  if atk_def_stacking > 1 else
        asm.NEW_CP_ACTIVE_RING1_BUFFED0_ASM  if atk_def_stacking > 0 else
        asm.NEW_CP_ACTIVE_RING1_NO_BUFF_ASM  if ring_stacking        else
        asm.NEW_CP_ACTIVE_RING1_NO_STACKING_ASM
        )
    patch_data = [
        [ARROW_UP_SPRITE_BLUE,    asm.ARROW_UP_SPRITE_BLUE_ASM],
        [ARROW_DOWN_SPRITE_RED,   asm.ARROW_DOWN_SPRITE_RED_ASM],
        [CALC_DAMAGE_MODIFIER,    asm.CALC_DAMAGE_MODIFIER_ASM],
        [FRAC_OF_8_MULTIPLY,      asm.FRAC_OF_8_MULTIPLY_ASM],
        [ENSURE_DAMAGE_MIN,       asm.ENSURE_DAMAGE_MIN_ASM],
        [CP_ACTIVE_RING1,         new_active_ring1_asm],
        [CP_ACTIVE_RING0,         asm.NEW_CP_ACTIVE_RING0_ASM, asm.ORIG_CP_ACTIVE_RING0_ASM],
        [EITHER_RING,             asm.EITHER_RING_ASM],
        [REMOVE_RING,             asm.REMOVE_RING_ASM],
        ]
    return [util.alloc_patch(*args, **kw) for args in patch_data]
