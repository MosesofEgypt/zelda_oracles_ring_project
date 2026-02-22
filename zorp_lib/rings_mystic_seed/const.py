# the banks that the patches should apply to
PATCH_BANKS = dict(
    MYSTIC_SEED_RING2       = 6,
    MYSTIC_SEED_RING3       = 6,
    MYSTIC_SEED_RING4       = 6,
    MYSTIC_SEED_RING5       = 6,

    MYSTIC_SEED_RING0       = 7,
    MYSTIC_SEED_RING1       = 7,
    MYSTIC_SEED_RING7       = 7,
    MYSTIC_SEED_RING8       = 7,
    MYSTIC_SEED_RING9       = 7,

    MYSTIC_SEED_RING_ICON   = 28,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict(
    MYSTIC_SEED_RING6       = 6,
    )

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
