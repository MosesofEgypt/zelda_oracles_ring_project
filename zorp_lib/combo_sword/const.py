from .. import util

# NOTE: more than 4 beams on one line causes link to disappear.
MAX_BEAMS   = 5
MAX_SPINS   = 63    # each spin is 4 frames, plus the initial.
#                     using an uint8 counter, that gives 253 values

# the banks that the patches should apply to
PATCH_BANKS = dict(
    SWORD_SPIN0     = 6,
    SWORD_SPIN1     = 6,
    SWORD_SPIN2     = 6,
    SWORD_SPIN3     = 6,
    SW_BEAM_CHECK   = 6,
    SW_BEAM_LIMIT0  = 6,
    SW_BEAM_LIMIT1  = 6,
    SW_BEAM_CHARGE0 = 6,
    SW_BEAM_CHARGE1 = 6,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

REPLACE_MAP = dict(
    SPIN_SWING_COUNTER      = util.to_bytes(15*4+1),
    SWORD_BEAM_LIMIT        = util.to_bytes(2),
    SUPER_BEAM_DELAY        = util.to_bytes(50),
    LIGHT_RING_L1_CUTOFF    = util.to_bytes(3*8),
    LIGHT_RING_L2_CUTOFF    = util.to_bytes(6*8),
    )

globals().update({name: name for name in (*PADDING_REPLACE_MAP, *REPLACE_MAP)})
