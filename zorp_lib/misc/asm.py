from .const import *
from ..const import *
from ..opcodes import *
from ..shared.const import *
from ..combo_bombs.asm import MINING_BOMB4_ASM as NEW_BOMB_RADIUS2_ASM, BLAST_Z

ORIG_BOMB_RADIUS0_ASM = [
    b'\x2e\x24',            # ld l,Item.collisionType
    b'\xcb\x77',            # bit 6,a
    b'\x28\x02',            # jr z,+
    b'\x36\x00',            # ld (hl),$00
    # +
    b'\x4e',                # ld c,(hl)
    b'\x2e\x26',            # ld l,Item.collisionRadiusY
    b'\xe6\x1f',            # and $1f
    b'\x22',                # ldi (hl),a
    b'\x22',                # ldi (hl),a
    ]
NEW_BOMB_RADIUS0_ASM = list(ORIG_BOMB_RADIUS0_ASM)
NEW_BOMB_RADIUS0_ASM[-3:-1] = [
    b'\xcd',BOMB_RADIUS1,   # call bombRadius1
    ]
BOMB_RADIUS1_ASM = [
    b'\xe6\x1f',            # and $1f
    b'\xf5',                # push af
    b'\x3e',BLAST_RING,     # ld a,BLAST_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x20\x05',            # jr nz,@done
    b'\xf1',                #   pop af
    # radius x2
    b'\xcb\x27',            #   sla a
    b'\x22',                #   ldi (hl),a
    b'\xc9',                #   ret
    # @done
    b'\xf1',                # pop af
    b'\x22',                # ldi (hl),a
    b'\xc9',                # ret
    ]
BLAST_N0 = -13
BLAST_P0 =  12
ORIG_BOMB_RADIUS2_ASM = [
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
    ]
# don't need the extended radius
NEW_BOMB_RADIUS2_ASM = NEW_BOMB_RADIUS2_ASM[:9*3]

ORIG_STEADFAST_RING0_ASM = [
    b'\x62',        # ld h,d
    b'\x2e\x25',    # ld l,SpecialObject.damageToApply
    b'\x7e',        # ld a,(hl)
    b'\x36\x00',    # ld (hl),$00
    b'\xb7',        # or a
    b'\x28\x0f',    # jr z,++
    b'\x47',        # ld b,a
    ]

NEW_STEADFAST_RING0_ASM = list(ORIG_STEADFAST_RING0_ASM)
NEW_STEADFAST_RING0_ASM[:2] = [
    b'\xcd', STEADFAST_RING1, # call steadfastRing1
    ]

ORIG_SWIMMERS_RING0_ASM = [
    OR_A,                                   # or a
    JR_NZ,      "+",                        # jr nz,+
    LD_A_A16,   W_GAME_KEYS_JUST_PRESSED,   # ld a,(wGameKeysJustPressed)
    AND,        0x10 | 0x20 | 0x40 | 0x80,  # and (BTN_RIGHT | BTN_LEFT | BTN_UP | BTN_DOWN)
    JR_NZ,      "@directionButtonPressed",  # jr nz,@directionButtonPressed
    Label("+"),
    LD_L,       0x3e,                       # ld l,SpecialObject.var3e
    DEC_HLP,                                # dec (hl)
    BIT7_HLP,                               # bit 7,(hl)
    JR_Z,       "++",                       # jr z,++
    LD_A,       0xFF,                       # ld a,$ff
    LD_HLP_A,                               # ld (hl),a
    JR,         17,                         # jr func_5933
    Label("@directionButtonPressed"),

    LD_A,       0x87,                       # ld a,SND_SPLASH
    CALL,       PLAY_SOUND,                 # call playSound
    LD_H_D,                                 # ld h,d
    LD_L,       0x3e,                       # ld l,SpecialObject.var3e
    LD_HLP,     4,                          # ld (hl),$04
    Label("++"),
    ]
NEW_SWIMMERS_RING0_ASM  = list(ORIG_SWIMMERS_RING0_ASM)
NEW_SWIMMERS_RING0_ASM[3:5] = [
    CALL,   SWIMMERS_RING1,         # call swimmersRing1
    ]
SWIMMERS_RING1_ASM = [
    LD_A,       SWIMMERS_RING,              # ld a,SWIMMERS_RING
    CALL,       CP_ACTIVE_RING0,            # call cpActiveRing
    JR_NZ,      "@manualSwim",              # jr nz,@manualSwim
    LD_A_A16,   W_FRAME_COUNTER,            # ld a,(wFrameCounter)
    AND,        4,                          # and 4
    JR_NZ,      "@manualSwim",              # jr nz,@manualSwim

    LD_A_A16,   W_GAME_KEYS_PRESSED,        # ld a,(wGameKeysPressed)
    RET,                                    # ret
    Label("@manualSwim"),
    LD_A_A16,   W_GAME_KEYS_JUST_PRESSED,   # ld a,(wGameKeysJustPressed)
    RET,                                    # ret
    ]
        

STEADFAST_RING1_ASM = [
    b'\x62',                # ld h,d
    b'\x2e\x25',            # ld l,SpecialObject.damageToApply

    # must be wearing ring ...
    b'\x3e',STEADFAST_RING, # ld a,STEADFAST_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\xc0',                # ret nz

    # using shield ...
    b'\xfa',W_USING_SHIELD, # ld a,(wUsingShield)
    b'\xb7',                # or a
    b'\xc8',                # ret z

    # and taking no damage ...
    b'\x7e',                # ld a,(hl)
    b'\xfe\x00',            # cp $00
    b'\xc0',                # ret nz

    # to reduce knockback to 0
    b'\x2e\x2d',            # ld l,SpecialObject.knockbackCounter
    b'\x36\x00',            # ld (hl),$00
    b'\x2e\x25',            # ld l,SpecialObject.damageToApply
    b'\xc9',                # ret
    ]

ORIG_FEATHER_SPEED0_ASM = [
    # NOTE: the code below was copied from featherParent.s
    # ; Jump higher in sidescrolling rooms
    b'\x01\x20\xfe',                 # ld bc,$fe20
    b'\xfa',W_ACTIVE_GROUP,          # ld a,(wActiveGroup)
    b'\xfe\x06',                     # cp FIRST_SIDESCROLL_GROUP
    b'\x38\x03',                     # jr c,+
    b'\x01\xd0\xfd',                 # ld bc,$fdd0
    # +
    b'\x21',LINK_SPEED_Z,            # ld hl,w1Link.speedZ
    b'\x71',                         # ld (hl),c
    b'\x2c',                         # inc l
    b'\x70',                         # ld (hl),b
    ]
NEW_FEATHER_SPEED0_ASM = list(ORIG_FEATHER_SPEED0_ASM)
NEW_FEATHER_SPEED0_ASM[6:8] = [
    b'\xcd', FEATHER_SPEED1
    ]

FEATHER_SPEED1_ASM = [
    b'\x3e',ROCS_RING,      # ld a,ROCS_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x21',LINK_SPEED_Z,   # ld hl,w1Link.speedZ
    b'\xc0',                # ret nz
    # ; Jump higher in sidescrolling rooms
    b'\x01\x90\xfd',        # ld bc,$fd90
    b'\xfa',W_ACTIVE_GROUP, # ld a,(wActiveGroup)
    b'\xfe\x06',            # cp FIRST_SIDESCROLL_GROUP
    b'\x38\x03',            # jr c,+
    b'\x01\x00\xfd',        # ld bc,$fd00
    # +
    b'\xc9',                # ret
    ]

ORIG_DISCOVERY_RING0_ASM = [
    b'\xcb\x37',    # swap a
    b'\x0f',        # rrca
    b'\xe6\x07',    # and $07
    b'\x21',        # ld hl,???
    ]
NEW_DISCOVERY_RING0_ASM = list(ORIG_DISCOVERY_RING0_ASM)
NEW_DISCOVERY_RING0_ASM[1:3] = b'\xcd', DISCOVERY_RING1

DISCOVERY_RING1_ASM = [
    b'\x0f',                # rrca
    b'\xe6\x07',            # and $07
    b'\xd5',                # push de
    b'\xf5',                # push af
    b'\x3e',DISCOVERY_RING, # ld a,DISCOVERY_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\xd1',                # pop de
    b'\x7a',                # ld a,d
    b'\x20\x06',            # jr nz,@done
    # increment to the next highest probability table
    b'\x3c',                # inc a
    b'\xfe\x08',            # cp $08
    b'\x38\x01',            # jr c,@done
    b'\x3d',                # dec a
    # @done
    b'\xd1',                # pop de
    b'\xc9',                # ret
    ]

ORIG_HASTE_RING0_ASM = [
    b'\x7b',    # ld a,e
    b'\x80',    # add b
    b'\x81',    # add c
    b'\xe6\x7f',# and $7f
    ]
NEW_HASTE_RING0_ASM = list(ORIG_HASTE_RING0_ASM)
NEW_HASTE_RING0_ASM[:3] = b'\xcd', HASTE_RING1
HASTE_RING1_ASM = [
    b'\x3e',HASTE_RING,     # ld a,HASTE_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing

    b'\x20\x1a',            # jr nz,@notJogging
    b'\x78',                # ld a,b
    b'\xfe\x03',            # cp $03
    b'\x20\x02',            # jr nz,@notStairs
    # upgrade stairs to grass
    b'\x06\x02',            # ld b,$02
    # @notStairs
    b'\xfe\x02',            # cp $02
    b'\x20\x02',            # jr nz,@notGrass
    # upgrade grass to normal
    b'\x06\x04',            # ld b,$04
    # @notGrass
    b'\xfe\x04',            # cp $04
    b'\x20\x09',            # jr nz,@notJogging
    b'\x7b',                # ld a,e
    b'\xfe\x03',            # cp $03
    b'\x28\x04',            # jr z,@notJogging
    # upgrade normal to pegasus grass
    b'\x06\x02',            # ld b,$02
    b'\x1e\x03',            # ld e,$03
    # @notJogging
    b'\x7b',                # ld a,e
    b'\x80',                # add b
    b'\x81',                # add c
    b'\xc9',                # ret
    ]

ORIG_ADVANCE_RING0_ASM = [
    b'\x21',LINK_INVINC_COUNTER,# ld hl,w1Link.invincibilityCounter
    b'\x7e',                    # ld a,(hl)
    b'\xb7',                    # or a
    b'\xc8',                    # ret z
    b'\xcb\x7f',                # bit 7,a
    b'\x20\x0f',                # jr nz,@incCounter
    b'\x35',                    # dec (hl)
    b'\x28\x0d',                # jr z,@normalFlags
    ]
NEW_ADVANCE_RING0_ASM = list(ORIG_ADVANCE_RING0_ASM)
NEW_ADVANCE_RING0_ASM[:2] = b'\xcd', ADVANCE_RING1

ADVANCE_RING1_ASM = [
    # don't need to do lengthy checks if not invincible
    b'\x21',LINK_INVINC_COUNTER,          # ld hl,w1Link.invincibilityCounter
    b'\x7e',                              # ld a,(hl)
    b'\xb7',                              # or a
    b'\xc8',                              # ret z

    b'\x01',GBA_NATURE_RING,GBA_TIME_RING,# ld bc,GBA_TIME_RING,GBA_NATURE_RING
    b'\xcd',EITHER_RING,                  # call eitherRingActive
    b'\x01\x05\x07',                      # ld bc,$07,$05
    b'\x28\x05',                          # jr z,+
    b'\x38\x03',                          #   jr c,+
    b'\x01\x00\x00',                      #     ld bc,$00,$00

    # +
    b'\x20\x04',                          # jr nz,@checkFrameCounter
    b'\x30\x02',                          #   jr nc,@checkFrameCounter
    b'\x0e\x04',                          #     ld c,$04

    # @checkFrameCounter
    b'\x78',                              # ld a,b
    b'\xb7',                              # or a
    b'\x28\x0e',                          # jr z,@done
    b'\xfa',W_FRAME_COUNTER,              #   ld a,(wFrameCounter)
    b'\xa0',                              #   and b
    b'\xb9',                              #   cp c
    b'\x38\x07',                          #   jr c,@done
    b'\xcb\x7f',                          #     bit 7,a
    b'\x28\x02',                          #     jr z,@increment
    b'\x35',                              #     dec (hl)
    b'\xc9',                              #     ret
    b'\x34',                              #     inc (hl)
    # @done
    b'\xc9',                              # ret
    ]

# make protection ring heal you to full if you die, but it breaks
ORIG_POTION_CHECK0_ASM = [
    # ; Replenish health if Link has a potion.
    b'\x3e',TREASURE_POTION,    # ld a,TREASURE_POTION
    b'\xcd',CHECK_HAVE_TREASURE,# call checkTreasureObtained
    b'\x30\x0f',                # jr nc,@noPotion
    ]
NEW_POTION_CHECK0_ASM = list(ORIG_POTION_CHECK0_ASM)
NEW_POTION_CHECK0_ASM[3] = POTION_CHECK1 # call potionCheck1

POTION_CHECK1_ASM = [
    b'\xcd',CHECK_HAVE_TREASURE,# call checkTreasureObtained
    b'\x38\x1d',                # jr c,@done
    b'\xd5',                    #   push de
    b'\x3e',PROTECTION_RING,    #   ld a,PROTECTION_RING
    b'\xcd',CP_ACTIVE_RING0,    #   call cpActiveRing
    b'\x3e',TREASURE_POTION,    #   ld a,TREASURE_POTION
    b'\x20\x10',                #   jr nz,@ringNotFound
    b'\xc5',                    #     push bc
    b'\x0e\x01',                #     ld c,$01
    b'\xcd',GIVE_TREASURE,      #     call giveTreasure
    b'\x3e',PROTECTION_RING,    #     ld a,PROTECTION_RING
    b'\xcd',REMOVE_RING,        #     call removeRing
    b'\x37',                    #     scf
    b'\xc1',                    #     pop bc
    b'\xd1',                    #   pop de
    b'\x18\x03',                #   jr @done
    # @ringNotFound
    b'\xd1',                    #   pop de
    b'\x37',                    #   scf
    b'\x3f',                    #   ccf
    # @done
    b'\xc9',                    # ret
    ]

ORIG_TOSS_RING_TEST0_ASM = [
    b'\x87',                    # add a
    b'\xc6',ENEMY_CODE_TABLE_B0,# add <enemyCodeTable
    b'\x6f',                    # ld l,a
    b'\x3e\x00',                # ld a,$00
    b'\xce',ENEMY_CODE_TABLE_B1,# adc >enemyCodeTable
    b'\x67',                    # ld h,a
    ]
NEW_TOSS_RING_TEST0_ASM = list(ORIG_TOSS_RING_TEST0_ASM)
NEW_TOSS_RING_TEST0_ASM[:3] = [
    b'\xcd',TOSS_RING_TEST1,    # call tossRingTest1
    ]
TOSS_RING_TEST1_ASM = [
    # https://github.com/Stewmath/oracles-disasm/blob/master/object_code/ages/enemies/pumpkinHead.s
    # https://github.com/Stewmath/oracles-disasm/blob/master/object_code/common/itemParents/bombsBraceletParent.s#L367
    b'\x87',                        # add a
    b'\xc6',ENEMY_CODE_TABLE_B0,    # add <enemyCodeTable
    b'\xe5',                        # push hl
    b'\xf5',                        # push af
    b'\x3e',TOSS_RING,              # ld a,TOSS_RING
    b'\xcd',CP_ACTIVE_RING0,        # call cpActiveRing
    b'\x20\x03',                    # jr nz,@done
    b'\xcd',OBJ_ADD_TO_GRAB_BUFFER, # call objectAddToGrabbableObjectBuffer
    # @done
    b'\xf1',                        # pop af
    b'\xe1',                        # pop hl
    b'\xc9',                        # ret
    ]

ORIG_PUNCH_WITH_ITEM_ASM = [
    b'\x2e',INVENTORY_B,# ld l,<wInventoryB
    b'\x2a',            # ldi a,(hl)
    b'\xb6',            # or (hl)
    b'\xc0',            # ret nz
    ]
NEW_PUNCH_WITH_ITEM_ASM = [
    # replace with a bunch of nops
    b'\x00'*5
    ]

ORIG_SOMARIA_PRIORITY_ASM = [
    b'\x00\x29',  # .db $00, wGameKeysPressed     ; ITEM_NONE
    b'\x05\x29',  # .db $05, wGameKeysPressed     ; ITEM_SHIELD
    b'\x03\x2a',  # .db $03, wGameKeysJustPressed ; ITEM_PUNCH
    b'\x23\x2a',  # .db $23, wGameKeysJustPressed ; ITEM_BOMB
    b'\x03\x2a',  # .db $03, wGameKeysJustPressed ; ITEM_CANE_OF_SOMARIA
    ]
NEW_SOMARIA_PRIORITY_ASM     = list(ORIG_SOMARIA_PRIORITY_ASM)
# we increase the priority slightly to prevent punching while
# swinging the cane from creating graphical effect errors
NEW_SOMARIA_PRIORITY_ASM[-1] = b'\x13\x2a'

ORIG_HASTE_RING_ICON_ASM = [
    # snowshoe ring sprite data
    b'\xc3\x04\xbe\x02',
    b'\xa1\x02\xbf\x02',
    ]
NEW_HASTE_RING_ICON_ASM  = [
    b'\xb9\x02\xbe\x02',
    b'\xa1\x02\xbf\x02',
    ]

ORIG_FAIRYS_RING_ICON_ASM = [
    # protection ring sprite data
    b'\xaf\x04\xdc\x06',
    b'\xb5\x06\xdd\x06',
    ]
NEW_FAIRYS_RING_ICON_ASM  = [
    b'\xbb\x46\xbd\x66',
    b'\xbd\x07\xbb\x27',
    ]
