from .const import *
from ..const import *
from ..shared.const import *

ORIG_VICTORY_RING0_ASM = [
    b'\x2a',                # ldi a,(hl)
    b'\x5e',                # ld e,(hl)
    b'\xb7',                # or a
    b'\x28\x04',            # jr z,+
    b'\x6f',                # ld l,a
    b'\x26\xc6',            # ld h,>wc600Block
    b'\x56',                # ld d,(hl)
    ]
ORIG_VICTORY_RING2_ASM = [
    b'\xfa',W_SHIELD_LEVEL, # ld a,(wShieldLevel)
    b'\xc6\x00',            # add $00
    b'\xea',W_USING_SHIELD, # ld (wUsingShield),a
    b'\xc9',                # ret
    ]
ORIG_VICTORY_RING4_ASM = [
    b'\xfa',W_SWORD_LEVEL,        # ld a,(wSwordLevel)
    b'\x21',SWORD_LEVEL_DATA_MIN2,# ld hl,swordLevelData-2
    b'\xdf',                      # rst_addDoubleIndex
    ]
ORIG_VICTORY_RING6_ASM = [
    b'\x4f',                # ld c,a
    b'\xfa',W_SWORD_LEVEL,  # ld a,(wSwordLevel)
    b'\xfe\x01',            # cp $01
    b'\x28\x02',            # jr z,tryBreakTileWithSword
    b'\x3e\x02',            # ld a,BREAKABLETILESOURCE_SWORD_L2
    ]
ORIG_VICTORY_RING7_ASM = [
    b'\xcb\x6f',            # bit 5,a
    b'\xc8',                # ret z
    b'\xcb\xae',            # res 5,(hl)
    b'\xfa',W_SWORD_LEVEL,  # ld a,(wSwordLevel)
    b'\xfe\x02',            # cp $02
    ]
NEW_VICTORY_RING0_ASM = list(ORIG_VICTORY_RING0_ASM)
NEW_VICTORY_RING2_ASM = list(ORIG_VICTORY_RING2_ASM)
NEW_VICTORY_RING4_ASM = list(ORIG_VICTORY_RING4_ASM)
NEW_VICTORY_RING6_ASM = list(ORIG_VICTORY_RING6_ASM)
NEW_VICTORY_RING7_ASM = list(ORIG_VICTORY_RING7_ASM)
NEW_VICTORY_RING0_ASM[-2:] = b'\xcd', VICTORY_RING1
NEW_VICTORY_RING2_ASM[:2]  = b'\xcd', VICTORY_RING3
NEW_VICTORY_RING4_ASM[:2]  = b'\xcd', VICTORY_RING5
NEW_VICTORY_RING6_ASM[1:3] = b'\xcd', VICTORY_RING5
NEW_VICTORY_RING7_ASM[3:5] = b'\xcd', VICTORY_RING8

VICTORY_RING1_ASM = [
    b'\x7a',                # ld a,d
    b'\x26\xc6',            # ld h,>wc600Block
    b'\x56',                # ld d,(hl)
    b'\xfe\x01',            # cp TREASURE_SHIELD
    b'\x28\x05',            # jr z,@checkRing
    b'\xfe\x05',            # cp TREASURE_SWORD
    b'\x28\x01',            # jr z,@checkRing
    b'\xc9',                # ret

    # @checkRing
    b'\x3e',VICTORY_RING,   # ld a,VICTORY_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x20\x06',            # jr nz,@done
    # increment sword and shield by 1 level
    b'\x7a',                # ld a,d
    b'\xfe\x03',            # cp $03
    b'\x30\x01',            # jr nc,@done
    b'\x14',                # inc d

    # @done
    b'\xc9',                # ret
    ]

VICTORY_RING3_ASM = [
    b'\xd5',                # push de
    b'\xfa',W_SHIELD_LEVEL, # ld a,(wShieldLevel)
    b'\x57',                # ld d,a
    b'\x3e',VICTORY_RING,   # ld a,VICTORY_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x7a',                # ld a,d
    b'\xd1',                # pop de
    b'\x20\x05',            # jr nz,@done
    # increment sword/shield by 1 level
    b'\xfe\x03',            #   cp $03
    b'\x30\x01',            #   jr nc,@done
    b'\x3c',                #   inc a

    # @done
    b'\xc9',                # ret
    ]

VICTORY_RING5_ASM = list(VICTORY_RING3_ASM)
VICTORY_RING5_ASM[2] = W_SWORD_LEVEL
# NOTE: it'd be nice to have 4, 6, and 7 call 5, but 7 is in a different
#       bank so it needs its own copy of the function in there
VICTORY_RING8_ASM = list(VICTORY_RING5_ASM)


ORIG_VICTORY_RING_ICON_ASM = [
    b'\xba\x07\xdc\x06',
    b'\xbb\x06\xdd\x06',
    ]
NEW_VICTORY_RING_ICON_ASM = [
    b'\xc6\x05\xc0\x25',
    b'\xc7\x05\xc1\x22',
    ]
