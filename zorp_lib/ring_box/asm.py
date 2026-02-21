from .const import *
from ..const import *
from ..opcodes import *
from ..shared.const import *

# this is the table to remap ring positions.
# each index corresponds to the selected ring index, and
# the value at that index is the actual ring to select
RING_MAP_TABLE_ASM = [
    # page 1
    POWER_RING_L1,   POWER_RING_L2,   POWER_RING_L3,    RED_RING,   GREEN_RING,
    GREEN_HOLY_RING, RED_HOLY_RING,   BLUE_HOLY_RING,
    ARMOR_RING_L1,   ARMOR_RING_L2,   ARMOR_RING_L3,    BLUE_RING,  GOLD_RING,
    GREEN_LUCK_RING, RED_LUCK_RING,   BLUE_LUCK_RING,

    # page 2
    HEART_RING_L1,   RANG_RING_L1,    FIST_RING,        LIGHT_RING_L1,
    ENERGY_RING,     SPIN_RING,       CHARGE_RING,      VICTORY_RING,
    HEART_RING_L2,   RANG_RING_L2,    EXPERTS_RING,     LIGHT_RING_L2,
    BLAST_RING,      PEACE_RING,      BOMBPROOF_RING,   BOMBERS_RING,

    # page 3
    HASTE_RING,      ZORA_RING,        SWIMMERS_RING,   ALCHEMY_RING,
    GREEN_JOY_RING,  RED_JOY_RING,     BLUE_JOY_RING,   GOLD_JOY_RING,
    HIKERS_RING,     MAPLES_RING,      DISCOVERY_RING,  GASHA_RING,
    STEADFAST_RING,  MYSTIC_SEED_RING, TOSS_RING,       ROCS_RING,       

    # page 4
    GREEN_COLOR_RING,RED_COLOR_RING,   BLUE_COLOR_RING, GOLD_COLOR_RING,
    GBOY_COLOR_RING, GBA_NATURE_RING,  CURSE_POWER_RING,FAIRYS_RING,
    OCTO_RING,       LIKE_LIKE_RING,   MOBLIN_RING,     SUBROSIAN_RING,
    FIRST_GEN_RING,  GBA_TIME_RING,    CURSE_ARMOR_RING,VASUS_RING, 
    ]
assert (len(set(RING_MAP_TABLE_ASM)) == 0x40 and len(RING_MAP_TABLE_ASM) == 0x40),\
       "Ring map table is not the expected size after removing duplicates(%i and %i vs %i)" %\
       (len(RING_MAP_TABLE_ASM), len(set(RING_MAP_TABLE_ASM)), 0x40)


ORIG_BOX_CAPACITY0_ASM = [
    b'\xd7',            # rst_addAToHl
    b'\x7e',            # ld a,(hl)
    b'\xb7',            # or a
    b'\xe1',            # pop hl
    b'\xc9',            # ret
    # @ringBoxCapacities:
    0, 1, 3, 5,         # .db $00 $01 $03 $05
    ]
ORIG_BOX_CAPACITY1_ASM = [
    # @ringPositions:
    0x84, 0x87, 0x8a, 0x8d, 0x90,
    # @ringBoxClearTiles:
    0x81, 0x12,     # Level-0
    0x87, 0x0c,     # Level-1
    0x8d, 0x06,     # Level-2
    ]
ORIG_BOX_CAPACITY2_ASM = [
    # Level-1 brackets
    0x2d,           # height/width to copy
    0x07, 0xd2,
    0x13, 0xd2,
    0x00,           # terminator
    # Level-2 brackets
    0x2d,           # height/width to copy
    0x0d, 0xd2,
    0x13, 0xd2,
    0x00,           # terminator
    ]

# DICT NOTES:
# @ offset 7895d
AGES_ORIG_BOX_CAPACITY3_ASM = [
    RING_TEXT_SYMBOLS[TXT_DCT0],  0x1f,
    b"a",
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_COLOR], 0x01,
    b"L-1",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xfb,
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x91,
    b"It",
    RING_TEXT_SYMBOLS[TXT_DCT3],  0x5e,
    RING_TEXT_SYMBOLS[TXT_DCT2],  0xc1,
    b"one",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0x45,
    b"!",
    RING_TEXT_SYMBOLS[TXT_TERM],

    RING_TEXT_SYMBOLS[TXT_DCT0],  0x1f,
    b"a",
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_COLOR], 0x01,
    b"L-2",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xfb,
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x91,
    b"It",
    RING_TEXT_SYMBOLS[TXT_DCT3],  0x5e,
    RING_TEXT_SYMBOLS[TXT_DCT2],  0xc1,
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x4c,
    RING_TEXT_SYMBOLS[TXT_DCT0],  0x29,
    b"!",
    RING_TEXT_SYMBOLS[TXT_TERM],

    RING_TEXT_SYMBOLS[TXT_DCT0],  0x1f,
    b"a",
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_COLOR], 0x01,
    b"L-3",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xfb,
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x91,
    b"It",
    RING_TEXT_SYMBOLS[TXT_DCT3],  0x5e,
    RING_TEXT_SYMBOLS[TXT_DCT2],  0xc1,
    b'five',
    RING_TEXT_SYMBOLS[TXT_DCT0],  0x29,
    b"!",
    RING_TEXT_SYMBOLS[TXT_TERM],
    ]
# @ offset 7bbba
AGES_ORIG_BOX_CAPACITY4_ASM = [
    b"L-1",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xfb,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    b"Holds",
    RING_TEXT_SYMBOLS[TXT_DCT2],  0xde,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    b"seed ",
    RING_TEXT_SYMBOLS[TXT_DCT3],  0x6d,
    b".",
    RING_TEXT_SYMBOLS[TXT_TERM],

    b"L-2",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xfb,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    b"Holds ",
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x4c,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    b"seed ",
    RING_TEXT_SYMBOLS[TXT_DCT3],  0x6d,
    b"s.",
    RING_TEXT_SYMBOLS[TXT_TERM],

    b"L-3",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xfb,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    b"Holds five",
    RING_TEXT_SYMBOLS[TXT_NEWL],
    b"seed ",
    RING_TEXT_SYMBOLS[TXT_DCT3],  0x6d,
    b"s.",
    RING_TEXT_SYMBOLS[TXT_TERM],
    ]

# @ offset 75b05
SEAS_ORIG_BOX_CAPACITY3_ASM = [
    RING_TEXT_SYMBOLS[TXT_DCT0],  0x1b,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_COLOR], 0x01,
    b"L-1",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xd0,
    b" Box",
    RING_TEXT_SYMBOLS[TXT_DCT1],  0xe4,
    b"It",
    RING_TEXT_SYMBOLS[TXT_DCT1],  0x16,
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x70,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_DCT2],  0xad,
    RING_TEXT_SYMBOLS[TXT_DCT0],  0x2a,
    b"!",
    RING_TEXT_SYMBOLS[TXT_TERM],

    RING_TEXT_SYMBOLS[TXT_DCT0],  0x1b,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_COLOR], 0x01,
    b"L-2",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xd0,
    b" Box",
    RING_TEXT_SYMBOLS[TXT_DCT1],  0xe4,
    b"It",
    RING_TEXT_SYMBOLS[TXT_DCT1],  0x16,
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x70,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_DCT1],  0xd9,
    RING_TEXT_SYMBOLS[TXT_DCT0],  0x13,
    b"!",
    RING_TEXT_SYMBOLS[TXT_TERM],

    RING_TEXT_SYMBOLS[TXT_DCT0],  0x1b,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_COLOR], 0x01,
    b"L-3",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xd0,
    b" Box",
    RING_TEXT_SYMBOLS[TXT_DCT1],  0xe4,
    b"It",
    RING_TEXT_SYMBOLS[TXT_DCT1],  0x16,
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x70,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    b'five',
    RING_TEXT_SYMBOLS[TXT_DCT0],  0x13,
    b"!",
    RING_TEXT_SYMBOLS[TXT_TERM],
    ]
# @ offset 772b0
SEAS_ORIG_BOX_CAPACITY4_ASM = [
    b"L-1",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xd0,
    b" Box",
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_DCT3],  0xee,
    b"s",
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x26,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_DCT3],  0x59,
    b" ",
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x51,
    b".",
    RING_TEXT_SYMBOLS[TXT_TERM],

    b"L-2",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xd0,
    b" Box",
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_DCT3],  0xee,
    b"s ",
    RING_TEXT_SYMBOLS[TXT_DCT1],  0xd9,
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_DCT3],  0x59,
    b" ",
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x51,
    b"s.",
    RING_TEXT_SYMBOLS[TXT_TERM],

    b"L-3",
    RING_TEXT_SYMBOLS[TXT_DCT0],  0xd0,
    b" Box",
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_DCT3],  0xee,
    b"s five",
    RING_TEXT_SYMBOLS[TXT_NEWL],
    RING_TEXT_SYMBOLS[TXT_DCT3],  0x59,
    b" ",
    RING_TEXT_SYMBOLS[TXT_DCT2],  0x51,
    b"s.",
    RING_TEXT_SYMBOLS[TXT_TERM],
    ]


ORIG_EQUIP_RING_ASM = [
    b'\x21',W_ACTIVE_RING,          # ld hl,wActiveRing
    b'\x4e',                        # ld c,(hl)
    b'\x2e',W_RING_BOX_CONTENTS_L,  # ld l,<wRingBoxContents
    b'\xd7',                        # rst_addAToHl
    b'\x7e',                        # ld a,(hl)
    b'\xb9',                        # cp c

    b'\x20\x05',                    # jr nz,+
    b'\xfe\xff',                    #   cp $ff
    b'\xc8',                        #   ret z
    b'\x3e\xff',                    #   ld a,$ff
    # +
    b'\xea',W_ACTIVE_RING,          # ld (wActiveRing),a
    b'\x3e\x56',                    # ld a,SND_SELECTITEM
    b'\xc3',PLAY_SOUND,             # jp playSound
    ]
ORIG_DRAW_EQUIP0_ASM = [
    # Draws the "E" on the equipped rings in your inventory
    # drawEquippedSpriteForActiveRing:
    b'\xcd',GET_BOX_CAPACITY,# call getRingBoxCapacity
    b'\xc8',                 # ret z

    b'\x47',                 # ld b,a
    b'\xfa',W_ACTIVE_RING,   # ld a,wActiveRing
    b'\xfe\xff',             # cp $ff
    b'\xc8',                 # ret z

    b'\x21',W_BOX_CONTENTS,  # ld hl,(wRingBoxContents)
    b'\x0e\x00',             # ld c,$00
    # @checkNextRing
    b'\xbe',                 # cp (hl)
    b'\x28\x06',             # jr z,@foundRing
    b'\x23',                 # inc hl
    b'\x0c',                 # inc c
    b'\x05',                 # dec b
    b'\x20\xf8',             # jr nz,@checkNextRing
    b'\xc9',                 # ret

    # @foundRing:
    b'\x3e\x18',             # ld a,$18
    b'\xcd',MUL_A_BY_C,      # call multiplyAByC
    b'\x4d',                 # ld c,l
    b'\x06\x00',             # ld b,$00
    b'\x21',EQUIP_SPRITE0,   # ld hl,(@sprite)
    b'\xc3',ADD_TO_OAM,      # jp addSpritesToOam_withOffset
    ]

ORIG_DRAW_EQUIP2_ASM = [
    # Draws the "E" on the equipped rings in vasu's list
    # drawEquippedSpriteForActiveRing:
    b'\xfa',W_ACTIVE_RING,      # ld a,wActiveRing
    b'\xfe\xff',                # cp $ff
    b'\xc8',                    # ret z

    b'\xcd',RING_IS_IN_BOX,     # call checkRingIsInBox
    b'\xd8',                    # ret c

    b'\xcd',GET_RING_SPRITE_OFF,# call getSpriteOffsetForRingBoxPosition
    b'\x21',EQUIP_SPRITE1,      # ld hl,(@equippedSprite)
    b'\xc3',ADD_TO_OAM,         # jp addSpritesToOam_withOffset
    ]
ORIG_SET_SELECTED_RING_ASM = [
    b'\xfa',RING_MENU_PAGE,  # ld a,(ringMenuPage)
    b'\xcb\x37',             # swap a
    b'\x4f',                 # ld c,a
    b'\xfa',RING_LIST_CURSOR,# ld a,(ringListCursorIndex)
    b'\x81',                 # add c
    b'\xea',SELECTED_RING,   # ld (selectedRing),a
    b'\xc9',                 # ret
    ]
ORIG_DRAW_RING0_ASM = [
    b'\xc5',               # push bc
    b'\xe5',               # push hl
    b'\x78',               # ld a,b
    b'\x21',RING_POS_LIST, # ld hl,ringPositionList-2
    b'\xdf',               # rst_addDoubleIndex
    b'\x2a',               # ldi a,(hl)
    b'\x56',               # ld d,(hl)
    b'\x5f',               # ld e,a
    b'\x79',               # ld a,c
    b'\xcd',GET_RING_TILES,# call getRingTiles
    b'\xe1',               # pop hl
    b'\xc1',               # pop bc
    b'\xc9',               # ret
    ]
ORIG_DRAW_RING_BOX_ASM = [
    b'\x21',W_BOX_CONTENTS,         # ld hl,wRingBoxContents
    b'\x06\x11',                    # ld b,$11

    # @nextRing:
    b'\x2a',                        # ldi a,(hl)
    b'\xfe\xff',                    # cp $ff
    b'\x20\x17',                    # jr nz,@drawRing

    b'\xe5',                        #   push hl
    b'\xc5',                        #   push bc
    b'\x78',                        #   ld a,b
    b'\x21',RING_POS_LIST,          #   ld hl,ringPositionList-2
    b'\xdf',                        #   rst_addDoubleIndex
    b'\x2a',                        #   ldi a,(hl)
    b'\x66',                        #   ld h,(hl)
    b'\x6f',                        #   ld l,a
    b'\x01\x02\x02',                #   ld bc,$02,$02
    b'\x11\x07\x00',                #   ld de,$00,$07
    b'\xcd',FILL_TILEMAP_RECTANGLE, #   call fillRectangleInTilemap
    b'\xc1',                        #   pop bc
    b'\xe1',                        #   pop hl
    b'\x18\x04',                    #   jr ++
    # @drawRing:
    b'\x4f',                        #     ld c,a
    b'\xcd',DRAW_RING0,             #     call drawRing
    # ++
    b'\x04',                        #     inc b
    b'\x7d',                        #     ld a,l
    b'\xfe',W_BOX_CONTENTS_PLUS_5_H,#     cp <wRingBoxContents+5
    b'\x38\xda',                    #     jr c,@nextRing
    b'\xc9',                        # ret
    ]
ORIG_SHOULD_DRAW_RING0_ASM = [
    # @nextRing
    b'\x79',               # ld a,c
    b'\x21',RINGS_OBTAINED,# ld hl,wRingsObtained
    b'\xcd',CHECK_FLAG,    # call checkFlag
    b'\xc4',DRAW_RING0,    # call nz drawRing
    b'\x0c',               # inc c
    b'\x05',               # dec b
    b'\x20\xf2',           # jr nz,@nextRing
    ]
ORIG_DRAW_CARRIED_ASM = [
    b'\x3e\x05',                 # ld a,$05
    b'\xf5',                     # push af
    b'\x21',W_BOX_CONTENTS_MIN_1,# ld hl,wRingBoxContents-1
    b'\xd7',                     # rst_addAToHl
    b'\xfa',RING_MENU_PAGE,      # ld a,(ringMenuPage)
    b'\xcb\x37',                 # swap a
    b'\x4f',                     # ld c,a
    ]
ORIG_GET_RING_BOX_SPRITE_OFF_ASM = [
    b'\xd7',                        # rst_addAToHl
    b'\x4e',                        # ld c,(hl)
    b'\x06\x00',                    # ld b,$00
    b'\xc9',                        # ret
    # @offsets:
    0x38, 0x50, 0x68, 0x80, 0x98,   # .db $38 $50 $68 $80 $98
    ]
ORIG_IS_RING_IN_BOX_ASM = [
    b'\xc5',                        # push bc
    b'\x21',W_BOX_CONTENTS_PLUS_4,  # ld hl,wRingBoxContents+4
    b'\x06\x05',                    # ld b,$05
    # @nextRing:
    b'\xbe',                        # cp (hl)
    b'\x28\x07',                    # jr z,@foundRing
    b'\x2d',                        #   dec l
    b'\x05',                        #   dec b
    b'\x20\xf9',                    #   jr nz,@nextRing
    b'\xc1',                        #     pop bc
    b'\x37',                        #     scf
    b'\xc9',                        #     ret
    # @foundRing:
    b'\x05',                        # dec b
    b'\x78',                        # ld a,b
    b'\xc1',                        # pop bc
    b'\xc9',                        # ret
    ]
ORIG_SEL_RING_FROM_LIST_ASM = [
    b'\x78',                    # ld a,b
    b'\x21',W_BOX_CONTENTS,     # ld hl,wRingBoxContents
    b'\xd7',                    # rst_addAToHl
    b'\x71',                    # ld (hl),c
    ]
ORIG_DISP_RING_BOX_TEXT_ASM = [
    b'\xfa',W_RING_BOX_CURSOR_IDX,  # ld a,(wRingBoxCursorIndex)
    b'\x21',W_BOX_CONTENTS,         # ld hl,wRingBoxContents
    b'\xd7',                        # rst_addAToHl
    b'\x7e',                        # ld a,(hl)
    b'\xea',SELECTED_RING,          # ld (selectedRing),a
    ]
ORIG_RING_BOX_CURSOR_MOVED_ASM = [
    b'\xd0',                        # ret nc
    b'\xc8',                        # ret z
    b'\x21',W_RING_BOX_CURSOR_IDX,  # ld hl,wRingBoxCursorIndex
    b'\x86',                        # add (hl)
    b'\xbb',                        # cp e
    b'\xd0',                        # ret nc
    b'\x77',                        # ld (hl),a
    b'\x3e\x84',                    # ld a,SND_MENU_MOVE
    b'\xc3',PLAY_SOUND,             # jp playSound

    # @directionOffsets:
     1, # .db $01 ; Right
    -1, # .db $ff ; Left
     0, # .db $00 ; Up
     0, # .db $00 ; Down
    ]
ORIG_INV_RING_BOX_CURSOR_MOVED_ASM = [
    b'\x77',                    # ld (hl),a
    b'\x3e\x84',                # ld a,SND_MENU_MOVE
    b'\xc3',PLAY_SOUND,         # jp playSound

    # @updateCursorOnRingBoxRow:
    b'\xe5',                    # push hl
    b'\x21',RING_ROW_POS_MAP,   # ld hl,@ringBoxRowPositionMappings
    # -
    b'\x2a',                    # ldi a,(hl)
    b'\xb9',                    # cp c
    b'\x20\xfc',                # jr nz,-

    b'\xcb\x58',                # bit 3,b
    b'\x28\x02',                # jr z,+
    b'\x2b',                    # dec hl
    b'\x2b',                    # dec hl
    # +
    b'\x7e',                    # ld a,(hl)
    b'\xe1',                    # pop hl
    b'\xc9',                    # ret

    # @ringBoxRowPositionMappings:
    0x0a, 0x10, 0x00, # .db $0a $10 $00
    0x0b, 0x11, 0x01, # .db $0b $11 $01
    0x0c, 0x12, 0x02, # .db $0c $12 $02
    0x0d, 0x13, 0x03, # .db $0d $13 $03
    0x0e, 0x14, 0x04, # .db $0e $14 $04
    0x0a, 0x0f, 0x00, # .db $0a $0f $00
    ]


ORIG_DRAW_INV_RING_BOX_ASM = [
    b'\xcd',GET_BOX_CAPACITY,    # call getRingBoxCapacity
    b'\xc8',                     # ret z
    b'\x47',                     # ld b,a
    # @drawRing:
    b'\x78',                     # ld a,b
    b'\x21',RING_POS_MIN_1,      # ld hl,@ringPositions-1
    b'\xd7',                     # rst_addAToHl
    b'\x5e',                     # ld e,(hl)
    b'\x16\xd1',                 # ld d,>w4TileMap+1

    b'\x78',                     # ld a,b
    b'\x21',W_BOX_CONTENTS_MIN_1,# ld hl,wRingBoxContents-1
    b'\xd7',                     # rst_addAToHl
    b'\x7e',                     # ld a,(hl)
    b'\xfe\xff',                 # cp $ff

    b'\x28\x10',                 # jr z,@nextRing

    b'\xc5',                     # push bc
    b'\x4f',                     # ld c,a
    b'\x78',                     # ld a,b
    b'\x21',W4_SUBSCREEN_TEXT_INDICES_PLUS_F, # ld hl,w4SubscreenTextIndices+$f
    b'\xd7',                     # rst_addAToHl
    b'\x79',                     # ld a,c
    b'\xf6\xc0',                 # or $c0
    b'\x77',                     # ld (hl),a

    # Draw ring
    b'\x79',                     # ld a,c
    b'\xcd',GET_RING_TILES,      # call getRingTiles

    b'\xc1',                     # pop bc
    # @nextRing:
    b'\x05',                     # dec b
    b'\x20\xdb',                 # jr nz,@drawRing

    # ; Set text and icon for ring box based on level
    b'\xfa',W_BOX_LEVEL,        # ld a,(wRingBoxLevel)
    b'\xc6\x1c',                # add <TX_091d-1
    b'\xea',W4_SUBSCREEN_TEXT_INDICES_PLUS_F, # ld (w4SubscreenTextIndices+$f),a
    b'\x11\x82\xd1',            # ld de,w4TileMap+$182
    b'\x3e\xfe',                # ld a,$fe
    b'\xc3',GET_RING_TILES,     # jp getRingTiles
    ]

ORIG_SUBMENU1_DRAW_CURSOR_ASM = [
    b'\xfa',MENU1_CURSOR_POS,    # ld a,(wInventorySubmenu1CursorPos)
    b'\x5f',                     # ld e,a
    b'\x21',SUBMENU1_CURSOR_OFFS,# ld hl,@data
    b'\xd7',                     # rst_addAToHl
    b'\x7e',                     # ld a,(hl)
    b'\xe6\xf0',                 # and $f0
    b'\x0f',                     # rrca
    ]
ORIG_SUBSCREEN1_MAIN_ASM = [
    b'\xfa',MENU1_CURSOR_POS,   # ld a,(wInventorySubmenu1CursorPos)
    b'\xcd',SHOW_ITEM_TEXT1,    # call showItemText1
    ]
ORIG_DRAW_RING_BOX_CURSOR_ASM = [
    b'\xfa',W_RING_BOX_CURSOR_IDX,  # ld a,(wRingBoxCursorIndex)
    b'\xcd',GET_RING_SPRITE_OFF,    # call getSpriteOffsetForRingBoxPosition
    b'\x21',RING_BOX_CURSOR,        # ld hl,@ringBoxCursor
    b'\xc3',ADD_TO_OAM,             # jp addSpritesToOam_withOffset
    ]

NEW_SET_SELECTED_RING_ASM       = list(ORIG_SET_SELECTED_RING_ASM)
NEW_SHOULD_DRAW_RING0_ASM       = list(ORIG_SHOULD_DRAW_RING0_ASM)
NEW_DRAW_RING0_ASM              = list(ORIG_DRAW_RING0_ASM)
NEW_GET_RING_BOX_SPRITE_OFF_ASM = list(ORIG_GET_RING_BOX_SPRITE_OFF_ASM)
NEW_SEL_RING_FROM_LIST_ASM      = list(ORIG_SEL_RING_FROM_LIST_ASM)
NEW_DISP_RING_BOX_TEXT_ASM      = list(ORIG_DISP_RING_BOX_TEXT_ASM)
NEW_RING_BOX_CURSOR_MOVED_ASM   = list(ORIG_RING_BOX_CURSOR_MOVED_ASM)
NEW_SUBSCREEN1_MAIN_ASM         = list(ORIG_SUBSCREEN1_MAIN_ASM)
NEW_DRAW_RING_BOX_CURSOR_ASM    = list(ORIG_DRAW_RING_BOX_CURSOR_ASM)

# replace the instruction with calls to new code
NEW_SET_SELECTED_RING_ASM[-3:-1]    = b'\xcd', GET_SELECTED_RING1
NEW_SHOULD_DRAW_RING0_ASM[4]        = SHOULD_DRAW_RING1
NEW_DRAW_RING0_ASM[-4]              = DRAW_RING1
NEW_GET_RING_BOX_SPRITE_OFF_ASM[:3] = [
    b'\xcd',GET_RING_BOX_SPRITE_OFF1,
    b'\x00',
    ]
NEW_SEL_RING_FROM_LIST_ASM[1:3] = [
    b'\xcd',SEL_RING_FROM_LIST1,
    ]
NEW_DISP_RING_BOX_TEXT_ASM[2:4] = [
    b'\xcd',SEL_RING_FROM_LIST1,
    ]
NEW_RING_BOX_CURSOR_MOVED_ASM[4:8] = [
    b'\xcd',RING_BOX_CURSOR_MOVED1,
    b'\x00'
    ]
NEW_RING_BOX_CURSOR_MOVED_ASM[-2:] = [-5, 5]
NEW_SUBSCREEN1_MAIN_ASM[:2] = [
    b'\xcd',SUBMENU1_DRAW_CURSOR1,
    ]
NEW_DRAW_RING_BOX_CURSOR_ASM[-1:] = [
    DRAW_RING_BOX_CURSOR1,
    ]

DRAW_RING_BOX_CURSOR1_ASM = [
    b'\xcd',ADD_TO_OAM,             # call addSpritesToOam_withOffset

    b'\xcd',GET_BOX_CAPACITY,       # call getRingBoxCapacity
    b'\xfe\x06',                    # cp $06
    b'\xd8',                        # ret c

    b'\xfa',W_RING_BOX_CURSOR_IDX,  # ld a,(wRingBoxCursorIndex)
    b'\x21',ARROW_DOWN_SPRITE_RED,  # ld hl,arrowDownSpriteRed
    b'\xfe\x05',                    # cp $05

    b'\x38\x03',                    # jr c,+
    b'\x21',ARROW_UP_SPRITE_BLUE,   #   ld hl,arrowUpSpriteBlue

    b'\x01\x1a\x11',                # ld bc,$11,$1a
    b'\xe5',                        # push hl
    b'\xcd',ADD_TO_OAM,             # call addSpritesToOam_withOffset
    b'\xe1',                        # pop hl

    b'\x0e\x20',                    # ld c,$20
    b'\xe5',                        # push hl
    b'\xcd',ADD_TO_OAM,             # call addSpritesToOam_withOffset
    b'\xe1',                        # pop hl

    b'\x0e\x26',                    # ld c,$26
    b'\xc3',ADD_TO_OAM,             # jp addSpritesToOam_withOffset
    ]

NEW_EQUIP_RING_ASM = [
    b'\x21',W_ACTIVE_RING,          # ld hl,wActiveRing
    b'\x4e',                        # ld c,(hl)
    b'\x2e',W_RING_BOX_CONTENTS_L,  # ld l,<wRingBoxContents
    b'\xfe\x05',                    # cp $05
    b'\x38\x03',                    # jr c,+
    b'\x21',W_BOX_CONTENTS_EXT,     #   ld hl,wRingBoxContentsExt
    # +
    b'\xcd',EQUIP_RING1,            # call equipRing1

    b'\xea',W_ACTIVE_RING,          # ld (wActiveRing),a
    b'\x3e\x56',                    # ld a,SND_SELECTITEM
    b'\xc3',PLAY_SOUND,             # jp playSound
    ]

EQUIP_RING1_ASM = [
    b'\xfe\x05',            # cp $05
    b'\x38\x02',            # jr c,+
    b'\xd6\x05',            #   sub $05
    # +
    b'\xd7',                # rst_addAToHl
    b'\x7e',                # ld a,(hl)
    b'\xb9',                # cp c

    b'\x20\x05',            # jr nz,++
    b'\xfe\xff',            #   cp $ff
    b'\xc8',                #   ret z
    b'\x3e\xff',            #   ld a,$ff
    # ++
    b'\xc9',                # ret
    ]
NEW_INV_RING_BOX_CURSOR_MOVED_ASM = [
    b'\x77',                            # ld (hl),a
    b'\xcd',DRAW_INV_RING_BOX,          # call @drawInvRingBox
    b'\x18\x11',                        # jr @playSoundAndReloadRings

    # @updateCursorOnRingBoxRow:
    b'\xe5',                            # push hl
    b'\x21',INV_RING_BOX_CURSOR_MOVED1, # ld hl,@invRingBoxCursorMoved1
    # -
    b'\x2a',                            # ldi a,(hl)
    b'\xb9',                            # cp c
    b'\x20\xfc',                        # jr nz,-

    b'\xcb\x58',                        # bit 3,b
    b'\x28\x02',                        # jr z,+
    b'\x2b',                            # dec hl
    b'\x2b',                            # dec hl
    # +
    b'\x7e',                            # ld a,(hl)

    # @done
    b'\xe1',                            # pop hl
    b'\xc9',                            # ret


    b'\x3e\x84',                        # ld a,SND_MENU_MOVE
    b'\xcd',PLAY_SOUND,                 # call playSound
    b'\xcd',RELOAD_INV_MENU_GFX,        # call reloadInvMenuGfx
    b'\x00'*10,                         # nop
    ]

INV_RING_BOX_CURSOR_MOVED1_ASM = [
    # @ringBoxRowPositionMappings:
    0x0a, 0x0f, 0x00,       # .db $0a $0f $00
    0x0a, 0x10, 0x15, 0x00, # .db $0a $10 $15 $00
    0x0b, 0x11, 0x16, 0x01, # .db $0b $11 $16 $01
    0x0c, 0x12, 0x17, 0x02, # .db $0c $12 $17 $02
    0x0d, 0x13, 0x18, 0x03, # .db $0d $13 $18 $03
    0x0e, 0x14, 0x19, 0x04, # .db $0e $14 $19 $04
    ]

NEW_SUBMENU1_DRAW_CURSOR_ASM = list(ORIG_SUBMENU1_DRAW_CURSOR_ASM)
NEW_SUBMENU1_DRAW_CURSOR_ASM[:2] = [
    b'\xcd',SUBMENU1_DRAW_CURSOR1, # call submenu1DrawCursor1
    ]

SUBMENU1_DRAW_CURSOR1_ASM = [
    b'\xfa',MENU1_CURSOR_POS,   # ld a,(wInventorySubmenu1CursorPos)
    b'\xfe\x15',                # cp $15
    b'\xd8',                    # ret c
    b'\xd6\x05',                # sub $05
    b'\xc9',                    # ret
    ]

NEW_DRAW_INV_RING_BOX_ASM = [
    b'\xcd',DRAW_INV_RING_BOX1,      # call drawInvRingBox1
    b'\xc8',                         # ret z
    b'\xe5',                         # push hl

    # @drawRing:
    b'\x78',                         # ld a,b
    b'\x21',RING_POS_MIN_1,          # ld hl,@ringPositions-1
    b'\xd7',                         # rst_addAToHl
    b'\x5e',                         # ld e,(hl)
    b'\x16\xd1',                     # ld d,>w4TileMap+1

    b'\x78',                         # ld a,b
    b'\xe1',                         # pop hl
    b'\xe5',                         # push hl
    b'\xd7',                         # rst_addAToHl
    b'\x7e',                         # ld a,(hl)
    b'\xfe\xff',                     # cp $ff

    b'\x28\x10',                     # jr z,@nextRing

    b'\xc5',                         #   push bc
    b'\x4f',                         #   ld c,a
    b'\x78',                         #   ld a,b
    b'\x21',W4_SUBSCREEN_TEXT_INDICES_PLUS_F, # ld hl,w4SubscreenTextIndices+$f
    b'\xd7',                         #   rst_addAToHl
    b'\x79',                         #   ld a,c
    b'\xf6\xc0',                     #   or $c0
    b'\x77',                         #   ld (hl),a

    # Draw ring
    b'\x79',                         #   ld a,c
    b'\xcd',GET_RING_TILES,          #   call getRingTiles

    b'\xc1',                         #   pop bc
    # @nextRing:
    b'\x05',                         # dec b
    b'\x20\xdc',                     # jr nz,@drawRing
    b'\xf1',                         # pop af

    # ; Set text and icon for ring box based on level
    b'\xfa',W_BOX_LEVEL,             # ld a,(wRingBoxLevel)
    b'\xc6\x1c',                     # add <TX_091d-1
    b'\xea',W4_SUBSCREEN_TEXT_INDICES_PLUS_F, # ld (w4SubscreenTextIndices+$f),a
    b'\x11\x82\xd1',                 # ld de,w4TileMap+$182
    b'\x3e\xfe',                     # ld a,$fe
    b'\xc3',GET_RING_TILES,          # jp getRingTiles
    ]

DRAW_INV_RING_BOX1_ASM = [
    b'\xcd',GET_BOX_CAPACITY,        # call getRingBoxCapacity
    b'\xc8',                         # ret z
    b'\x47',                         # ld b,a
    
    b'\xfa',MENU1_CURSOR_POS,        # ld a,(wInventorySubmenu1CursorPos)
    b'\xfe\x15',                     # cp $15
    b'\x78',                         # ld a,b
    b'\x21',W_BOX_CONTENTS_MIN_1,    # ld hl,wRingBoxContents-1
    b'\x38\x03',                     # jr c,+
    b'\x21',W_BOX_CONTENTS_EXT_MIN_1,#   ld hl,wRingBoxContentsExt-1
    # +
    b'\xfe\x06',                     # cp $06
    b'\x38\x02',                     # jr c,+
    b'\x3e\x05',                     #   ld a,$05
    b'\x47',                         # ld b,a
    b'\xb7',                         # or a
    b'\xc9',                         # ret
    ]

NEW_DRAW_RING_BOX_ASM = [
    b'\x21',W_BOX_CONTENTS,         # ld hl,wRingBoxContents
    b'\xcd',DRAW_RING_BOX1,         # call drawRingBox1

    # @nextRing:
    b'\xf5',                        # push af
    b'\xe5',                        # push hl
    b'\x21',RING_POS_LIST,          # ld hl,ringPositionList-2
    b'\xdf',                        # rst_addDoubleIndex
    b'\x2a',                        # ldi a,(hl)
    b'\x66',                        # ld h,(hl)
    b'\x6f',                        # ld l,a
    b'\x01\x02\x02',                # ld bc,$02,$02
    b'\x11\x07\x00',                # ld de,$00,$07
    b'\xcd',FILL_TILEMAP_RECTANGLE, # call fillRectangleInTilemap
    b'\xe1',                        # pop hl
    b'\x2a',                        # ldi a,(hl)
    b'\xfe\xff',                    # cp $ff
    b'\xc1',                        # pop bc
    b'\x4f',                        # ld c,a
    b'\x78',                        # ld a,b
    b'\x28\x05',                    # jr z,++
    b'\xf5',                        #   push af
    b'\xcd',DRAW_RING0,             #   call drawRing
    b'\xf1',                        #   pop af
    # ++
    b'\x3c',                        # inc a
    b'\xfe\x16',                    # cp $16
    b'\x38\xdb',                    # jr c,@nextRing
    b'\xc9',                        # ret
    ]

NEW_DRAW_EQUIP0_ASM = [
    # Draws the "E" on the equipped rings in your inventory
    # drawEquippedSpriteForActiveRing:
    b'\xfa',MENU1_CURSOR_POS,   # ld a,(wInventorySubmenu1CursorPos)
    b'\xcd',DRAW_EQUIP1,        # call drawEquip1

    # @checkNextRing
    b'\x7e',                    # ld a,(hl)
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\x28\x06',                # jr z,@foundRing
    # @moveToNextRing
    b'\x23',                    # inc hl
    b'\x0c',                    # inc c
    b'\x05',                    # dec b
    b'\x20\xf5',                # jr nz,@checkNextRing
    b'\xc9',                    # ret

    # @foundRing:
    b'\xc5',                    # push bc
    b'\xf5',                    # push af
    b'\xe5',                    # push hl
    b'\x3e\x18',                # ld a,$18
    b'\xcd',MUL_A_BY_C,         # call multiplyAByC
    b'\x43',                    # ld b,e    HACK (relies on multiplyAByC setting e to $00)
    b'\x4d',                    # ld c,l
    b'\x21',EQUIP_SPRITE0,      # ld hl,(@sprite)
    b'\xcd',ADD_TO_OAM,         # call addSpritesToOam_withOffset
    b'\xe1',                    # pop hl
    b'\xf1',                    # pop af
    b'\xc1',                    # pop bc
    b'\x18\xe5',                # jr @moveToNextRing
    ]
DRAW_EQUIP1_ASM = [
    b'\xfe\x10',                    # cp $10
    b'\x38\x25',                    # jr c,@done
    b'\xfe\x15',                    #   cp $15
    b'\x21',ARROW_DOWN_SPRITE_RED,  #   ld hl,arrowDownSpriteRed
    b'\x38\x03',                    #   jr c,+
    b'\x21',ARROW_UP_SPRITE_BLUE,   #     ld hl,arrowUpSpriteBlue

    b'\xcd',GET_BOX_CAPACITY,       #   call getRingBoxCapacity
    b'\xfe\x06',                    #   cp $06
    b'\x38\x16',                    #   jr c,@done
    b'\xfa',W_FRAME_COUNTER,        #     ld a,(wFrameCounter)
    b'\xcb\x5f',                    #     bit 3,a
    b'\x28\x0d',                    #     jr z,@done
    b'\x01\x20\x70',                #       ld bc,$68,$20
    b'\xe5',                        #       push hl
    b'\xcd',ADD_TO_OAM,             #       call addSpritesToOam_withOffset
    b'\xe1',                        #       push hl

    b'\x0e\x99',                    #       ld c,$99
    b'\xcd',ADD_TO_OAM,             #       call addSpritesToOam_withOffset

    # @done

    b'\xcd',GET_BOX_CAPACITY,   # call getRingBoxCapacity
    b'\xfe\x06',                # cp $06
    b'\x38\x02',                # jr c,@done
    b'\x3e\x05',                #   ld a,$05
    b'\x47',                    # ld b,a
    b'\x0e\x00',                # ld c,$00
    b'\x21',W_BOX_CONTENTS,     # ld hl,(wRingBoxContents)
    b'\xfa',MENU1_CURSOR_POS,   # ld a,(wInventorySubmenu1CursorPos)
    b'\xd6\x15',                # sub $15
    b'\xd8',                    # ret c
    b'\x21',W_BOX_CONTENTS_EXT, # ld hl,wRingBoxContentsExt
    b'\xc9',                    # ret
    ]

DRAW_RING_BOX1_ASM = [
    b'\xfa',W_RING_BOX_CURSOR_IDX,  # ld a,(wRingBoxCursorIndex)
    b'\xfe\x05',                    # cp $05
    b'\x3e\x11',                    # ld a,$11
    b'\xd8',                        # ret c
    b'\x21',W_BOX_CONTENTS_EXT,     # ld hl,wRingBoxContentsExt
    b'\xc9',                        # ret
    ]

GET_RING_BOX_SPRITE_OFF1_ASM = [
    b'\xf5',            # push af
    b'\xfe\x05',        # cp $05
    b'\x38\x02',        # jr c,+
    b'\xd6\x05',        #   sub,$05
    b'\xd7',            # rst_addAToHl
    b'\x4e',            # ld c,(hl)
    b'\x06\x00',        # ld b,$00
    b'\xf1',            # pop af
    b'\xc9',            # ret
    ]

NEW_IS_RING_IN_BOX_ASM = [
    PUSH_BC,                    # push bc
    LD_B_A,                     # ld b,a
    CALL,   GET_BOX_CAPACITY,   # call getRingBoxCapacity
    LD_C_A,                     # ld c,a
    XOR_A,                      # xor a

    CALL,   IS_RING_IN_BOX1,    # call isRingInBox1

    POP_BC,                     # pop bc
    SCF,                        # scf
    CCF,                        # ccf
    RET,                        # ret
    b'\x00'*6
    ]
IS_RING_IN_BOX1_ASM = [
    Label("@nextRing"),
    PUSH_AF,                    # push af
    CP,             5,          # cp $05
    JR_C,       "else",         # jr c,else
    LD_HL,  W_BOX_CONTENTS_EXT, #   ld hl,wRingBoxContentsExt
        SUB,            5,      #   sub 5
        JR,            "+",     #   jr +
    Label("else"),
        LD_HL,  W_BOX_CONTENTS, #   ld hl,wRingBoxContents

    Label("+"),
    RST_10H,                    # rst_addAToHl

    LD_A_B,                     # ld a,b
    CP_HLP,                     # cp (hl)
    JR_Z,      "@foundRing",    # jr z,@foundRing
    POP_AF,                     #   pop af
    INC_A,                      #   inc a
    CP_C,                       #   cp c
    JR_NZ,      "@nextRing",    #   jr nz,@nextRing
    # intentional stack manipulation
    POP_BC,                     #     pop bc
    POP_BC,                     #     pop bc
    SCF,                        #     scf
    RET,                        #     ret

    Label("@foundRing"),
    POP_AF,                     # pop af
    RET,                        # ret
    ]
SEL_RING_FROM_LIST1_ASM = [
    b'\x21',W_BOX_CONTENTS,     # ld hl,wRingBoxContents
    b'\xfe\x05',                # cp $05
    b'\xd8',                    # ret c
    b'\x21',W_BOX_CONTENTS_EXT, # ld hl,wRingBoxContentsExt
    b'\xd6\x05',                # sub,$05
    b'\xc9',                    # ret
    ]

RING_BOX_CURSOR_MOVED1_ASM = [
    b'\x86',                    # add (hl)

    # if would move to before start, move relative to end
    b'\xfe\x80',                # cp $80
    b'\x38\x03',                # jr c,+
    b'\x47',                    #   ld b,a
    b'\x7b',                    #   ld a,e
    b'\x80',                    #   add b

    # +
    # if would move past end, move relative to start
    b'\xbb',                    # cp e
    b'\x38\x01',                # jr c,++
    b'\x93',                    #   sub e

    # ++
    # handle edge cases when ring box size isn't at least 5
    b'\xbb',                    # cp e
    b'\x38\x02',                # jr c,+++
    b'\x7b',                    #   ld a,e
    b'\x3d',                    #   dec a

    # +++
    b'\xfe\x80',                # cp $80
    b'\x38\x01',                # jr c,++++
    b'\xaf',                    #   xor a

    # ++++
    b'\x77',                    # ld (hl),a
    b'\xf5',                    # push af
    b'\x21',DISP_RING_NUM_COMP, # ld hl,displayedRingNumberComparator
    b'\x7e',                    # ld a,(h1)
    b'\xfe\xff',                # cp $ff
    b'\x20\x02',                # jr nz,@redraw
    # force redraw by setting previous value to an invalid index
    LD_HLP,         0x80,       #   ld (hl),$80
    # @redraw
    b'\xcd',DRAW_RING_BOX,      # call drawRingBox
    b'\xf1',                    # pop af
    b'\xc9',                    # ret
    ]

# NOTE: it would be fairly complicated to modify this to show every
#       ring as equipped. since the only rings that wont be equipped
#       are transform rings, we wont show anything since its assumed
NEW_DRAW_EQUIP2_ASM     = list(ORIG_DRAW_EQUIP2_ASM)
NEW_DRAW_EQUIP2_ASM[0]  = b'\xc9' # ret

# NOTE: just like the previous one, we won't bother drawing the "C"
#       on rings we're carrying since it'd be fairly complex for
#       very little payoff(besides, you can just look at your box)
NEW_DRAW_CARRIED_ASM     = list(ORIG_DRAW_CARRIED_ASM)
NEW_DRAW_CARRIED_ASM[0]  = b'\xc9\x00' # ret nop


REMAP_SELECTED_RING_ASM = [
    # only remap rings if in the ring box, not the appraisal menu
    b'\xc5',               # push bc
    b'\x4f',               # ld c,a
    b'\xfa',RING_MENU_MODE,# ld a,(wRingMenu_mode)
    b'\xfe\x00',           # cp $00
    b'\x79',               # ld a,c
    b'\xc1',               # pop bc
    b'\x28\x07',           # jr z,@done
    b'\xe5',               # push hl
    b'\x21',RING_MAP_TABLE,# ld hl,@ringMapTable
    b'\xd7',               # rst_addAToHl
    b'\x7e',               # ld a,(h1)
    b'\xe1',               # pop hl
    # @done
    ]

GET_SELECTED_RING1_ASM = [
    *REMAP_SELECTED_RING_ASM,
    b'\xea',SELECTED_RING, # ld (selectedRing),a
    b'\xc9',               # ret
    ]
DRAW_RING1_ASM = [
    b'\x78',               # ld a,b
    # if the selected ring is 16 or higher, it's
    # in the ring box and shouldnt be remapped.
    # we check $11 instead of $10 because the
    # original code uses one-based indexing.
    b'\xfe\x11',           # cp $11
    b'\x79',               # ld a,c
    b'\x38\x04',           # jr c,@remap
    b'\xcd',GET_RING_TILES,#   call getRingTiles
    b'\xc9',               #   ret
    # @remap
    *REMAP_SELECTED_RING_ASM,
    # @done
    b'\xcd',GET_RING_TILES,# call getRingTiles
    b'\xc9',               # ret
    ]
SHOULD_DRAW_RING1_ASM = [
    *REMAP_SELECTED_RING_ASM,
    b'\xcd',CHECK_FLAG,    # call checkFlag
    b'\xc9',               # ret
    ]


ORIG_RING_BOX_MENU0_ASM = [
    b'\xfa',MENU1_CURSOR_POS,# ld a,(wInventorySubmenu1CursorPos)
    b'\xd6\x10',             # sub $10
    b'\xd8',                 # ret c
    ]
NEW_RING_BOX_MENU0_ASM = [
    b'\xcd',RING_BOX_MENU1,# call ringBoxMenu
    b'\xd6\x10',           # sub $10
    b'\xd8',               # ret c
    ]
RING_BOX_MENU1_ASM = [
    # this will allow opening the ring list menu from the inventory
    LD_A_A16,   MENU1_CURSOR_POS,       # ld a,(wInventorySubmenu1CursorPos)
    CP,         0x0F,                   # cp $0f
    RET_NZ,                             # ret nz
    # make the ring box only openable in the menu at level-3
    # or if you're carrying the friendship ring
    LD_A,       VASUS_RING,             # ld a,VASUS_RING
    CALL,       CP_ACTIVE_RING0,        # call cpActiveRing
    JR_Z,       "@openPortalBox",       # jr z,@openPortalBox
    LD_A_A16,   W_BOX_LEVEL,            # ld a,(wRingBoxLevel)
    CP,         PORTAL_BOX_LEVEL,       # cp $portalBoxLevel
    RET_C,                              # ret c
    Label("@openPortalBox"),
    LD_A,       0x56,                   # ld a,SND_SELECTITEM
    CALL,       PLAY_SOUND,             # call playSound
    LD_A,       0x81,                   # ld a,RING_MENU_TYPE_LIST | 0x80
    LD_A16_A,   RING_MENU_MODE,         # ld (wRingMenu_mode),a
    LD_A,       MENU_TYPE_RINGS,        # ld a,$04
    LD_A16_A,   OPENED_MENU_TYPE,       # ld (wOpenedMenuType),a
    CALL,       OPEN_MENU,              # call openMenu
    # set the camera coords to zero or it messes up text rendering
    XOR_A,                              # xor a
    PUSH_HL,                            # push hl
    LD_HL,  H_CAMERA_Y,                 # ld hl,(hCameraY)
    LDI_HLP_A,                          # ldi (hl),a
    LDI_HLP_A,                          # ldi (hl),a
    LDI_HLP_A,                          # ldi (hl),a
    LDI_HLP_A,                          # ldi (hl),a
    LD_HL,  W_SCREEN_OFF_Y,             # ld hl,(wScreenOffsetY)
    LDI_HLP_A,                          # ldi (hl),a
    LDI_HLP_A,                          # ldi (hl),a
    POP_HL,                             # pop hl
    RET,                                # ret
    ]

ORIG_OPEN_MENU0_ASM = [
    # @openMenu:
    LD_A_A16,   OPENED_MENU_TYPE,   # ld a,(wOpenedMenuType)
    CP,         3,                  # cp MENU_SAVEQUIT
    LD_A,       0x54,               # ld a,SND_OPENMENU
    CALL_NZ,    PLAY_SOUND,         # call nz,playSound
    LD_A,       2,                  # ld a,$02
    CALL,       SET_MUSIC_VOLUME,   # call setMusicVolume
    ]

NEW_OPEN_MENU0_ASM = list(ORIG_OPEN_MENU0_ASM)
NEW_OPEN_MENU0_ASM[-1] = OPEN_MENU1

OPEN_MENU1_ASM = [
    CALL,       SET_MUSIC_VOLUME,   # call setMusicVolume
    LD_A_A16,   RING_MENU_MODE,     # ld a,(wRingMenu_mode)
    BIT7_A,                         # bit 7,a
    RET_Z,                          # ret z
    RES7_A,                         # res 7,a
    LD_A16_A,   RING_MENU_MODE,     # ld (wRingMenu_mode),a
    # graphics were already saved, so if we're entering the ring menu
    # from within another menu we don't want to save the graphics again.
    # avoid this by using stack manipulation to jump out of the parent call
    POP_AF,                         # pop af
    RET,                            # ret
    ]
