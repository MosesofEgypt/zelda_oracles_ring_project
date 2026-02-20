from ..const import *
from .const import *
from .. import util
from . import asm, const

def prepare_combo_boomerang_patches(**kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    patch_data = [
        [RANG_CHECK1, asm.RANG_CHECK1_ASM],
        [RANG_CHECK0, asm.NEW_RANG_CHECK0_ASM, asm.ORIG_RANG_CHECK0_ASM],
        [RANG_TIMER3, asm.RANG_TIMER3_ASM],
        [RANG_TIMER2, asm.RANG_TIMER2_ASM],
        [RANG_TIMER1, asm.NEW_RANG_TIMER1_ASM, asm.ORIG_RANG_TIMER1_ASM],
        [RANG_TIMER0, asm.NEW_RANG_TIMER0_ASM, asm.ORIG_RANG_TIMER0_ASM],
        ]
    return [util.alloc_patch(*args, **kw) for args in patch_data]
