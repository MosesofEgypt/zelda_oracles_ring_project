# the banks that the patches should apply to
PATCH_BANKS = dict(
    VICTORY_RING2       = 6,
    VICTORY_RING3       = 6,
    VICTORY_RING7       = 6,
    VICTORY_RING8       = 6,

    VICTORY_RING4       = 7,
    VICTORY_RING5       = 7,
    VICTORY_RING6       = 7,
    
    VICTORY_RING_ICON   = 28,
    
    VICTORY_RING0       = 63,
    VICTORY_RING1       = 63,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
