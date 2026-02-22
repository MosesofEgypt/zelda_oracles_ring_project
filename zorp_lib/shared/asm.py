from .const import *
from ..const import *
from ..opcodes import *


ARROW_UP_SPRITE_BLUE_ASM = [
    # @sprite:
    0x01,                   # .db $01
    0x00, 0x00, 0x0e, 0x04, # .db $00 $00 $0e $04
    ]
ARROW_DOWN_SPRITE_RED_ASM       = list(ARROW_UP_SPRITE_BLUE_ASM)
ARROW_DOWN_SPRITE_RED_ASM[-1]   = 0x45


ORIG_CP_ACTIVE_RING0_ASM = [
    PUSH_HL,                # push h1
    LD_HL,  W_ACTIVE_RING,  # ld hl,(wActiveRing)
    CP_HLP,                 # cp (hl)
    POP_HL,                 # pop hl
    RET,                    # ret
    ]
NEW_CP_ACTIVE_RING0_ASM = [
    CP,     0xFF,           # cp $ff
    JP_NZ,  CP_ACTIVE_RING1,# jp nz,cpActiveRing1
    OR_A,                   # or a
    RET,                    # ret
    ]

# these are utility functions being inserted into the padding of bank0
EITHER_RING_ASM = [
    # checks if rings b or c are active
    # stores result for b and c in the z and c flags respectively
    PUSH_DE,                    # push de
    PUSH_AF,                    # push af
    LD_A_B,                     # ld a,b
    CALL,CP_ACTIVE_RING0,       # call cpActiveRing
    PUSH_AF,                    # push af
    LD_A_C,                     # ld a,c
    CALL,CP_ACTIVE_RING0,       # call cpActiveRing

    JR_NZ, "@secondNotFound",   # jr nz,@secondNotFound
        POP_AF,                 #   pop af
        SCF,                    #   scf
        JR, "@cleanup",         #   jr @cleaup

    Label("@secondNotFound"),
    POP_AF,                     # pop af
    SCF,                        # scf
    CCF,                        # ccf

    Label("@cleanup"),
    POP_DE,                     # pop de
    LD_A_D,                     # ld a,d
    POP_DE,                     # pop de
    RET,                        # ret
    ]
NEW_CP_ACTIVE_RING1_BUFFED1_ASM = [
    PUSH_HL,                        # push h1
    PUSH_BC,                        # push bc
    LD_B,       5,                  # ld b,$05
    LD_HL,      W_BOX_CONTENTS,     # ld hl,wRingBoxContents

    Label("@nextRing1"),
    CP_HLP,                         # cp (hl)
    JR_Z, "@doneChecking1",         # jr z,@doneChecking1
        INC_L,                      #   inc l
        DEC_B,                      #   dec b
        JR_NZ,"@nextRing1",         #   jr nz,@nextRing1

    Label("@doneChecking1"),
    CP_HLP,                         # cp (hl)
    JR_Z, "@doneChecking2",         # jr z,@doneChecking2
        LD_B,   5,                  #   ld b,$05
        LD_HL,  W_BOX_CONTENTS_EXT, #   ld hl,wRingBoxContentsExt

    Label("@nextRing2"),
    CP_HLP,                         #   cp (hl)
    JR_Z, "@doneChecking2",         #   jr z,@doneChecking2
        INC_L,                      #     inc l
        DEC_B,                      #     dec b
        JR_NZ,"@nextRing2",         #     jr nz,@nextRing2

    Label("@doneChecking2"),
    PLACEHOLDER0,                   # empty placeholder to insert extra checks at

    # @cleanup:
    CP_HLP,                         # cp (hl)
    POP_BC,                         # pop bc
    POP_HL,                         # pop hl
    RET,                            # ret
    ]
NEW_CP_ACTIVE_RING1_BUFFED0_ASM = list(NEW_CP_ACTIVE_RING1_BUFFED1_ASM)
tmp_idx = NEW_CP_ACTIVE_RING1_BUFFED0_ASM.index(PLACEHOLDER0)
NEW_CP_ACTIVE_RING1_BUFFED0_ASM[tmp_idx: tmp_idx+1] = [
    # check if ring id is in the range 0x09 to 0x0b
    # this ensures the attack/defense multiplier rings aren't always active
    CP,     RED_RING,                   # cp RED_RING
    JR_C,   "@equipNotNeeded",          # jr c,@equipNotNeeded
        CP,     CURSED_RING,            #   cp CURSED_RING
        JR_C,   "@mustBeEquipped",      #   jr c,@mustBeEquipped
            CP,     GOLD_RING,          #       cp GOLD_RING
            JR_NZ,  "@equipNotNeeded",  #       jr nz,@equipNotNeeded

    Label("@mustBeEquipped"),
    LD_HL,  W_ACTIVE_RING,              # ld hl,(wActiveRing)
    Label("@equipNotNeeded"),
    ]
NEW_CP_ACTIVE_RING1_NO_BUFF_ASM = list(NEW_CP_ACTIVE_RING1_BUFFED0_ASM)
# change the check to also include the attack/defense modifiers
NEW_CP_ACTIVE_RING1_NO_BUFF_ASM[tmp_idx+1] = POWER_RING_L1

NEW_CP_ACTIVE_RING1_NO_STACKING_ASM = list(NEW_CP_ACTIVE_RING1_BUFFED1_ASM)
NEW_CP_ACTIVE_RING1_NO_STACKING_ASM[tmp_idx+1] = [
    LD_HL,  W_ACTIVE_RING,      # ld hl,(wActiveRing)
    ]

REMOVE_RING_ASM = [
    PUSH_HL,                        # push h1
    PUSH_BC,                        # push bc
    LD_B_A,                         # ld b,a
    LD_HL,  RINGS_OBTAINED,         # ld hl,wRingsObtained
    CALL,   UNSET_FLAG,             # call unsetFlag
    LD_A_B,                         # ld a,b

    LD_B,       5,                  # ld b,$05
    # remove from primary ring box
    LD_HL,      W_BOX_CONTENTS,     # ld hl,wRingBoxContents

    Label("@nextRing1"),
    CP_HLP,                         # cp (hl)
    JR_NZ,"@dontRemove1",           # jr nz,@dontRemove1
        LD_HLP, 0xFF,               #   ld (hl),$ff

    # else
    Label("@dontRemove1"),
        INC_L,                      #   inc l
        DEC_B,                      #   dec b
        JR_NZ,"@nextRing1",         #   jr nz,@nextRing1

    LD_B,       5,                  # ld b,$05
    # remove from extended ring box
    LD_HL,      W_BOX_CONTENTS_EXT, # ld hl,wRingBoxContentsExt


    Label("@nextRing2"),
    CP_HLP,                         # cp (hl)
    JR_NZ,"@dontRemove2",           # jr nz,@dontRemove2
        LD_HLP, 0xFF,               #   ld (hl),$ff

    # else
    Label("@dontRemove2"),
        INC_L,                      #   inc l
        DEC_B,                      #   dec b
        JR_NZ,"@nextRing2",         #   jr nz,@nextRing2

    # remove from active ring
    LD_HL,      W_ACTIVE_RING,      # ld hl,(wActiveRing)
    CP_HLP,                         # cp (hl)
    JR_NZ,"@done",                  # jr nz,@done
        LD_HLP, 0xFF,               #   ld (hl),$ff

    Label("@done"),
    POP_BC,                         # pop bc
    POP_HL,                         # pop hl
    RET,                            # ret
    ]
FRAC_OF_8_MULTIPLY_ASM = [
    # tuck the full multiplier into c for later
    LD_C_A,                         # ld c,a
    # copy the fractional-multiples into b for decrementing
    AND,        7,                  # and $07
    LD_B_A,                         # ld b,a
    # reset a and add whole-multiples of the damage for each fraction
    LD_A,       0,                  # ld a,$00

    JR_Z, "@addWholeMultiples",     # jr z,@addWholeMultiples
    Label("@addFractionLoop"),
        ADD_E,                      #   add e
        DEC_B,                      #   dec b
        JR_NZ,"@addFractionLoop",   #   jr nz,@addFractionLoop

    # convert the whole multiples into fractions
    SRA_A,                          # sra a
    SRA_A,                          # sra a
    SRA_A,                          # sra a

    Label("@addWholeMultiples"),
    # copy the whole-multiples into b for decrementing
    LD_B_C,                         # ld b,c
    SRA_B,                          # sra b
    SRA_B,                          # sra b
    SRA_B,                          # sra b

    JR_Z, "@done",                  # jr z,@done
    Label("@addWholeLoop"),
        ADD_E,                      #   add e
        DEC_B,                      #   dec b
        JR_NZ,"@addWholeLoop",      #   jr nz,@addWholeLoop

    Label("@done"),
    RET,                            # ret
    ]
CALC_DAMAGE_MODIFIER_ASM = [
    # get the location of the power ring mod table, which should
    # be the 2 bytes past the most recent pointer on the stack
    POP_BC,                         # pop bc   # get a copy
    PUSH_BC,                        # push bc  # put it back
    PUSH_DE,                        # push de
    PUSH_AF,                        # push af
    LD_D_B,                         # ld d,b
    LD_E_C,                         # ld e,c
    INC_DE,                         # inc de
    INC_DE,                         # inc de

    # for each power and armor ring, check if it's equipped and
    # increase or reduce the damage by the associated amount.
    LD_BC,      0,      6,          # ld bc,$06,$00

    Label("@powerArmorLoop"),
        LD_A_B,                     #   ld a,b
        CALL, CP_ACTIVE_RING0,      #   call cpActiveRing
        JR_NZ,"@nextRing",          #   jr nz,@nextRing
            LD_A_DEP,               #   ld a,(de)
            ADD_C,                  #   add c
            LD_C_A,                 #   ld c,a

        Label("@nextRing"),
            INC_DE,                 #   inc de
            DEC_B,                  #   dec b
            JR_NZ,"@powerArmorLoop",#   jr nz,@powerArmorLoop

    LD_B_C,                         # ld b,c
    POP_AF,                         # pop af
    # return the modifier plus the base damage in a
    ADD_B,                          # add b
    POP_DE,                         # pop de
    RET,                            # ret
    ]
ENSURE_DAMAGE_MIN_ASM = [
    BIT7_A,         # bit 7,a
    RET_NZ,         # ret nz
    LD_A,   0xFF,   # ld a,$ff
    RET,            # ret
    ]
