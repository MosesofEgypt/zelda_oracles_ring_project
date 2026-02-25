from .const import *
from ..opcodes import *
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

ORIG_SWIMMING_CHECK0_ASM = [
    b'\x21',W_LINK_SWIMMING_STATE,# ld hl,wLinkSwimmingState
    b'\x2a',                      # ldi a,(hl)
    b'\xb6',                      # or (hl)
    b'\x20',ITEM_DELETE_PARENT,   # jr nz,@deleteParent
    ]
NEW_SWIMMING_CHECK0_ASM = (
    b'\xcd',LINK_DIVING_CHECK,    # call linkDivingCheck
    b'\x00'*2,                    # nop
    b'\x20',ITEM_DELETE_PARENT,   # jr nz,@deleteParent
    )

ORIG_SWIMMING_CHECK1_ASM = [
    b'\xfa',W_LINK_SWIMMING_STATE,# ld a,(wLinkSwimmingState)
    b'\xb7',                      # or a
    b'\x28',PARENT_ITEM_CHECK_AB, # jr z,@checkAB
    b'\x18',UPDATE_PARENT_ITEMS,  # jr @updateParentItems
    ]
NEW_SWIMMING_CHECK1_ASM = (
    b'\xcd',LINK_DIVING_CHECK,    # call linkDivingCheck
    b'\x00',                      # nop
    b'\x28',PARENT_ITEM_CHECK_AB, # jr z,@checkAB
    b'\x18',UPDATE_PARENT_ITEMS,  # jr @updateParentItems
    )

LINK_DIVING_CHECK_ASM = [
    LD_A_A16,   W_LINK_SWIMMING_STATE,  # ld a,(wLinkSwimmingState)
    OR_A,                               # or a
    RET_Z,                              # ret z
    PUSH_BC,                            # push bc
    LD_B,       0,                      # ld b,0
    LD_A,       SWIMMERS_RING,          # ld a,SWIMMERS_RING
    CALL,       CP_ACTIVE_RING0,        # call cpActiveRing
    JR_NZ,      "+",                    # jr nz,+
        INC_B,                          #   inc b

    Label("+"),
    LD_A,       ZORA_RING,              # ld a,ZORA_RING
    CALL,       CP_ACTIVE_RING0,        # call cpActiveRing
    JR_NZ,      "++",                   # jr nz,++
        INC_B,                          #   inc b

    Label("++"),
    LD_A,       ROCS_RING,              # ld a,ROCS_RING
    CALL,       CP_ACTIVE_RING0,        # call cpActiveRing
    JR_NZ,      "+++",                  # jr nz,+++
        INC_B,                          #   inc b

    Label("+++"),
    LD_A,       0x4A,                   # ld a,TREASURE_MERMAID_SUIT
    CALL,       CHECK_HAVE_TREASURE,    # call checkTreasureObtained
    JR_NC,      "++++",                 # jr nc,++++
        INC_B,                          #   inc b

    Label("++++"),
    LD_A_B,                             # ld a,b
    POP_BC,                             # pop bc
    CP,         2,                      # cp 2
    JR_NC,      "@isADolphin",          # jr nc,@isADolphin

    RET,                                # ret
    Label("@isADolphin"),
    XOR_A,                              # xor a
    RET,                                # ret
    ]

ORIG_UNDERWATER_ITEM_B0_ASM = [
    BIT6_A,                         # bit TILESETFLAG_BIT_UNDERWATER,a
    JR_Z,   "@normal",              # jr z,@normal

    # @underwater:
    LD_DE,  W_INVENTORY_A_L,  BTN_A,# ldde BTN_A, <wInventoryA
    CALL,   CHECK_ITEM_USED,        # call checkItemUsed
    JR,     0x21,                   # jr @updateParentItems
    Label("@normal"),
    ]

NEW_UNDERWATER_ITEM_B0_ASM = list(ORIG_UNDERWATER_ITEM_B0_ASM)
NEW_UNDERWATER_ITEM_B0_ASM[:3] = [
    CALL,   UNDERWATER_ITEM_B1, # call underwaterItemB1
    RET_Z,                      # ret z
    ]

UNDERWATER_ITEM_B1_ASM = [
    BIT6_A,                             # bit TILESETFLAG_BIT_UNDERWATER,a
    JR_Z,   "@doNormal",                # jr z,@doNormal
        PUSH_BC,                        #   push bc
        LD_BC,  SWIMMERS_RING,ZORA_RING,#   ld bc,SWIMMERS_RING,ZORA_RING
        CALL,   EITHER_RING,            #   call eitherRingActive
        POP_BC,                         #   pop bc
        RET_NZ,                         #   ret nz
        JR_C,   "@doNormal",            #   jr c,@doNormal
        OR,     1,                      #   or a,1
        RET,                            #   ret
    Label("@doNormal"),
    # NOTE: it just so happens that this is the code we need to jump to
    CALL,   SWIMMING_CHECK1,            # call swimmingCheck1
    XOR_A,                              # xor a
    RET,                                # ret
    ]
