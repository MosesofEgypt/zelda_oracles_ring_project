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
    b'\xca',CLEAR_PARENT_ITEM,       # jp z,clearParentItem
    b'\xcd',ITEM_LOAD_ANIM_INC_STATE,# call parentItemLoadAnimationAndIncState
    b'\x1e\x01',                     # ld e,$01
    b'\x3e',BOMBERS_RING,            # ld a,BOMBERS_RING
    b'\xcd',CP_ACTIVE_RING0,         # call cpActiveRing
    b'\x20\x01',                     # jr nz,+
    b'\x1c',                         #   inc e
    ]
NEW_REMOTE_BOMB2_ASM    = [
    b'\xcd',REMOTE_BOMB3,   # call remoteBomb3
    b'\x00'*2,              # nop
    b'\x1e\x01',            # ld e,$01
    b'\x3e',BOMBERS_RING,   # ld a,BOMBERS_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x20\x02',            # jr nz,+
    b'\x1e\x04',            #   ld e,$04
    ]

REMOTE_BOMB3_ASM = [
    b'\xf5',                        # push af
    b'\x01',BOMBERS_RING,PEACE_RING,# ld bc,PEACE_RING,BOMBERS_RING
    b'\xcd',EITHER_RING,            # call eitherRingActive
    b'\x20\x09',                    # jr nz,@done
    b'\x30\x07',                    # jr nc,@done
    # check if there's a bomb to remote detonate
    b'\x0e\x03',                    # ld c,ITEM_BOMB
    b'\xcd',FIND_ITEM_WITH_ID,      # call findItemWithID
    b'\x28\x08',                    # jr z,@remoteDetonate
    # @done
    b'\xf1',                        # pop af
    b'\xc8',CLEAR_PARENT_ITEM,      # jp z,clearParentItem
    b'\xcd',ITEM_LOAD_ANIM_INC_STATE,# call parentItemLoadAnimationAndIncState
    b'\xc9',                        # ret
    # @remoteDetonate
    b'\x2e\x2f',                    # ld l,Item.var2f
    # NOTE: we're intentionally mucking with the stack here to make
    #       the return jump out of the bombUpdateAnimation code. This
    #       allows us to add as little code as necessary, as we don't need
    #       to add logic to @bombUpdateAnimation to handle the return there.
    b'\xf1',                        # pop af
    b'\xf1',                        # pop af
    # skip if already exploding
    b'\xcb\x66',                    # bit 4,(hl)
    b'\xc0',                        # ret nz
    # set the bit that indicates to explode
    b'\xcb\xe6',                    # set 4,(hl)
    b'\xc3',CLEAR_PARENT_ITEM,      # jp clearParentItem
    ]
