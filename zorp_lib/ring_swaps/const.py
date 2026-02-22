# the banks that the patches should apply to
PATCH_BANKS = dict(
    RING_DROP_SWAP2     = 11,

    RING_DROP_SWAP0     = 22,
    RING_DROP_SWAP1     = 22,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
