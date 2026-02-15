from ..const import *
from .const import *
from .. import util
from . import asm, const

def prepare_combo_sword_patches(
        *, sword_spin_capped=True, 
        super_spin_count=15, sword_beam_limit=2, super_beam_delay=50,
        light_ring_l1_cutoff=3.0, light_ring_l2_cutoff=6.0,
        **kw):
    super_spin_count            = max(1, min(MAX_SPINS, super_spin_count))
    sword_beam_limit            = max(1, min(MAX_BEAMS, sword_beam_limit))
    super_beam_delay            = max(0, min(255,       super_beam_delay))

    light_ring_l1_cutoff        = max(1, min(9, light_ring_l1_cutoff))
    light_ring_l2_cutoff        = max(1, min(9, light_ring_l2_cutoff))

    sword_spin1_asm       = (
        asm.SWORD_SPIN1_CAPPED_ASM  if sword_spin_capped else
        asm.SWORD_SPIN1_UNCAPPED_ASM
        )

    kw["replace_map"].update(
        SPIN_SWING_COUNTER    = util.to_bytes(super_spin_count*4+1),
        SWORD_BEAM_LIMIT      = util.to_bytes(sword_beam_limit),
        SUPER_BEAM_DELAY      = util.to_bytes(super_beam_delay),
        **{name: util.to_bytes(int(8*val)) for name, val in (
            [LIGHT_RING_L1_CUTOFF,      light_ring_l1_cutoff],
            [LIGHT_RING_L2_CUTOFF,      light_ring_l2_cutoff],
            )},
        )

    kw["text_overrides"].update(
        LIGHT_RING_L1_VAL   = util.val_to_str(light_ring_l1_cutoff,   1, percent=False),
        LIGHT_RING_L2_VAL   = util.val_to_str(light_ring_l2_cutoff,   1, percent=False),
        )

    patch_data = [
        [SW_BEAM_LIMIT1,    asm.SW_BEAM_LIMIT1_ASM],
        [SW_BEAM_CHARGE1,   asm.SW_BEAM_CHARGE1_ASM],
        [SWORD_SPIN1,       sword_spin1_asm],
        [SWORD_SPIN3,       asm.SWORD_SPIN3_ASM],
        [SW_BEAM_CHECK,     asm.NEW_SW_BEAM_CHECK_ASM,    asm.ORIG_SW_BEAM_CHECK_ASM],
        [SW_BEAM_LIMIT0,    asm.NEW_SW_BEAM_LIMIT0_ASM,   asm.ORIG_SW_BEAM_LIMIT0_ASM],
        [SW_BEAM_CHARGE0,   asm.NEW_SW_BEAM_CHARGE0_ASM,  asm.ORIG_SW_BEAM_CHARGE0_ASM],
        [SWORD_SPIN0,       asm.NEW_SWORD_SPIN0_ASM,      asm.ORIG_SWORD_SPIN0_ASM],
        [SWORD_SPIN2,       asm.NEW_SWORD_SPIN2_ASM,      asm.ORIG_SWORD_SPIN2_ASM],
        ]

    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    return [util.alloc_patch(*args, **kw) for args in patch_data]
