from .const import *
from ..const import *
from ..shared.const import *

ORIG_TEXT_SNIPS0_ASM = [
    b'\x47',                        # ld b,a
    b'\xe1',                        # pop hl
    b'\x09',                        # add hl,bc
    b'\xfa',W_TEXT_INDEX_L,         # ld a,(wTextIndexL)
    b'\xdf',                        # rst_addDoubleIndex
    b'\xcd',READ_W7_TEXT_TABLE_BYTE,# call readByteFromW7TextTableBank
    b'\x4f',                        # ld c,a
    b'\xcd',READ_W7_TEXT_TABLE_BYTE,# call readByteFromW7TextTableBank
    b'\x47',                        # ld b,a
    b'\xfa',W_ACTIVE_LANGUAGE,      # ld a,(wActiveLanguage)
    ]
NEW_TEXT_SNIPS0_ASM = list(ORIG_TEXT_SNIPS0_ASM)
NEW_TEXT_SNIPS0_ASM[-2:] = [
    b'\xcd', TEXT_SNIPS1
    ]

TEXT_SNIPS1_ASM = [
    b'\xf5',                        # push af
    b'\xfa',W_TEXT_INDEX_H,         # ld a,(wTextIndexH)
    b'\xfe',RING_TEXT_GROUP+4,      # cp RING_TEXT_GROUP
    b'\x20\x11',                    # jr nz,@done
    b'\xfa',W_TEXT_INDEX_L,         #   ld a,(wTextIndexL)
    b'\xd6',RING_TEXT_SNIPS_INDEX,  #   sub RING_TEXT_SNIPS_INDEX+4
    b'\x38\x0a',                    #   jr c,@done
    b'\xe5',                        #     push hl
    b'\x21',TEXT_SNIPS2,            #     ld hl,(textSnips2)
    b'\xdf',                        #     rst_addDoubleIndex
    b'\x2a',                        #     ldi a,(hl)
    b'\x4f',                        #     ld c,a
    b'\x2a',                        #     ldi a,(hl)
    b'\x47',                        #     ld b,a
    b'\xe1',                        #     pop hl

    # @done
    b'\xf1',                        # pop af
    b'\xfa',W_ACTIVE_LANGUAGE,      # ld a,(wActiveLanguage)
    b'\xc9',                        # ret
    ]
