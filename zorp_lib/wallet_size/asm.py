from .const import *
from ..const import *
from ..shared.const import *

ORIG_WALLET_SIZE0_ASM = [
    b'\x2a',                 # ldi a,(hl)
    b'\x66',                 # ld h,(hl)
    b'\x6f',                 # ld l,a
    b'\x01',b'\x99',b'\x09', # ld bc,$0999
    b'\xcd',COMPARE_HL_TO_BC,# call compareHlToBc
    b'\x3d',                 # dec a
    b'\xc0',                 # ret nz
    ]
NEW_WALLET_SIZE0_ASM = [
    b'\x01',b'\x99',b'\x99', # ld bc,$9999
    b'\xd0',                 # ret nc
    b'\x00'*7,
    ]

ORIG_WALLET_SIZE1_ASM = [
    b'\x0e\x10',                # ld c,$10
    b'\xfa',W_DISP_RUPEES,      # ld a,(wDisplayedRupees)
    b'\x47',                    # ld b,a
    b'\xe6\x0f',                # and $0f
    b'\x81',                    # add c
    b'\x32',                    # ldd (hl),a
    b'\x78',                    # ld a,b
    b'\xcb\x37',                # swap a
    b'\xe6\x0f',                # and $0f
    b'\x81',                    # add c
    b'\x32',                    # ldd (hl),a
    b'\xfa',W_DISP_RUPEES_PLUS, # ld a,(wDisplayedRupees+1)
    b'\xe6\x0f',                # and $0f
    b'\x81',                    # add c
    b'\x32',                    # ldd (hl),a
    ]
# NOTE: this doesn't really work since it cuts off the right
#       side of the A button's bracket. it's also taking on the
#       horizontally-mirrored flag of the bracket, so for it to
#       work we'd need to remove the right side of the bracket
#       for the B button, and shift the A button left by 1 tile
NEW_WALLET_SIZE1_ASM = [
    b'\x11',W_DISP_RUPEES,          # ld de,wDisplayedRupees
    b'\x00',                        # nop
    # @loopOuter
    b'\x1a',                        #   ld a,(de)
    b'\x0e\x02',                    #   ld c,$02
    # @loopInner
    b'\xe6\x0f',                    #     and $0f
    b'\xc6\x10',                    #     add $10
    b'\x32',                        #     ldd (hl),a
    b'\x1a',                        #     ld a,(de)
    b'\xcb\x37',                    #     swap a
    b'\x0d',                        #     dec c
    b'\x20\xf5',                    #     jr nz,@loopInner
    b'\x13',                        #   inc de
    b'\x3e',W_DISP_RUPEES_PLUS_B0,  #   ld a,W_DISP_RUPEES_PLUS_B0
    b'\xbb',                        #   cp e
    b'\x30\xeb',                    #   jr nc,@loopOuter
    ]
NEW_WALLET_SIZE1_ASM = [
    # write an X into the tens place(which may be overwritten below)
    b'\x36\x1b',                # ld (hl),$1b
    b'\x2b',                    # dec hl
    # only display the thousands and hundreds
    # digits if the rupee count is over 999
    b'\x11',W_DISP_RUPEES_PLUS, # ld de,wDisplayedRupees+1
    b'\x1a',                    # ld a,(de)
    b'\xfe\x10',                # cp $10
    b'\x30\x02',                # jr nc,@drawUpperTwoDigits
    # revert pointers back so we can overwrite the X
    b'\x23',                    # inc hl
    b'\x1b',                    # dec de
    # @drawUpperTwoDigits
    b'\xbf',                    # xor a
    b'\xcd',DRAW_DIGIT,         # call drawDigit
    b'\xcd',DRAW_DIGIT,         # call drawDigit

    b'\xbf',                    # xor a
    b'\xcd',DRAW_DIGIT,         # call drawDigit
    ]
DRAW_DIGIT_ASM = [
    b'\xf5',                        # push af
    b'\x3e',W_DISP_RUPEES_PLUS_B0,  # ld a,<wDisplayedRupees+1
    b'\xbb',                        # cp e
    b'\x30\x02',                    # jr nc,@start
    b'\xf1',                        # pop af
    b'\xc9',                        # ret
    # @start
    b'\xf1',                        # pop af
    b'\x1a',                        # ld a,(de)
    b'\x28\x03',                    # jr z,@draw
    b'\xcb\x37',                    # swap a
    b'\x13',                        # inc de
    # @draw
    b'\xe6\x0f',                    # and $0f
    b'\xc6\x10',                    # add $10
    b'\x32',                        # ldd (hl),a
    b'\xb7',                        # or a
    b'\xc9',                        # ret
    ]
