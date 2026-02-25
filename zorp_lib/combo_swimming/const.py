# the banks that the patches should apply to
PATCH_BANKS = dict(
    SWIM_CHECK          = 5,

    SWIMMING_CHECK0     = 6,
    SWIMMING_CHECK1     = 6,

    UNDERWATER_ITEM_B0  = 6,
    UNDERWATER_ITEM_B1  = 6,

    LINK_DIVING_CHECK   = 6,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
