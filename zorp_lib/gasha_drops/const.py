# the banks that the patches should apply to
PATCH_BANKS = dict(
    GET_RANDOM_TIERED_RING  = 0,

    GET_RANDOM_TIERED_RING1 = 63,
    RING_TIER_MASKS         = 63,
    RING_TIER_TABLE         = 63,
    RING_TIER0_TABLE        = 63,
    RING_TIER1_TABLE        = 63,
    RING_TIER2_TABLE        = 63,
    RING_TIER3_TABLE        = 63,
    RING_TIER4_TABLE        = 63,
    GASHA_MATURITY_TABLE    = 63,
    GET_RING_TIER_MASK      = 63,
    GET_RINGS_OBTAINED      = 63,
    )
AGES_PATCH_BANKS = dict(
    SPAWN_GASHA_TREASURE        = 11,
    GET_RING_TIER_AND_CHANCE    = 11,
    DETERMINE_GASHA_DROP        = 11,
    DETERMINE_RING_DROP_TIER    = 11,
    DEC_GASHA_MATURITY          = 11,
    )
SEAS_PATCH_BANKS = dict(
    SPAWN_GASHA_TREASURE        = 10,
    GET_RING_TIER_AND_CHANCE    = 10,
    DETERMINE_GASHA_DROP        = 10,
    DETERMINE_RING_DROP_TIER    = 10,
    DEC_GASHA_MATURITY          = 10,
    )

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

REPLACE_MAP = dict(
    RING_TIER_3_MAX_KILLS   = 100,
    RING_TIER_2_MAX_KILLS   = 130,
    RING_TIER_1_MAX_KILLS   = 160,

    RING_TIER_2_MIN_KILLS   = 70,
    RING_TIER_1_MIN_KILLS   = 100,
    RING_TIER_0_MIN_KILLS   = 130,
    )

globals().update({name: name for name in (*PADDING_REPLACE_MAP, *REPLACE_MAP)})


# NOTE: we're going to use this huge space(16 + 250 bytes)
#       to add all our new code to the rom. we need to define
#       it so we can find and clear it first though.
GASHA_SPOT_RANK_TABLE_INFO = dict(
    ages=dict(start=0x714, size=266, bank=11,
              md5="1d37818ab8011cac6d34e371bd1a955a"),
    seas=dict(start=0x991, size=266, bank=10,
              md5="c04cd8086c1aceb42a6f66ddeda3d6c9"),
    )
AGES_BANK_GARBAGE = {
    0x0b: [GASHA_SPOT_RANK_TABLE_INFO["ages"]],
    }
SEAS_BANK_GARBAGE = {
    0x0a: [GASHA_SPOT_RANK_TABLE_INFO["seas"]],
    }
