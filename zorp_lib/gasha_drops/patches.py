from ..const import *
from .const import *
from .. import util
from . import asm, const

def prepare_gasha_drop_patches(
        tier_3_max_kills=70, tier_2_max_kills=90, tier_1_max_kills=110, 
        tier_2_min_kills=50, tier_1_min_kills=60, tier_0_min_kills=70, 
        **kw
        ):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    kw["replace_map"].update(
        RING_TIER_3_MAX_KILLS = max(0, min(255, tier_3_max_kills)),
        RING_TIER_2_MAX_KILLS = max(0, min(255, tier_2_max_kills)),
        RING_TIER_1_MAX_KILLS = max(0, min(255, tier_1_max_kills)),
        RING_TIER_2_MIN_KILLS = max(0, min(255, tier_2_min_kills)),
        RING_TIER_1_MIN_KILLS = max(0, min(255, tier_1_min_kills)),
        RING_TIER_0_MIN_KILLS = max(0, min(255, tier_0_min_kills)),
        )

    orig_ring_tiers_table_asm = (
        asm.AGES_ORIG_RING_TIERS_TABLE_ASM if kw.get("is_ages") else
        asm.SEAS_ORIG_RING_TIERS_TABLE_ASM
        )
    orig_gasha_maturity_table_asm = (
        asm.AGES_ORIG_GASHA_MATURITY_TABLE_ASM if kw.get("is_ages") else
        asm.SEAS_ORIG_GASHA_MATURITY_TABLE_ASM
        )
    ring_tier4_table_asm = (
        asm.RING_TIER4_TABLE_SECRET_ASM if kw.get("gasha_secret_rings") else
        asm.RING_TIER4_TABLE_ASM
        )
    game_str    = "ages" if kw.get("is_ages") else "seas"
    gasha_info  = const.GASHA_SPOT_RANK_TABLE_INFO[game_str]
    patch_data = [
        [RING_TIER4_TABLE,          ring_tier4_table_asm],
        [RING_TIER3_TABLE,          asm.RING_TIER3_TABLE_ASM],
        [RING_TIER2_TABLE,          asm.RING_TIER2_TABLE_ASM],
        [RING_TIER1_TABLE,          asm.RING_TIER1_TABLE_ASM],
        [RING_TIER0_TABLE,          asm.RING_TIER0_TABLE_ASM],
        [GET_RING_TIER_MASK,        asm.GET_RING_TIER_MASK_ASM],
        [GET_RINGS_OBTAINED,        asm.GET_RINGS_OBTAINED_ASM],
        [GET_RANDOM_TIERED_RING1,   asm.GET_RANDOM_TIERED_RING1_ASM],
        [RING_TIER_TABLE,           asm.NEW_RING_TIERS_TABLE_ASM,       orig_ring_tiers_table_asm],
        [GET_RANDOM_TIERED_RING,    asm.NEW_GET_RANDOM_TIERED_RING_ASM, asm.ORIG_GET_RANDOM_TIERED_RING_ASM],
        [RING_TIER_MASKS,           asm.RING_TIER_MASKS_ASM,            asm.ORIG_RING_TIER_TABLES_ASM],
        [GASHA_MATURITY_TABLE,      asm.NEW_GASHA_MATURITY_TABLE_ASM,   orig_gasha_maturity_table_asm],
        [SPAWN_GASHA_TREASURE,      asm.NEW_SPAWN_GASHA_TREASURE_ASM,   asm.ORIG_SPAWN_GASHA_TREASURE_ASM],
        [DETERMINE_GASHA_DROP,      asm.NEW_DETERMINE_GASHA_DROP_ASM,   asm.ORIG_DETERMINE_GASHA_DROP_ASM],
        [DEC_GASHA_MATURITY,        asm.NEW_DEC_GASHA_MATURITY_ASM,     asm.ORIG_DEC_GASHA_MATURITY_ASM],
        ]
    util.clear_rom_garbage(
        ages_garbage_map=const.AGES_BANK_GARBAGE,
        seas_garbage_map=const.SEAS_BANK_GARBAGE,
        **kw
        )

    # back this up so we can allocate the patches within the space
    # cleared of the removed code and revert back for later patches
    bank_info       = kw["patch_banks"].setdefault(
        gasha_info["bank"], [0, BANK_SIZE, BANK_SIZE]
        )
    orig_bank_info  = list(bank_info)
    bank_info[:-1]  = [
        gasha_info["start"], gasha_info["start"]+gasha_info["size"],
        ]
    patches = [
        util.alloc_patch(*args, **kw) for args in [
            [DETERMINE_RING_DROP_TIER, asm.DETERMINE_RING_DROP_TIER_ASM],
            [GET_RING_TIER_AND_CHANCE, asm.GET_RING_TIER_AND_CHANCE_ASM],
            ]
        ]
    # restore the original bank info
    bank_info[:]    = orig_bank_info

    patches.extend([
        util.alloc_patch(*args, **kw) for args in patch_data
        ])
    return patches
