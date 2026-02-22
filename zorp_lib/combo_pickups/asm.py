from .const import *
from ..const import *
from ..shared.const import *

ORIG_HEART_CHECK_ASM = [
    b'\x5f',              # ld e,a
    b'\xfa',W_ACTIVE_RING,# ld a,wActiveRing
    b'\x01\x08\x02',      # ld bc $02,$08
    b'\xfe',HEART_RING_L1,# cp HEART_RING_L1
    b'\x28\x07',          # jr z,@heartRingEquipped
    b'\xfe',HEART_RING_L2,# cp HEART_RING_L2
    b'\x20\x2b',          # jr nz,@clearCounter
    b'\x01\x10\x03',      # ld bc $03,$10
    # @heartRingEquipped
    b'\x7b',              # ld a,e
    ]
NEW_HEART_CHECK_ASM = [
    b'\x5f',                            # ld e,a
    b'\x01',HEART_RING_L1,HEART_RING_L2,# ld bc,HEART_RING_L2,HEART_RING_L1
    b'\xcd',EITHER_RING,                # call eitherRingActive
    b'\x01\x10\x03',                    # ld bc $03,$10
    b'\x28\x06',                        # jr z,@heartRingEquipped
    b'\x01\x08\x02',                    # ld bc $02,$08
    b'\x30\x29',                        # jr nc,@clearCounter
    b'\x00',                            # nop
    # @heartRingEquipped
    b'\x7b',                            # ld a,e
    ]
NEW_HEART_CHECK_STACKED_ASM = [
    b'\x01',HEART_RING_L1,HEART_RING_L2,# ld bc,HEART_RING_L2,HEART_RING_L1
    b'\xcd',EITHER_RING,                # call eitherRingActive
    b'\x01\x10\x02',                    # ld bc $02,$10
    b'\x28\x04',                        # jr z,@heartLevel2Or3
    b'\x0e\x08',                        # ld c $08
    b'\x30\x2b',                        # jr nc,@clearCounter
    # @heartLevel2Or3
    b'\x38\x01',                        # jr c,@heartRingEquipped
    b'\x04',                            # inc b
    # @heartRingEquipped
    b'\x00',                            # nop
    ]
NEW_HEART_CHECK_SUPER0_ASM = [
    b'\x01',HEART_RING_L1,HEART_RING_L2,# ld bc,HEART_RING_L2,HEART_RING_L1
    b'\xcd',EITHER_RING,                # call eitherRingActive
    b'\x01\x10\x02',                    # ld bc $02,$10
    b'\x28\x04',                        # jr z,@heartLevel2Or3
    b'\x0e\x08',                        # ld c $08
    b'\x30\x2b',                        # jr nc,@clearCounter
    # @heartLevel2Or3
    b'\xcd',HEART_CHECK_SUPER1,         # call heartCheckSuper1
    b'\x00',                            # nop
    ]
HEART_CHECK_SUPER1_ASM = [
    b'\x38\x01',                        # jr c,@heartLevel3
    b'\x04',                            #   inc b
    # @heartLevel3
    b'\xf5',                            # push af
    b'\x3e',BLUE_JOY_RING,              # ld a,BLUE_JOY_RING
    b'\xcd',CP_ACTIVE_RING0,            # call cpActiveRing
    b'\x20\x02',                        # jr nz,@checkGoldJoy
    b'\xcb\x21',                        #   sla c
    b'\xf1',                            # pop af
    b'\xf5',                            # push af
    b'\x3e',GOLD_JOY_RING,              # ld a,GOLD_JOY_RING
    b'\xcd',CP_ACTIVE_RING0,            # call cpActiveRing
    b'\x20\x02',                        # jr nz,@done
    b'\xcb\x21',                        #   sla c
    # @done
    b'\xf1',                            # pop af
    b'\xc9',                            # ret
    ]


ORIG_JOY_RING0_ASM  = [
    b'\x79',                # ld a,c
    b'\xcd',GET_RUPEE_VALUE,# call getRupeeValue
    b'\x7b',                # ld a,e
    b'\xfe',W_NUM_RUPEES_B0,# cp <wNumRupees
    ]
ORIG_JOY_RING2_ASM  = [
    b'\x62',                 # ld h,d
    b'\x6b',                 # ld l,e
    b'\x3e',W_LINK_HEALTH_B0,# ld a,<wLinkHealth
    b'\xbb',                 # cp e
    ]
NEW_JOY_RING0_ASM       = list(ORIG_JOY_RING0_ASM)
NEW_JOY_RING2_ASM       = list(ORIG_JOY_RING2_ASM)
NEW_JOY_RING0_ASM[2]    = JOY_RING1
NEW_JOY_RING2_ASM[2:]  = b'\xcd', JOY_RING3

JOY_RING1_ASM   = [
    b'\xcd',GET_RUPEE_VALUE,# call getRupeeValue
    b'\x3e',GOLD_JOY_RING,  # ld a,GOLD_JOY_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\xc0',                # ret nz
    b'\x7b',                # ld a,e
    b'\xfe',W_NUM_RUPEES_B0,# cp <wNumRupees
    b'\x3e',RED_JOY_RING,   # ld a,RED_JOY_RING
    b'\x28\x02',            # jr z,@notOreChunks
    b'\x3e',GREEN_JOY_RING, # ld a,GREEN_JOY_RING
    # @notOreChunks
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\xc0',                # ret nz
    # double the item value
    b'\x60',                # ld h,b
    b'\x69',                # ld l,c
    b'\x09',                # add bc
    b'\x44',                # ld b,h
    b'\x4d',                # ld c,l
    b'\xc9',                # ret
    ]
JOY_RING3_ASM = [
    b'\x3e',W_LINK_HEALTH_B0,# ld a,<wLinkHealth
    b'\xbb',                 # cp e
    b'\xc0',                 # ret nz
    b'\x3e',GOLD_JOY_RING,   # ld a,GOLD_JOY_RING
    b'\xcd',CP_ACTIVE_RING0, # call cpActiveRing
    b'\x20\x05',             # jr nz,@done
    b'\x3e',BLUE_JOY_RING,   # ld a,BLUE_JOY_RING
    b'\xcd',CP_ACTIVE_RING0, # call cpActiveRing
    b'\x20\x03',             # jr nz,@done
    b'\x79',                 # ld a,c
    b'\x87',                 # add a
    b'\x4f',                 # ld c,a
    # @done
    b'\xaf',                 # xor a
    b'\xc9',                 # ret
    ]
