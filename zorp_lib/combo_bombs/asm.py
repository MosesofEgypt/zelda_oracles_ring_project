from .const import *
from ..const import *
from ..opcodes import *
from ..shared.const import *

ORIG_MINING_BOMB0_ASM = [
    b'\x7e',                # ld a,(hl)
    b'\x81',                # add c
    b'\x4f',                # ld c,a
    b'\x3e\x00',            # ld a,$00
    b'\x8b',                # adc e
    b'\xc0',                # ret nz
    b'\x3e\x04',            # ld ld a,BREAKABLETILESOURCE_BOMB
    b'\xc3',TRY_BREAK_TILE, # jp tryToBreakTile
    ]
NEW_MINING_BOMB0_ASM = list(ORIG_MINING_BOMB0_ASM)
NEW_MINING_BOMB0_ASM[-1] = MINING_BOMB1

MINING_BOMB1_ASM = [
    b'\xe5',                          # push hl
    b'\xcd',TRY_BREAK_TILE,           # call tryToBreakTile

    # in order to destroy everything(even after tiles change)
    # we need to reset the counter once it hits 0xFF
    # handle the counter states, even if rings change
    b'\x62',                          # ld h,d
    b'\x2e\x06',                      # ld l,Item.counter1
    b'\x7e',                          # ld a,(hl)
    b'\xfe\x0f',                      # cp $0f
    b'\x20\x04',                      # jr nz,@continueCycle
    # if the first cycle stopped, start the next
    b'\x36\x2c',                      #   ld (hl),$2c
    b'\x18\x06',                      #   jr @checkShovel
    # @continueCycle
    b'\xfe\x1f',                      # cp $1f
    b'\x20\x02',                      # jr nz,@checkShovel
    # move to end of second cycle
    b'\x36\xff',                      #   ld (hl),$ff

    b'\xe1',                          # pop hl
    # @checkShovel
    b'\x3e\x15',                      # ld a,TREASURE_SHOVEL
    b'\xcd',CHECK_HAVE_TREASURE,      # call checkTreasureObtained
    b'\xd0',                          # ret nc

    # determines the tile offset to use, and handles the counter reset
    b'\xc5',                          # push bc
    b'\x01',BLAST_RING,DISCOVERY_RING,# ld bc,DISCOVERY_RING,BLAST_RING
    b'\xcd',EITHER_RING,              # call eitherRingActive
    b'\xc1',                          # pop bc
    b'\xc0',                          # ret nz
    b'\xd0',                          # ret nc
    b'\x3e\x06',                      # ld a,BREAKABLETILESOURCE_SHOVEL
    b'\xcd',TRY_BREAK_TILE,           # call tryToBreakTile

    b'\xe5',                          # push hl
    b'\x62',                          # ld h,d
    b'\x2e\x06',                      # ld l,Item.counter1
    b'\x7e',                          # ld a,(hl)

    b'\xfe\x07',                      # cp $07
    b'\x20\x02',                      # jr nz,@done
    # hitting 0x07 means the first cycle just started, so move
    # timer to a value we can recognize the cycle number
    b'\x36\x1c',                      #   ld (hl),$1c
    # @done
    b'\xe1',                          # pop hl
    b'\xc9',                          # ret
    ]

ORIG_MINING_BOMB2_ASM = [
    b'\x7e',                    # ld a,(hl)
    b'\x35',                    # dec (hl)
    b'\x6f',                    # ld l,a
    b'\x87',                    # add a
    b'\x85',                    # add l
    b'\x21',BOMB_OFFSET_DATA,   # ld hl,@bombOffsetData
    b'\xd7',                    # rst_addAToHl
    ]
NEW_MINING_BOMB2_ASM = [
    b'\x7e',                # ld a,(hl)
    b'\x35',                # dec (hl)
    b'\xe6\x0f',            # and $0f
    b'\x6f',                # ld l,a
    b'\x87',                # add a
    b'\xcd',MINING_BOMB3,   # call miningBomb3
    ]

BLAST_N1 = -32
BLAST_P1 =  31
BLAST_N0 = -16
BLAST_P0 =  15
BLAST_Z  =  0
MINING_BOMB3_ASM = [
    b'\x85',                # add l
    b'\x21',MINING_BOMB4,   # ld hl,@miningBomb4
    b'\xd7',                # rst_addAToHl
    b'\xc9',                # ret
    ]

MINING_BOMB4_ASM = [
    # b0: necessary Z-axis proximity
    # b1: offset from y-position
    # b2: offset from x-position
    # @data:
    b'\xf8', BLAST_N0, BLAST_N0,
    b'\xf8', BLAST_P0, BLAST_N0,
    b'\xf8', BLAST_P0, BLAST_P0,
    b'\xf8', BLAST_N0, BLAST_P0,

    b'\xf4', BLAST_Z,  BLAST_N0,
    b'\xf4', BLAST_P0, BLAST_Z,
    b'\xf4', BLAST_Z,  BLAST_P0,
    b'\xf4', BLAST_N0, BLAST_Z,

    b'\xf2', BLAST_Z,  BLAST_Z,

    b'\xfc', BLAST_Z,  BLAST_N1,
    b'\xfc', BLAST_P1, BLAST_Z,
    b'\xfc', BLAST_Z,  BLAST_P1,
    b'\xfc', BLAST_N1, BLAST_Z,
    ]

ORIG_REMOTE_BOMB0_ASM = [
    b'\xfe\xff',            # cp $ff
    b'\x20\x0a',            # jr nz,itemInitializeBombExplosion
    b'\x18\xce',            # jr itemUpdateExplosion
    # bombUpdateAnimation:
    b'\xcd',ITEM_ANIMATE,   # call itemAnimate
    b'\x1e\x21',            # ld e,Item.animParameter
    b'\x1a',                # ld a,(de)
    b'\xb7',                # or a
    b'\xc8',                # ret z
    ]
NEW_REMOTE_BOMB0_ASM    = list(ORIG_REMOTE_BOMB0_ASM)
NEW_REMOTE_BOMB0_ASM[4] = REMOTE_BOMB1

REMOTE_BOMB1_ASM = [
    b'\x01',BOMBERS_RING,PEACE_RING,  # ld bc,PEACE_RING,BOMBERS_RING
    b'\xcd',EITHER_RING,              # call eitherRingActive
    b'\x20\x07',                      # jr nz,@notRemote
    b'\x30\x05',                      # jr nc,@notRemote
    b'\xcd',BOMB_RESET_ANIM_AND_VIS,  # call bombResetAnimationAndSetVisiblec1
    # NOTE: we're intentionally mucking with the stack here to make
    #       the return jump out of the bombUpdateAnimation code. This
    #       allows us to add as little code as necessary, as we don't need
    #       to add logic to @bombUpdateAnimation to handle the return there.
    b'\xf1',                          # pop af
    b'\xc9',                          # ret
    b'\xcd',ITEM_ANIMATE,             # call itemAnimate
    # @notRemote
    b'\x01',HASTE_RING,BOMBPROOF_RING,# ld bc,BOMBPROOF_RING,HASTE_RING
    b'\xcd',EITHER_RING,              # call eitherRingActive
    b'\x20\x08',                      # jr nz,@done
    b'\x30\x06',                      # jr nc,@done
    # force immediate explosion
    b'\x2e\x2f',                      # ld l,Item.var2f
    SET4_HLP,                         # set 4,(hl)
    b'\xf1',                          # pop af
    b'\x1f',                          # rra
    # @done
    b'\xc9',                          # ret
    ]

ORIG_REMOTE_BOMB2_ASM = [
    JP_Z,   CLEAR_PARENT_ITEM,       # jp z,clearParentItem
    CALL,   ITEM_LOAD_ANIM_INC_STATE,# call parentItemLoadAnimationAndIncState
    LD_E,   1,                       # ld e,$01
    LD_A,   BOMBERS_RING,            # ld a,BOMBERS_RING
    CALL,   CP_ACTIVE_RING0,         # call cpActiveRing
    JR_NZ,  "-",                     # jr nz,+
    INC_E,                           #   inc e
    Label("-"),
    ]
NEW_REMOTE_BOMB2_ASM    = [
    CALL,   REMOTE_BOMB3,   # call remoteBomb3
    NOP,    NOP,            # nop
    LD_E,   1,              # ld e,$01
    LD_A,   BOMBERS_RING,   # ld a,BOMBERS_RING
    CALL,   CP_ACTIVE_RING0,# call cpActiveRing
    JR_NZ,  "-",            # jr nz,+
        LD_E,   4,          #   ld e,$04
    Label("-"),
    ]

REMOTE_BOMB3_ASM = [
    PUSH_AF,                        # push af
    LD_BC,  BOMBERS_RING,PEACE_RING,# ld bc,PEACE_RING,BOMBERS_RING
    CALL,   EITHER_RING,            # call eitherRingActive
    JR_NZ,  "@done",                # jr nz,@done
    JR_NC,  "@done",                # jr nc,@done
    # check if there's a bomb to remote detonate
    LD_C,   3,                      # ld c,ITEM_BOMB
    CALL,   FIND_ITEM_WITH_ID,      # call findItemWithID
    JR_Z,   "@remoteDetonate",      # jr z,@remoteDetonate
    Label("@done"),
    POP_AF,                         # pop af
    JP_Z,   CLEAR_PARENT_ITEM,      # jp z,clearParentItem
    JP,    ITEM_LOAD_ANIM_INC_STATE,# jp parentItemLoadAnimationAndIncState
    Label("@remoteDetonate"),
    LD_L,   0x2f,                   # ld l,Item.var2f
    # NOTE: we're intentionally mucking with the stack here to make
    #       the return jump out of the bombUpdateAnimation code. This
    #       allows us to add as little code as necessary, as we don't need
    #       to add logic to @bombUpdateAnimation to handle the return there.
    POP_AF,                         # pop af
    POP_AF,                         # pop af
    # skip if already exploding
    BIT4_HLP,                       # bit 4,(hl)
    RET_NZ,                         # ret nz
    # set the bit that indicates to explode
    SET4_HLP,                       # set 4,(hl)
    JP,     CLEAR_PARENT_ITEM,      # jp clearParentItem
    ]
