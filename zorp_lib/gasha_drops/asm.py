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
    # @param        d       Ring tier
    # @param[out]   e       Randomly chosen ring from the given tier

    PUSH_BC,                        # push bc
    # to make it easier to get the highest tier ring, we'll bump
    # from tier0 to tier4 if all other tiers have been collected
    LD_A_D,                         # ld a,d
    OR_A,                           # or a
    JR_NZ,  "@checkIsTier4",        # jr nz,@checkIsTier4
        # use e as a counter to increment through the bytes
        LD_E,       7,              #   ld e,7

        Label("@checkCollected"),
        LD_BC,      3,  0,          #   ld bc,0,3

        Label("@combineMasks"),
        # get the rings obtained mask byte in b
        CALL, GET_RING_TIER_MASK,   #   call getRingTierMask
        OR_B,                       #   or b
        LD_B_A,                     #   ld b,a
        DEC_C,                      #   dec c
        LD_A_C,                     #   ld a,c
        CP,         0xFF,           #   cp $FF
        JR_NZ,  "@combineMasks",    #   jr nz,@combineMasks

        # get the rings obtained byte in a
        CALL, GET_RINGS_OBTAINED,   #   call getRingsObtained
        AND_B,                      #   and b
        CP_B,                       #   cp b
        # if the masked obtained rings doesn't equal the
        # mask, then we don't have all tier 0-3 rings
        JR_NZ,  "@checkIsTier4",    #   jr nz,@checkIsTier4
        DEC_E,                      #   dec e
        LD_A_E,                     #   ld a,e
        CP,         0xFF,           #   cp $FF
        JR_NZ,  "@checkCollected",  #   jr nz,@checkIsTier4

    # increment to the secret ring tier
    LD_D,           4,              # ld d,4

    # cant guarantee new secret-tier rings
    Label("@checkIsTier4"),
    POP_BC,                         # pop bc
    LD_C_D,                         # ld c,d
    LD_A_D,                         # ld a,d
    CP,             4,              # cp $04
    JR_NC,  "@selectRandomRing",    # jr nc,@selectRandomRing

    # determine if we can guarantee a new ring
    CALL,   GET_RANDOM_NUMBER,      # call getRandomNumber
    CP_B,                           # cp b
    JR_NC,  "@selectRandomRing",    # jr nc,@selectRandomRing

    # loop over each tier until we can guarantee a new ring
    DEC_C,                          # dec c
    Label("@trySelectNewRing"),
    INC_C,                          # inc c
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
    RET_C,                          # ret c
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
    BIT0_HLP,                       # bit 0,(hl)
    JR_NZ,          "+",            # jr nz,+
    SET0_HLP,                       # set 0,(hl)
    LD_B,           4,              # ld b,GASHATREASURE_TIER3_RING
    JR, 0x5A,                       # jr @spawnTreasure
    Label("+"),

    LD_C,           0,              # ld c,$00
    LD_HL,  W_GASHA_MATURITY_H,     # ld hl,wGashaMaturity+1
    LDD_A_HLP,                      # ldd a,(hl)
    SRL_A,                          # srl a
    JR_NZ,          12,             # jr nz,++
    LD_A_HLP,                       # ld a,(hl)
    RRA,                            # rra
    ]

NEW_DETERMINE_GASHA_DROP_ASM = [
    # make the heart piece always spawn if it hasn't yet
    BIT1_HLP,                       # bit 1,(hl)
    JR_NZ,          "+",            # jr nz,+
    SET1_HLP,                       # set 1,(hl)
    LD_B,           0,              # ld b,GASHATREASURE_HEART_PIECE
    JR, 0x5A,                       # jr @spawnTreasure
    Label("+"),

    # otherwise, spawn a ring with the tier dependent on kill count
    LD_HL,  W_GASHA_KILL_COUNTERS,  # ld hl,wGashaSpotKillCounters
    LD_E,           0x43,           # ld e,Interaction.var03
    LD_A_DEP,                       # ld a,(de)
    RST_10H,                        # rst_addAToHl
    CALL, DETERMINE_RING_DROP_TIER, # call determineRingDropTier
    # skip straight to decrementing and dropping the item
    JR,             48,             # jr @decGashaMaturity
    ]

DETERMINE_RING_DROP_TIER_ASM = [
    # start with the best guaranteed tier ring for the kill count
    LD_B,       4,              # ld b,GASHATREASURE_TIER3_RING
    LD_A_HLP,                   # ld a,(hl)

    CP,  RING_TIER_3_MAX_KILLS, # cp a,ringTier3MaxKills
    JR_C,    "@check2",         # jr c,@check2
        DEC_B,                  #   dec b


    Label("@check2"),
    CP,  RING_TIER_2_MAX_KILLS, # cp a,ring2MaxKills
    JR_C,    "@maybe2",         # jr c,@maybe2
        DEC_B,                  #   dec b
        JR,  "@check1",         #   jr @check1

    Label("@maybe2"),
    CP,  RING_TIER_2_MIN_KILLS, # cp a,ring2MinKills
    JR_C,    "@check1",         # jr c,@check1
        CALL,GET_RANDOM_NUMBER, #   call getRandomNumber
        CP,     0x80,           #   cp $80
        JR_C,"@check1",         #   jr c,@check1
            DEC_B,              #   dec b


    Label("@check1"),
    CP,  RING_TIER_1_MAX_KILLS, # cp a,ring1MaxKills
    JR_C,    "@maybe1",         # jr c,@maybe1
        DEC_B,                  #   dec b
        JR,  "@maybe0",         #   jr @check0

    Label("@maybe1"),
    CP,  RING_TIER_1_MIN_KILLS, # cp a,ring1MinKills
    JR_C,    "@maybe0",         # jr c,@maybe0
        CALL,GET_RANDOM_NUMBER, #   call getRandomNumber
        CP,     0x80,           #   cp $80
        JR_C,"@maybe0",         #   jr c,@maybe0
            DEC_B,              #   dec b


    Label("@maybe0"),
    CP,  RING_TIER_0_MIN_KILLS, # cp a,ring0MinKills
    JR_C,    "@checkZero",      # jr c,@checkUnderflow
        CALL,GET_RANDOM_NUMBER, #   call getRandomNumber
        CP,     0x80,           #   cp $80
        JR_C,"@checkZero",      #   jr c,@checkUnderflow
            DEC_B,              #   dec b

    # ensure we didn't go too low
    Label("@checkZero"),
    LD_A_B,                     # ld a,b
    OR_A,                       # or a
    RET_NZ,                     # ret nz
    LD_B,       1,              # ld b,GASHATREASURE_TIER0_RING
    RET,                        # ret
    ]

ORIG_DEC_GASHA_MATURITY_ASM = [
    Label("@notPotion"),
    CP,             0,          # cp GASHATREASURE_HEART_PIECE
    JR_NZ,  "@decGashaMaturity",# jr nz,@decGashaMaturity
    LD_HL,  W_GASHA_SPOT_FLAGS, # ld hl,wGashaSpotFlags
    BIT1_HLP,                   # bit 1,(hl)
    JR_Z,        "+",           # jr z,+
    INC_B,                      # inc b
    Label("+"),
    SET1_HLP,                   # set 1,(hl)
    Label("@decGashaMaturity"),
    LD_HL,  W_GASHA_MATURITY,   # ld hl,wGashaMaturity
    LD_A_HLP,                   # ld a,(hl)
    SUB,        200,            # sub 200
    LDI_HLP_A,                  # ldi (hl),a
    LD_A_HLP,                   # ld a,(hl)
    SBC,        0,              # sbc $00
    ]

NEW_DEC_GASHA_MATURITY_ASM = [
    Label("@decGashaMaturity"),
    # subtract ~25% from wGashaMaturity(we're ignoring the lower byte
    # and just zeroing it, so the subtraction could be more or less)
    LD_HL,  W_GASHA_MATURITY_H, # ld hl,wGashaMaturity+1
    LD_A_HLP,                   # ld a,(hl)
    LD_E_A,                     # ld e,a
    SRL_A,                      # srl a
    SRL_A,                      # srl a
    LD_C_A,                     # ld c,a
    LD_A_E,                     # ld a,e
    SUB_C,                      # sub c
    LDD_HLP_A,                  # ldd (hl),a
    LD_HLP,         0,          # ld (hl),$00
    *([NOP]*9),
    ]

ORIG_SPAWN_GASHA_TREASURE_ASM = [
    RST_18H,                        # rst_addDoubleIndex
    LDI_A_HLP,                      # ldi a,(hl)
    LD_C_HLP,                       # ld c,(hl)
    CP,         0x2d,               # cp TREASURE_RING
    JR_NZ,       "+",               # jr nz,+
    CALL,   GET_RANDOM_TIERED_RING, # call getRandomRingOfGivenTier
    Label("+"),
    LD_B_A,                         # ld b,a
    CALL,                           # call ???
    ]

NEW_SPAWN_GASHA_TREASURE_ASM = [
    CP,            0,                 # cp GASHATREASURE_HEART_PIECE
    JR_Z,        "+",                 # jr z,+
    CALL,   GET_RING_TIER_AND_CHANCE, # call getRingTierAndChance
    CALL,   GET_RANDOM_TIERED_RING,   # call getRandomRingOfGivenTier
    Label("+"),
    LD_B_A,                           # ld b,a
    CALL,                             # call ???
    ]

GET_RING_TIER_AND_CHANCE_ASM = [
    # convert ring tier from GASHATREASURE into TREASURE
    DEC_A,                      # dec a
    LD_B_A,                     # ld b,a
    LD_HL,  W_GASHA_MATURITY_H, # ld hl,wGashaMaturity+1
    LD_A_HLP,                   # ld a,(hl)
    # use the lower 4 bits of the high byte of gasha
    # maturity as the chance to guarantee a new ring
    CP,             0x10,       # cp $10
    JR_C,            "+",       # jr c,+
    LD_A,           0xFF,       # ld a,$FF
    Label("+"),
    AND,            0x0F,       # and $0F
    SWAP_A,                     # swap a
    OR_B,                       # or a,b
    LD_C_A,                     # ld c,a
    RET,                        # ret
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

ORIG_GASHA_MATURITY_LEVELS_ASM = [
    # @gashaMaturityValues:
    150,                # .db 300/2
    100,                # .db 200/2
    60,                 # .db 120/2
    20,                 # .db  40/2
    0,                  # .db   0/2
    # @gashaTreasures:
    0x2B,           1,  # .db TREASURE_HEART_PIECE, $01
    0x2D,           0,  # .db TREASURE_RING, RING_TIER_0
    0x2D,           1,  # .db TREASURE_RING, RING_TIER_1
    0x2D,           2,  # .db TREASURE_RING, RING_TIER_2
    0x2D,           3,  # .db TREASURE_RING, RING_TIER_3
    0x2D,           4,  # .db TREASURE_RING, RING_TIER_4
    0x2F,           1,  # .db TREASURE_POTION, $01
    0x28, RUPEEVAL_200, # .db TREASURE_RUPEES, RUPEEVAL_200
    0x29,         0x18, # .db TREASURE_HEART_REFILL, $18
    0x29,         0x14, # .db TREASURE_HEART_REFILL, $14
    # this is padding that will have been written by a call
    # to clear_rom_garbage. we'll essentially be using this
    # space for any new bank 10/11 code we'll be adding
    b'\x00' * GASHA_SPOT_RANK_TABLE_INFO["ages"]["size"]
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
