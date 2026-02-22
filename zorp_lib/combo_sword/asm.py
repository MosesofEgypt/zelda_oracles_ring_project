from .const import *
from ..const import *
from ..shared.const import *

ORIG_SWORD_SPIN0_ASM = [
    b'\x62',                  # ld h,d
    b'\x2e\x21',              # ld l,Item.animParameter
    b'\xcb\x7e',              # bit 7,(hl)
    b'\xc8',                  # ret z
    b'\xcb\xbe',              # res 7,(hl)
    b'\x2e\x06',              # ld l,Item.counter1
    b'\x35',                  # dec (hl)
    b'\xc0',                  # ret nz
    b'\x3e\x05',              # ld a,$05
    b'\xea',WEAPON_ITEM_STATE,# ld (w1WeaponItem.state),a
    b'\xc3',SWORD_DELETE_SELF,# jp @deleteSelf
    ]
NEW_SWORD_SPIN0_ASM = list(ORIG_SWORD_SPIN0_ASM)
NEW_SWORD_SPIN0_ASM[5:7] = b'\xcd', SWORD_SPIN1

SWORD_SPIN_RING_CHECK_ASM = [
    b'\x2e\x06',        # ld l,Item.counter1
    b'\x35',            # dec (hl)
    b'\x2e\x2f',        # ld l,Item.var2f
    b'\x3e\x01',        # ld a,$01
    b'\xbe',            # cp (hl)
    b'\x2e\x06',        # ld l,Item.counter1
    b'\x28\x03',        # jr z,@superSpin
    # @notSuperSpin
    b'\x7e',            # ld a,(hl)
    b'\xb7',            # or a
    b'\xc9',            # ret
    # @superSpin
    ]
SWORD_SPIN_SOUND_ASM = [
    b'\x7e',            # ld a,(hl)
    b'\xe6\x03',        # and $03
    b'\x20\x07',        # jr nz,@done
    b'\xe5',            # push hl
    b'\x3e\x6b',        # ld a,SND_SWORDSPIN
    b'\xcd',PLAY_SOUND, # call playSound
    b'\xe1',            # pop hl
    # @done
    ]
SWORD_SPIN_INDEFINITE_ASM = [
    b'\xe5',                    # push hl
    b'\xcd',PARENT_CHECK_BUTTON,# call parentItemCheckButtonPressed
    b'\xe1',                    # pop hl
    b'\x28\x07',                # jr z,@cleanup
    b'\x7e',                    # ld a,(hl)
    b'\xfe',                    # cp a,$01
    b'\x28\x03',                # jr nz,@cleanup
    b'\xc6\x04',                # add $04
    b'\x77',                    # ld (hl),a
    # @cleanup
    ]
SWORD_SPIN_CLEANUP_ASM = [
    b'\x7e',                  # ld a,(hl)
    b'\xb7',                  # or a
    b'\xc0',                  # ret nz
    b'\x3e\x05',              # ld a,$05
    b'\xea',WEAPON_ITEM_STATE,# ld (w1WeaponItem.state),a
    b'\xcd',SWORD_DELETE_SELF,# call @deleteSelf
    ]
SWORD_SPIN_DIZZY_ASM = [
    b'\x3e\x64',              # ld a,SND_LINK_DEAD
    b'\xcd',PLAY_SOUND,       # call playSound
    b'\xe5',                  # push hl
    b'\x21',LINK_FORCED_STATE,# ld hl,linkForcedState
    b'\x3e\x14',              # ld a,LINK_STATE_COLLAPSED
    b'\x22',                  # ldi(hl),a
    b'\x3e\x00',              # ld a,$00
    b'\x22',                  # ldi(hl),a
    b'\x21',LINK_OBJECT_ADDR, # ld hl,w1Link
    b'\x2e\x06',              # ld l,w1Link.counter1
    b'\x36\x01',              # ld (hl),$01
    b'\xe1',                  # pop hl
    ]
SWORD_SPIN_RETURN_ASM = [
    b'\x7e',                  # ld a,(hl)
    b'\xb7',                  # or a
    b'\xc9',                  # ret
    ]

SWORD_SPIN1_CAPPED_ASM = [
    *SWORD_SPIN_RING_CHECK_ASM,
    *SWORD_SPIN_SOUND_ASM,
    *SWORD_SPIN_CLEANUP_ASM,
    *SWORD_SPIN_DIZZY_ASM,
    *SWORD_SPIN_RETURN_ASM,
    ]
SWORD_SPIN1_UNCAPPED_ASM = [
    *SWORD_SPIN_RING_CHECK_ASM,
    *SWORD_SPIN_SOUND_ASM,
    *SWORD_SPIN_INDEFINITE_ASM,
    *SWORD_SPIN_CLEANUP_ASM,
    *SWORD_SPIN_DIZZY_ASM,
    *SWORD_SPIN_RETURN_ASM,
    ]
ORIG_SWORD_SPIN2_ASM = [
    b'\x21',WEAPON_ITEM_STATE,      # ld hl,w1WeaponItem.state
    b'\x36\x04',                    # ld (hl),$04
    b'\x2e\x3a',                    # ld l,Item.var3a
    b'\xcb\x26',                    # sla (hl)
    b'\xcd',ITEM_DISABLE_LINK_MOVE, # call itemDisableLinkMovement
    b'\x3e\x6b',                    # ld a,SND_SWORDSPIN
    b'\xc3',PLAY_SOUND,             # jp playSound
    ]
NEW_SWORD_SPIN2_ASM = list(ORIG_SWORD_SPIN2_ASM)
NEW_SWORD_SPIN2_ASM[6] = SWORD_SPIN3

SWORD_SPIN3_ASM = [
    b'\x21',W_LINK_SWIMMING_STATE,  # ld hl,wLinkSwimmingState
    b'\x7e',                        # ld a,(hl)
    b'\xb6',                        # or (hl)
    b'\x20\x11',                    # jr nz,@disable
    b'\xc5',                        # push bc
    b'\x01',CHARGE_RING,SPIN_RING,  # ld bc,CHARGE_RING,SPIN_RING
    b'\xcd',EITHER_RING,            # call eitherRingActive
    b'\xc1',                        # pop bc
    b'\x62',                        # ld h,d
    b'\x2e\x2f',                    # ld l,Item.var2f
    b'\x36\x00',                    # ld (hl),$00
    b'\x20\x02',                    # jr nz,@disable
    b'\x38\x04',                    # jr c,@doSuperSpin
    # @disable
    b'\xcd',ITEM_DISABLE_LINK_MOVE, # call itemDisableLinkMovement
    b'\xc9',                        # ret
    # @doSuperSpin
    # mark it as a super spin using an unused variable
    b'\x36\x01',                    # ld (hl),$01
    b'\x2e\x06',                    # ld l,Item.counter1
    b'\x36',SPIN_SWING_COUNTER,     # ld (hl),SPIN_SWING_COUNTER
    b'\xc9',                        # ret
    ]


ORIG_SW_BEAM_CHECK_ASM = [
    b'\x0e\x08',            # ld c,$08
    b'\x3e',LIGHT_RING_L1,  # ld a,LIGHT_RING_L1
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x28\x0b',            # jr z,++
    b'\x0e\x0c',            #   ld c,$0c
    b'\x3e',LIGHT_RING_L2,  #   ld a,LIGHT_RING_L2
    b'\xcd',CP_ACTIVE_RING0,#   call cpActiveRing
    b'\x28\x02',            #   jr z,++
    b'\x0e\x00',            #     ld c,$00
    # ++
    b'\x21',W_LINK_HEALTH,  # ld hl,wLinkHealth
    b'\x2a',                # ldi a,(hl)
    b'\x81',                # add c
    b'\xbe',                # cp (hl)
    b'\xd8',                # ret c
    # @createSwordBeam
    ]
NEW_SW_BEAM_CHECK_ASM = [
    b'\x01',LIGHT_RING_L1,LIGHT_RING_L2,# ld bc,LIGHT_RING_L2,LIGHT_RING_L1
    b'\xcd',EITHER_RING,                # call eitherRingActive
    b'\x20\x04',                        # jr nz,@lightLevel0or1
    b'\x0e',LIGHT_RING_L2_CUTOFF,       #   ld c,$LIGHT_RING_L2_CUTOFF
    b'\x38\x0f',                        #   jr c,@createSwordBeam
    # @lightLevel0or1
    b'\x28\x06',                        # jr z,++
    b'\x0e',LIGHT_RING_L1_CUTOFF,       #   ld c,LIGHT_RING_L1_CUTOFF
    b'\x38\x02',                        #   jr c,++
    b'\x0e\x00',                        #   ld c,$00
    # ++
    b'\x21',W_LINK_HEALTH,              # ld hl,wLinkHealth
    b'\x2a',                            # ldi a,(hl)
    b'\x81',                            # add c
    b'\xbe',                            # cp (hl)
    b'\xd8',                            # ret c
    # @createSwordBeam
    ]

ORIG_SW_BEAM_CHARGE0_ASM = [
    b'\x3e',ENERGY_RING,        # ld a,ENERGY_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\x20\x06',                # jr nz,+
    b'\xcd',CREATE_SWORD_BEAM,  #   call createSwordBeam
    b'\xc3',TRIGGER_SWORD_POKE, #   jp @triggerSwordPoke
    ]
NEW_SW_BEAM_CHARGE0_ASM = list(ORIG_SW_BEAM_CHARGE0_ASM)
NEW_SW_BEAM_CHARGE0_ASM[-2:] = b'\xcd', SW_BEAM_CHARGE1

SW_BEAM_CHARGE1_ASM = [
    b'\x01',CHARGE_RING,ENERGY_RING,# ld bc,ENERGY_RING,CHARGE_RING
    b'\xcd',EITHER_RING,            # call eitherRingActive
    # NOTE: we're intentionally mucking with the stack here to make
    #       the return jump out of the @state2 code. This allows us
    #       to add as little code as necessary, as we don't need to
    #       add logic to @state2 to handle the return there.
    b'\xc1',                        # pop bc
    b'\xc2',TRIGGER_SWORD_POKE,     # jp nz,@triggerSwordPoke
    b'\xd2',TRIGGER_SWORD_POKE,     # jp nc,@triggerSwordPoke
    b'\x62',                        # ld h,d
    b'\x2e\x06',                    # ld l,Item.counter1
    b'\x36',SUPER_BEAM_DELAY,       # ld (hl),SUPER_BEAM_DELAY
    b'\xc9',                        # ret
    ]

ORIG_SW_BEAM_LIMIT0_ASM = [
    b'\x01',b'\x00',ITEM_SWORD_BEAM, # ldbc ITEM_SWORD_BEAM,$00
    b'\x1e\x01',                     # ld e,$01
    b'\xcd',GET_FREE_ITEM_SLOT,      # call getFreeItemSlotWithObjectCap
    b'\xd8',                         # ret c
    ]
NEW_SW_BEAM_LIMIT0_ASM = [
    b'\x1e\x01',                     # ld e,$01
    b'\xcd',SW_BEAM_LIMIT1,          # call swordBeamLimit1
    b'\xcd',GET_FREE_ITEM_SLOT,      # call getFreeItemSlotWithObjectCap
    b'\xd8',                         # ret c
    ]

SW_BEAM_LIMIT1_ASM = [
    b'\xf5',                            # push af
    b'\x01',b'\x00',ITEM_SWORD_BEAM,    # ldbc ITEM_SWORD_BEAM,$00
    b'\x3e',ENERGY_RING,                # ld a,ENERGY_RING
    b'\xcd',CP_ACTIVE_RING0,            # call cpActiveRing
    b'\x20\x11',                        # jr nz,@done
    b'\x01',LIGHT_RING_L1,LIGHT_RING_L2,# ld bc,LIGHT_RING_L2,LIGHT_RING_L1
    b'\xcd',EITHER_RING,                # call eitherRingActive
    b'\x01',b'\x00',ITEM_SWORD_BEAM,    # ldbc ITEM_SWORD_BEAM,$00
    b'\x28\x04',                        # jr z,@increaseBeamLimit
    b'\x38\x02',                        # jr c,@increaseBeamLimit
    b'\x20\x02',                        # jr nz,@done
    # @increaseBeamLimit
    b'\x1e',SWORD_BEAM_LIMIT,           # ld e,swordBeamLimit
    # @done
    b'\xf1',                            # pop af
    b'\xc9',                            # ret
    ]
