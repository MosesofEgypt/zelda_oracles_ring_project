from .const import *
from .. import util
from . import asm, const


def prepare_color_ring_patches(**kw):
    patch_data = [
        [GBOY_COLOR_RING_ICON,  asm.NEW_GBOY_COLOR_RING_ICON_ASM,  asm.ORIG_GBOY_COLOR_RING_ICON_ASM],
        [RUPEE_RING_ICON,       asm.NEW_RUPEE_RING_ICON_ASM,       asm.ORIG_RUPEE_RING_ICON_ASM],
        [SLAYERS_RING_ICON,     asm.NEW_SLAYERS_RING_ICON_ASM,     asm.ORIG_SLAYERS_RING_ICON_ASM],
        [SIGN_RING_ICON,        asm.NEW_SIGN_RING_ICON_ASM,        asm.ORIG_SIGN_RING_ICON_ASM],
        [MAIN_LOOP1,            asm.MAIN_LOOP1_ASM],
        [MAIN_LOOP,             asm.NEW_MAIN_LOOP_ASM,             asm.ORIG_MAIN_LOOP_ASM],
        [ENTRYPOINT,            asm.NEW_ENTRYPOINT_ASM,            asm.ORIG_ENTRYPOINT_ASM],
        [RING_PALETTE6,         asm.RING_PALETTE6_ASM],
        [RING_PALETTE5,         asm.RING_PALETTE5_ASM],
        ]
    if kw.get("is_ages"):
        patch_data.extend([
            [RING_PALETTE4, asm.NEW_RING_PALETTE4_ASM, asm.AGES_ORIG_RING_PALETTE4_ASM],
            ])
    else:
        patch_data.extend([
            [RING_PALETTE4, asm.NEW_RING_PALETTE4_ASM, asm.SEAS_ORIG_RING_PALETTE4_ASM],
            ])
    patch_data.extend([
        [RING_PALETTE3, asm.NEW_RING_PALETTE3_ASM, asm.ORIG_RING_PALETTE3_ASM],
        [RING_PALETTE2, asm.NEW_RING_PALETTE2_ASM, asm.ORIG_RING_PALETTE2_ASM],
        [RING_PALETTE1, asm.NEW_RING_PALETTE1_ASM, asm.ORIG_RING_PALETTE1_ASM],
        [RING_PALETTE0, asm.NEW_RING_PALETTE0_ASM, asm.ORIG_RING_PALETTE0_ASM],
        ])

    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    return [util.alloc_patch(*args, **kw) for args in patch_data]
