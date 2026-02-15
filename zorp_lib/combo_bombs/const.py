# the banks that the patches should apply to
PATCH_BANKS = dict(
    REMOTE_BOMB2    = 6,
    REMOTE_BOMB3    = 6,

    MINING_BOMB0    = 7,
    MINING_BOMB1    = 7,
    MINING_BOMB2    = 7,
    MINING_BOMB3    = 7,
    MINING_BOMB4    = 7,
    REMOTE_BOMB0    = 7,
    REMOTE_BOMB1    = 7,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
