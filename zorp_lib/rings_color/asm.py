from .const import *
from ..const import *
from ..shared.const import *


ORIG_GBOY_COLOR_RING_ICON_ASM = [
    # whisp ring sprite data
    b'\xc0\x02\xbe\x02',
    b'\xc1\x02\xbf\x02',
    ]
NEW_GBOY_COLOR_RING_ICON_ASM  = [
    b'\x4f\x62\xda\x02',
    b'\x4d\x02\xdd\x07',
    ]

ORIG_RUPEE_RING_ICON_ASM = [
    b'\xcb\x03\xdc\x07',
    b'\xde\x07\xdd\x07',
    ]
NEW_RUPEE_RING_ICON_ASM  = [
    b'\xcb\x02\xdc\x07',
    b'\xde\x07\xdd\x07',
    ]

ORIG_SLAYERS_RING_ICON_ASM = [
    b'\xcf\x05\xdc\x06',
    b'\xde\x06\xdd\x06',
    ]
NEW_SLAYERS_RING_ICON_ASM  = [
    b'\xcf\x04\xdc\x06',
    b'\xde\x06\xdd\x06',
    ]

ORIG_SIGN_RING_ICON_ASM = [
    b'\xcd\x05\xdc\x06',
    b'\xde\x06\xdd\x06',
    ]
NEW_SIGN_RING_ICON_ASM  = [
    b'\xcd\x05\xdc\x06',
    b'\xd3\x03\xde\x26',
    ]

ORIG_ENTRYPOINT_ASM = [
    b'\x00',                # nop
    b'\xf3',                # di
    b'\xfe\x11',            # cp $11
    b'\x3e\x00',            # ld a,$00
    b'\x20\x07',            # jr nz,+

    # ; Check GBA Mode
    b'\x3c',                # inc a
    b'\xcb\x40',            # bit 0,b
    b'\x28\x02',            # jr z,+
    b'\x3e\xff',            # ld a,$ff
    # +
    b'\xe0',H_GAMEBOY_TYPE, # ldh (<hGameboyType),a
    b'\x3e\x37',            # ld a,$37
    b'\xe0\x94',            # ldh (<hRng1),a
    b'\x3e\x0d',            # ld a,$0d
    b'\xe0\x95',            # ldh (<hRng1),a
    ]
NEW_ENTRYPOINT_ASM    = list(ORIG_ENTRYPOINT_ASM)
NEW_ENTRYPOINT_ASM[7] = b'\x00\x00'

ORIG_MAIN_LOOP_ASM = [
    b'\x87',                            # add a
    b'\x28\x08',                        # jr z,+

    b'\xfa',W_KEYS_PRESSED,             # ld a,(wKeysPressed)
    b'\xd6',0x01 | 0x02 | 0x08 | 0x04,  # sub (BTN_A | BTN_B | BTN_START | BTN_SELECT)
    b'\xca',RESET_GAME,                 # jp z,resetGame
    # +

    b'\x3e\x10',                        # ld a,$10
    b'\xe0',H_OAM_TAIL,                 # ldh (<hOamTail),a
    b'\x26',W_THREAD_STATE_BUFFER_H,    # ld h,>wThreadStateBuffer
    b'\x3e',W_THREAD_STATE_BUFFER_L,    # ld a,<wThreadStateBuffer
    b'\xe0',H_ACTIVE_THREAD,            # ldh (<hActiveThread),a
    # --
    ]
NEW_MAIN_LOOP_ASM = list(ORIG_MAIN_LOOP_ASM)
NEW_MAIN_LOOP_ASM[6:8] = [
    b'\xcd',MAIN_LOOP1,     # call mainLoop1
    ]

MAIN_LOOP1_ASM = [
    b'\xca',RESET_GAME,             # jp z,resetGame

    # clear the extended box contents if the extra byte at the end
    # isn't 0x00, as that indicates this code was never run there
    b'\xe5',                        # push hl
    b'\xaf',                        # xor a
    b'\x21',W_BOX_CONTENTS_EXT,     # ld hl,wRingBoxContentsExt
    b'\x2c'*5,                      # inc l // (5 times)
    # @checkNext
    b'\xbe',                        # cp (hl)
    b'\x20\x09',                    # jr nz,@done
    b'\x2f',                        #   cpl
    b'\x06\x06',                    #   ld b,$06
    b'\x21',W_BOX_CONTENTS_EXT,     #   ld hl,wRingBoxContentsExt
    b'\xcd',FILL_MEMORY,            #   call fillMemory
    # @done
    b'\xe1',                        # pop hl

    # change mode to GBC if wearing ring
    b'\x3e',GBOY_COLOR_RING,        # ld a,GBOY_COLOR_RING
    b'\xcd',CP_ACTIVE_RING0,        # call cpActiveRing
    b'\x3e',GAMEBOY_TYPE_GBA,       # ld a,GAMEBOY_TYPE_GBA
    b'\x20\x02',                    # jr nz,@notGBC
    b'\x3e',GAMEBOY_TYPE_GBC,       # ld a,GAMEBOY_TYPE_GBC
    b'\xe0',H_GAMEBOY_TYPE,         # ldh (<hGameboyType),a
    b'\xc9',                        # ret
    ]

ORIG_RING_PALETTE0_ASM = [
    b'\x20', b'\xee',             # jr nz,@resetIDToNormal
    b'\xfa',W_PALETTE_THREAD_MODE,# ld a,(wPaletteThread_mode)
    b'\xb7',                      # or a
    b'\xc0',                      # ret nz
    b'\xfa',W_SCROLL_MODE,        # ld a,(wScrollMode)
    b'\xe6\x0e',                  # and $0e
    b'\xc0',                      # ret nz
    ]
ORIG_RING_PALETTE1_ASM = list(ORIG_RING_PALETTE0_ASM)
ORIG_RING_PALETTE1_ASM[:2] = [
    b'\xea',W_FORCE_LINK_PUSH_ANIM,# ld (wForceLinkPushAnimation),a
    ]
ORIG_RING_PALETTE2_ASM = [
    b'\xfa',W_PALETTE_THREAD_MODE,# ld a,(wPaletteThread_mode)
    b'\xb7',                      # or a
    b'\xc0',                      # ret nz
    b'\xcd',UPDATE_LINK_DAMAGED,  # call updateLinkDamageTaken
    b'\xcd',RET_IF_TEXT_IS_ACTIVE,# call retIfTextIsActive
    ]
ORIG_RING_PALETTE3_ASM = [
    b'\x1e\x32'                 # ld e,SpecialObject.var32
    b'\x3e\xff',                # ld a,$ff
    b'\x12',                    # ld (de),a
    b'\x1e\x01'                 # ld e,SpecialObject.id
    b'\x1a',                    # ld a,(de)
    b'\x21',SPECOBJ_OAM_DATA,   # ld hl,@data
    b'\xdf',                    # rst_addDoubleIndex
    
    b'\x1e\x1d',                # ld e,Item.oamTileIndexBase
    b'\x2a',                    # ldi a,(hl)
    b'\x12',                    # ld (de),a

    b'\x1d',                    # dec e
    b'\x2a',                    # ldi a,(hl)
    b'\x12',                    # ld (de),a

    b'\x1d',                    # dec e
    b'\x12',                    # ld (de),a
    b'\xc9',                    # ret
    ]

NEW_RING_PALETTE0_ASM = list(ORIG_RING_PALETTE0_ASM)
NEW_RING_PALETTE1_ASM = list(ORIG_RING_PALETTE1_ASM)
NEW_RING_PALETTE2_ASM = list(ORIG_RING_PALETTE2_ASM)
NEW_RING_PALETTE3_ASM = list(ORIG_RING_PALETTE3_ASM)
NEW_RING_PALETTE0_ASM[2:4] = b'\xcd', RING_PALETTE5
NEW_RING_PALETTE1_ASM[2:4] = b'\xcd', RING_PALETTE5
NEW_RING_PALETTE2_ASM[:2]  = b'\xcd', RING_PALETTE5
NEW_RING_PALETTE3_ASM[-3:] = b'\xc3', RING_PALETTE4

AGES_ORIG_RING_PALETTE4_ASM = [
    # this is some unused code we're overwriting
    b'\xaf',            # xor a
    b'\xcd',b'\xcf\x2a',# call setLinkIDOverride
    b'\x06\x02',        # ld b,INTERAC_GREENPOOF
    b'\xc3',b'\xc3\x24',# jp objectCreateInteractionWithSubid00
    ]
SEAS_ORIG_RING_PALETTE4_ASM = list(AGES_ORIG_RING_PALETTE4_ASM)
SEAS_ORIG_RING_PALETTE4_ASM[2] = b'\x16\x2a' # setLinkIDOverride
SEAS_ORIG_RING_PALETTE4_ASM[5] = b'\xaf\x24' # objectCreateInteractionWithSubid00

NEW_RING_PALETTE4_ASM = [
    b'\x1d',                # dec e
    b'\x12',                # ld (de),a
    b'\xf5',                # push af
    b'\xcd',RING_PALETTE5,  # call ringPalette5
    b'\xf1',                # pop af
    b'\xc9',                # ret
    b'\x00',                # nop
    ]

RING_PALETTE5_ASM = [
    b'\xfa',W_PALETTE_THREAD_MODE,  # ld a,(wPaletteThread_mode)
    b'\xf5',                        # push af
    b'\xe5',                        # push hl
    b'\xd5',                        # push de
    b'\xc5',                        # push bc
    b'\x21',LINK_OBJECT_ADDR,       # ld hl,w1Link
    b'\x2e\x1b',                    # ld l,w1Link.oamFlagsBackup
    # get the backup oam flags in e, and the palette portion in d
    b'\x2a',                        # ldi a,(hl)
    b'\x5f',                        # ld e,a
    b'\xe6\x07',                    # and $07
    b'\x57',                        # ld d,a
    b'\xe5',                        # push hl
    b'\x6f',                        # ld l,a
    b'\x26\x00',                    # ld h,$00

    b'\x01',b'\x00',GREEN_COLOR_RING,# ld bc,GREEN_COLOR_RING,$00
    b'\xcd',RING_PALETTE6,           # call ringPalette6

    b'\x01',b'\x01',BLUE_COLOR_RING,# ld bc,BLUE_COLOR_RING,$01
    b'\xcd',RING_PALETTE6,          # call ringPalette6

    b'\x01',b'\x02',RED_COLOR_RING, # ld bc,RED_COLOR_RING,$02
    b'\xcd',RING_PALETTE6,          # call ringPalette6

    b'\x01',b'\x03',GOLD_COLOR_RING,# ld bc,GOLD_COLOR_RING,$03
    b'\xcd',RING_PALETTE6,          # call ringPalette6

    # if no ring was found, reset palette to normal
    b'\x7c',                        # ld a,h
    b'\xb7',                        # or a
    b'\x20\x02',                    # jr nz,@changePalette
    b'\x2e\x00',                    #   ld l,$00

    # @changePalette
    # add the "object palette" flag
    b'\x7d',                        # ld a,l
    b'\xf6\x08',                    # or $08
    b'\x57',                        # ld d,a
    b'\xe1',                        # pop hl

    # if both link's oam flags are equal, replace them both.
    # if they're different(i.e. he's flashing), only replace the backup
    b'\x3a',                        # ldd a,(hl)
    b'\xbb',                        # cp e
    b'\x7a',                        # ld a,d
    b'\x77',                        # ld (hl),a
    b'\x20\x02',                    # jr nz,@done
    b'\x2c',                        # inc l
    b'\x77',                        # ld (hl),a

    # @done
    b'\xc1',                        # pop bc
    b'\xd1',                        # pop de
    b'\xe1',                        # pop hl
    b'\xf1',                        # pop af
    b'\xc9',                        # ret
    ]

RING_PALETTE6_ASM = [
    b'\x78',                # ld a,b
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\xc0',                # ret nz
    b'\x24',                # inc h
    b'\x79',                # ld a,c
    b'\xba',                # cp d
    b'\xc8',                # ret z
    b'\x6f',                # ld l,a
    b'\xc9',                # ret
    ]
