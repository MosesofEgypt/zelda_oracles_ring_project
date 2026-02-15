from .. import util

# the banks that the patches should apply to
PATCH_BANKS = dict(
    CURSE_ARMOR_DAMAGE      = 0,

    CURSE_RING_HEART_CAP    = 6,
    LINK_APPLY_DAMAGE       = 6,
    DBL_EDGE_RING           = 6,
    ARMOR_RING0             = 6,
    ARMOR_RING1             = 6,
    ARMOR_RING2             = 6,

    POWER_RING              = 7,
    SWORD_DAMAGE            = 7,
    GOLD_RING               = 7,

    GOLD_RING_ICON          = 28,
    CURSE_ARMOR_RING_ICON   = 28,
    CURSE_POWER_RING_ICON   = 28,
    )
AGES_PATCH_BANKS = dict(
    WHISP_RING_CHECK        = 13,
    )

SEAS_PATCH_BANKS = dict(
    WHISP_RING_CHECK        = 12,
    )

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

REPLACE_MAP = dict(
    # NOTE: values are in multiples of 8, so 150% would be 0xc
    RED_RING_ATK_MOD            = util.to_bytes(8),
    GREEN_RING_ATK_MOD          = util.to_bytes(6),
    CURSE_POWER_RING_ATK_MOD    = util.to_bytes(8),
    GOLD_RING_ATK_MOD           = util.to_bytes(4),

    BLUE_RING_DEF_MOD           = util.to_bytes(4),
    GREEN_RING_DEF_MOD          = util.to_bytes(3),
    CURSE_POWER_RING_DEF_MOD    = util.to_bytes(0),
    GOLD_RING_DEF_MOD           = util.to_bytes(2),

    HOLY_RING_DEF_MOD           = util.to_bytes(2),
    LUCK_RING_CHANCE            = util.to_bytes(int(127.5*0.3)),
    # so, even though damage to link is handled in 1/8 hearts, his
    # actual health is tracked in 1/4 hearts(the code subtracts 1
    # from his health for every 2 damage till it's less than 2).
    GOLD_RING_HI_CUTOFF         = util.to_bytes(4*4),
    CURSE_RING_HEART_MAX        = util.to_bytes(4*4),

    MAX_ATK_MOD                 = util.to_bytes(8*3),  # maximum of 300% damage dealt
    MAX_DEF_MOD0                = util.to_bytes(64+4), # == 0x40 + MOD1
    MAX_DEF_MOD1                = util.to_bytes(4),    # == 8*(min_damage_percent) + 1
    )

globals().update({name: name for name in (*PADDING_REPLACE_MAP, *REPLACE_MAP)})
