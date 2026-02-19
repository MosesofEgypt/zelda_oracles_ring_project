from .const import *
from ..const import *
from ..shared.const import *


ORIG_ALCHEMY_RING_ICON_ASM = [
    # gold luck ring sprite data
    b'\xc4\x05\xbe\x02',
    b'\xc5\x05\xbf\x02',
    ]
NEW_ALCHEMY_RING_ICON_ASM  = [
    b'\xcb\x05\xb2\x26',
    b'\xa1\x02\xbf\x02',
    ]

ORIG_ALCHEMY_RING0_ASM = [
    b'\x0e\x9a',# .db ENEMY_BLADE_TRAP          $80|GREEN_LUCK_RING
    b'\x18\x20',# .db PART_OCTOROK_PROJECTILE   $00|RED_HOLY_RING
    b'\x19\x1f',# .db PART_ZORA_FIRE            $00|BLUE_HOLY_RING
    b'\x29\x9b',# .db PART_BEAM                 $80|BLUE_LUCK_RING
    b'\x00',    # .db $00
    ]
NEW_ALCHEMY_RING0_ASM = list(ORIG_ALCHEMY_RING0_ASM)
NEW_ALCHEMY_RING0_ASM[2] = b'\x00\x00'

ORIG_ALCHEMY_RING1_ASM = [
    b'\xaf',                        # xor a
    b'\xea',W_LINK_IN_AIR,          # ld (wLinkInAir),a
    b'\xea',W_LINK_SWIMMING_STATE,  # ld (wLinkSwimmingState),a
    b'\x3e',GOLD_LUCK_RING,         # ld a,GOLD_LUCK_RING
    b'\xcd',CP_ACTIVE_RING0,        # call cpActiveRing
    b'\x3e\xfc',                    # ld a,$fc
    b'\x20\x02',                    # jr nz,+
    b'\xcb\x2f',                    # sra a
    # +
    ]
NEW_ALCHEMY_RING1_ASM = list(ORIG_ALCHEMY_RING1_ASM)
NEW_ALCHEMY_RING1_ASM[6] = BLUE_LUCK_RING

ORIG_ALCHEMY_RING2_ASM = [
    b'\xfa',W_LINK_SWIMMING_STATE,  # ld a,(wLinkSwimmingState)
    b'\xb7',                        # or a
    b'\xc2',CLEAR_PARENT_ITEM,      # jp nz,clearParentItem
    b'\xfa',W_NUM_BOMBCHUS,         # ld a,(wNumBombchus)
    b'\xb7',                        # or a
    ]
ORIG_ALCHEMY_RING3_ASM = [
    b'\xcd',TRY_PICKUP_BOMBS,       # call tryPickupBombs
    b'\xc2',BEGIN_PICKUP_SET_ANIM,  # jp nz,beginPickupAndSetAnimation
    b'\xfa',W_NUM_BOMBS,            # ld a,(wNumBombs)
    b'\xb7',                        # or a
    ]
ORIG_ALCHEMY_RING4_ASM = [
    b'\x21',W_NUM_EMBER_SEEDS,  # ld hl,wNumEmberSeeds
    b'\xd7',                    # rst_addAToHl
    b'\x7e',                    # ld a,(hl)
    b'\xb7',                    # or a
    b'\xc0',                    # ret nz
    b'\xe1',                    # pop hl
    b'\xc3',CLEAR_PARENT_ITEM,  # jp clearParentItem
    ]

NEW_ALCHEMY_RING2_ASM = list(ORIG_ALCHEMY_RING2_ASM)
NEW_ALCHEMY_RING3_ASM = list(ORIG_ALCHEMY_RING3_ASM)
NEW_ALCHEMY_RING4_ASM = list(ORIG_ALCHEMY_RING4_ASM)
NEW_ALCHEMY_RING2_ASM[-3:-1] = [ b'\xcd', ALCHEMY_RING5 ]
NEW_ALCHEMY_RING3_ASM[-3:-1] = [ b'\xcd', ALCHEMY_RING6 ]
NEW_ALCHEMY_RING4_ASM[-5:-2] = [ b'\xc3', ALCHEMY_RING7 ]


# NOTE: need to apply the new ammo count otherwise the game will
#       continuously drain rupees each time these are checked
ALCHEMY_RING5_ASM = [
    b'\xfa',W_NUM_BOMBCHUS, # ld a,(wNumBombchus)
    b'\xcd',ALCHEMY_RING8,  # call alchemyRing8
    b'\xc8',                # ret z
    b'\xea',W_NUM_BOMBCHUS, # ld (wNumBombchus),a
    b'\xc9',                # ret
    ]
ALCHEMY_RING6_ASM = [
    b'\xfa',W_NUM_BOMBS,    # ld a,(wNumBombs)
    b'\xcd',ALCHEMY_RING8,  # call alchemyRing8
    b'\xc8',                # ret z
    b'\xea',W_NUM_BOMBS,    # ld (wNumBombs),a
    b'\xc9',                # ret
    ]
ALCHEMY_RING7_ASM = [
    b'\xc5',                # push bc
    b'\xe5',                # push hl
    b'\xcd',ALCHEMY_RING8,  # call alchemyRing8
    b'\xe1',                # pop hl
    b'\xc1',                # pop bc
    b'\x77',                # ld (hl),a
    b'\xc0',                # ret nz
    b'\xe1',                # pop hl
    b'\xc9',                # ret
    ]

ALCHEMY_RING8_ASM = [
    # return if link's has at least 1 of the item
    b'\xb7',                        # or a
    b'\xc0',                        # ret nz

    # ring must be equipped
    b'\x3e',ALCHEMY_RING,           # ld a,ALCHEMY_RING
    b'\xcd',CP_ACTIVE_RING0,        # call cpActiveRing
    b'\x28\x05',                    # jr z,@checkItemType
    b'\xc3',CLEAR_PARENT_ITEM,      #   call clearParentItem
    b'\xaf',                        #   xor a
    b'\xc9',                        #   ret

    # @checkItemType
    b'\x1e\x01',                    # ld e,Item.id
    b'\x1a',                        # ld a,(de)

    # default to expecting the cost will be for a seed
    b'\x1e',ALCHEMY_COST_SEED,      #   ld e,alchemyCostSeed

    # @checkBombs
    b'\xfe\x03',                    # cp $03
    b'\x20\x02',                    # jr nz,@checkBombchu
    b'\x1e',ALCHEMY_COST_BOMB,      # ld e,alchemyCostBomb

    # @checkBombchu
    b'\xfe\x0d',                    # cp $0d
    b'\x20\x02',                    # jr nz,@checkHaveRupees
    b'\x1e',ALCHEMY_COST_BOMBCHU,   # ld e,alchemyCostBombchu

    # @checkHaveRupees
    b'\x7b',                        # ld a,e
    b'\xcd',CP_RUPEE_VALUE,         # call cpRupeeValue
    b'\xb7',                        # or a
    b'\x7b',                        # ld a,e

    # if we don't have enough rupees, clear the parent and return
    b'\x28\x05',                    # jr z,@doAlchemy
    b'\xc3',CLEAR_PARENT_ITEM,      #   call clearParentItem
    b'\xaf',                        #   xor a
    b'\xc9',                        #   ret

    # if we have that many rupees, remove them
    # @doAlchemy
    b'\xcd',REMOVE_RUPEE_VALUE,     # call removeRupeeValue
    # set the amount of ammo in "a" to 1
    b'\x3e\x01',                    # ld a,$01
    b'\x01',GOLD_JOY_RING,GREEN_JOY_RING,# ld bc,GREEN_JOY_RING,GOLD_JOY_RING
    b'\xcd',EITHER_RING,            # call eitherRingActive
    b'\x20\x02',                    # jr nz,@checkGoldJoy
    b'\x3e\x02',                    #   ld a,$02
    # @checkGoldJoy
    b'\x30\x02',                    # jr nc,@done
    b'\xcb\x27',                    #   sla a
    # @done
    b'\xb7',                        # or a
    b'\xc9',                        # ret
    ]
