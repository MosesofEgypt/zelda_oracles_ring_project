from .const import *
from ..const import *
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
    b'\xcd',NUDGE_ANGLE_TOWARDS,# call objectNudgeAngleTowards
    b'\xcd',ITEM_DEC_COUNTER1,  # call itemDecCounter1
    b'\x20',RANG_UPDATE_ANIM,   # jr nz,@updateSpeedAndAnimation
    ]

NEW_RANG_TIMER0_ASM    = list(ORIG_RANG_TIMER0_ASM)
NEW_RANG_TIMER0_ASM[3] = RANG_TIMER1  # call rangeTimer1
RANG_TIMER1_ASM = [
    b'\xc5',                          # push bc
    b'\x01',RANG_RING_L1,RANG_RING_L2,# ld bc,RANG_RING_L2,RANG_RING_L1
    b'\xcd',EITHER_RING,              # call eitherRingActive
    b'\xc1',                          # pop bc
    b'\x20\x04',                      # jr nz,@reduceFlightTime
    b'\x30\x02',                      # jr nc,@reduceFlightTime
    b'\x1f',                          # rra
    b'\xc9',                          # ret
    # @reduceFlightTime
    b'\xcd',ITEM_DEC_COUNTER1,        # call itemDecCounter1
    b'\xc9',                          # ret
    ]
