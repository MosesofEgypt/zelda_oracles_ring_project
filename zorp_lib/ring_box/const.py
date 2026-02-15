from .. import util

# the banks that the patches should apply to
PATCH_BANKS = dict(
    BOX_CAPACITY0               = 2,
    BOX_CAPACITY1               = 2,
    BOX_CAPACITY2               = 2,

    DISP_RING_BOX_TEXT          = 2,
    DRAW_CARRIED                = 2,
    DRAW_EQUIP0                 = 2,
    DRAW_EQUIP1                 = 2,
    DRAW_EQUIP2                 = 2,
    DRAW_INV_RING_BOX           = 2,
    DRAW_INV_RING_BOX1          = 2,
    DRAW_RING0                  = 2,
    DRAW_RING1                  = 2,
    DRAW_RING_BOX               = 2,
    DRAW_RING_BOX1              = 2,
    DRAW_RING_BOX_CURSOR        = 2,
    DRAW_RING_BOX_CURSOR1       = 2,
    DRAW_RING_LIST_CURSOR       = 2,
    DRAW_RING_LIST_CURSOR1      = 2,
    EQUIP_RING                  = 2,
    EQUIP_RING1                 = 2,
    GET_RING_BOX_SPRITE_OFF     = 2,
    GET_RING_BOX_SPRITE_OFF1    = 2,
    GET_SELECTED_RING1          = 2,
    INV_RING_BOX_CURSOR_MOVED   = 2,
    INV_RING_BOX_CURSOR_MOVED1  = 2,
    IS_RING_IN_BOX              = 2,
    IS_RING_IN_BOX1             = 2,
    RING_BOX_CURSOR_MOVED       = 2,
    RING_BOX_CURSOR_MOVED1      = 2,
    RING_MAP_TABLE              = 2,
    SEL_RING_FROM_LIST          = 2,
    SEL_RING_FROM_LIST1         = 2,
    SET_SELECTED_RING           = 2,
    SHOULD_DRAW_RING0           = 2,
    SHOULD_DRAW_RING1           = 2,
    SUBMENU1_DRAW_CURSOR        = 2,
    SUBMENU1_DRAW_CURSOR1       = 2,
    SUBSCREEN1_MAIN             = 2,

    RING_BOX_MENU0              = 2,
    RING_BOX_MENU1              = 2,
    )
AGES_PATCH_BANKS = dict(
    BOX_CAPACITY3               = 30,
    BOX_CAPACITY4               = 30,
    )
SEAS_PATCH_BANKS = dict(
    BOX_CAPACITY3               = 29,
    BOX_CAPACITY4               = 29,
    )

REPLACE_MAP = dict(
    PORTAL_BOX_LEVEL            = util.to_bytes(4),
    )

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in (*PADDING_REPLACE_MAP, *REPLACE_MAP)})
