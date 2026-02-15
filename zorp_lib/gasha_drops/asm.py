from .const import *
from ..const import *
from ..opcodes import *
from ..shared.const import *


RING_TIER0_TABLE_ASM = [
    # tier0: cosmetic/low-utility
    OCTO_RING,          5,
    LIKE_LIKE_RING,     5,
    MOBLIN_RING,        5,
    SUBROSIAN_RING,     5,
    FIRST_GEN_RING,     2,
    GBOY_COLOR_RING,    4,
    PEACE_RING,         1,
    FIST_RING,          5,
    TOSS_RING,          5,
    MAPLES_RING,        1,
    GREEN_JOY_RING,     1,
    0xff,               0, # terminator
    ]

RING_TIER1_TABLE_ASM = [
    # tier1: bad-buff/mod-utility
    CURSE_POWER_RING,   5,
    RANG_RING_L1,       4,
    ARMOR_RING_L1,      2,
    CURSE_ARMOR_RING,   5,
    BOMBERS_RING,       1,
    BOMBPROOF_RING,     1,
    ZORA_RING,          3,
    HIKERS_RING,        1,
    GASHA_RING,         4,
    RED_JOY_RING,       1,
    BLUE_JOY_RING,      3,
    0xff,               0, # terminator
    ]

RING_TIER2_TABLE_ASM = [
    # tier2: mod-buff/high-utility
    POWER_RING_L2,      2,
    BLAST_RING,         1,
    RANG_RING_L2,       5,
    ARMOR_RING_L2,      2,
    GREEN_HOLY_RING,    2,
    BLUE_HOLY_RING,     2,
    RED_HOLY_RING,      2,
    ROCS_RING,          4,
    HEART_RING_L1,      1,
    STEADFAST_RING,     3,
    LIGHT_RING_L1,      1,
    0xff,               0, # terminator
    ]

RING_TIER3_TABLE_ASM = [
    # tier3: high-buff/good-utility
    ENERGY_RING,        1,
    FAIRYS_RING,        3,
    GREEN_LUCK_RING,    2,
    RED_LUCK_RING,      2,
    BLUE_LUCK_RING,     2,
    ALCHEMY_RING,       1,
    MYSTIC_SEED_RING,   3,
    LIGHT_RING_L2,      1,
    CHARGE_RING,        1,
    HEART_RING_L2,      1,
    EXPERTS_RING,       3,
    0xff,               0, # terminator
    ]

# NOTE: the below tables are ringId followed by weight within the tier
RING_TIER4_TABLE_ASM = [
    # tier4: best-buff/best-utility
    # NOTE: only available if every other tiered ring was obtained
    GREEN_RING,         1,
    GOLD_RING,          1,
    0xff,               0, # terminator
    ]

RING_TIER4_TABLE_SECRET_ASM = [
    GREEN_RING,         3,
    GOLD_RING,          3,
    # these rings are normally obtained with secrets, but
    # we'll allow them to be obtained via gasha nut if the
    # player was diligent enough to get every tier 1-4 ring
    # ages secret
    SPIN_RING,          1,
    HASTE_RING,         1,
    # seas secret
    GOLD_JOY_RING,      1,
    SWIMMERS_RING,      1,
    0xff,               0, # terminator
    ]

ORIG_GET_RANDOM_TIERED_RING_ASM = [
    # getRandomRingOfGivenTier:
    # @param        c   Ring tier
    # @param[out]   a   TREASURE_RING (to be passed to "giveTreasure")
    # @param[out]   c   Randomly chosen ring from the given tier (to be passed to "giveTreasure")
    LDH_A_A8,   H_ROM_BANK,     # ldh a,(<hRomBank)
    PUSH_AF,                    # push af
    LD_A,       0x3F,           # ld a,$3f
    LDH_A8_A,   H_ROM_BANK,     # ldh (<hRomBank),a
    SET_ROM_BANK,               # setrombank

    b'\x06\x01',                # ld b,$01
    b'\x79',                    # ld a,c
    b'\xfe\x04',                # cp $04
    b'\x28\x02',                # jr z,+
    b'\x06\x07',                # ld b,$07
    # +
    b'\x21',RING_TIER_TABLE,    # ld hl,bank3f.ringTierTable
    b'\xdf',                    # rst_addDoubleIndex
    b'\x2a',                    # ldi a,(hl)
    b'\x66',                    # ld h,(hl)
    b'\x6f',                    # ld l,a

    b'\xcd',GET_RANDOM_NUMBER,  # call getRandomNumber

    b'\xa0',                    # and b
    b'\x4f',                    # ld c,a
    b'\x06\x00',                # ld b,$00
    b'\x09',                    # add hl,bc
    b'\x4e',                    # ld c,(hl)

    b'\xf1',                    # pop af
    b'\xe0',H_ROM_BANK,         # ldh (<hRomBank),a
    SET_ROM_BANK,               # setrombank

    b'\x3e\x2d',                # ld a,TREASURE_RING
    b'\xc9',                    # ret
    ]
NEW_GET_RANDOM_TIERED_RING_ASM = list(ORIG_GET_RANDOM_TIERED_RING_ASM)

ORIG_DETERMINE_GASHA_DROP_ASM = [
    # Get a value of 0-4 in 'c', based on the range of
    # wGashaMaturity (0 = best prizes, 4 = worst prizes)
    b'\x0e\x00',                    # ld c,$00
    b'\x21',W_GASHA_MATURITY_H,     # ld hl,wGashaMaturity+1
    b'\x3a',                        # ldd a,(hl)
    b'\xcb\x3f',                    # srl a
    b'\x20\x0c',                    # jr nz,++
    b'\x7e',                        # ld a,(hl)
    b'\x1f',                        # rra
    b'\x21',GASHA_MATURITY_LEVELS,  # ld hl,@gashaMaturityValues
    # --
    b'\xbe',                        # cp (hl)
    b'\x30\x04',                    # jr nc,++
    b'\x23',                        # inc hl
    b'\x0c',                        # inc c
    b'\x18\xf9',                    # jr --
    # ++
    # Get the probability distribution to use, based on
    # 'c' (above) and which gasha spot this is (var03)
    b'\x1e\x03',                    # ld e,Interaction.var03
    b'\x1a',                        # ld a,(de)
    b'\x21',GASHA_SPOT_RANKS,       # ld hl,@gashaSpotRanks
    b'\xd7',                        # rst_addAToHl
    b'\x7e',                        # ld a,(hl)
    b'\xd7',                        # rst_addAToHl

    # a = c*10
    b'\x79',                        # ld a,c
    b'\x87',                        # add a
    b'\x4f',                        # ld c,a
    b'\x87',                        # add a
    b'\x87',                        # add a
    b'\x81',                        # add c

    b'\xd7',                        # rst_addAToHl
    # call getRandomIndexFromProbabilityDistribution

    # If it would be a potion, but he has one already, just refill his health
    b'\x78',                        # ld a,b
    b'\xfe\x06',                    # cp GASHATREASURE_POTION
    #b'\x20\x',                      # jr nz,@noPotion

    b'\x3e',TREASURE_POTION,        # ld a,TREASURE_POTION
    b'\xcd',CHECK_HAVE_TREASURE,    # call checkTreasureObtained
    #b'\x30\x',                      # jr nc,@decGashaMaturity

    
    b'\x21',W_LINK_MAX_HEALTH,      # ld hl,wLinkMaxHealth
    b'\x3a',                        # ldd a,(hl)
    b'\x77',                        # ld (hl),a
    ]

# NOTE: can put the extra code for the new function here
#       in the space cleared of gashaTreasures
ORIG_GET_GASHA_RING_TIER_ASM = [
    b'\x78',                # ld a,b
    b'\x1e\x02',            # ld e,Interaction.subid
    b'\x12',                # ld (de),a
    b'\x21',GASHA_TREASURES,# ld hl,@gashaTreasures
    b'\xdf',                # rst_addDoubleIndex
    b'\x2a',                # ldi a,(hl)
    b'\x4e',                # ld c,(hl)
    b'\x3e\x2d',            # ld a,TREASURE_RING
    b'\x20\x03',            # jr nz,+
    ]

AGES_ORIG_RING_TIERS_TABLE_ASM = [
    b'\x9c\x47', # .dw @tier0
    b'\xa4\x47', # .dw @tier1
    b'\xac\x47', # .dw @tier2
    b'\xb4\x47', # .dw @tier3
    b'\xbc\x47', # .dw @tier4
    ]
SEAS_ORIG_RING_TIERS_TABLE_ASM = [
    b'\xbb\x47', # .dw @tier0
    b'\xc3\x47', # .dw @tier1
    b'\xcb\x47', # .dw @tier2
    b'\xd3\x47', # .dw @tier3
    b'\xdb\x47', # .dw @tier4
    ]
NEW_RING_TIERS_TABLE_ASM = [
    # NOTE: just so i don't have to go with the old confusing naming
    #       convention of tier 0 being the 2nd best and 4 being the
    #       best tier, we're reversing it. this way tier quality will
    #       increase with the tier number. to keep from having to update
    #       a ton of code, we're sticking with the original tier order
    RING_TIER3_TABLE,
    RING_TIER2_TABLE,
    RING_TIER1_TABLE,
    RING_TIER0_TABLE,
    RING_TIER4_TABLE,
    ]

ORIG_RING_TIER_TABLES_ASM = [
    EXPERTS_RING,   CHARGE_RING,    FIRST_GEN_RING, BOMBPROOF_RING,
    ENERGY_RING,    DBL_EDGED_RING, CHARGE_RING,    DBL_EDGED_RING,
    POWER_RING_L2,  PEACE_RING,     HEART_RING_L2,  RED_JOY_RING,
    GASHA_RING,     PEACE_RING,     WHIMSICAL_RING, PROTECTION_RING,
    MAPLES_RING,    TOSS_RING,      RED_LUCK_RING,  WHISP_RING,
    ZORA_RING,      FIST_RING,      QUICKSAND_RING, ROCS_RING,
    CURSED_RING,    LIKE_LIKE_RING, BLUE_LUCK_RING, GREEN_HOLY_RING,
    BLUE_HOLY_RING, RED_HOLY_RING,  OCTO_RING,      MOBLIN_RING,
    # we only need 32 bytes to overwrite with the tier masks, so we're
    # ignoring these, even though they actually are part of the table
    #GREEN_RING,     RANG_RING_L2
    ]


for ring_list in [
        RING_TIER0_TABLE_ASM, RING_TIER1_TABLE_ASM, RING_TIER2_TABLE_ASM,
        RING_TIER3_TABLE_ASM, RING_TIER4_TABLE_ASM, RING_TIER4_TABLE_SECRET_ASM
        ]:
    total_weight = sum(ring_list[1::2])
    curr_cutoff  = 0
    for i, v in enumerate(ring_list[1::2]):
        ring_list[i*2] = int(curr_cutoff)
        curr_cutoff   += 255*(v/total_weight)


RING_TIER_MASKS_ASM = list(
    sum(1<<i for i in ring_list[::2])
    for ring_list in [
       RING_TIER0_TABLE_ASM, RING_TIER1_TABLE_ASM,
       RING_TIER2_TABLE_ASM, RING_TIER3_TABLE_ASM,
       ])
# 8 bytes per tier, indicating how to mask wObtainedRings
# to figure out if link has every ring in this tier
RING_TIER_MASKS_ASM = [
    bytes([(RING_TIER_MASKS_ASM[i//8] >> (8*(i%8)))&0xFF])
    for i in range(8*4)
    ]
