
# the banks that the patches should apply to
PATCH_BANKS = dict(
    FRIENDSHIP_RING_ICON    = 28,
    STEADFAST_RING_ICON     = 28,
    GREEN_JOY_RING_ICON     = 28,
    GOLD_JOY_RING_ICON      = 28,
    GASHA_RING_ICON         = 28,
    ENERGY_RING_ICON        = 28,
    BOMBERS_RING_ICON       = 28,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
