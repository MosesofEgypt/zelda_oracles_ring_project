from .const import *
from ..const import *
from ..shared.const import *



ORIG_HIKERS_RING0_ASM = [
    b'\xc3',PULL_LINK_INTO_HOLE,# jp,pullLinkIntoHole
    b'\x3e',SNOWSHOE_RING,      # ld a,SNOWSHOE_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\x28',                    # jr z,???
    ]
ORIG_HIKERS_RING1_ASM = [
    b'\x20\x1e',                # jr nz,@notOnIce
    b'\x3e',SNOWSHOE_RING,      # ld a,SNOWSHOE_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\x28\x17',                # jr z,@notOnIce
    ]
ORIG_HIKERS_RING2_ASM = [
    b'\xfe\x05',                  # cp TILETYPE_GRASS
    b'\x28\x0a',                  # jr z,+
    b'\x04',                      # inc b
    b'\xfe\x06',                  # cp TILETYPE_STAIRS
    b'\x28\x05',                  # jr z,+
    b'\xfe\x04',                  # cp TILETYPE_VINES
    b'\x28\x01',                  # jr z,+
    b'\x04',                      # inc b
    b'\xcd',CHECK_PEGASUS_COUNTER,# call checkPegasusSeedCounter
    ]
HIKERS_RING3_ASM = [
    b'\xd5',                      # push de
    b'\xf5',                      # push af
    b'\x3e',HIKERS_RING,          # ld a,HIKERS_RING
    b'\xcd',CP_ACTIVE_RING0,      # call cpActiveRing
    b'\xd1',                      # pop de
    b'\x7a',                      # ld a,d
    b'\xd1',                      # pop de
    b'\x20\x02',                  # jr nz,@notTrailblazing
    b'\x06\x04',                  # ld b,$04
    # @notTrailblazing
    b'\xcd',CHECK_PEGASUS_COUNTER,# call checkPegasusSeedCounter
    b'\xc9',                      # ret
    ]

NEW_HIKERS_RING0_ASM = list(ORIG_HIKERS_RING0_ASM)
NEW_HIKERS_RING1_ASM = list(ORIG_HIKERS_RING1_ASM)
NEW_HIKERS_RING2_ASM = list(ORIG_HIKERS_RING2_ASM)
NEW_HIKERS_RING0_ASM[3]  = HIKERS_RING
NEW_HIKERS_RING1_ASM[2]  = HIKERS_RING
NEW_HIKERS_RING2_ASM[-1] = HIKERS_RING3


ORIG_HIKERS_RING_ICON_ASM = [
    # quicksand ring sprite data
    b'\xca\x03\xbe\x02',
    b'\xa1\x02\xbf\x02',
    ]
NEW_HIKERS_RING_ICON_ASM  = [
    b'\xc3\x02\xbe\x02',
    b'\xa1\x02\xbf\x02',
    ]
