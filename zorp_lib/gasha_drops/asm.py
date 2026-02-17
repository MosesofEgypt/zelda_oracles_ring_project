from .const import *
from ..const import *
from ..opcodes import *
from ..shared.const import *


# NOTE: the below tables are ringId followed by weight within the tier
RING_TIER0_TABLE_ASM = [
    # tier0: high-buff/good-utility
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
    0xff,               # terminator
    ]

RING_TIER1_TABLE_ASM = [
    # tier1: mod-buff/high-utility
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
    0xff,               # terminator
    ]

RING_TIER2_TABLE_ASM = [
    # tier2: bad-buff/mod-utility
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
    0xff,               # terminator
    ]

RING_TIER3_TABLE_ASM = [
    # tier3: cosmetic/low-utility
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
    0xff,               # terminator
    ]

RING_TIER4_TABLE_ASM = [
    # tier4: best-buff/best-utility
    # NOTE: only available if every other tiered ring was obtained
    GREEN_RING,         1,
    GOLD_RING,          1,
    0xff,               # terminator
    ]

RING_TIER4_TABLE_SECRET_ASM = [
    # tier4: best-buff/best-utility
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
    0xff,               # terminator
    ]

AGES_ORIG_GASHA_MATURITY_TABLE_ASM = [
    0x40, 150,  # .db TREASURE_ESSENCE          150
    0x2b,  36,  # .db TREASURE_HEART_PIECE       36
    0x41, 100,  # .db TREASURE_TRADEITEM        100
    0x29,   4,  # .db TREASURE_HEART_REFILL	  4
    0x00,       # .db $00
    ]

SEAS_ORIG_GASHA_MATURITY_TABLE_ASM = [
    0x40, 150,  # .db TREASURE_ESSENCE          150
    0x2b, 100,  # .db TREASURE_HEART_PIECE      100
    0x41, 100,  # .db TREASURE_TRADEITEM        100
    0x29,   4,  # .db TREASURE_HEART_REFILL	  4
    0x00,       # .db $00
    ]

NEW_GASHA_MATURITY_TABLE_ASM = [
    0x40, 250,  # .db TREASURE_ESSENCE          250
    0x2b, 150,  # .db TREASURE_HEART_PIECE      150
    0x41, 200,  # .db TREASURE_TRADEITEM        200
    0x29,   2,  # .db TREASURE_HEART_REFILL	  2
    0x00,       # .db $00
    ]

ORIG_GET_RANDOM_TIERED_RING_ASM = [
    # getRandomRingOfGivenTier:
    # @param        c   Ring tier
    # @param[out]   a   TREASURE_RING (to be passed to "giveTreasure")
    # @param[out]   c   Randomly chosen ring from the given tier (to be passed to "giveTreasure")
    LDH_A,      H_ROM_BANK,     # ldh a,(<hRomBank)
    PUSH_AF,                    # push af
    LD_A,       0x3F,           # ld a,$3f
    LDH_A8,     H_ROM_BANK,     # ldh (<hRomBank),a
    SET_ROM_BANK,               # setrombank

    LD_B,       1,              # ld b,$01
    LD_A_C,                     # ld a,c
    CP,         4,              # cp $04
    JR_Z,     "+",              # jr z,+
    LD_B,       7,              #   ld b,$07
    Label("+"),
    LD_HL,      RING_TIER_TABLE,# ld hl,bank3f.ringTierTable
    RST_18H,                    # rst_addDoubleIndex
    LDI_A_HLP,                  # ldi a,(hl)
    LD_H_HLP,                   # ld h,(hl)
    LD_L_A,                     # ld l,a

    CALL,   GET_RANDOM_NUMBER,  # call getRandomNumber

    AND_B,                      # and b
    LD_C_A,                     # ld c,a
    LD_B,        0,             # ld b,$00
    ADD_HL_BC,                  # add hl,bc
    LD_C_HLP,                   # ld c,(hl)

    POP_AF,                     # pop af
    LDH_A8,     H_ROM_BANK,     # ldh (<hRomBank),a
    SET_ROM_BANK,               # setrombank

    LD_A,       0x2D,           # ld a,TREASURE_RING
    RET,                        # ret
    ]
NEW_GET_RANDOM_TIERED_RING_ASM = [
    # getRandomRingOfGivenTier:
    # @param        c   b0-b3: Ring tier,   b4-b7: new-ring chance
    # @param[out]   a   TREASURE_RING (to be passed to "giveTreasure")
    # @param[out]   c   Randomly chosen ring from the given tier (to be passed to "giveTreasure")
    LDH_A,      H_ROM_BANK,         # ldh a,(<hRomBank)
    PUSH_AF,                        # push af
    PUSH_BC,                        # push bc
    PUSH_DE,                        # push de
    LD_A,       0x3F,               # ld a,$3f
    LDH_A8,     H_ROM_BANK,         # ldh (<hRomBank),a
    SET_ROM_BANK,                   # setrombank

    # put the new-ring-chance into b as a value in the range 0x0F - 0xFF
    LD_A_C,                         # ld a,c
    OR,         0x0F,               # or $0f
    LD_B_A,                         # ld b,a

    # put the ring tier into c as a value in the range 0x00 - 0x04
    LD_A_C,                         # ld a,c
    AND,           7,               # and a,$07
    CP,            4,               # cp $04
    JR_C, "@tierDecided",           # jr c,@tierDecided
        LD_A,      4,               #   ld a,$04
    Label("@tierDecided"),
    LD_C_A,                         # ld c,a

    # store the original tier in d for checking if secret tier is accessible
    LD_D_C,                         # ld d,c
    DEC_C,                          # dec c

    # select a ring based on tier, decrementing it until we're either
    # not guaranteed to get a new ring, or we find a new ring to get.
    CALL, GET_RANDOM_TIERED_RING1,  # call getRandomTieredRing1

    # load the selected ring into the output register
    LD_C_E,                         # ld c,e

    POP_DE,                         # pop de
    POP_AF,                         # pop af
    LD_B_A,                         # ld b,a
    POP_AF,                         # pop af
    LDH_A8,     H_ROM_BANK,         # ldh (<hRomBank),a
    SET_ROM_BANK,                   # setrombank

    LD_A,       0x2d,               # ld a,TREASURE_RING
    RET,                            # ret
    ]

GET_RANDOM_TIERED_RING1_ASM = [
    # @param        b       New-ring chance
    # @param        c       Ring tier - 1(for incrementing)
    # @param        d       Ring tier(for checking if secret tier is accessible)
    # @param[out]   e       Randomly chosen ring from the given tier

    # cant guarantee new secret-tier rings
    LD_A_D,                         # ld a,d
    CP,             4,              # cp $04
    JR_NC,  "@selectRandomRing",    # jr nc,@selectRandomRing

    # check whether or not we're going to guarantee the ring is new
    Label("@trySelectNewRing"),
    INC_C,                          # inc c
    CALL,   GET_RANDOM_NUMBER,      # call getRandomNumber
    CP_B,                           # cp b

    # select a random ring if the guaranteed-new chance wasn't hit
    JR_NC,  "@selectRandomRing",    # jr nc,@selectRandomRing
        # use e as a counter to increment through the bytes
        XOR_A,                      #   xor a
        LD_E_A,                     #   ld e,a
        DEC_E,                      #   dec e

        Label("@tryGetNewRing"),
        PUSH_BC,                    #   push bc
        INC_E,                      #   inc e

        # get the rings obtained mask byte in b
        CALL, GET_RING_TIER_MASK,   #   call getRingTierMask
        LD_B_A,                     #   ld b,a

        # get the rings obtained byte in a
        CALL, GET_RINGS_OBTAINED,   #   call getRingsObtained

        # if the masked obtained rings byte equals the mask then we have all
        # rings under this mask. need to increment to checking the next byte
        AND_B,                      #   and b
        CP_B,                       #   cp b
        POP_BC,                     #   pop bc

        JR_Z,   "@checkNextByte",   #   jr z,@checkNextByte
            # select a random byte and bit in the masks to start with
            # and cycle through them until we find a ring we don't have
            CALL, GET_RANDOM_NUMBER,#     call getRandomNumber
            # put the byte offset in e
            LD_E_A,                 #     ld e,a
            DEC_E,                  #     dec e

            Label("@selectByteLoop"),
            # get the rings obtained mask byte in b
            INC_E,                  #     inc e
            LD_A_E,                 #     ld a,e
            AND,  0x07,             #     and $07
            LD_E_A,                 #     ld e,a
            CALL,GET_RINGS_OBTAINED,#     call getRingsObtained
            LD_B_A,                 #     ld b,a

            # mask it with the obtained rings
            CALL,GET_RING_TIER_MASK,#     call getRingTierMask
            OR_A,                   #     or a
            # mask must contain some rings
            JR_Z, "@selectByteLoop",#     jr z,@selectByteLoop
            LD_A_B,                 #     ld a,b
            # mask must contain a missing ring
            AND_HLP,                #     and (hl)
            XOR_HLP,                #     xor (hl)
            JR_Z, "@selectByteLoop",#     jr z,@selectByteLoop

            # found a byte with an unobtained ring. start with a random
            # bit and cycle through them until we hit an unobtained ring
            LD_D,       0,          #     ld d,$00
            LD_C_HLP,               #     ld c,(hl)

            # since e will contain the final ring index, we need to multiply
            # it by 8 to convert it from a byte offset into an index offset
            LD_A_E,                 #     ld a,e
            ADD_A,                  #     add a
            ADD_A,                  #     add a
            ADD_A,                  #     add a
            LD_E_A,                 #     ld e,a
            CALL, GET_RANDOM_NUMBER,#     call getRandomNumber
            AND,    0x07,           #     and $07

            # rotate mask and obtained bytes a random number of times
            Label("@selectBitLoop"),
            RRC_B,                  #     rrc b
            RRC_C,                  #     rrc c
            INC_D,                  #     inc d
            DEC_A,                  #     dec a
            JR_NZ, "@selectBitLoop",#     jr nz,@selectBitLoop

            # find the first bit with the mask set and the obtained unset
            Label("@selectRingLoop"),
            RRC_B,                  #     rrc b
            RRC_C,                  #     rrc c
            INC_D,                  #     inc d
            BIT0_C,                 #     bit 0,c
            JR_Z, "@selectRingLoop",#     jr z,@selectRingLoop
            BIT0_B,                 #     bit 0,b
            JR_NZ,"@selectRingLoop",#     jr nz,@selectRingLoop

            # we're at a random bit in these bytes, so we need to
            # make sure we don't increment outside the [0-7] range
            LD_A_D,                 #     ld a,d
            AND,  0x07,             #     and $07
            OR_E,                   #     or e
            LD_E_A,                 #     ld e,a
            RET,                    #     ret

        Label("@checkNextByte"),
        LD_A_E,                     #   ld a,e
        CP,         7,              #   cp $07
        JR_NZ, "@tryGetNewRing",    #   jr nz,@tryGetNewRing

        # that was the last byte, so we might have to try another tier
        LD_A,       3,                  # ld a,$03
        CP_C,                           # cp c
        JR_Z, "@maybeGoToSecretTier",   # jr z,@maybeGoToSecretTier
            JR_NC, "@trySelectNewRing", #   jr nc,@trySelectNewRing
                # reset to the original tier and select randomly
                LD_C_D,                 #     ld c,d
                JR, "@selectRandomRing",#     jr @selectRandomRing

        Label("@maybeGoToSecretTier"),
            # we can only increment to the final tier if we
            # went through the other tiers, starting with 0
            LD_A_D,                     #   ld a,d
            OR_D,                       #   or d

            # reset to the original tier
            LD_C_D,                     #   ld c,d
            JR_NZ, "@selectRandomRing", #   jr nz,@selectRandomRing
                # go to secret tier, fall through, and select randomly
                LD_C,       4,          #     ld c,$04

    Label("@selectRandomRing"),
    # get the tier table pointer
    LD_A_C,                         # ld a,c
    LD_HL,      RING_TIER_TABLE,    # ld hl,ringTierTable
    RST_18H,                        # rst_addDoubleIndex
    LDI_A_HLP,                      # ldi a,(hl)
    LD_H_HLP,                       # ld h,(hl)
    LD_L_A,                         # ld l,a

    CALL,       GET_RANDOM_NUMBER,  # call getRandomNumber
    # to simplify logic, the random number will only be in the range [0,254]
    CP,         0xFF,               # cp $FF
    LD_B_A,                         # ld b,a
    JR_NZ, "@selectRingByWeight",   # jr nz,@selectRingByWeight
    DEC_B,                          #   dec b

    # loop through the rings in the tier until one of weighted
    # offsets is greater than or equal to the random number.
    Label("@selectRingByWeight"),
    LDI_A_HLP,                      # ldi a,(hl)

    # return if we hit the end of the table somehow
    CP,         0xFF,               # cp $FF
    RET_Z,                          # ret z

    LD_E_A,                         # ld e,a
    LDI_A_HLP,                      # ldi a,(hl)
    CP_B,                           # cp b
    RET_NC,                         # ret nc
    JR,     "@selectRingByWeight",  # jr @selectRingByWeight
    ]

GET_RING_TIER_MASK_ASM = [
    # @param        c       Ring tier
    # @param        e       Byte offset[0-7]
    # @param[out]   a       Ring tier byte mask

    # the masks table has a stride of 8, so we need to
    # multiply the tier by 8 to get our starting offset
    LD_A_C,                     # ld a,c
    ADD_A,                      # add a
    ADD_A,                      # add a
    ADD_A,                      # add a
    ADD_E,                      # add e
    LD_HL,      RING_TIER_MASKS,# ld hl,ringTierMasks
    RST_10H,                    # rst_addAToHl
    LD_A_HLP,                   # ld a,(hl)
    RET,                        # ret
    ]

GET_RINGS_OBTAINED_ASM = [
    # @param        e       Byte offset[0-7]
    # @param[out]   a       Rings-obtained byte

    # the masks table has a stride of 8, so we need to
    # multiply the tier by 8 to get our starting offset
    LD_A_E,                     # ld a,e
    LD_HL,      RINGS_OBTAINED, # ld hl,wRingsObtained
    RST_10H,                    # rst_addAToHl
    LD_A_HLP,                   # ld a,(hl)
    RET,                        # ret
    ]

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
    LD_A_C,                         # ld a,c
    ADD_A,                          # add a
    LD_C_A,                         # ld c,a
    ADD_A,                          # add a
    ADD_A,                          # add a
    ADD_C,                          # add c

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
    LD_A_B,                 # ld a,b
    LD_E,       2,          # ld e,Interaction.subid
    LD_DEP_A,               # ld (de),a
    LD_HL,  GASHA_TREASURES,# ld hl,@gashaTreasures
    RST_18H,                # rst_addDoubleIndex
    LDI_A_HLP,              # ldi a,(hl)
    LD_C_HLP,               # ld c,(hl)
    LD_A,       0x2d,       # ld a,TREASURE_RING
    JR_NZ,      3,          # jr nz,+
    ]

TIER_TABLE_START = 0x479C
AGES_ORIG_RING_TIERS_TABLE_ASM = [
    TIER_TABLE_START,       # .dw @tier0
    TIER_TABLE_START + 8*1, # .dw @tier1
    TIER_TABLE_START + 8*2, # .dw @tier2
    TIER_TABLE_START + 8*3, # .dw @tier3
    TIER_TABLE_START + 8*4, # .dw @tier4
    ]
TIER_TABLE_START = 0x47BB
SEAS_ORIG_RING_TIERS_TABLE_ASM = [
    TIER_TABLE_START,       # .dw @tier0
    TIER_TABLE_START + 8*1, # .dw @tier1
    TIER_TABLE_START + 8*2, # .dw @tier2
    TIER_TABLE_START + 8*3, # .dw @tier3
    TIER_TABLE_START + 8*4, # .dw @tier4
    ]
del TIER_TABLE_START
NEW_RING_TIERS_TABLE_ASM = [
    RING_TIER0_TABLE,
    RING_TIER1_TABLE,
    RING_TIER2_TABLE,
    RING_TIER3_TABLE,
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
        curr_cutoff     += 255.5*(v/total_weight)
        ring_list[1+i*2] = int(curr_cutoff)


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
