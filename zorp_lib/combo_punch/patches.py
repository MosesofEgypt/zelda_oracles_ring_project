from ..const import *
from .const import *
from .. import util
from . import asm, const

def prepare_combo_punch_patches(
        *, ring_stacking=True, sword_beam_limit=2, **kw
        ):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    sword_beam_limit    = max(1, min(MAX_BEAMS, sword_beam_limit))

    old_punch_check0_asm  = (
        asm.AGES_ORIG_PUNCH_CHECK0_ASM if kw["is_ages"] else
        asm.SEAS_ORIG_PUNCH_CHECK0_ASM
        )
    new_punch_check0_asm  = (
        asm.AGES_NEW_PUNCH_CHECK0_ASM  if kw["is_ages"] else
        asm.SEAS_NEW_PUNCH_CHECK0_ASM
        )
    super_punch3_asm  = (
        asm.AGES_SUPER_PUNCH3_ASM if kw["is_ages"] else
        asm.SEAS_SUPER_PUNCH3_ASM
        )

    patch_data = [
        [SUPER_PUNCH0,    asm.NEW_SUPER_PUNCH0_ASM, asm.ORIG_SUPER_PUNCH0_ASM],
        [SUPER_PUNCH2,    asm.NEW_SUPER_PUNCH2_ASM, asm.ORIG_SUPER_PUNCH2_ASM],
        [PUNCH_HADOUKEN,  asm.PUNCH_HADOUKEN_ASM],
        [PUNCH_CHECK0,    new_punch_check0_asm,     old_punch_check0_asm],
        [PUNCH_CHECK1,    asm.NEW_PUNCH_CHECK1_ASM, asm.ORIG_PUNCH_CHECK1_ASM],
        [HADOUKEN_SEED3,  asm.HADOUKEN_SEED3_ASM],
        [HADOUKEN_SEED2,  asm.NEW_HADOUKEN_SEED2_ASM, asm.ORIG_HADOUKEN_SEED2_ASM],
        [HADOUKEN_SEED1,  asm.HADOUKEN_SEED1_ASM],
        [HADOUKEN_SEED0,  asm.NEW_HADOUKEN_SEED0_ASM, asm.ORIG_HADOUKEN_SEED0_ASM],
        ]
    if ring_stacking:
        patch_data.extend([
            [SUPER_PUNCH1,  asm.SUPER_PUNCH1_ASM],
            [SUPER_PUNCH3,  super_punch3_asm],
            ])

    return [util.alloc_patch(*args, **kw) for args in patch_data]
