# the banks that the patches should apply to
PATCH_BANKS = dict(
    TOSS_RING_TEST0 = 0,
    TOSS_RING_TEST1 = 0,

    HASTE_RING0     = 5,
    HASTE_RING1     = 5,

    ADVANCE_RING0   = 5,
    ADVANCE_RING1   = 5,

    STEADFAST_RING0 = 6,
    STEADFAST_RING1 = 6,

    PUNCH_WITH_ITEM = 6,

    FEATHER_SPEED0  = 6,
    FEATHER_SPEED1  = 6,

    POTION_CHECK0   = 6,
    POTION_CHECK1   = 6,

    BOMB_RADIUS0    = 7,
    BOMB_RADIUS1    = 7,
    BOMB_RADIUS2    = 7,

    HASTE_RING_ICON = 28,
    FAIRYS_RING_ICON= 28,

    DISCOVERY_RING0 = 63,
    DISCOVERY_RING1 = 63,
    )
AGES_PATCH_BANKS = dict(
    SWIMMERS_RING0  = 5,
    SWIMMERS_RING1  = 5,

    SOMARIA_PRIO    = 6,
    )
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
