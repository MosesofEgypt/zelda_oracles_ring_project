from .. import util
from ..combo_sword.const import SWORD_BEAM_LIMIT, MAX_BEAMS

# the banks that the patches should apply to
PATCH_BANKS = dict(
    PUNCH_HADOUKEN  = 6,
    PUNCH_CHECK0    = 6,
    PUNCH_CHECK1    = 6,

    BRACELET_PUNCH0 = 6,
    BRACELET_PUNCH1 = 6,

    HADOUKEN_SEED0  = 7,
    HADOUKEN_SEED1  = 7,
    HADOUKEN_SEED2  = 7,
    HADOUKEN_SEED3  = 7,

    SUPER_PUNCH0    = 7,
    SUPER_PUNCH1    = 7,
    SUPER_PUNCH2    = 7,
    SUPER_PUNCH3    = 7,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

REPLACE_MAP = dict(
    SWORD_BEAM_LIMIT    = util.to_bytes(2),
    )

globals().update({name: name for name in (*PADDING_REPLACE_MAP, *REPLACE_MAP)})
