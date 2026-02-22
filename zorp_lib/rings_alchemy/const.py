from ..util import to_bytes
from ..const import RUPEEVAL_002, RUPEEVAL_005, RUPEEVAL_050

# the banks that the patches should apply to
PATCH_BANKS = dict(
    ALCHEMY_RING1           = 5,

    ALCHEMY_RING2           = 6,
    ALCHEMY_RING3           = 6,
    ALCHEMY_RING4           = 6,
    ALCHEMY_RING5           = 6,
    ALCHEMY_RING6           = 6,
    ALCHEMY_RING7           = 6,
    ALCHEMY_RING8           = 6,

    ALCHEMY_RING0           = 7,

    ALCHEMY_RING_ICON       = 28,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()


REPLACE_MAP = dict(
    ALCHEMY_COST_SEED       = to_bytes(RUPEEVAL_002),
    ALCHEMY_COST_BOMB       = to_bytes(RUPEEVAL_005),
    ALCHEMY_COST_BOMBCHU    = to_bytes(RUPEEVAL_050),
    )

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in (*PADDING_REPLACE_MAP, *REPLACE_MAP)})
