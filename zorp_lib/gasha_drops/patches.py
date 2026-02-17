from ..const import *
from .const import *
from .. import util
from . import asm, const

'''NOTES
REF:
    normal tree growth == 40 kills
    fast tree growth == 20 kills

determine tier by checking kill count(gasha ring will cut it in half):
            min kills   max kills
    tier 1:      40         100
    tier 2:      70         130
    tier 3:     100         160
    tier 4:     130         ---

REF:
    using shovel increases by 1
    getting essence increases by 150
    getting heart piece increases by 36(100 in seasons)
    getting trade item increases by 100
    getting any heart refill increases by 4
    moving screens increases by 5(except going through load door)
    playing subrosian bros/goron dance hall game increases by 30
    harvesting decreases by 200

CHANGE:
    getting essence increases by 250
    getting heart piece increases by 100
    getting trade item increases by 200
    getting any heart refill increases by 2
    moving screens increases by 2(except going through load door)
    harvesting decreases by 25%

determine chance to guarantee new ring using gasha maturity
'''

def prepare_gasha_drop_patches(**kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
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
    patch_data = [
        [RING_TIER4_TABLE,        ring_tier4_table_asm],
        [RING_TIER3_TABLE,        asm.RING_TIER3_TABLE_ASM],
        [RING_TIER2_TABLE,        asm.RING_TIER2_TABLE_ASM],
        [RING_TIER1_TABLE,        asm.RING_TIER1_TABLE_ASM],
        [RING_TIER0_TABLE,        asm.RING_TIER0_TABLE_ASM],
        [GET_RING_TIER_MASK,      asm.GET_RING_TIER_MASK_ASM],
        [GET_RINGS_OBTAINED,      asm.GET_RINGS_OBTAINED_ASM],
        [GET_RANDOM_TIERED_RING1, asm.GET_RANDOM_TIERED_RING1_ASM],
        [RING_TIER_TABLE,         asm.NEW_RING_TIERS_TABLE_ASM,       orig_ring_tiers_table_asm],
        [GET_RANDOM_TIERED_RING,  asm.NEW_GET_RANDOM_TIERED_RING_ASM, asm.ORIG_GET_RANDOM_TIERED_RING_ASM],
        [RING_TIER_MASKS,         asm.RING_TIER_MASKS_ASM,            asm.ORIG_RING_TIER_TABLES_ASM],
        [GASHA_MATURITY_TABLE,    asm.NEW_GASHA_MATURITY_TABLE_ASM,   orig_gasha_maturity_table_asm],
        ]
    0 and util.clear_rom_garbage(
        ages_garbage_map=const.AGES_BANK_GARBAGE,
        seas_garbage_map=const.SEAS_BANK_GARBAGE,
        **kw
        )
    return [util.alloc_patch(*args, **kw) for args in patch_data]
