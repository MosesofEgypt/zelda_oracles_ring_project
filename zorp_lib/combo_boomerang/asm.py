from .const import *
from ..const import *
from ..opcodes import *
from ..shared.const import *


ORIG_RANG_CHECK0_ASM = [
    b'\x0e\xff',            # ld c,-1
    b'\x3e',RANG_RING_L1,   # ld a,RANG_RING_L1
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x28\x09',            # jr z,+
    b'\x3e',RANG_RING_L2,   # ld a,RANG_RING_L2
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x20\x07',            # jr nz,++
    b'\x0e\xfe',            # ld c,-2
    # +
    ]
NEW_RANG_CHECK0_ASM = [
    b'\xcd',RANG_CHECK1,    # call rangCheck1
    b'\xcd',EITHER_RING,    # call eitherRingActive
    b'\x0e\xff',            # ld c,-1
    b'\x20\x05',            # jr nz,@rangLevel0Or1
    b'\x0d',                # dec c
    b'\x20\x02',            # jr nz,@rangLevel2
    b'\x0e\xfc',            # ld c,-4
    b'\x30\x06',            # jr nc,++
    b'\x00',                # nop
    ]
RANG_CHECK1_ASM = [
    b'\x3e',TOSS_RING,                # ld a,TOSS_RING
    b'\xcd',CP_ACTIVE_RING0,          # call cpActiveRing
    b'\x01',RANG_RING_L1,RANG_RING_L2,# ld bc,RANG_RING_L2,RANG_RING_L1
    b'\x28\x06',                      # jr z,@checkRings
    b'\x3e',HASTE_RING,               # ld a,HASTE_RING
    b'\xcd',CP_ACTIVE_RING0,          # call cpActiveRing
    b'\xc0',                          # ret nz
    # @checkRings
    b'\xcd',EITHER_RING,              # call eitherRingActive
    b'\x28\x04',                      # jr z,@speedIncrease
    b'\x38\x02',                      # jr c,@speedIncrease
    b'\x18\x08',                      # jr @done
    # @speedIncrease
    b'\x2e\x10',                      # ld l,Item.speed
    b'\x36\x78',                      # ld (hl),SPEED_300
    b'\x2e\x06',                      # ld l,Item.counter1
    b'\x36\x78',                      # ld (hl),$78
    # @done
    b'\x01',RANG_RING_L1,RANG_RING_L2,# ld bc,RANG_RING_L2,RANG_RING_L1
    b'\xc9',                          # ret
    ]


ORIG_RANG_TIMER0_ASM = [
    CALL,   NUDGE_ANGLE_TOWARDS,# call objectNudgeAngleTowards
    CALL,   ITEM_DEC_COUNTER1,  # call itemDecCounter1
    JR_NZ,  RANG_UPDATE_ANIM,   # jr nz,@updateSpeedAndAnimation
    ]
NEW_RANG_TIMER0_ASM    = list(ORIG_RANG_TIMER0_ASM)
NEW_RANG_TIMER0_ASM[3] = RANG_TIMER2  # call rangeTimer1

ORIG_RANG_TIMER1_ASM = [
    CALL,   OBJ_CLINK_INTERAC,  # call objectCreateClinkInteraction
    LD_H_D,                     # ld h,d
    LD_L,       9,              # ld l,Item.angle
    LD_A_HLP,                   # ld a,(hl)
    XOR,    0x10,               # xor $10
    LD_HLP_A,                   # ld (hl),a
    ]
NEW_RANG_TIMER1_ASM = [
    LD_E,   7,                  # ld e,Item.counter2
    LD_A_DEP,                   # ld a,(de)
    OR_A,                       # or a
    JR_Z,   "+",                # jr z,+
    DEC_A,                      #   dec a
    Label("+"),
    CALL,   RANG_TIMER3,        # call rangTimer3
    ]

RANG_TIMER2_ASM = [
    PUSH_BC,                          # push bc
    LD_BC,  RANG_RING_L1,RANG_RING_L2,# ld bc,RANG_RING_L2,RANG_RING_L1
    CALL,   EITHER_RING,              # call eitherRingActive
    POP_BC,                           # pop bc
    JR_NZ,  "@reduceFlightTime",      # jr nz,@reduceFlightTime
    JR_NC,  "@reduceFlightTime",      # jr nc,@reduceFlightTime
    RRA,                              # rra
    RET,                              # ret
    Label("@reduceFlightTime"),
    CALL,   ITEM_DEC_COUNTER1,        # call itemDecCounter1
    RET,                              # ret
    ]
RANG_TIMER3_ASM = [
    LD_DEP_A,                         # ld (de),a

    # if the parent was deleted, return
    PUSH_HL,                          # push hl
    LD_H_D,                           # ld h,d
    LD_L,   0x16,                     # ld l,Item.relatedObj1
    LDI_A_HLP,                        # ldi a,(hl)
    LD_H_HLP,                         # ld h,(hl)
    LD_L_A,                           # ld l,a
    LD_A_HLP,                         # ld a,(hl)
    CP,     0,                        # cp $00
    POP_HL,                           # pop hl
    RET_Z,                            # ret z

    # if boomerang has already changed angle, wait a couple
    # frames before it's allowed to try changing again
    LD_A_DEP,                         # ld a,(de)
    OR_A,                             # or a
    JR_NZ,  "@skipRebound",           # jr nz,@skipRebound

    # setup a timer so the clink doesn't happen too often
    LD_A,   5,                        # ld a,5
    LD_DEP_A,                         # ld (de),a

    CALL,   OBJ_CLINK_INTERAC,        # call objectCreateClinkInteraction
    LD_H_D,                           # ld h,d
    LD_L,   9,                        # ld l,Item.angle
    LD_A_HLP,                         # ld a,(hl)
    XOR,    0x10,                     # xor $10
    LD_HLP_A,                         # ld (hl),a

    Label("@skipRebound"),
    # if this isn't the magic boomerang, return when wall is struck
    LD_E,   2,                        # ld e,Item.subid
    LD_A_DEP,                         # ld a,(de)
    OR_A,                             # or a
    RET_Z,                            # ret z

    # this is the magic boomerang, so if both rang rings are equipped
    # then it can continue flying as long as the button is held, even
    # after hitting a solid tile.
    PUSH_BC,                          # push bc
    LD_BC,  RANG_RING_L1,RANG_RING_L2,# ld bc,RANG_RING_L2,RANG_RING_L1
    CALL,   EITHER_RING,              # call eitherRingActive
    POP_BC,                           # pop bc
    RET_NZ,                           # ret nz
    RET_NC,                           # ret nc

    # intentional stack manipulation
    POP_AF,                           # pop af
    JP, RANG_UPDATE_SPEED_ANIM,       # jp @updateSpeedAndAnimation
    ]
