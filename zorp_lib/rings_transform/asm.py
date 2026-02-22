from .const import *
from ..const import *
from ..shared.const import *

ORIG_GET_XFORM_LINK_ID_ASM = [
    # getTransformedLinkID
    b'\x21',W_DISABLE_RING_XFORMS,  # ld hl,wDisableRingTransformations
    b'\x7e',                        # ld a,(hl)
    b'\xb7',                        # or a
    b'\x28\x03',                    # jr z,+

    b'\x35',                        # dec (hl)
    b'\x18\x23',                    # jr ++

    # +
    b'\xfa',W_TILESET_FLAGS,        # ld a,(wTilesetFlags)
    b'\xe6',0x40|0x20,              # and TILESETFLAG_40 | TILESETFLAG_SIDESCROLL
    b'\x20\x1c',                    # jr nz,++

    b'\xfa',W_MENU_DISABLED,        # ld a,(wMenuDisabled)
    b'\xb7',                        # or a
    b'\x20\x16',                    # jr nz,++

    b'\xfa',W_IN_SHOP,              # ld a,(wInShop)
    b'\x47',                        # ld b,a
    b'\xfa',W_LINK_GRAB_STATE,      # ld a,(wLinkGrabState)
    b'\xb0',                        # or b
    b'\x20\x0c',                    # jr nz,++

    b'\xfa',W_ACTIVE_RING,          # ld a,(wActiveRing)
    b'\x5f',                        # ld e,a
    b'\x21',RING_TO_XFORM_ID,       # ld hl,@ringToID
    b'\xcd',LOOKUP_KEY,             # call lookupKey
    b'\x47',                        # ld b,a
    b'\xc9',                        # ret
    # ++
    b'\x06\x00',                    # ld b,$00
    b'\xc9',                        # ret

    # @ringToID:
    OCTO_RING,      0x05,           # .db OCTO_RING         SPECIALOBJECT_LINK_AS_OCTOROK
    MOBLIN_RING,    0x06,           # .db MOBLIN_RING       SPECIALOBJECT_LINK_AS_MOBLIN
    LIKE_LIKE_RING, 0x07,           # .db LIKE_LIKE_RING    SPECIALOBJECT_LINK_AS_LIKELIKE
    SUBROSIAN_RING, 0x03,           # .db SUBROSIAN_RING    SPECIALOBJECT_LINK_AS_SUBROSIAN
    FIRST_GEN_RING, 0x04,           # .db FIRST_GEN_RING    SPECIALOBJECT_LINK_AS_RETRO
    0x00,                           # .db $00
    ]

NEW_GET_XFORM_LINK_ID_ASM = [
    b'\xcd',GET_CAN_REMAP_SPRITE,   # call getCanRemapSprite
    b'\x7b',                        # ld a,e
    b'\xc8',                        # ret z

    # @checkRings
    b'\xaf',                        # xor a
    b'\xc5',                        # push bc
    # redirect id to transformed one if ring equipped
    b'\x01',FIRST_GEN_RING,SUBROSIAN_RING, # ld bc,SUBROSIAN_RING,FIRST_GEN_RING
    b'\xcd',EITHER_RING,            # call eitherRingActive
    # @checkSubrosian
    b'\x20\x02',                    # jr nz,@checkFirstGen
    b'\x3e\x03',                    #   ld a,$03
    # @checkFirstGen
    b'\x30\x02',                    # jr nc,@checkOctorock
    b'\x3e\x04',                    #   ld a,$04
    # @checkOctorock
    b'\x01',MOBLIN_RING,OCTO_RING,  # ld bc,OCTO_RING,MOBLIN_RING
    b'\xcd',EITHER_RING,            # call eitherRingActive
    b'\x20\x02',                    # jr nz,@checkMoblin
    b'\x3e\x05',                    #   ld a,$05
    # @checkMoblin
    b'\x30\x02',                    # jr nc,@checkLikeLike
    b'\x3e\x06',                    #   ld a,$06
    # @checkLikeLike
    b'\x01\xff',LIKE_LIKE_RING,     # ld bc,LIKE_LIKE_RING,$ff
    b'\xcd',EITHER_RING,            # call eitherRingActive
    b'\x20\x02',                    # jr nz,@done
    b'\x3e\x07',                    #   ld a,$07

    # @done
    b'\xc1',                        # pop bc
    b'\xb7',                        # or a
    b'\xc3',REMAP_XFORM_LINK,       # jp remapTransformedLink
    b'\x00'*9,                      # nop
    ]

GET_CAN_REMAP_SPRITE_ASM = [
    b'\x21',SPECOBJ_GFX_TABLE,      # ld hl,@specialObjectGraphicsTable

    # if this isn't a link object, don't bother remapping
    b'\xfe\x02',                    # cp $02
    b'\x38\x13',                    # jr c,@checkFrame
    b'\xfe\x08',                    #   cp $08
    b'\x28\x0f',                    #   jr z,@checkFrame
    # we can remap all the companion riding sprites except rickey
    # those sprites indices less than 0x0e and greater than 0x2e
    b'\xfe\x09',                    #     cp $09  // riding-companion
    b'\x20\x09',                    #     jr nz,@cantRemap
    b'\x79',                        #     ld a,c
    b'\xfe\x0e',                    #     cp $0e
    b'\x38\x04',                    #     jr c,@cantRemap
    b'\xfe\x2f',                    #     cp $2f
    b'\x38\x02',                    #     jr c,@checkFrame
    # @cantRemap
    b'\xbf',                        #     cp a
    b'\xc9',                        #     ret

    # @checkFrame
    b'\x79',                        # ld a,c
    # if the frame is one that can't be well
    # represented otherwise, dont substitute it
    b'\xfe\x08',                    # cp $08  # falling in hole 1
    b'\xc8',                        # ret z
    b'\xfe\x09',                    # cp $09  # falling in hole 2
    b'\xc8',                        # ret z
    b'\xfe\x0a',                    # cp $0a  # falling in hole 3
    b'\xc8',                        # ret z
    b'\xfe\x04',                    # cp $04  # collapsed
    b'\xc8',                        # ret z
    b'\xfe\x32',                    # cp $32  # squash thin
    b'\xc8',                        # ret z
    b'\xfe\x33',                    # cp $33  # squash flat
    b'\xc8',                        # ret z

    # don't remap if swimming(no custom sprites makes it look baaaaad)
    b'\xfa',W_LINK_SWIMMING_STATE,  # ld a,(wLinkSwimmingState)
    b'\xb7',                        # or a
    b'\x20\x02',                    # jr nz,@done
    b'\x3c',                        #   inc a
    b'\xc9',                        #   ret

    # @done
    b'\xfa',W_ACTIVE_GROUP,         # ld a,(wActiveGroup)
    b'\xfe\x06',                    # cp FIRST_SIDESCROLL_GROUP
    b'\x20\x02',                    # jr nz,@done
    b'\xaf',                        #   xor a
    b'\xc9',                        #   ret
    b'\xb7',                        # or a
    b'\xc9',                        # ret
    ]

REMAP_XFORM_LINK_NORMAL_ASM = [
    # certain special animations are better to hardcode a sprite
    b'\xfe\x04',                    # cp $04  # stand-facing
    b'\x20\x02',                    # jr nz,@checkLeftFacing
    b'\x3e\x06',                    #   ld a,$06

    # @checkLeftFacing
    b'\xfe\x1d',                    # cp $1d  # dance-left
    b'\x20\x02',                    # jr nz,@checkRightFacing
    b'\x3e\x07',                    #   ld a,$07

    # @checkRightFacing
    b'\xfe\x1e',                    # cp $1e  # dance-right
    b'\x20\x02',                    # jr nz,@checkGaleSeed
    b'\x3e\x05',                    #   ld a,$05

    # @checkGaleSeed
    # handle gale seed having 8 directions
    b'\xfe\x10',                    # cp $10
    b'\x38\x06',                    # jr c,@checkSeedShooter
    b'\xfe\x18',                    #   cp $18
    b'\x30\x02',                    #   jr nc,@checkSeedShooter
    b'\xcb\x2f',                    #     sra a

    # @checkSeedShooter
    # handle seed shooter and big sword swing having 8 directions
    b'\xfe\x38',                    # cp $38
    b'\x38\x06',                    # jr c,@fourDirectional
    b'\xfe\x50',                    #   cp $50
    b'\x30\x02',                    #   jr nc,@fourDirectional
    b'\xcb\x2f',                    #     sra a
    # @fourDirectional
    b'\xc9',                        # ret
    ]

REMAP_XFORM_LINK_RIDING_ASM = [
    # this is all we need to do to fix this. the first 13 sprites
    # are for ricky, which throws off the count for the others.
    b'\x3c',                        # inc a
    b'\xbf',                        # cp a
    b'\xc9',                        # ret
    ]

REMAP_XFORM_LINK_ASM = [
    # replace the id if we selected a new one
    b'\x20\x02',                    # jr nz,@doRemap
    b'\x7b',                        #   ld a,e
    b'\xc9',                        #   ret

    # check if link-riding object or not
    b'\x47',                        # ld b,a
    b'\x7b',                        # ld a,e
    b'\xfe\x09',                    # cp $09

    # @doRemap
    b'\x58',                        # ld e,b
    b'\x79',                        # ld a,c
    b'\x06\x00',                    # ld b,$00

    b'\xcc',REMAP_XFORM_LINK_RIDING,# call  z remapTransformLinkRiding
    b'\xc4',REMAP_XFORM_LINK_NORMAL,# call nz remapTransformLinkNormal

    # put the index in the range the transformed sprites support
    b'\xe6\x07',                    # and $07

    # setup the registers with the new object id and animation index
    b'\x4f',                        # ld c,a
    b'\x7b',                        # ld a,e
    b'\xc9',                        # ret
    ]

ORIG_GET_SPECOBJ_GFX_FRAME_ASM = [
    b'\x5f',                    # ld e,a
    b'\x21',SPECOBJ_GFX_TABLE,  # ld hl,@specialObjectGraphicsTable
    b'\xdf',                    # rst_addDoubleIndex
    b'\x2a',                    # ldi a,(hl)
    b'\x66',                    # ld h,(hl)
    b'\x6f',                    # ld l,a
    b'\x09',                    # add hl,bc
    b'\x09',                    # add hl,bc
    b'\x09',                    # add hl,bc
    ]
NEW_GET_SPECOBJ_GFX_FRAME_ASM = list(ORIG_GET_SPECOBJ_GFX_FRAME_ASM)
NEW_GET_SPECOBJ_GFX_FRAME_ASM[1:3] = [
    b'\xcd',GET_XFORM_LINK_ID,
    ]

ORIG_GET_XFORM_LINK_ID_CALL0_ASM = [
    b'\x21',GET_XFORM_LINK_ID,  # ld hl,@getTransformedLinkID
    b'\x1e\x06',                # ld e,bank6
    b'\xcd',INTER_BANK_CALL,    # call interBankCall
    b'\x78',                    # ld a,b
    ]

NEW_GET_XFORM_LINK_ID_CALL0_ASM = list(ORIG_GET_XFORM_LINK_ID_CALL0_ASM)
NEW_GET_XFORM_LINK_ID_CALL0_ASM[-3:-1] = [
    b'\x06\x00',    # ld b,$00
    b'\x00',        # nop
    ]

ORIG_GET_XFORM_LINK_ID_CALL1_ASM     = list(ORIG_GET_XFORM_LINK_ID_CALL0_ASM)
NEW_GET_XFORM_LINK_ID_CALL1_ASM      = list(NEW_GET_XFORM_LINK_ID_CALL0_ASM)
ORIG_GET_XFORM_LINK_ID_CALL1_ASM[-1] = b'\x1e\x01' # ld e,SpecialObject.id
NEW_GET_XFORM_LINK_ID_CALL1_ASM[-1]  = b'\x1e\x01' # ld e,SpecialObject.id
