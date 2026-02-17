from ..const import *
from .const import *
from .. import util
from . import asm, const


def prepare_transform_ring_patches(**kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    patch_data = [
        [GET_CAN_REMAP_SPRITE,    asm.GET_CAN_REMAP_SPRITE_ASM],
        [REMAP_XFORM_LINK,        asm.REMAP_XFORM_LINK_ASM],
        [REMAP_XFORM_LINK_NORMAL, asm.REMAP_XFORM_LINK_NORMAL_ASM],
        [REMAP_XFORM_LINK_RIDING, asm.REMAP_XFORM_LINK_RIDING_ASM],
        [GET_XFORM_LINK_ID,       asm.NEW_GET_XFORM_LINK_ID_ASM,       asm.ORIG_GET_XFORM_LINK_ID_ASM],
        [GET_SPECOBJ_GFX_FRAME,   asm.NEW_GET_SPECOBJ_GFX_FRAME_ASM,   asm.ORIG_GET_SPECOBJ_GFX_FRAME_ASM],
        [GET_XFORM_LINK_ID_CALL1, asm.NEW_GET_XFORM_LINK_ID_CALL1_ASM, asm.ORIG_GET_XFORM_LINK_ID_CALL1_ASM],
        [GET_XFORM_LINK_ID_CALL0, asm.NEW_GET_XFORM_LINK_ID_CALL0_ASM, asm.ORIG_GET_XFORM_LINK_ID_CALL0_ASM],
        ]
    return [util.alloc_patch(*args, **kw) for args in patch_data]
