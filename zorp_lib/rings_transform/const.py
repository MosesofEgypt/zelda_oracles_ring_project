# the banks that the patches should apply to
PATCH_BANKS = dict(
    GET_XFORM_LINK_ID_CALL0 = 5,
    GET_XFORM_LINK_ID_CALL1 = 5,

    GET_CAN_REMAP_SPRITE    = 6,
    REMAP_XFORM_LINK        = 6,
    REMAP_XFORM_LINK_NORMAL = 6,
    REMAP_XFORM_LINK_RIDING = 6,
    GET_XFORM_LINK_ID       = 6,
    GET_SPECOBJ_GFX_FRAME   = 6,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
