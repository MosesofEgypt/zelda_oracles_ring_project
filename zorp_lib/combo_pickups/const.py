# the banks that the patches should apply to
PATCH_BANKS = dict(
    HEART_CHECK_SUPER1  = 5,
    HEART_CHECK         = 5,

    JOY_RING0           = 63,
    JOY_RING1           = 63,
    JOY_RING2           = 63,
    JOY_RING3           = 63,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
