from .const import *
from ..const import *
from ..shared.const import *
from ..misc.asm import NEW_FEATHER_SPEED0_ASM, FEATHER_SPEED1_ASM,\
     FEATHER_SPEED1


ORIG_COLLISION_CHECK0_ASM = [
    b'\x87',                 # add a
    b'\xcd',MULTIPLY_A_BY_16,# call multiplyABy16
    b'\x21',OBJECT_COLL_TBL, # ld hl,objectCollisionTable
    b'\x09',                 # add hl,bc
    b'\xc1',                 # pop bc
    b'\xf0\x90',             # ld a,(<hFF90)
    b'\xd7',                 # rst_addAToHl
    b'\x7e',                 # ld a,(h1)
    b'\xc7',                 # rst_jumpTable
    ]

NEW_COLLISION_CHECK0_ASM = list(ORIG_COLLISION_CHECK0_ASM)
NEW_COLLISION_CHECK0_ASM[-4:-1] = [
    b'\xcd',COLLISION_CHECK1,# call collisionCheck1
    b'\x00',                 # nop
    ]

COLLISION_CHECK1_ASM = [
    b'\xf0\x90',              # ld a,(<hFF90)
    b'\xd7',                  # rst_addAToHl
    b'\x7e',                  # ld a,(h1)
    b'\xcd',COLLISION_BOUNCE0,# call collisionBounce
    b'\xc9',                  # ret
    ]

# TODO: make a table of part/enemy ids you cant bounce off(i.e. fireballs)
# TODO: make a table of enemy ids you cant stun with the bounce(i.e. bosses)
# TODO: make it possible to downstab if attacking while in air.
#       need to ensure it doesn't get abused by chaining downstabs on bosses
COLLISION_BOUNCE0_ASM = [
    # only bounce if link is in the air, the collision effect
    # is specifically COLLISIONEFFECT_DAMAGE_LINK, and link is
    # wearing the rings. we don't want to consider other damage
    # types, as they're rare and the situations they're use
    # in don't warrant link being able to bounce off safely
    # @checkCollisionType
    b'\xfe\x02',                     # cp $02
    b'\xc0',                         # ret nz
    # @checkLinkInAirAndFalling
    b'\xc5',                         # push bc
    b'\xf5',                         # push af
    b'\xfa',W_LINK_IN_AIR,           # ld a,(wLinkInAir)
    b'\xe6\x0f',                     # and $0f
    # check that he is fully in the air
    b'\xfe\x02',                     # cp $02
    b'\xc1',                         # pop bc
    b'\x78',                         # ld a,b
    b'\xc1',                         # pop bc
    b'\xc0',                         # ret nz
    # @checkRingsEquipped
    b'\xc5',                         # push bc
    b'\x01',STEADFAST_RING,ROCS_RING,# ld bc,STEADFAST_RING,ROCS_RING
    b'\xcd',EITHER_RING,             # call eitherRingActive
    b'\xc1',                         # pop bc
    b'\xc0',                         # ret nz
    b'\xd0',                         # ret nc
    # convert collisions that would damage link into an extra jump
    b'\xc5',                         # push bc
    *(
        COLLISION_BOUNCE1 if val is FEATHER_SPEED1 else val
        for val in NEW_FEATHER_SPEED0_ASM
        ),
    b'\xc1',                         # pop bc
    # change collision type
    b'\x3e',EXPERTS_RING,            # ld a,EXPERTS_RING
    b'\xcd',CP_ACTIVE_RING0,         # call cpActiveRing
    b'\x28\x08',                     # jr z,@expertJump
    b'\x3e\x53',                     # ld a,SND_JUMP
    b'\xcd',PLAY_SOUND,              # call playSound
    b'\x3e\x0d',                     # ld a,COLLISIONEFFECT_BUMP
    #b'\x3e\x10',                     # ld a,COLLISIONEFFECT_SHIELD_BUMP_HIGH_KNOCKBACK
    b'\xc9',                         # ret
    b'\x3e\x22',                     # ld a,COLLISIONEFFECT_STUN
    b'\xc9',                         # ret
    ]

COLLISION_BOUNCE1_ASM = list(FEATHER_SPEED1_ASM)
