from .const import *
from ..const import *
from ..shared.const import *
from ..combo_sword.const import SWORD_BEAM_LIMIT


AGES_ORIG_PUNCH_CHECK0_ASM = [
    b'\xfa',W_ACTIVE_RING,# ld a,wActiveRing
    b'\xfe',EXPERTS_RING, # cp EXPERTS_RING
    b'\x28\x09',          # jr z,@expertsRing
    ]
SEAS_ORIG_PUNCH_CHECK0_ASM = [
    b'\xfa',W_ACTIVE_RING,# ld a,wActiveRing
    b'\xfe',EXPERTS_RING, # cp EXPERTS_RING
    b'\xc0',              # ret nz
    ]

AGES_NEW_PUNCH_CHECK0_ASM = [
    b'\x3e',EXPERTS_RING,   # ld a,EXPERTS_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x28\x09',            # jr z,@expertsRing
    ]
SEAS_NEW_PUNCH_CHECK0_ASM = [
    b'\x3e',EXPERTS_RING,   # ld a,EXPERTS_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\xc0',                # ret nz
    ]

AGES_NEW_PUNCH_CHECK0_ASM = [
    b'\x3e',EXPERTS_RING,   # ld a,EXPERTS_RING
    b'\xcd',PUNCH_HADOUKEN, # call punchHadouken
    b'\x28\x09',            # jr z,@expertsRing
    ]
SEAS_NEW_PUNCH_CHECK0_ASM = [
    b'\x3e',EXPERTS_RING,   # ld a,EXPERTS_RING
    b'\xcd',PUNCH_HADOUKEN, # call punchHadouken
    b'\xc0',                # ret nz
    ]
PUNCH_HADOUKEN_ASM = [
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\xc0',                    # ret nz
    b'\xe5',                    # push hl
    b'\xf5',                    # push af

    b'\x3e\x13',                # ld a,TREASURE_SLINGSHOT
    b'\xcd',CHECK_HAVE_TREASURE,# call checkTreasureObtained
    b'\x38\x07',                # jr c,@checkRing
    b'\x3e\x0f',                # ld a,TREASURE_SHOOTER
    b'\xcd',CHECK_HAVE_TREASURE,# call checkTreasureObtained
    b'\x30\x23',                # jr nc,@done
    # @checkRing
    b'\x3e',ENERGY_RING,        # ld a,ENERGY_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\x20\x1c',                # jr nz,@done

    b'\x1e\x19',                # ld e,Item.relatedObj2+1
    b'\x3e\xd0',                # ld a,>w1Link
    b'\x12',                    # ld (de),a

    b'\x1e',SWORD_BEAM_LIMIT,   # ld e,SWORD_BEAM_LIMIT
    # NOTE: the subid in seasons dictates which side-angle the
    #       seed is meant to shoot from. 0-4 make it veer off
    #       either slightly or heavily right/left, while 5 makes
    #       it shoot straight ahead. link's dir is accounted for
    b'\x01\x65\x20',            # ld bc,ITEM_EMBER_SEED,$65
    b'\xcd',ITEM_CREATE_CHILD,  # call itemCreateChildWithID
    b'\x38\x0d',                # jr c,@done

    b'\xfa',LINK_DIRECTION,     # ld a,(w1Link.direction)
    b'\x87',                    # add a
    b'\x87',                    # add a
    b'\x87',                    # add a
    b'\x2e\x09',                # ld l,Item.angle
    b'\x77',                    # ld (hl),a
    b'\x2e\x37',                # ld l,Item.var37
    b'\x36\x01',                # ld (hl),$01
    # @done
    b'\xf1',                    # pop af
    b'\xe1',                    # pop hl
    b'\xc9',                    # ret
    ]

ORIG_HADOUKEN_SEED0_ASM = [
    b'\x21',W_SEED_SHOOTER_IN_USE,# ld hl,wIsSeedShooterInUse
    b'\x34',                      # inc (hl)
    b'\x3e\x78',                  # ld a,SPEED_300
    # @setSpeed:
    b'\x1e\x10',                  # ld e,Item.speed
    b'\x12',                      # ld (de),a
    ]
NEW_HADOUKEN_SEED0_ASM = list(ORIG_HADOUKEN_SEED0_ASM)
NEW_HADOUKEN_SEED0_ASM[:2] = [
    b'\xcd', HADOUKEN_SEED1, # call hadoukenSeed1
    ]
HADOUKEN_SEED1_ASM = [
    b'\x1e\x37',                  # ld e,Item.var37
    b'\x1a',                      # ld a,(de)
    b'\xb7',                      # or a
    b'\x21',W_SEED_SHOOTER_IN_USE,# ld hl,wIsSeedShooterInUse
    b'\x20\x01',                  # jr nz,@hadouken
    # decrement shooter in use if fired from hadouken
    b'\xc9',                      # ret
    # @hadouken
    # set bounces to 0
    b'\x1e\x34',                  # ld e,Item.var34
    b'\x3e\x01',                  # ld a,$01
    b'\x12',                      # ld (de),a
    # change the gfx to a fireball
    b'\xcd',SEED_INIT_STATE3,     # call @initState3
    # make it blue
    #b'\x1e\x1c',                  # ld e,Item.oamFlags
    #b'\x3e\x0c',                  # ld a,$0e
    #b'\x12',                      # ld (de),a
    #b'\x1d',                      # dec e
    #b'\x12',                      # ld (de),a
    #b'\x3e\x0a',                  # ld a,$06
    # @changeSprite
    #b'\xf5',                      # push af
    #b'\xcd',ITEM_ANIMATE,         # call itemAnimate
    #b'\xf1',                      # pop af
    #b'\x3d',                      # dec a
    #b'\x20\xf8',                  # jr nz,@changeSprite
    # change the state back to 1 so things continue as normal
    b'\x1e\x04',                  # ld e,Item.state
    b'\x3e\x01',                  # ld a,$01
    b'\x12',                      # ld (de),a
    b'\x21',W_SEED_SHOOTER_IN_USE,# ld hl,wIsSeedShooterInUse
    b'\x35',                      # dec (hl)
    b'\xc9',                      # ret
    ]

ORIG_HADOUKEN_SEED2_ASM = [
    b'\x1e\x02',                  # ld e,Item.subid
    b'\x1a',                      # ld a,(de)
    b'\xb7',                      # or a
    b'\x28\x08',                  # jr z,@delete
    b'\x21',W_SEED_SHOOTER_IN_USE,# ld hl,wIsSeedShooterInUse
    b'\x7e',                      # ld a,(hl)
    b'\xb7',                      # or a
    b'\x28\x01',                  # jr z,@delete
    b'\x35',                      # dec (hl)
    # @delete
    ]
NEW_HADOUKEN_SEED2_ASM = list(ORIG_HADOUKEN_SEED2_ASM)
NEW_HADOUKEN_SEED2_ASM[:2] = [
    b'\xcd', HADOUKEN_SEED3, # call hadoukenSeed3
    ]

HADOUKEN_SEED3_ASM = [
    b'\x1e\x37',    # ld e,Item.var37
    b'\x1a',        # ld a,(de)
    b'\xb7',        # or a
    b'\x1e\x02',    # ld e,Item.subid
    b'\x1a',        # ld a,(de)
    b'\x28\x02',    # jr z,@deleteSeed
    b'\x3e\x00',    # ld a,$00
    b'\xc9',        # ret
    ]

ORIG_PUNCH_CHECK1_ASM = [
    b'\xfa',W_ACTIVE_RING,# ld a,(wActiveRing)
    b'\xfe',EXPERTS_RING, # cp EXPERTS_RING
    b'\x28\x03',          # jr z,@punch
    b'\xfe',FIST_RING,    # cp FIST_RING
    b'\xc0',              # ret nz
    ]
NEW_PUNCH_CHECK1_ASM = [
    b'\x01',FIST_RING,EXPERTS_RING,# ld bc,EXPERTS_RING,FIST_RING
    b'\xcd',EITHER_RING,           # call eitherRingActive
    b'\x28\x02',                   # jr z,@punch
    b'\xd0',                       # ret nc
    b'\x00',                       # nop
    ]

ORIG_SUPER_PUNCH0_ASM = [
    b'\x28\x12',                  # jr z,++
    b'\x2e\x26',                  # ld l,Item.collisionRadiusY
    b'\x3e\x06',                  # ld a,$06
    b'\x22',                      # ldi(hl),a
    b'\x22',                      # ldi(hl),a
    # Increase Item.damage
    b'\x7e',                      # ld a,(hl)
    b'\xc6\xfd',                  # add $fd
    b'\x77',                      # ld (hl),a
    b'\x2e\x24',                  # ld l,Item.collisionType
    # increment from ITEMCOLLISION_FIST_PUNCH to ITEMCOLLISION_EXPERT_PUNCH 
    b'\x34',                      # inc (hl)
    b'\xcd',EXPERT_TRY_BREAK_TILE,# call tryBreakTileWithExpertsRing
    b'\x0e\x6f',                  # ld c,SND_EXPLOSION
    # ++
    b'\x79',                      # ld a,c
    b'\xc3',PLAY_SOUND,           # jp playSound
    ]
NEW_SUPER_PUNCH0_ASM = [
    b'\x28\x12',                  # jr z,++
    b'\xcd',SUPER_PUNCH1,         # call superPunch1
    b'\x2e\x24',                  # ld l,Item.collisionType
    # increment to ITEMCOLLISION_EXPERT_PUNCH
    b'\x34',                      # inc (hl)
    # @setCollisionSize
    b'\x2e\x26',                  # ld l,Item.collisionRadiusY
    b'\x3e\x06',                  # ld a,$06
    b'\x22',                      # ldi(hl),a
    b'\x22',                      # ldi(hl),a
    # @setCollisionDamage
    b'\x70',                      # ld (hl),b
    b'\xc5',                      # push bc
    b'\xcd',EXPERT_TRY_BREAK_TILE,# call tryBreakTileWithExpertsRing
    b'\xc1',                      # pop bc
    # ++
    b'\x79',                      # ld a,c
    b'\xc3',PLAY_SOUND,           # jp playSound
    ]

SUPER_PUNCH1_ASM = [
    b'\x3e',FIST_RING,          # ld a,FIST_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    # Increase Item.damage
    b'\x06\xfd',                # ld b,$fd
    b'\x20\x04',                # jr nz,@notSuperPunch
    b'\x06\xfb',                #   ld b,$fb
    b'\x0e\x00',                #   ld c,$00
    # only need to play explosion sound if not a super punch, since
    # we'll be creating an explosion effect that plays it anyway.
    # @notSuperPunch
    b'\x0e\x6f',                # ld c,SND_EXPLOSION
    b'\xc9',                    # ret
    ]

ORIG_SUPER_PUNCH2_ASM = [
    b'\xfa',LINK_DIRECTION,# ld a,(w1Link.direction)
    b'\x87',               # add a
    b'\x4f',               # ld c,a
    b'\x3e\x03',           # ld a,BREAKABLETILESOURCE_EXPERTS_RING
    b'\x18\x0a',           # jr tryBreakTileWithSword
    ]
NEW_SUPER_PUNCH2_ASM = [
    b'\xfa',LINK_DIRECTION,# ld a,(w1Link.direction)
    b'\x87',               # add a
    b'\x4f',               # ld c,a
    b'\xcd',SUPER_PUNCH3,  # call superPunch3
    b'\xc9',               # ret
    ]

CREATE_EXPLOSION_IN_FRONT_OF_LINK_ASM = [
    b'\xc5',                       # push bc
    b'\x01\x80\x05',               # ldbc INTERAC_PUFF,$00
    b'\xcd',OBJ_CREATE_INTERAC,    # call objectCreateInteraction
    b'\x20\x17',                   # jr nz,@unableToCreateExplosion
    # move the explosions coordinates to in front of link
    b'\xe5',                       #   push hl
    b'\x4c',                       #   ld c,h
    b'\xfa',LINK_DIRECTION,        #   ld a,(w1Link.direction)
    b'\x87',                       #   add a
    # copy offsets for explosion into b and a
    b'\x21',LINK_OFFSETS,          #   ld hl,@linkOffsets
    b'\xdf',                       #   rst_addDoubleIndex
    b'\x46',                       #   ld b,(hl)
    b'\x2c',                       #   inc l
    b'\x7e',                       #   ld a,(hl)
    # point back to the interaction
    b'\x61',                       #   ld h,c
    b'\x2e\x4d',                   #   ld l,interaction.xh
    # add the its x coordinate to the offset and update xh with it
    b'\x86',                       #   add a,(hl)
    b'\x32',                       #   ldd (hl),a
    b'\x2d',                       #   dec l
    # add the its y coordinate to the offset and update yh with it
    b'\x78',                       #   ld a,b
    b'\x86',                       #   add a,(hl)
    b'\x77',                       #   ld (hl),a
    b'\xe1',                       #   pop hl
    # @unableToCreateExplosion
    b'\xc1',                       # pop bc
    ]

DO_SUPER_PUNCH_ASM = [
    # create an explosion effect
    *CREATE_EXPLOSION_IN_FRONT_OF_LINK_ASM,
    b'\xc5',                       #   push bc
    # break rocks with your bare hands if you've obtained bombs
    b'\x3e\x03',                   #   ld a,TREASURE_BOMBS
    b'\xcd',CHECK_HAVE_TREASURE,   #   call checkTreasureObtained
    b'\x30\x07',                   #   jr nc,@notBombable
    b'\x3e\x04',                   #     ld a,BREAKABLETILESOURCE_BOMB
    b'\xcd',SWORD_TRY_BREAK_TILE,  #     call tryBreakTileWithSword
    b'\xc1',                       #     pop bc
    b'\xc5',                       #     push bc
    # @notBombable
    # break pots and rocks if you've obtained the bracelet
    b'\x3e\x16',                   #   ld a,TREASURE_BRACELET
    b'\xcd',CHECK_HAVE_TREASURE,   #   call checkTreasureObtained
    b'\x30\x0e',                   #   jr nc,@notBreakable
    b'\x3e\x02',                   #     ld a,BREAKABLETILESOURCE_SWORD_L2
    b'\xcd',SWORD_TRY_BREAK_TILE,  #     call tryBreakTileWithSword
    b'\xc1',                       #     pop bc
    b'\xc5',                       #     push bc
    b'\x3e\x00',                   #     ld a,BREAKABLETILESOURCE_BRACELET
    b'\xcd',SWORD_TRY_BREAK_TILE,  #     call tryBreakTileWithSword
    b'\xc1',                       #     pop bc
    b'\xc5',                       #     push bc
    # @notBreakable
    # destroy the ground and clear dirt if you've obtained the shovel
    b'\x3e\x15',                   #   ld a,TREASURE_SHOVEL
    b'\xcd',CHECK_HAVE_TREASURE,   #   call checkTreasureObtained
    b'\x30\x07',                   #   jr nc,@notDiggable
    b'\x3e\x06',                   #     ld a,BREAKABLETILESOURCE_SHOVEL
    b'\xcd',SWORD_TRY_BREAK_TILE,  #     call tryBreakTileWithSword
    b'\xc1',                       #     pop bc
    b'\xc5',                       #     push bc
    # @notDiggable
    # cut down trees if you've obtained ember seeds
    b'\x3e\x20',                   #   ld a,TREASURE_EMBER_SEEDS
    b'\xcd',CHECK_HAVE_TREASURE,   #   call checkTreasureObtained
    b'\x30\x07',                   #   jr nc,@notBurnable
    b'\x3e\x0c',                   #     ld a,BREAKABLETILESOURCE_EMBER_SEED
    b'\xcd',SWORD_TRY_BREAK_TILE,  #     call tryBreakTileWithSword
    b'\xc1',                       #     pop bc
    b'\xc5',                       #     push bc
    # @notBurnable
    b'\xc1',                       #   pop bc
    # @done
    ]

SUPER_PUNCH3_ASM = [
    b'\xc5',                       # push bc
    b'\x01',FIST_RING,EXPERTS_RING,# ld bc,EXPERTS_RING,FIST_RING
    b'\xcd',EITHER_RING,           # call eitherRingActive
    b'\xc1',                       # pop bc
    b'\x30\x60',                   # jr nc,@notSuperPunch
    b'\x20\x5e',                   # jr nz,@notSuperPunch
    *DO_SUPER_PUNCH_ASM,
    b'\x3e\x03',                   # ld a,BREAKABLETILESOURCE_EXPERTS_RING
    b'\xcd',SWORD_TRY_BREAK_TILE,  # call tryBreakTileWithSword
    b'\xc9',                       # ret
    ]
