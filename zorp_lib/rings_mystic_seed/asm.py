from .const import *
from ..const import *
from ..shared.const import *


AGES_ORIG_MYSTIC_SEED_RING0_ASM = [
    b'\x2e\x02',                # ld l,Item.subid
    b'\x7e',                    # ld a,(hl)
    b'\xb7',                    # or a
    b'\xcc',ITEM_UPDATE_ANGLE,  # call z,itemUpdateAngle
    b'\x2e\x34',                # ld l,Item.var34
    b'\x36\x03',                # ld (hl),$03
    b'\x2e\x02',                # ld l,Item.subid
    b'\x3a',                    # ldd a,(hl)
    ]
AGES_NEW_MYSTIC_SEED_RING0_ASM = list(AGES_ORIG_MYSTIC_SEED_RING0_ASM)
AGES_NEW_MYSTIC_SEED_RING0_ASM[-2:] = [
    b'\xcd', MYSTIC_SEED_RING1
    ]
AGES_MYSTIC_SEED_RING1_ASM = [
    b'\x3e',MYSTIC_SEED_RING,   # ld a,MYSTIC_SEED_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\x20\x0e',                # jr nz,@done
    # increase bounces to 6
    b'\x36\x06',                # ld (hl),$06
    # increase scent seed damage
    b'\x2e\x01',                # ld l,Item.id
    b'\x7e',                    # ld a,(hl)
    b'\xfe\x21',                # cp ITEM_SCENT_SEED
    b'\x20\x05',                # jr nz,@done
    b'\x2e\x28',                # ld l,Item.damage
    b'\x7e',                    # ld a,(hl)
    b'\x87',                    # add a
    b'\x77',                    # ld (hl),a
    # @done
    b'\x2e\x02',                # ld l,Item.subid
    b'\x3a',                    # ldd a,(hl)
    b'\xc9',                    # ret
    ]

AGES_ORIG_MYSTIC_SEED_RING2_ASM = [
    b'\xfa',W_SEED_SHOOTER_IN_USE,  # ld a,(wIsSeedShooterInUse)
    b'\xb7',                        # or a
    b'\xc2',CLEAR_PARENT_ITEM,      # jp nz,clearParentItem
    b'\x1e\x19',                    # ld e,Item.relatedObj2+1
    b'\x3e\xd0',                    # ld a,>w1Link
    b'\x12',                        # ld (de),a
    b'\x3e\x01',                    # ld a,$01
    ]
AGES_NEW_MYSTIC_SEED_RING2_ASM = list(AGES_ORIG_MYSTIC_SEED_RING2_ASM)
AGES_NEW_MYSTIC_SEED_RING2_ASM[:2] = [
    b'\xcd', MYSTIC_SEED_RING3
    ]

AGES_MYSTIC_SEED_RING3_ASM = [
    b'\x3e',MYSTIC_SEED_RING,       # ld a,MYSTIC_SEED_RING
    b'\xcd',CP_ACTIVE_RING0,        # call cpActiveRing
    b'\xfa',W_SEED_SHOOTER_IN_USE,  # ld a,(wIsSeedShooterInUse)
    # if the ring is on, we can fire 5 seeds at once
    b'\x20\x04',                    # jr nz,@lowerLimit
    b'\xd6\x05',                    # sub,$05
    b'\x18\x02',                    # jr @checkUnderLimit
    # @lowerLimit
    b'\xd6\x01',                    # sub,$01
    # @checkUnderLimit
    b'\x3e\x01',                    # ld a,$01
    b'\x30\x01',                    # jr nc,@done
    b'\x3d',                        # dec a
    # @done
    b'\xc9',                        # ret
    ]

AGES_ORIG_MYSTIC_SEED_RING4_ASM = [
    b'\xcd',ITEM_CREATE_CHILD,      # call itemCreateChildWithID
    b'\x1e\x09',                    # ld e,Item.angle
    b'\x1a',                        # ld a,(de)
    b'\x87',                        # add a
    b'\x87',                        # add a
    b'\x2e\x09',                    # ld l,Item.angle
    b'\x77',                        # ld (hl),a
    ]
AGES_NEW_MYSTIC_SEED_RING4_ASM = list(AGES_ORIG_MYSTIC_SEED_RING4_ASM)
AGES_NEW_MYSTIC_SEED_RING4_ASM[1]  = MYSTIC_SEED_RING5

AGES_MYSTIC_SEED_RING5_ASM = [
    b'\xfa',W_SEED_SHOOTER_IN_USE,  # ld a,(wIsSeedShooterInUse)
    b'\x4f',                        # ld c,a
    b'\x0c',                        # inc c
    b'\x1e\x00',                    # ld e,$00
    b'\xcd',ITEM_CREATE_CHILD,      # call itemCreateChildWithID
    b'\x30\x06',                    # jr nc,@childCreatedSuccessfully
    # NOTE: we're intentionally mucking with the stack here
    #       to make the return jump out of the @state1 code.
    #       the second pop is because the shooter code that
    #       we're skipping does that as well, so we need to.
    b'\xc1',                        # pop bc
    b'\xf1',                        # pop af
    b'\xc2',CLEAR_PARENT_ITEM,      # jp nz,clearParentItem
    b'\xc9',                        # ret
    # @childCreatedSuccessfully
    b'\x2e\x02',                    # ld l,Item.subid
    b'\x34',                        # inc (hl)
    b'\xc9',                        # ret
    ]

SEAS_ORIG_MYSTIC_SEED_RING0_ASM = [
    b'\xd7',                      # rst_addAToHl
    b'\x1e\x09',                  # ld e,Item.angle
    b'\x1a',                      # ld a,(de)
    b'\x86',                      # add (hl)
    b'\xe6\x1f',                  # and $1f
    b'\x12',                      # ld (de),a
    ]
SEAS_NEW_MYSTIC_SEED_RING0_ASM = list(SEAS_ORIG_MYSTIC_SEED_RING0_ASM)
SEAS_NEW_MYSTIC_SEED_RING0_ASM[3:5] = [
    b'\xcd', MYSTIC_SEED_RING1
    ]
SEAS_MYSTIC_SEED_RING1_ASM = [
    b'\xc5',                    # push bc
    b'\xd5',                    # push de
    b'\x4f',                    # ld c,a
    
    b'\x3e',MYSTIC_SEED_RING,   # ld a,MYSTIC_SEED_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\x20\x0c',                # jr nz,@correctSeeds4And5
    # increase scent seed damage
    b'\x1e\x01',                # ld e,Item.id
    b'\x1a',                    # ld a,(de)
    b'\xfe\x21',                # cp ITEM_SCENT_SEED
    b'\x20\x05',                # jr nz,@correctSeeds4And5
    b'\x1e\x28',                # ld e,Item.damage
    b'\x1a',                    # ld a,(de)
    b'\x87',                    # add a
    b'\x12',                    # ld (de),a

    # @correctSeeds4And5
    b'\x1e\x02',                # ld e,Item.subid
    b'\x1a',                    # ld a,(de)
    b'\x46',                    # ld b,(hl)
    b'\xd1',                    # pop de
    b'\xfe\x04',                # cp $04
    b'\x20\x02',                # jr nz,+
    b'\x06\x05',                # ld b,$05
    # +
    b'\xfe\x05',                # cp $05
    b'\x20\x02',                # jr nz,++
    b'\x06\xfb',                # ld b,$fb
    # ++
    # @done
    b'\x79',                    # ld a,c
    b'\x80',                    # add b
    b'\xe6\x1f',                # and $1f
    b'\xc1',                    # pop bc
    b'\xc9',                    # ret
    ]

SEAS_ORIG_MYSTIC_SEED_RING2_ASM = [
    b'\xfa',W_LINK_SWIMMING_STATE,  # ld a,(wLinkSwimmingState)
    b'\x47',                        # ld b,a
    b'\xfa',W_SEED_SHOOTER_IN_USE,  # ld a,(wIsSeedShooterInUse)
    b'\xb0',                        # or b
    b'\xc2',                        # jp nz,???
    ]
SEAS_NEW_MYSTIC_SEED_RING2_ASM = list(SEAS_ORIG_MYSTIC_SEED_RING2_ASM)
SEAS_NEW_MYSTIC_SEED_RING2_ASM[3:5] = [
    b'\xcd', MYSTIC_SEED_RING3
    ]
SEAS_MYSTIC_SEED_RING3_ASM = [
    b'\xf5',                        # push af
    b'\x3e',MYSTIC_SEED_RING,       # ld a,MYSTIC_SEED_RING
    b'\xcd',CP_ACTIVE_RING0,        # call cpActiveRing
    b'\xfa',W_SEED_SHOOTER_IN_USE,  # ld a,(wIsSeedShooterInUse)
    b'\x06\x01',                    # ld b,$01
    # if the ring is on, we can fire 5 seeds at once
    b'\x20\x04',                    # jr nz,@lowerLimit
    b'\xd6\x05',                    # sub,$05
    b'\x18\x02',                    # jr @checkUnderLimit
    # @lowerLimit
    b'\xd6\x01',                    # sub,$01
    # @checkUnderLimit
    b'\x30\x01',                    # jr nc,@done
    b'\x05',                        # dec b
    # @done
    b'\xf1',                        # pop af
    b'\xc9',                        # ret
    ]

SEAS_ORIG_MYSTIC_SEED_RING4_ASM = [
    b'\x0e\x01',                # ld c,$01
    b'\xfa',W_SLINGSHOT_LEVEL,  # ld a,(wSlingshotLevel)
    b'\xfe\x02',                # cp $02
    b'\x20\x02',                # jr nz,+
    b'\x0e\x03',                # ld c,$03
    ]
SEAS_NEW_MYSTIC_SEED_RING4_ASM = list(SEAS_ORIG_MYSTIC_SEED_RING4_ASM)
SEAS_NEW_MYSTIC_SEED_RING4_ASM[-2:] = [
    b'\x00',
    b'\xcd', MYSTIC_SEED_RING5
    ]
SEAS_MYSTIC_SEED_RING5_ASM = [
    b'\xc0',                    # ret nz
    b'\x0e\x03',                # ld c,$03
    b'\x3e',MYSTIC_SEED_RING,   # ld a,MYSTIC_SEED_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\x20\x02',                # jr nz,@checkSlots
    b'\x0e\x05',                # ld c,$05
    # @checkSlots
    b'\xcd',GET_FREE_ITEM_SLOTS,# call getNumFreeItemSlots
    # @checkSlotLoop
    b'\xb9',                    # cp c
    b'\xd0',                    # ret nc
    b'\x0d',                    # dec c
    b'\x0d',                    # dec c
    b'\xe6\x03',                # and $03
    b'\x20\xf8',                # jr nz,@checkSlotLoop
    b'\xc9',                    # ret
    ]

SEAS_ORIG_MYSTIC_SEED_RING6_ASM = [
    b'\x1e\x19',                # ld e,Item.relatedObj2+1
    b'\x3e\xd0',                # ld a,>w1Link
    b'\x12',                    # ld (de),a
    b'\xc5',                    # push bc
    b'\x1e\x01',                # ld e,$01
    b'\xcd',ITEM_CREATE_CHILD,  # call itemCreateChildWithID
    b'\xc1',                    # pop bc
    b'\x0d',                    # dec c
    ]
SEAS_NEW_MYSTIC_SEED_RING6_ASM = list(SEAS_ORIG_MYSTIC_SEED_RING6_ASM)
SEAS_NEW_MYSTIC_SEED_RING6_ASM[4] = b'\x1e\x00'

ORIG_MYSTIC_SEED_RING7_ASM = [
    b'\x2a',            # ldi a,(hl)
    b'\x12',            # ld (de),a
    b'\x1c',            # inc e
    b'\x12',            # ld (de),a
    b'\x1c',            # inc e
    b'\x2a',            # ldi a,(hl)
    b'\x12',            # ld (de),a
    b'\x2a',            # ldi a,(hl)
    b'\x1e\x06',        # ld e,Item.counter1
    b'\x12',            # ld (de),a
    b'\x7e',            # ld a,(hl)
    b'\xc3',PLAY_SOUND, # jp playSound
    ]
NEW_MYSTIC_SEED_RING7_ASM = list(ORIG_MYSTIC_SEED_RING7_ASM)
NEW_MYSTIC_SEED_RING7_ASM[:4] = [
    b'\xc5',                  # push bc
    b'\xcd',MYSTIC_SEED_RING8,# call mysticSeedRing8
    ]
NEW_MYSTIC_SEED_RING7_ASM[-3:] = [
    b'\xc3',MYSTIC_SEED_RING9,# call mysticSeedRing9
    b'\x00',                  # nop
    ]
MYSTIC_SEED_RING8_ASM = [
    b'\x47',    # ld b,a
    b'\x2a',    # ldi a,(hl)
    b'\x12',    # ld (de),a
    b'\x1c',    # inc e
    b'\x12',    # ld (de),a
    b'\xc9',    # ret
    ]

MYSTIC_SEED_RING9_ASM = [
    b'\x4f',                 # ld c,a
    b'\x78',                 # ld a,b
    b'\xfe\x40',             # cp $40
    b'\x20\x02',             # jr nz,@checkScentSeed
    b'\x0e\x1d',             # ld c,$1d
    # @checkScentSeed
    b'\xfe\x4e',             # cp $4e
    b'\x20\x02',             # jr nz,@checkRing
    b'\x0e\xff',             # ld c,$ff
    # @checkRing
    b'\x3e',MYSTIC_SEED_RING,# ld a,MYSTIC_SEED_RING
    b'\xcd',CP_ACTIVE_RING0, # call cpActiveRing
    b'\x20\x02',             # jr nz,@done
    b'\x79',                 # ld a,c
    b'\x12',                 # ld (de),a
    # @done
    b'\xc1',                 # pop bc
    b'\x7e',                 # ld a,(hl)
    b'\xc3',PLAY_SOUND,      # jp playSound
    ]

ORIG_MYSTIC_SEED_RING_ICON_ASM = [
    # pegasus ring sprite data
    b'\xb9\x02\xdc\x07',
    b'\xbd\x07\xdd\x07',
    ]
NEW_MYSTIC_SEED_RING_ICON_ASM  = [
    b'\xbc\x07\xbe\x02',
    b'\xbf\x22\xbf\x02',
    ]
