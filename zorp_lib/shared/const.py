# the banks that the patches should apply to
PATCH_BANKS = dict(
    CP_ACTIVE_RING0         = 0,
    CP_ACTIVE_RING1         = 0,
    EITHER_RING             = 0,
    REMOVE_RING             = 0,
    FRAC_OF_8_MULTIPLY      = 0,
    CALC_DAMAGE_MODIFIER    = 0,
    ENSURE_DAMAGE_MIN       = 0,

    ARROW_UP_SPRITE_BLUE    = 2,
    ARROW_DOWN_SPRITE_RED   = 2,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
