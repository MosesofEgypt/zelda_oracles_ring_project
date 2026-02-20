from .const import *
from ..const import *
from ..shared.const import *

ORIG_ARMOR_RING0_ASM = [
    b'\x1e\x25',                # ld e,SpecialObject.damageToApply
    b'\x1a',                    # ld a,(de)
    b'\xb7',                    # or a
    b'\xc8',                    # ret z

    b'\x47',                    # ld b,a
    b'\x21',POWER_RING_MODS,    # ld hl,@ringDamageModifierTable
    b'\xfa',W_ACTIVE_RING,      # ld a,(wActiveRing)
    b'\x5f',                    # ld e,a
    # --
    b'\x2a',                    # ldi a,(hl)
    b'\xb7',                    # or a
    b'\x28\x06',                # jr z,@matchingRingNotFound

    b'\xbb',                    # cp e
    b'\x28\x26',                # jr z,@matchingRingFound
    b'\x23',                    # inc hl
    b'\x18\xf6',                # jr --
    # @matchingRingNotFound:
    b'\x7b',                    # ld a,e
    b'\xfe',BLUE_RING,          # cp BLUE_RING
    b'\x28\x0b',                # jr z,@blueRing
    b'\xfe',GREEN_RING,         # cp GREEN_RING
    b'\x28\x0c',                # jr z,@greenRing
    b'\xfe',CURSED_RING,        # cp CURSED_RING
    b'\xc0',                    # ret nz

    # Cursed ring: damage *= 2
    b'\x78',                    #   ld a,b
    b'\x87',                    #   add a
    b'\x18\x15',                #   jr @writeDamageToApply
    # Blue ring: damage /= 2
    # @blueRing:
    b'\x78',                    #   ld a,b
    b'\xcb\x2f',                #   sra a
    b'\x18\x10',                #   jr @writeDamageToApply
    # Green ring: damage *= 0.75
    # @greenRing:
    b'\x78',                    #   ld a,b
    b'\x2f',                    #   cpl
    b'\x3c',                    #   inc a
    b'\x87',                    #   add a
    b'\x87',                    #   add a
    b'\x80',                    #   add b
    b'\xcb\x2f',                #   sra a
    b'\xcb\x2f',                #   sra a
    b'\x2f',                    #   cpl
    b'\x3c',                    #   inc a
    b'\x18\x02',                #   jr @writeDamageToApply

    # @matchingRingFound:
    b'\x7e',                    # ld a,(hl)
    b'\x80',                    # add b

    # @writeDamageToApply:
    b'\xcb\x7f',                # bit 7,a
    b'\x20\x02',                # jr nz,+
    b'\x3e\xff',                # ld a,$ff
    # +
    b'\x1e\x25',                # ld e,SpecialObject.damageToApply
    b'\x12',                    # ld (de),a
    b'\xc9',                    # ret

    # @ringDamageModifierTable:
    b'\x01\xfe',                # .db POWER_RING_L1   $fe
    b'\x02\xfc',                # .db POWER_RING_L2   $fc
    b'\x03\xf8',                # .db POWER_RING_L3   $f8
    b'\x04\x01',                # .db ARMOR_RING_L1   $01
    b'\x05\x02',                # .db ARMOR_RING_L2   $02
    b'\x06\x03',                # .db ARMOR_RING_L3   $03
    b'\x00',                    # .db $00
    ]
NEW_ARMOR_RING0_ASM    = [
    # linkUpdateDamageToApplyForRings:
    b'\x1e\x25',                        # ld e,SpecialObject.damageToApply
    b'\x1a',                            # ld a,(de)
    b'\xb7',                            # or a
    b'\xc8',                            # ret z
    # for each power and armor ring, check if it's equipped and
    # increase or reduce the damage by the associated amount.
    b'\xcd',CALC_DAMAGE_MODIFIER,       # call calcDamageModifier
    b'\x18\x06',                        # jr @armorModTableEnd
    # @armorModTableStart
     6,                                 # ARMOR_RING_L3_DEF_MOD
     4,                                 # ARMOR_RING_L2_DEF_MOD
     2,                                 # ARMOR_RING_L1_DEF_MOD
    -2,                                 # POWER_RING_L3_DEF_MOD
    -2,                                 # POWER_RING_L2_DEF_MOD
    -2,                                 # POWER_RING_L1_DEF_MOD
    # @armorModTableEnd
    b'\xcd',ARMOR_RING1,                # call armorRing1
    b'\x01',GREEN_RING,BLUE_RING,       # ld bc,BLUE_RING,GREEN_RING
    b'\xcd',EITHER_RING,                # call eitherRingActive
    b'\x06\x00',                        # ld b,$00
    b'\x20\x02',                        # jr nz,@checkGreen
    b'\x06',BLUE_RING_DEF_MOD,          #   ld b,BLUE_RING_DEF_MOD
    # @checkGreen
    b'\x30\x02',                        # jr nc,@checkCursed
    b'\xd6',GREEN_RING_DEF_MOD,         #   sub GREEN_RING_DEF_MOD
    # @checkCursed
    b'\x90',                            # sub b
    b'\x01',GOLD_RING,CURSE_POWER_RING, # ld bc,CURSE_POWER_RING,GOLD_RING
    b'\xcd',EITHER_RING,                # call eitherRingActive
    b'\x06\x00',                        # ld b,$00
    b'\x20\x02',                        # jr nz,@checkGold
    b'\x06',CURSE_POWER_RING_DEF_MOD,   #   ld b,CURSE_POWER_RING_DEF_MOD
    # @checkGold
    b'\x30\x0e',                        # jr nc,@capToMinDamage
    b'\xd6',GOLD_RING_DEF_MOD,          #   sub GOLD_RING_DEF_MOD
    b'\x4f',                            #   ld c,a
    b'\x21',W_LINK_HEALTH,              #   ld hl,wLinkHealth
    b'\x7e',                            #   ld a,(hl)
    b'\xfe',GOLD_RING_HI_CUTOFF,        #   cp GOLD_RING_HI_CUTOFF
    b'\x79',                            #   ld a,c
    b'\x30\x02',                        #   jr nc,@capToMinDamage
    b'\xd6',GOLD_RING_DEF_MOD,          #     sub GOLD_RING_DEF_MOD
    b'\x90',                            # sub b

    # @capToMinDamage
    # what we're doing is a bit complicated, but essentially we want
    # to ensure the minimum damage multiplier is 3/8. because math
    # get complex if things go below 0, we added 0x40 to keep it
    # above, so now we need to subtract it
    b'\xd6',MAX_DEF_MOD0,               # sub MAX_DEF_MOD0
    b'\x30\x02',                        # jr nc,@applyMultipliers
    b'\x3e\xff',                        # ld a,$ff
    b'\xc6',MAX_DEF_MOD1,               # add MAX_DEF_MOD1
    # @applyMultipliers
    b'\xcd',FRAC_OF_8_MULTIPLY,         # call fractionOf8Multiply
    b'\xcd',ENSURE_DAMAGE_MIN,          # call ensureDamageMin
    # +
    b'\xcd',ARMOR_RING2,                # call armorRing2
    b'\xc9',                            # ret
    ]

ARMOR_RING1_ASM = [
    # tuck the new base damage away into e
    b'\x5f',                    # ld e,a
    # calculate the multipliers(divisor is 8, so 1.5x will be $0c)
    b'\x3e\x48',                # ld a,$48

    b'\x01',BLUE_HOLY_RING,GREEN_HOLY_RING, # ld bc,GREEN_HOLY_RING,BLUE_HOLY_RING
    b'\xcd',EITHER_RING,        # call eitherRingActive
    b'\x06\x00',                # ld b,$00
    b'\x20\x02',                # jr nz,@checkBlueHoly
    b'\x06',HOLY_RING_DEF_MOD,  #   ld b,HOLY_RING_DEF_MOD
    # @checkBlueHoly
    b'\x30\x02',                # jr nc,@checkRedHoly
    b'\xd6',HOLY_RING_DEF_MOD,  #   sub HOLY_RING_DEF_MOD

    # @checkRedHoly
    b'\x01\xff',RED_HOLY_RING,  # ld bc,RED_HOLY_RING,$ff
    b'\xcd',EITHER_RING,        # call eitherRingActive
    b'\x30\x02',                # jr nc,@done
    b'\xd6',HOLY_RING_DEF_MOD,  #   sub HOLY_RING_DEF_MOD
    # @done
    b'\xc9',                    # ret
    ]

ARMOR_RING2_ASM = [
    # for each luck ring, give a 25% chance to reduce damage taken to 1/4 heart
    b'\x1e\x01',                # ld e,$01

    # if wearing blue cursed, all damage becomes 1/4 heart
    b'\xcd',CURSE_ARMOR_DAMAGE, # call curseArmorDamage
    b'\x28\x27',                # jr z,@done

    b'\x01',BLUE_LUCK_RING,GREEN_LUCK_RING, # ld bc,GREEN_LUCK_RING,BLUE_LUCK_RING
    b'\xcd',EITHER_RING,        # call eitherRingActive
    b'\x20\x01',                # jr nz,@checkBlueLuck
    b'\x1c',                    #   inc e
    # @checkBlueLuck
    b'\x30\x01',                # jr nc,@checkRedLuck
    b'\x1c',                    #   inc e
    # @checkRedLuck
    b'\x01\xff',RED_LUCK_RING,  # ld bc,RED_LUCK_RING,$ff
    b'\xcd',EITHER_RING,        # call eitherRingActive
    b'\x20\x01',                # jr nz,@checkLuckChance
    b'\x1c',                    #   inc e

    b'\x47',                    # ld b,a
    # @checkLuckChance
    # each luck ring gives a separate chance to reduce all damage taken
    # to nothing. the probabilities for this to occur while wearing
    # 1 / 2 / 3 rings are the following:
    #   if each ring == 25% chance  ->  25% / 44% / 58%
    #   if each ring == 30% chance  ->  30% / 51% / 66%
    #   if each ring == 33% chance  ->  33% / 55% / 70%
    #   if each ring == 38% chance  ->  38% / 60% / 76%
    #   if each ring == 50% chance  ->  50% / 75% / 88%
    b'\x1d',                    # dec e
    b'\x28\x0b',                # jr z,@done
    b'\xcd',GET_RANDOM_NUMBER,  # call getRandomNumber
    b'\xe6\x7f',                # and $7f
    b'\xfe',LUCK_RING_CHANCE,   # cp luckRingChance
    b'\x30\xf4',                # jr nc,@checkLuckChance
    # take 0 damage
    b'\x06\x00',                # ld b,$00

    # @done
    b'\x78',                    # ld a,b
    b'\x1e\x25',                # ld e,SpecialObject.damageToApply
    b'\x12',                    # ld (de),a
    b'\xc9',                    # ret
    ]

CURSE_ARMOR_DAMAGE_ASM = [
    # if wearing blue curse, all damage becomes 1/4 heart
    b'\xf5',                    # push af
    b'\x3e',CURSE_ARMOR_RING,   # ld a,CURSE_ARMOR_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\xc1',                    # pop bc
    b'\x20\x02',                # jr nz,@doFullDamage
    b'\x06\xfe',                # ld b,$fe
    # @doFullDamage
    b'\x78',                    # ld a,b
    b'\xc9',                    # ret
    ]

ORIG_DBL_EDGE_RING_ASM = [
    b'\xfa',W_LINK_HEALTH,      # ld a,(wLinkHealth)
    b'\xfe\x05',                # cp $05
    b'\x38\x0c',                # jr c,++
    b'\x3e',DBL_EDGED_RING,     # ld a,DBL_EDGED_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\x20\x05',                # jr nz,++
    b'\x1e\x3a',                # ld e,Item.var3a
    b'\x3e\xf8',                # ld a,$f8
    b'\x12',                    # ld (de),a
    # ++
    ]

NEW_DBL_EDGE_RING_ASM = list(ORIG_DBL_EDGE_RING_ASM)
NEW_DBL_EDGE_RING_ASM[2:3] = [
    b'\xfe\xff',                # cp $ff
    ]

ORIG_LINK_APPLY_DAMAGE_ASM = [
    b'\x7e',                    # ld a,(hl)
    b'\x36\x00',                # ld (hl),$00
    b'\xb7',                    # or a
    b'\x28\x0f',                # jr z,++
    b'\x47',                    # ld b,a

    b'\x3e',PROTECTION_RING,    # ld a,PROTECTION_RING
    b'\xcd',CP_ACTIVE_RING0,    # call cpActiveRing
    b'\x20\x02',                # jr nz,+
    b'\x06\xf8',                # ld b,$f8
    ]

NEW_LINK_APPLY_DAMAGE_ASM = [
    b'\x7e',                        # ld a,(hl)
    b'\x36\x00',                    # ld (hl),$00
    b'\xb7',                        # or a
    b'\x47',                        # ld b,a
    b'\x20\x09',                    # jr nz,@endOfCurseRingCapCode

    b'\x3e',CURSE_POWER_RING,       # ld a,CURSE_POWER_RING
    b'\xcd',CP_ACTIVE_RING0,        # call cpActiveRing
    b'\xcd',CURSE_RING_HEART_CAP,   # call curseRingHeartCap
    b'\x62',                        # ld h,d
    # @endOfCurseRingCapCode
    ]

CURSE_RING_HEART_CAP_ASM = [
    b'\xc0',                        # ret nz
    # prevent hardlock due to fairy waiting till link is healed
    b'\xfa',W_DISABLED_OBJECTS,     # ld a,(wDisabledObjects)
    b'\xb7',                        # or a
    b'\xc0',                        # ret nz
    b'\x21',W_LINK_HEALTH,          # ld hl,wLinkHealth
    b'\x3e',CURSE_RING_HEART_MAX,   # ld a,CURSE_RING_HEART_MAX
    b'\x96',                        # sub (hl)
    b'\xd0',                        # ret nc
    b'\x47',                        # ld b,a
    b'\xcb\x20',                    # sla b
    b'\xc9',                        # ret
    ]

ORIG_POWER_RING_ASM = [
    # itemCalculateSwordDamage:
    b'\x1e\x3a',                # ld e,Item.var3a
    b'\x1a',                    # ld a,(de)
    b'\x47',                    # ld b,a
    b'\xfa',PARENT_ITEM_VAR3A,  # ld a,(w1ParentItem2.var3a)
    b'\xb7',                    # or a
    b'\x20\x37',                # jr nz,@applyDamageModifier

    b'\x21',SWORD_DAMAGE_MODS,  # ld hl,@swordDamageModifiers
    b'\xfa',W_ACTIVE_RING,      # ld a,(wActiveRing)
    b'\x5f',                    # ld e,a
    # @nextRing:
    b'\x2a',                    # ldi a,(hl)
    b'\xb7',                    # or a
    b'\x28\x06',                # jr z,@noRingModifier
    b'\xbb',                    # cp e
    b'\x28\x28',                # jr z,@foundRingModifier
    b'\x23',                    # inc hl
    b'\x18\xf6',                # jr @nextRing

    # @noRingModifier:
    b'\x7b',            # ld a,e
    b'\xfe',RED_RING,   # cp RED_RING
    b'\x28\x0b',        # jr z,@redRing
    b'\xfe',GREEN_RING, # cp GREEN_RING
    b'\x28\x0a',        # jr z,@greenRing
    b'\xfe',CURSED_RING,# cp CURSED_RING
    b'\x28\x0f',        # jr z,@cursedRing

    b'\x78',            # ld a,b
    b'\x18\x17',        # jr @setDamage
    # Red ring: damage *= 2
    #@redRing:
    b'\x78',            # ld a,b
    b'\x18\x13',        # jr @applyDamageModifier
    # Green ring: damage *= 1.5
    # @greenRing:
    b'\x78',            # ld a,b
    b'\x2f',            # cpl
    b'\x3c',            # inc a
    b'\xcb\x2f',        # sra a
    b'\x2f',            # cpl
    b'\x3c',            # inc a
    b'\x18\x0a',        # jr @applyDamageModifier
    # Cursed ring: damage /= 2
    # @cursedRing:
    b'\x78',            # ld a,b
    b'\x2f',            # cpl
    b'\x3c',            # inc a
    b'\xcb\x2f',        # sra a
    b'\x2f',            # cpl
    b'\x3c',            # inc a
    b'\x18\x02',        # jr @setDamage

    # @foundRingModifier:
    b'\x7e',            # ld a,(hl)

    # @applyDamageModifier:
    b'\x80',            # add b

    # @setDamage:
    b'\xcb\x7f',        # bit 7,a
    b'\x20\x02',        # jr nz,+
    b'\x3e\xff',        # ld a,$ff
    # +
    b'\x1e\x28',        # ld e,Item.damage
    b'\x12',            # ld (de),a
    b'\xc9',            # ret

    # @swordDamageModifiers
    b'\x01\xff',        # .db POWER_RING_L1   $ff
    b'\x02\xfe',        # .db POWER_RING_L2   $fe
    b'\x03\xfd',        # .db POWER_RING_L3   $fd
    b'\x04\x01',        # .db ARMOR_RING_L1   $01
    b'\x05\x01',        # .db ARMOR_RING_L2   $01
    b'\x06\x01',        # .db ARMOR_RING_L3   $01
    b'\x00',            # .db $00
    ]
NEW_POWER_RING_ASM = [
    # get the swords base damage and store it in e
    b'\x1e\x3a',                        # ld e,Item.var3a
    b'\x1a',                            # ld a,(de)  # the sword's base damage
    b'\x5f',                            # ld e,a
    # calculate the multipliers(divisor is 8, so 1.5x will be $0c)
    b'\x3e\x08',                        # ld a,$08
    b'\x01',GREEN_RING,RED_RING,        # ld bc,RED_RING,GREEN_RING
    b'\xcd',EITHER_RING,                # call eitherRingActive
    b'\x06\x00',                        # ld b,$00
    b'\x20\x02',                        # jr nz,@checkGreen
    b'\x06',RED_RING_ATK_MOD,           #   ld b,RED_RING_ATK_MOD
    # @checkGreen
    b'\x30\x02',                        # jr nc,@checkCursed
    b'\xc6',GREEN_RING_ATK_MOD,         #   add GREEN_RING_ATK_MOD
    # @checkCursed
    b'\x80',                            # add b
    b'\x01',GOLD_RING,CURSE_POWER_RING, # ld bc,CURSE_POWER_RING,GOLD_RING
    b'\xcd',EITHER_RING,                # call eitherRingActive
    b'\x06\x00',                        # ld b,$00
    b'\x20\x02',                        # jr nz,@checkGold
    b'\x06',CURSE_POWER_RING_ATK_MOD,   #   ld b,CURSE_POWER_RING_ATK_MOD
    # @checkGold
    b'\x30\x10',                        # jr nc,@capToMaxDamage
    b'\xc6',GOLD_RING_ATK_MOD,          #   add GOLD_RING_ATK_MOD
    b'\x4f',                            #   ld c,a
    b'\xe5',                            #   push hl
    b'\x21',W_LINK_HEALTH,              #   ld hl,wLinkHealth
    b'\x7e',                            #   ld a,(hl)
    b'\xfe',GOLD_RING_HI_CUTOFF,        #   cp GOLD_RING_HI_CUTOFF
    b'\xe1',                            #   pop hl
    b'\x79',                            #   ld a,c
    b'\x20\x02',                        #   jr nz,@capToMaxDamage
    b'\xc6',GOLD_RING_ATK_MOD,          #     add GOLD_RING_ATK_MOD
    # @capToMaxDamage
    b'\x80',                            # add b
    b'\xfe',MAX_ATK_MOD,                # cp MAX_ATK_MOD
    b'\x38\x02',                        # jr c,@applyMultipliers
    b'\x3e',MAX_ATK_MOD,                # ld a,MAX_ATK_MOD
    # @applyMultipliers
    b'\xcd',FRAC_OF_8_MULTIPLY,         # call fractionOf8Multiply
    b'\xcd',CALC_DAMAGE_MODIFIER,       # call calcDamageModifier
    b'\x18\x06',                        # jr @powerModTableEnd
    # @powerModTableStart
     3,                                 # ARMOR_RING_L3_ATK_MOD
     2,                                 # ARMOR_RING_L2_ATK_MOD
     1,                                 # ARMOR_RING_L1_ATK_MOD
    -1,                                 # POWER_RING_L3_ATK_MOD
    -1,                                 # POWER_RING_L2_ATK_MOD
    -1,                                 # POWER_RING_L1_ATK_MOD
    # @powerModTableEnd
    b'\x5f',                            # ld e,a
    b'\xfa',PARENT_ITEM_VAR3A,          # ld a,(w1ParentItem2.var3a)
    # incorporate the modifiers
    b'\x83',                            # add e
    # @setDamage
    b'\xcd',ENSURE_DAMAGE_MIN,          # call ensureDamageMin
    # +
    b'\xcd',CURSE_ARMOR_DAMAGE,         # call curseArmorDamage
    b'\x1e\x28',                        # ld e,Item.damage
    b'\x12',                            # ld (de),a
    b'\xc9',                            # ret
    ]

ORIG_SWORD_DAMAGE_ASM = [
    # b0: collisionType
    # b1: base damage
    # @swordLevelData:
    0x80 | 0x04,# $80 | ITEMCOLLISION_L1_SWORD
    -2,         # 2 damage
    0x80 | 0x05,# $80 | ITEMCOLLISION_L2_SWORD
    -3,         # 3 damage
    0x80 | 0x06,# $80 | ITEMCOLLISION_L3_SWORD
    -5,         # 5 damage
    ]

ORIG_WHISP_RING_CHECK_ASM = [
    b'\x20\x0c',            # jr nz,@normalStatus
    b'\x3e',WHISP_RING,     # ld a,WHISP_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x28\x05',            # jr z,@normalStatus    
    b'\x3e',180,            # ld a,180
    ]
NEW_WHISP_RING_CHECK_ASM = [
    b'\x20\x0c',            # jr nz,@normalStatus
    b'\x3e',RED_HOLY_RING,  # ld a,RED_HOLY_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x28\x05',            # jr z,@normalStatus    
    b'\x3e',180,            # ld a,180
    ]

ORIG_GOLD_RING_ASM = [
    b'\x3e',WHIMSICAL_RING, # ld a,WHIMSICAL_RING
    b'\xcd',CP_ACTIVE_RING0,# call cpActiveRing
    b'\x20',b'\x0f',        # jr nz,@@setDamage
    ]
NEW_GOLD_RING_ASM = list(ORIG_GOLD_RING_ASM)
NEW_GOLD_RING_ASM[-2] = b'\x18' # always jump

ORIG_GOLD_RING_ICON_ASM = [
    # whimsical ring sprite data
    b'\xcf\x04\xbe\x02',
    b'\xa1\x02\xbf\x02',
    ]
NEW_GOLD_RING_ICON_ASM = [
    b'\xa9\x05\xbe\x02',
    b'\xa7\x02\xbf\x02',
    ]

ORIG_CURSE_ARMOR_RING_ICON_ASM = [
    # double edged ring sprite data
    b'\xb8\x04\xdc\x06',
    b'\xde\x06\xdd\x06',
    ]
NEW_CURSE_ARMOR_RING_ICON_ASM  = [
    b'\xae\x03\xbe\x02',
    b'\xa1\x02\xbf\x02',
    ]

ORIG_CURSE_POWER_RING_ICON_ASM = [
    # cursed ring sprite data
    b'\xae\x03\xbe\x02',
    b'\xa1\x02\xbf\x02',
    ]
NEW_CURSE_POWER_RING_ICON_ASM  = [
    b'\xae\x04\xbe\x02',
    b'\xa1\x02\xbf\x02',
    ]
