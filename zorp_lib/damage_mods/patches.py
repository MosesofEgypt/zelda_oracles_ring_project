from .const import *
from .. import util
from . import asm, const

def prepare_damage_modifier_patches(
        *, l1_sword_damage=2, l2_sword_damage=3, l3_sword_damage=5,
        red_ring_atk_mod =1.0,  green_ring_atk_mod=0.75,  curse_power_ring_atk_mod=1.0,
        blue_ring_def_mod=0.5,  green_ring_def_mod=0.375, curse_power_ring_def_mod=0.0,
        gold_ring_atk_mod=0.5,  gold_ring_def_mod=0.25,   atk_mod_max=5.0, 
        holy_ring_def_mod=0.25, luck_ring_chance=0.3,     def_mod_max=0.375,
        gold_ring_heart_cutoff=4.0, curse_ring_heart_max=4.0,
        **kw
        ):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)

    red_ring_atk_mod            = max(0, min(5, red_ring_atk_mod))
    green_ring_atk_mod          = max(0, min(5, green_ring_atk_mod))
    curse_power_ring_atk_mod    = max(0, min(5, curse_power_ring_atk_mod))
    # NOTE: gold ring is capped at 7/8 because a 3 digit percentage
    #       is too much to try rendering in the description textbox
    gold_ring_atk_mod           = max(0, min(7/8, gold_ring_atk_mod))
    gold_ring_def_mod           = max(0, min(7/8, gold_ring_def_mod))
    blue_ring_def_mod           = max(0, min(1, blue_ring_def_mod))
    green_ring_def_mod          = max(0, min(1, green_ring_def_mod))
    curse_power_ring_def_mod    = max(0, min(1, curse_power_ring_def_mod))
    holy_ring_def_mod           = max(0, min(1, holy_ring_def_mod))

    curse_ring_heart_max        = max(1, min(16, curse_ring_heart_max))
    gold_ring_heart_cutoff      = max(1, min(9,  gold_ring_heart_cutoff))

    atk_mod_max                 = max(0, min(5, atk_mod_max))
    def_mod_max                 = max(0, min(5, def_mod_max + 1/8))
    luck_ring_chance            = max(0, min(126/127, luck_ring_chance))

    new_sword_damage_asm        = list(asm.ORIG_SWORD_DAMAGE_ASM)
    new_sword_damage_asm[1]     = -max(0, min(128, l1_sword_damage))
    new_sword_damage_asm[3]     = -max(0, min(128, l2_sword_damage))
    new_sword_damage_asm[5]     = -max(0, min(128, l3_sword_damage))

    kw["replace_map"].update(
        **{name: util.to_bytes(int(4*val)) for name, val in (
            [CURSE_RING_HEART_MAX,  curse_ring_heart_max],
            [GOLD_RING_HI_CUTOFF,   gold_ring_heart_cutoff],
            )},
        **{name: util.to_bytes(int(8*val)) for name, val in (
            [RED_RING_ATK_MOD,          red_ring_atk_mod],
            [GREEN_RING_ATK_MOD,        green_ring_atk_mod],
            [CURSE_POWER_RING_ATK_MOD,  curse_power_ring_atk_mod],
            [GOLD_RING_ATK_MOD,         gold_ring_atk_mod],
            [BLUE_RING_DEF_MOD,         blue_ring_def_mod],
            [GREEN_RING_DEF_MOD,        green_ring_def_mod],
            [CURSE_POWER_RING_DEF_MOD,  curse_power_ring_def_mod],
            [HOLY_RING_DEF_MOD,         holy_ring_def_mod],
            [GOLD_RING_DEF_MOD,         gold_ring_def_mod],
            [MAX_ATK_MOD,               atk_mod_max],
            [MAX_DEF_MOD0,              def_mod_max + 8],
            [MAX_DEF_MOD1,              def_mod_max],
            )},
        LUCK_RING_CHANCE = util.to_bytes(int(127.5*luck_ring_chance)),
        )

    kw["text_overrides"].update(
        RED_RING_VAL        = util.val_to_str(red_ring_atk_mod),
        CURSE_RING_VAL1     = util.val_to_str(curse_power_ring_atk_mod),
        GREEN_RING_VAL1     = util.val_to_str(green_ring_atk_mod),

        BLUE_RING_VAL       = util.val_to_str(blue_ring_def_mod),
        GREEN_RING_VAL2     = util.val_to_str(green_ring_def_mod),

        GOLD_RING_VAL1      = util.val_to_str(gold_ring_atk_mod, 2),
        GOLD_RING_VAL2      = util.val_to_str(gold_ring_def_mod, 2),
        HOLY_RING_VAL       = util.val_to_str(holy_ring_def_mod, pad=False),
        LUCK_RING_VAL       = util.val_to_str(luck_ring_chance, 2)[1:],

        CURSE_RING_VAL2     = util.val_to_str(curse_ring_heart_max,   2, percent=False),
        GOLD_RING_VAL3      = util.val_to_str(gold_ring_heart_cutoff, 1, percent=False),
        )

    patch_data = [
        [WHISP_RING_CHECK,      asm.NEW_WHISP_RING_CHECK_ASM,      asm.ORIG_WHISP_RING_CHECK_ASM],
        [CURSE_RING_HEART_CAP,  asm.CURSE_RING_HEART_CAP_ASM],
        [LINK_APPLY_DAMAGE,     asm.NEW_LINK_APPLY_DAMAGE_ASM,     asm.ORIG_LINK_APPLY_DAMAGE_ASM],
        [GOLD_RING,             asm.NEW_GOLD_RING_ASM,             asm.ORIG_GOLD_RING_ASM],
        [GOLD_RING_ICON,        asm.NEW_GOLD_RING_ICON_ASM,        asm.ORIG_GOLD_RING_ICON_ASM],
        [CURSE_POWER_RING_ICON, asm.NEW_CURSE_POWER_RING_ICON_ASM, asm.ORIG_CURSE_POWER_RING_ICON_ASM],
        [CURSE_ARMOR_RING_ICON, asm.NEW_CURSE_ARMOR_RING_ICON_ASM, asm.ORIG_CURSE_ARMOR_RING_ICON_ASM],
        [CURSE_ARMOR_DAMAGE,    asm.CURSE_ARMOR_DAMAGE_ASM],
        [ARMOR_RING2,           asm.ARMOR_RING2_ASM],
        [ARMOR_RING1,           asm.ARMOR_RING1_ASM],
        [ARMOR_RING0,           asm.NEW_ARMOR_RING0_ASM,           asm.ORIG_ARMOR_RING0_ASM],
        [POWER_RING,            asm.NEW_POWER_RING_ASM,            asm.ORIG_POWER_RING_ASM],
        [DBL_EDGE_RING,         asm.NEW_DBL_EDGE_RING_ASM,         asm.ORIG_DBL_EDGE_RING_ASM],
        [SWORD_DAMAGE,          new_sword_damage_asm,              asm.ORIG_SWORD_DAMAGE_ASM],
        ]
    return [util.alloc_patch(*args, **kw) for args in patch_data]
