from .const import *
from ..const import *
from ..shared.const import *

ORIG_SWIM_CHECK_ASM = [
    b'\x0e\x98',              # ld c,$98
    b'\xcd',UPDATE_LINK_SPEED,# call @updateLinkSpeed_withParam
    b'\xfa',W_ACTIVE_RING,    # ld a,(wActiveRing)
    b'\xfe',SWIMMERS_RING,    # cp SWIMMERS_RING
    b'\x20\x05',              # jr nz,+
    ]
NEW_SWIM_CHECK_ASM = [
    b'\x0e\x98',              # ld c,$98
    b'\xcd',UPDATE_LINK_SPEED,# call @updateLinkSpeed_withParam
    b'\x3e',SWIMMERS_RING,    # ld a,SWIMMERS_RING
    b'\xcd',CP_ACTIVE_RING0,  # call cpActiveRing
    b'\x20\x05',              # jr nz,+
    ]

ORIG_FEATHER_CHECK0_ASM = [
    b'\x21',W_LINK_SWIMMING_STATE,# ld hl,wLinkSwimmingState
    b'\x2a',                      # ldi a,(hl)
    b'\xb6',                      # or (hl)
    b'\x20',FEATHER_DELETE_PARENT,# jr nz,@deleteParent
    ]
NEW_FEATHER_CHECK0_ASM = (
    b'\xcd',LINK_DIVING_CHECK,    # call linkDivingCheck
    b'\x00'*2,                    # nop
    b'\x20',FEATHER_DELETE_PARENT,# jr nz,@deleteParent
    )

ORIG_FEATHER_CHECK1_ASM = [
    b'\xfa',W_LINK_SWIMMING_STATE,# ld a,(wLinkSwimmingState)
    b'\xb7',                      # or a
    b'\x28',PARENT_ITEM_CHECK_AB, # jr z,@checkAB
    b'\x18',UPDATE_PARENT_ITEMS,  # jr @updateParentItems
    ]
NEW_FEATHER_CHECK1_ASM = (
    b'\xcd',LINK_DIVING_CHECK,    # call linkDivingCheck
    b'\x00',                      # nop
    b'\x28',PARENT_ITEM_CHECK_AB, # jr z,@checkAB
    b'\x18',UPDATE_PARENT_ITEMS,  # jr @updateParentItems
    )

LINK_DIVING_CHECK_ASM = [
    b'\xfa',W_LINK_SWIMMING_STATE,  # ld a,(wLinkSwimmingState)
    b'\xfe\x00',                    # cp $00
    b'\xc8',                        # ret z
    b'\xc5',                        # push bc
    b'\x01',SWIMMERS_RING,ZORA_RING,# ld bc,SWIMMERS_RING,ZORA_RING
    b'\xcd',EITHER_RING,            # call eitherRingActive
    b'\xc1',                        # pop bc
    b'\x20\x02',                    # jr nz,@maybeADolphin
    b'\x38\x0a',                    # jr c,@isADolphin
    # @maybeADolphin
    b'\x3e',ROCS_RING,              # ld a,ROCS_RING
    b'\xcd',CP_ACTIVE_RING0,        # call cpActiveRing
    b'\xfa',W_LINK_SWIMMING_STATE,  # ld a,(wLinkSwimmingState)
    b'\x20\x05',                    # jr nz,@notADolphin
    # @isADolphin
    b'\xe6\x80',                    # and $80
    b'\x2f',                        # cpl
    b'\xe6\x80',                    # and $80
    # @notADolphin
    b'\xb7',                        # or a
    b'\xc9',                        # ret
    ]
