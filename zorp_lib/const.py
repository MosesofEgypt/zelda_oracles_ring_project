BANK_SIZE   = 0x4000
MAX_BANKS   = 0x40

# these are the locations in each bank that padding
# starts for the english ages and seasons roms.
# if a bank is missing from here, it has no padding.
AGES_BANK_PAD_STARTS = {
    0:  16120,
    1:  16163,
    2:  15847,
    3:  15971,
    4:  16091,
    5:  15668,
    6:  14835,
    7:  15499,
    8:  16219,
    9:  15854,
    10: 15879,
    11: 16289,
    12: 16275,
    13: 16041,
    14: 16247,
    15: 16272,
    16: 16116,
    17: 16228,
    18: 16015,
    19: 16111,
    20: 15037,
    21: 15355,
    22: 15874,
    23: 12003,
    24: 15980,
    25: 16335,
    26: 16064,
    27: 16095,
    28: 15808,
    56: 10987,
    63: 15527,
    }
SEAS_BANK_PAD_STARTS = {
    0:  16072,
    1:  16009,
    2:  13755,
    3:  15831,
    4:  15874,
    5:  15917,
    6:  14292,
    7:  14576,
    8:  16320,
    9:  16206,
    10: 15337,
    11: 16237,
    12: 16032,
    13: 15218,
    14: 16099,
    15: 16285,
    16: 15342,
    17: 16048,
    18: 15487,
    19: 15314,
    20: 12233,
    21: 14637,
    22: 14854,
    23: 16170,
    24: 15980,
    25: 14033,
    26: 12512,
    27: 15424,
    56: 15856,
    63: 12619,
    }

ROM_SIG_OFFSET  = 0x134
ROM_SIG_AGES    = b"ZELDA NAYRU"
ROM_SIG_SEAS    = b"ZELDA DIN\x00\x00"
ROM_REGION_AGES = b'AZ8'
ROM_REGION_SEAS = b'AZ7'
ROM_LANGUAGE_EN = b'E'
ROM_LANGUAGE_JP = b'J'

ROM_SIG_EN_AGES = ROM_SIG_AGES + ROM_REGION_AGES + ROM_LANGUAGE_EN
ROM_SIG_EN_SEAS = ROM_SIG_SEAS + ROM_REGION_SEAS + ROM_LANGUAGE_EN

# to ensure we have as much space to work with as possible(mostly for
# text updates), we'll need to know where garbage data is and clear it.
AGES_BANK_GARBAGE = {
    0x01: [dict(start=0x3F23, size=160,  md5="de942b7919378ea3c279e10b8c2b6155")],
    0x02: [dict(start=0x3DE7, size=174,  md5="0a916ecd44b2b43e48c1b504d5471e5c")],
    0x03: [dict(start=0x3E63, size=90,   md5="641b0614514a197c7c1ae7a381d9a975")],
    0x04: [dict(start=0x3EDE, data=b'\xef\x44\x43\xff')],
    0x05: [dict(start=0x3D35, size=104,  md5="ba5f2c925298545e73f2c8bf69acc89b")],
    0x06: [dict(start=0x39F3, size=62,   md5="303598c79ce06be026e4739243848922")],
    0x07: [dict(start=0x3CB5, size=331,  md5="3774967b99efeca5c6f196690904dbb8")],
    0x0b: [dict(start=0x3FA1, data=b"\xcd\x8f\x25\xd0\xc3\x5c\x3b")],
    0x0e: [dict(start=0x3F77, size=16,   md5="a88fecce548c04c283bc1e442f1a74b5")],
    0x11: [dict(start=0x3F64, size=15,   md5="bd19f104fe6aeb0dea0e0c058fa8c147")],
    0x17: [dict(start=0x2EE3, size=4167, md5="6e7a8caeeba092b95dffe567820e53d8")],
    #0x18: [dict(start=0x0, size=0, md5="")],
    0x1c: [dict(start=0x3DC0, size=576,  md5="fd93b05e78fc64158bea9baab8693d1a")],
    0x3f: [dict(start=0x3CA7, size=99,   md5="3831b91eb8ad3f3d523ac0b97c4425b7")],
    }
SEAS_BANK_GARBAGE = {
    }

# enums that represent rupee values in the game's calculations
RUPEEVAL_000 = 0x00
RUPEEVAL_001 = 0x01
RUPEEVAL_002 = 0x02
RUPEEVAL_005 = 0x03
RUPEEVAL_010 = 0x04
RUPEEVAL_020 = 0x05
RUPEEVAL_040 = 0x06
RUPEEVAL_030 = 0x07
RUPEEVAL_060 = 0x08
RUPEEVAL_070 = 0x09
RUPEEVAL_025 = 0x0a
RUPEEVAL_050 = 0x0b
RUPEEVAL_100 = 0x0c
RUPEEVAL_200 = 0x0d
RUPEEVAL_400 = 0x0e
RUPEEVAL_150 = 0x0f
RUPEEVAL_300 = 0x10
RUPEEVAL_500 = 0x11
RUPEEVAL_900 = 0x12
RUPEEVAL_080 = 0x13
RUPEEVAL_999 = 0x14

# ring constants
FRIENDSHIP_RING, MAPLES_RING,  GASHA_RING, DISCOVERY_RING = 0x00, 0x0f, 0x3a, 0x28
STEADFAST_RING,  SNOWSHOE_RING, ROCS_RING, QUICKSAND_RING = 0x10, 0x21, 0x22, 0x23
PEGASUS_RING,    SWIMMERS_RING, ZORA_RING, TOSS_RING      = 0x11, 0x15, 0x3c, 0x12
BOMBERS_RING,    PEACE_RING,   BLAST_RING, BOMBPROOF_RING = 0x19, 0x3b, 0x0c, 0x30

POWER_RING_L1, POWER_RING_L2, POWER_RING_L3     = 0x01, 0x02, 0x03
ARMOR_RING_L1, ARMOR_RING_L2, ARMOR_RING_L3     = 0x04, 0x05, 0x06
RED_RING, BLUE_RING, GREEN_RING                 = 0x07, 0x08, 0x09
RED_HOLY_RING, BLUE_HOLY_RING, GREEN_HOLY_RING  = 0x20, 0x1f, 0x1e
RED_LUCK_RING, BLUE_LUCK_RING, GREEN_LUCK_RING  = 0x1d, 0x1b, 0x1a
GOLD_LUCK_RING = 0x1c

CURSED_RING,    DBL_EDGED_RING  = 0x0a, 0x32
WHIMSICAL_RING, PROTECTION_RING = 0x3e, 0x3f
FIST_RING,      EXPERTS_RING    = 0x3d, 0x0b
RANG_RING_L1,   RANG_RING_L2    = 0x0d, 0x29
HEART_RING_L1, HEART_RING_L2    = 0x13, 0x14
LIGHT_RING_L1, LIGHT_RING_L2    = 0x17, 0x18

ENERGY_RING, SPIN_RING, CHARGE_RING, WHISP_RING = 0x31, 0x2f, 0x16, 0x39

RED_JOY_RING, BLUE_JOY_RING, GREEN_JOY_RING, GOLD_JOY_RING   = 0x24, 0x25, 0x27, 0x26
OCTO_RING, MOBLIN_RING, LIKE_LIKE_RING, SUBROSIAN_RING       = 0x2a, 0x2b, 0x2c, 0x2d
FIRST_GEN_RING, GBA_TIME_RING, GBA_NATURE_RING, VICTORY_RING = 0x2e, 0x0e, 0x33, 0x36
SLAYERS_RING, RUPEE_RING, SIGN_RING, HUNDREDTH_RING          = 0x34, 0x35, 0x37, 0x38

# custom/reworked rings
GOLD_RING           = WHIMSICAL_RING
VASUS_RING          = FRIENDSHIP_RING
FAIRYS_RING         = PROTECTION_RING
HASTE_RING          = SNOWSHOE_RING
HIKERS_RING         = QUICKSAND_RING
MYSTIC_SEED_RING    = PEGASUS_RING
CURSE_POWER_RING    = CURSED_RING
CURSE_ARMOR_RING    = DBL_EDGED_RING
ALCHEMY_RING        = GOLD_LUCK_RING

GREEN_COLOR_RING    = RUPEE_RING
RED_COLOR_RING      = SLAYERS_RING
BLUE_COLOR_RING     = HUNDREDTH_RING
GOLD_COLOR_RING     = SIGN_RING
GBOY_COLOR_RING     = WHISP_RING


REPLACE_MAP = dict(
    PLACEHOLDER0            = b'',         # for inserting new code into asm variants
    MUL_A_BY_C              = b'\x9d\x01', # multiplyAByC
    COMPARE_HL_TO_BC        = b'\xd6\x01', # call compareHlToBc
    UPDATE_LINK_SPEED       = b'\xe8\x5c', # @updateLinkSpeed_withParam
    MENU1_CURSOR_POS        = b'\xd1\xcb', # wInventorySubmenu1CursorPos
    MENU_TYPE_RINGS         = b'\x04',
    RING_MENU_TYPE_LIST     = b'\x01',
    W_FRAME_COUNTER         = b'\x00\xcc', # wFrameCounter
    W_BOX_CONTENTS_EXT      = b'\xba\xc5', # wRingBoxContentsExt
    W_BOX_CONTENTS_EXT_MIN_1 = b'\xb9\xc5', # wRingBoxContentsExt-1
    RING_LIST_CURSOR        = b'\xb4\xcb', # ringListCursorIndex
    SELECTED_RING           = b'\xb3\xcb', # selectedRing
    RING_MENU_PAGE          = b'\xb6\xcb', # ringMenuPage
    OPENED_MENU_TYPE        = b'\xcb\xcb', # wOpenedMenuType
    MENU_LOAD_STATE         = b'\xcc\xcb', # wMenuLoadState
    MENU_ACTIVE_STATE       = b'\xcd\xcb', # wMenuActiveState
    SUBMENU_STATE           = b'\xce\xcb', # wSubmenuState
    TEXT_DISPLAY_MODE       = b'\xa1\xcb', # wTextDisplayMode
    RING_MENU_MODE          = b'\xd3\xcb', # wRingMenu_mode
    RINGS_OBTAINED          = b'\x16\xc6', # wRingsObtained
    W_SCREEN_OFF_Y          = b'\x08\xcd', # wScreenOffsetY
    W_SCROLL_MODE           = b'\x00\xcd', # wScrollMode
    W_PALETTE_THREAD_MODE   = b'\xab\xc4', # wPaletteThread_mode
    W_ACTIVE_LANGUAGE       = b'\x2a\xc6', # wActiveLanguage
    CHECK_FLAG              = b'\x05\x02', # checkFlag
    SET_FLAG                = b'\x0e\x02', # setFlag
    UNSET_FLAG              = b'\x18\x02', # unsetFlag
    MULTIPLY_A_BY_16        = b'\xac\x01', # multiplyABy16
    ITEM_TRY_BREAK_TILE     = b'\x36\x2b', # itemTryToBreakTile
    LINK_OBJECT_ADDR        = b'\x00\xd0', # w1Link
    LINK_DIRECTION          = b'\x08\xd0', # w1Link.direction
    LINK_SPEED_Z            = b'\x14\xd0', # w1Link.speedZ
    LINK_INVINC_COUNTER     = b'\x2b\xd0', # w1Link.invincibilityCounter
    WEAPON_ITEM_STATE       = b'\x04\xd6', # w1WeaponItem.state
    PARENT_ITEM_VAR3A       = b'\x3a\xd2', # w1ParentItem2.var3a
    W_TEXT_INDEX_L          = b'\xa2\xcb', # wTextIndexL
    W_TEXT_INDEX_H          = b'\xa3\xcb', # wTextIndexH
    W_KEYS_PRESSED          = b'\x81\xc4', # wKeysPressed
    W_THREAD_STATE_BUFFER_L = b'\xe0',     # wThreadStateBuffer
    W_THREAD_STATE_BUFFER_H = b'\xc2',     # wThreadStateBuffer+1
    INTER_BANK_CALL         = b'\x8a\x00', # interBankCall
    ENEMY_CODE_TABLE_B1     = b'\x2f',     # >enemyCodeTable
    SET_ROM_BANK            = b'\xea\x22\x22',
    RESET_GAME              = b'\x69\x01',
    ITEM_SWORD_BEAM         = b'\x27',
    TREASURE_POTION         = b'\x2f',
    H_GAMEBOY_TYPE          = b'\x96',
    H_ROM_BANK              = b'\x97',
    GAMEBOY_TYPE_GBC        = b'\x01',
    GAMEBOY_TYPE_GBA        = b'\xff',
    DISP_RING_NUM_COMP      = b'\xbf\xcb', # displayedRingNumberComparator
    W_RING_BOX_CURSOR_IDX   = b'\xbd\xcb', # ringBoxCursorIndex
    W4_SUBSCREEN_TEXT_INDICES = b'\xe0\xd3', # w4SubscreenTextIndices
    W4_SUBSCREEN_TEXT_INDICES_PLUS_F = b'\xef\xd3', # w4SubscreenTextIndices+$f
    FIRST_SIDESCROLL_GROUP  = 6,
    )
AGES_REPLACE_MAP = dict(
    GET_RANDOM_NUMBER       = b'\x3e\x04', # getRandomNumber
    PLAY_SOUND              = b'\x98\x0c', # playSound
    SET_MUSIC_VOLUME        = b'\xad\x0c', # setMusicVolume
    CLEAR_MEMORY            = b'\x6f\x04', # clearMemory
    FILL_MEMORY             = b'\x70\x04', # fillMemory
    GET_BOX_CAPACITY        = b'\xf5\x5c', # getRingBoxCapacity
    EQUIP_SPRITE0           = b'\x55\x5b', # @sprite
    EQUIP_SPRITE1           = b'\xbf\x71', # @sprite
    ADD_TO_OAM              = b'\x61\x0d', # @addSpritesToOam_withOffset
    READ_W7_TEXT_TABLE_BYTE = b'\x5d\x19', # readByteFromW7TextTableBank
    LINK_OFFSETS            = b'\xfa\x61', # @linkOffsets
    RING_IS_IN_BOX          = b'\x56\x70', # ringMenu_checkRingIsInBox
    GET_RING_SPRITE_OFF     = b'\xc4\x71', # ringMenu_getSpriteOffsetForRingBoxPosition
    OPEN_MENU               = b'\xb0\x1a', # openMenu
    CLOSE_MENU              = b'\xba\x8f', # closeMenu
    FAST_FADEOUT_WHITE      = b'\x63\x32', # fastFadeoutToWhite
    FAST_FADEIN_WHITE       = b'\x90\x32', # fastFadeinFromWhite
    FADEOUT_WHITE           = b'\x6c\x32', # fadeoutToWhite
    FADEIN_WHITE            = b'\x99\x32', # fadeinFromWhite
    SAVE_GFX_ON_MENU        = b'\xa8\x1a', # saveGraphicsOnEnterMenu
    RELOAD_GFX_ON_MENU      = b'\xac\x1a', # reloadGraphicsOnExitMenu
    CP_ACTIVE_RING0         = b'\xb0\x23', # cpActiveRing
    W_GASHA_KILL_COUNTERS   = b'\x4f\xc6', # wGashaSpotKillCounters
    W_ACTIVE_RING           = b'\xcb\xc6', # wActiveRing
    W_LINK_HEALTH           = b'\xaa\xc6', # wLinkHealth
    W_LINK_HEALTH_B0        = b'\xaa',     # <wLinkHealth
    W_GASHA_SPOT_FLAGS      = b'\x4c\xc6', # wGashaSpotFlags
    W_LINK_MAX_HEALTH       = b'\xab\xc6', # wLinkMaxHealth
    W_NUM_RUPEES            = b'\xad\xc6', # wNumRupees
    W_NUM_RUPEES_B0         = b'\xad',     # <wNumRupees
    W_SHIELD_LEVEL          = b'\xaf\xc6', # wShieldLevel
    W_NUM_BOMBS             = b'\xb0\xc6', # wNumBombs
    W_SWORD_LEVEL           = b'\xb2\xc6', # wSwordLevel
    W_NUM_BOMBCHUS          = b'\xb3\xc6', # wNumBombchus
    W_SEED_SATCHEL_LEVEL    = b'\xb4\xc6', # wSeedSatchelLevel
    W_NUM_EMBER_SEEDS       = b'\xb9\xc6', # wNumEmberSeeds
    W_NUM_SCENT_SEEDS       = b'\xba\xc6', # wNumScentSeeds
    W_NUM_PEGASUS_SEEDS     = b'\xbb\xc6', # wNumPegasusSeeds
    W_NUM_GALE_SEEDS        = b'\xbc\xc6', # wNumGaleSeeds
    W_NUM_MYSTERY_SEEDS     = b'\xbd\xc6', # wNumMysterySeeds
    W_BOX_CONTENTS_PLUS_5_H = b'\xcb',     # wRingBoxContents+5
    W_BOX_CONTENTS_PLUS_4   = b'\xca\xc6', # wRingBoxContents+4
    W_BOX_CONTENTS_MIN_1    = b'\xc5\xc6', # wRingBoxContents-1
    W_BOX_CONTENTS          = b'\xc6\xc6', # wRingBoxContents
    W_BOX_LEVEL             = b'\xcc\xc6', # wRingBoxLevel
    W_DISP_RUPEES           = b'\xe5\xcb', # wDisplayedRupees
    W_DISP_RUPEES_PLUS      = b'\xe6\xcb', # wDisplayedRupees+1
    W_DISP_RUPEES_PLUS_B0   = b'\xe6',     # <wDisplayedRupees+1
    W_ACTIVE_GROUP          = b'\x2d\xcc', # wActiveGroup
    W_TILESET_FLAGS         = b'\x34\xcc', # wTilesetFlags
    W_LINK_GRAB_STATE       = b'\x5a\xcc', # wLinkGrabState
    W_LINK_IN_AIR           = b'\x5c\xcc', # wLinkInAir
    W_LINK_SWIMMING_STATE   = b'\x5d\xcc', # wLinkSwimmingState
    W_FORCE_LINK_PUSH_ANIM  = b'\x66\xcc', # wForceLinkPushAnimation
    W_USING_SHIELD          = b'\x6f\xcc', # wUsingShield
    W_DISABLED_OBJECTS      = b'\x8a\xcc', # wDisabledObjects
    W_IN_SHOP               = b'\xd3\xcc', # wInShop
    W_SEED_SHOOTER_IN_USE   = b'\xda\xcc', # wIsSeedShooterInUse
    BOX_SIZE                = b'\x01\x5d', # ringBoxCapacities
    RING_POS_LIST           = b'\xd2\x72', # ringPositionList
    GET_RING_TILES          = b'\xfe\x72', # getRingTiles
    DRAW_RING0              = b'\xc3\x72', # drawRing
    INVENTORY_B             = b'\x88',     # wInventoryB
    GET_FREE_ITEM_SLOT      = b'\x16\x54', # getFreeItemSlotWithObjectCap
    CHECK_HAVE_TREASURE     = b'\x48\x17', # checkTreasureObtained
    GIVE_TREASURE           = b'\x33\x17', # giveTreasure
    GET_RANDOM_TIERED_RING  = b'\xe0\x17', # getRandomRingOfGivenTier
    NUDGE_ANGLE_TOWARDS     = b'\xd4\x1f', # objectNudgeAngleTowards
    ITEM_DEC_COUNTER1       = b'\xd6\x23', # itemDecCounter1
    RANG_UPDATE_ANIM        = b'\x70',     # updateSpeedAndAnimation
    SWORD_TRY_BREAK_TILE    = b'\x9d\x61', # tryBreakTileWithSword
    PARENT_CHECK_BUTTON     = b'\x96\x54', # parentItemCheckButtonPressed
    ITEM_DISABLE_LINK_MOVE  = b'\x5d\x54', # itemDisableLinkMovement
    SWORD_DELETE_SELF       = b'\x00\x4d', # swordParent.deleteSelf
    LINK_FORCED_STATE       = b'\x4f\xcc', # linkForcedState
    CREATE_SWORD_BEAM       = b'\x56\x4d', # createSwordBeam
    TRIGGER_SWORD_POKE      = b'\x23\x4d', # @triggerSwordPoke
    EXPERT_TRY_BREAK_TILE   = b'\x8a\x61', # tryBreakTileWithExpertsRing
    OBJECT_COLL_TBL         = b'\x0a\x6d', # objectCollisionTable
    OBJ_CREATE_INTERAC      = b'\xc5\x24', # objectCreateInteraction
    UPDATE_INTERAC          = b'\x62\x3b', # updateInteraction
    FEATHER_DELETE_PARENT   = b'\x33\xfa', # @deleteParent
    PARENT_ITEM_CHECK_AB    = b'\x0f',     # @parentItem.checkAB
    UPDATE_PARENT_ITEMS     = b'\x19\xfa', # @parentItem.updateParentItems
    PULL_LINK_INTO_HOLE     = b'\x4b\x5f', # pullLinkIntoHole
    CHECK_PEGASUS_COUNTER   = b'\xe8\x2b', # checkPegasusSeedCounter
    SWORD_LEVEL_DATA_MIN2   = b'\xf9\x5e', # @swordLevelData-2
    SWORD_DAMAGE_MODS       = b'\x81\x62', # @swordDamageModifiers
    POWER_RING_MODS         = b'\xae\x46', # @ringDamageModifierTable
    ITEM_CREATE_CHILD       = b'\xe3\x53', # itemCreateChildWithID
    SEED_INIT_STATE3        = b'\x82\x4e', # @initState3
    ITEM_ANIMATE            = b'\xd9\x49', # itemAnimate
    GET_RUPEE_VALUE         = b'\x81\x17', # getRupeeValue
    CLEAR_PARENT_ITEM       = b'\x42\x4a', # clearParentItem
    ITEM_UPDATE_ANGLE       = b'\xf0\x2c', # itemUpdateAngle
    RING_TO_XFORM_ID        = b'\x5d\x46', # @ringToID
    LOOKUP_KEY              = b'\x06\x1e', # @lookupKey
    W_DISABLE_RING_XFORMS   = b'\x56\xcc', # wDisableRingTransformations
    W_MENU_DISABLED         = b'\x02\xcc', # wMenuDisabled
    SPECOBJ_GFX_TABLE       = b'\x51\x44', # specialObjectGraphicsTable
    UPDATE_LINK_DAMAGED     = b'\x68\x42', # updateLinkDamageTaken
    RET_IF_TEXT_IS_ACTIVE   = b'\x59\x18', # retIfTextIsActive
    SPECOBJ_OAM_DATA        = b'\x0d\x42', # @data
    H_CAMERA_Y              = b'\xaa\xff', # hCameraY
    ENEMY_CODE_TABLE_B0     = b'\x34',     # <enemyCodeTable
    OBJ_ADD_TO_GRAB_BUFFER  = b'\x2e\x2c', # objectAddToGrabbableObjectBuffer
    GRABBABLE_OBJ_BUFFER    = b'\x74\xcc', # wGrabbableObjectBuffer
    BOMB_RESET_ANIM_AND_VIS = b'\xf0\x55', # bombResetAnimationAndSetVisiblec1
    INIT_BOMB_EXPLOSION     = b'\x9f\x55', # itemInitializeBombExplosion
    ITEM_LOAD_ANIM_INC_STATE= b'\x78\x53', # parentItemLoadAnimationAndIncState
    FIND_ITEM_WITH_ID       = b'\xb9\x22', # findItemWithID
    CP_RUPEE_VALUE          = b'\x65\x17', # cpRupeeValue
    REMOVE_RUPEE_VALUE      = b'\x78\x17', # removeRupeeValue
    TRY_PICKUP_BOMBS        = b'\xad\x50', # tryPickupBombs
    BEGIN_PICKUP_SET_ANIM   = b'\x88\x51', # beginPickupAndSetAnimation
    TRY_BREAK_TILE          = b'\xf6\x2b', # tryToBreakTile
    BOMB_OFFSET_DATA        = b'\x82\x56', # @bombOffsetData
    GASHA_TREASURES         = b'\x00\x47', # gashaTreasures
    H_OAM_TAIL              = b'\x9f',     # hOamTail
    H_ACTIVE_THREAD         = b'\x9e',     # hActiveThread
    RING_LIST_CURSOR_SPRITE = b'\x9e\x71', # @ringListCursorSprite
    FILL_TILEMAP_RECTANGLE  = b'\x08\x5d', # fillRectangleInTilemap
    W_RING_BOX_CONTENTS_L   = b'\xc6',     # wRingBoxContents
    RING_POS_MIN_1          = b'\x31\x5c', # ringPositions
    RING_ROW_POS_MAP        = b'\xf2\x58', # ringBoxRowPositionMappings
    SUBMENU1_CURSOR_OFFS    = b'\xb5\x59',
    SHOW_ITEM_TEXT1         = b'\x38\x55', # showItemText1
    RING_BOX_CURSOR         = b'\xea\x71', # @ringBoxCursor
    RELOAD_INV_MENU_GFX     = b'\xb2\x55', # reloadInvMenuGfx
    W_GASHA_MATURITY        = b'\x5f\xc6', # wGashaMaturity
    W_GASHA_MATURITY_H      = b'\x60\xc6', # wGashaMaturity+1
    OBJ_CLINK_INTERAC       = b'\x81\x4b', # objectCreateClinkInteraction
    RANG_UPDATE_SPEED_ANIM  = b'\xc6\x57', # @updateSpeedAndAnimation
    OBJ_GET_REL_OBJ1_VAR    = b'\x60\x21', # objectGetRelatedObject1Var
    W_ACTIVE_COLLISIONS     = b'\x33\xcc', # wActiveCollisions
    )
SEAS_REPLACE_MAP = dict(
    GET_RANDOM_NUMBER       = b'\x1a\x04', # getRandomNumber
    PLAY_SOUND              = b'\x74\x0c', # playSound
    SET_MUSIC_VOLUME        = b'\x89\x0c', # setMusicVolume
    CLEAR_MEMORY            = b'\x4b\x04', # clearMemory
    FILL_MEMORY             = b'\x4c\x04', # fillMemory
    GET_BOX_CAPACITY        = b'\xa8\x5c', # getRingBoxCapacity
    EQUIP_SPRITE0           = b'\xde\x5a', # @sprite
    EQUIP_SPRITE1           = b'\xf0\x70', # @sprite
    ADD_TO_OAM              = b'\x3d\x0d', # @addSpritesToOam_withOffset
    READ_W7_TEXT_TABLE_BYTE = b'\x36\x19', # readByteFromW7TextTableBank
    LINK_OFFSETS            = b'\x79\x5f', # @linkOffsets
    RING_IS_IN_BOX          = b'\x87\x6f', # ringMenu_checkRingIsInBox
    GET_RING_SPRITE_OFF     = b'\xf5\x70', # ringMenu_getSpriteOffsetForRingBoxPosition
    OPEN_MENU               = b'\x76\x1a', # openMenu
    CLOSE_MENU              = b'\x7b\x8f', # closeMenu
    FAST_FADEOUT_WHITE      = b'\x3b\x31', # fastFadeoutToWhite
    FAST_FADEIN_WHITE       = b'\x68\x32', # fastFadeinFromWhite
    FADEOUT_WHITE           = b'\x44\x31', # fadeoutToWhite
    FADEIN_WHITE            = b'\x71\x32', # fadeinFromWhite
    SAVE_GFX_ON_MENU        = b'\x6e\x1a', # saveGraphicsOnEnterMenu
    RELOAD_GFX_ON_MENU      = b'\x72\x1a', # reloadGraphicsOnExitMenu
    CP_ACTIVE_RING0         = b'\x6b\x23', # cpActiveRing
    W_GASHA_KILL_COUNTERS   = b'\x4c\xc6', # wGashaSpotKillCounters
    W_ACTIVE_RING           = b'\xc5\xc6', # wActiveRing
    W_LINK_HEALTH           = b'\xa2\xc6', # wLinkHealth
    W_LINK_HEALTH_B0        = b'\xa2',     # <wLinkHealth
    W_GASHA_SPOT_FLAGS      = b'\x49\xc6', # wGashaSpotFlags
    W_LINK_MAX_HEALTH       = b'\xa3\xc6', # wLinkMaxHealth
    W_NUM_RUPEES            = b'\xa5\xc6', # wNumRupees
    W_NUM_RUPEES_B0         = b'\xa5',     # <wNumRupees
    W_SHIELD_LEVEL          = b'\xa9\xc6', # wShieldLevel
    W_NUM_BOMBS             = b'\xaa\xc6', # wNumBombs
    W_SWORD_LEVEL           = b'\xac\xc6', # wSwordLevel
    W_NUM_BOMBCHUS          = b'\xad\xc6', # wNumBombchus
    W_SEED_SATCHEL_LEVEL    = b'\xae\xc6', # wSeedSatchelLevel
    W_NUM_EMBER_SEEDS       = b'\xb5\xc6', # wNumEmberSeeds
    W_NUM_SCENT_SEEDS       = b'\xb6\xc6', # wNumScentSeeds
    W_NUM_PEGASUS_SEEDS     = b'\xb7\xc6', # wNumPegasusSeeds
    W_NUM_GALE_SEEDS        = b'\xb8\xc6', # wNumGaleSeeds
    W_NUM_MYSTERY_SEEDS     = b'\xb9\xc6', # wNumMysterySeeds
    W_SLINGSHOT_LEVEL       = b'\xb3\xc6', # wSlingshotLevel
    W_BOX_CONTENTS_PLUS_5_H = b'\xc5',     # wRingBoxContents+5
    W_BOX_CONTENTS_PLUS_4   = b'\xc4\xc6', # wRingBoxContents+4
    W_BOX_CONTENTS_MIN_1    = b'\xbf\xc6', # wRingBoxContents-1
    W_BOX_CONTENTS          = b'\xc0\xc6', # wRingBoxContents
    W_BOX_LEVEL             = b'\xc6\xc6', # wRingBoxLevel
    W_DISP_RUPEES           = b'\xe6\xcb', # wDisplayedRupees
    W_DISP_RUPEES_PLUS      = b'\xe7\xcb', # wDisplayedRupees+1
    W_DISP_RUPEES_PLUS_B0   = b'\xe7',     # <wDisplayedRupees+1
    W_ACTIVE_GROUP          = b'\x49\xcc', # wActiveGroup
    W_TILESET_FLAGS         = b'\x50\xcc', # wTilesetFlags
    W_LINK_GRAB_STATE       = b'\x75\xcc', # wLinkGrabState
    W_LINK_IN_AIR           = b'\x77\xcc', # wLinkInAir
    W_LINK_SWIMMING_STATE   = b'\x78\xcc', # wLinkSwimmingState
    W_FORCE_LINK_PUSH_ANIM  = b'\x81\xcc', # wForceLinkPushAnimation
    W_USING_SHIELD          = b'\x89\xcc', # wUsingShield
    W_DISABLED_OBJECTS      = b'\xa4\xcc', # wDisabledObjects
    W_IN_SHOP               = b'\xea\xcc', # wInShop
    W_SEED_SHOOTER_IN_USE   = b'\xf1\xcc', # wIsSeedShooterInUse
    BOX_SIZE                = b'\xb4\x5c', # ringBoxCapacities
    RING_POS_LIST           = b'\x03\x72', # ringPositionList
    GET_RING_TILES          = b'\x2f\x72', # getRingTiles
    DRAW_RING0              = b'\xf4\x71', # drawRing
    INVENTORY_B             = b'\x80',     # wInventoryB
    GET_FREE_ITEM_SLOT      = b'\x68\x53', # getFreeItemSlotWithObjectCap
    CHECK_HAVE_TREASURE     = b'\x17\x17', # checkTreasureObtained
    GIVE_TREASURE           = b'\x02\x17', # giveTreasure
    GET_RANDOM_TIERED_RING  = b'\xb9\x17', # getRandomRingOfGivenTier
    NUDGE_ANGLE_TOWARDS     = b'\x92\x1f', # objectNudgeAngleTowards
    ITEM_DEC_COUNTER1       = b'\x91\x23', # itemDecCounter1
    RANG_UPDATE_ANIM        = b'\x73',     # updateSpeedAndAnimation
    SWORD_TRY_BREAK_TILE    = b'\x1c\x5f', # tryBreakTileWithSword
    PARENT_CHECK_BUTTON     = b'\xe8\x53', # parentItemCheckButtonPressed
    ITEM_DISABLE_LINK_MOVE  = b'\xaf\x53', # itemDisableLinkMovement
    SWORD_DELETE_SELF       = b'\x17\x4c', # swordParent.deleteSelf
    LINK_FORCED_STATE       = b'\x6a\xcc', # linkForcedState
    CREATE_SWORD_BEAM       = b'\x66\x4c', # createSwordBeam
    TRIGGER_SWORD_POKE      = b'\x3a\x4c', # @triggerSwordPoke
    EXPERT_TRY_BREAK_TILE   = b'\x09\x5f', # tryBreakTileWithExpertsRing
    OBJECT_COLL_TBL         = b'\x90\x6a', # objectCollisionTable
    OBJ_CREATE_INTERAC      = b'\xb1\x24', # objectCreateInteraction
    UPDATE_INTERAC          = b'\x36\x3b', # updateInteraction
    FEATHER_DELETE_PARENT   = b'\x3c\xfa', # @deleteParent
    PARENT_ITEM_CHECK_AB    = b'\x08',     # @parentItem.checkAB
    UPDATE_PARENT_ITEMS     = b'\x12\xfa', # @parentItem.updateParentItems
    PULL_LINK_INTO_HOLE     = b'\xd9\x5d', # pullLinkIntoHole
    CHECK_PEGASUS_COUNTER   = b'\x2f\x2b', # checkPegasusSeedCounter
    SWORD_LEVEL_DATA_MIN2   = b'\x7d\x5c', # @swordLevelData-2
    SWORD_DAMAGE_MODS       = b'\x03\x60', # @swordDamageModifiers
    POWER_RING_MODS         = b'\x8d\x46', # @ringDamageModifierTable
    ITEM_CREATE_CHILD       = b'\x35\x53', # itemCreateChildWithID
    SEED_INIT_STATE3        = b'\x2c\x4e', # @initState3
    ITEM_ANIMATE            = b'\xc1\x49', # itemAnimate
    GET_RUPEE_VALUE         = b'\x5a\x17', # getRupeeValue
    CLEAR_PARENT_ITEM       = b'\xe7\x49', # clearParentItem
    GET_FREE_ITEM_SLOTS     = b'\x83\x53', # getNumFreeItemSlots
    RING_TO_XFORM_ID        = b'\x3c\x46', # @ringToID
    LOOKUP_KEY              = b'\xc4\x1d', # @lookupKey
    W_DISABLE_RING_XFORMS   = b'\x71\xcc', # wDisableRingTransformations
    W_MENU_DISABLED         = b'\x02\xcc', # wMenuDisabled
    SPECOBJ_GFX_TABLE       = b'\x47\x44', # specialObjectGraphicsTable
    UPDATE_LINK_DAMAGED     = b'\x26\x42', # updateLinkDamageTaken
    RET_IF_TEXT_IS_ACTIVE   = b'\x32\x18', # retIfTextIsActive
    SPECOBJ_OAM_DATA        = b'\xcb\x41', # @data
    H_CAMERA_Y              = b'\xa8\xff', # hCameraY
    ENEMY_CODE_TABLE_B0     = b'\x16',     # <enemyCodeTable
    OBJ_ADD_TO_GRAB_BUFFER  = b'\x6e\x2b', # objectAddToGrabbableObjectBuffer
    GRABBABLE_OBJ_BUFFER    = b'\x8e\xcc', # wGrabbableObjectBuffer
    BOMB_RESET_ANIM_AND_VIS = b'\x8d\x54', # bombResetAnimationAndSetVisiblec1
    INIT_BOMB_EXPLOSION     = b'\x3c\x54', # itemInitializeBombExplosion
    ITEM_LOAD_ANIM_INC_STATE= b'\xe2\x52', # parentItemLoadAnimationAndIncState
    FIND_ITEM_WITH_ID       = b'\x74\x22', # findItemWithID
    CP_RUPEE_VALUE          = b'\x39\x17', # cpRupeeValue
    REMOVE_RUPEE_VALUE      = b'\x51\x17', # removeRupeeValue
    TRY_PICKUP_BOMBS        = b'\xed\x4e', # tryPickupBombs
    BEGIN_PICKUP_SET_ANIM   = b'\xd0\x4f', # beginPickupAndSetAnimation
    TRY_BREAK_TILE          = b'\x3d\x2b', # tryToBreakTile
    BOMB_OFFSET_DATA        = b'\x1f\x55', # @bombOffsetData
    GASHA_TREASURES         = b'\x7d\x49', # gashaTreasures
    H_OAM_TAIL              = b'\x9d',     # hOamTail
    H_ACTIVE_THREAD         = b'\x9c',     # hActiveThread
    RING_LIST_CURSOR_SPRITE = b'\xce\x70', # @ringListCursorSprite
    FILL_TILEMAP_RECTANGLE  = b'\xbb\x5c', # fillRectangleInTilemap
    W_RING_BOX_CONTENTS_L   = b'\xc0',     # wRingBoxContents
    RING_POS_MIN_1          = b'\xba\x5b', # @ringPositions
    RING_ROW_POS_MAP        = b'\x9e\x58', # ringBoxRowPositionMappings
    SUBMENU1_CURSOR_OFFS    = b'\x6f\x59',
    SHOW_ITEM_TEXT1         = b'\xfb\x54', # showItemText1
    RING_BOX_CURSOR         = b'\x1b\x71', # @ringBoxCursor
    RELOAD_INV_MENU_GFX     = b'\x7c\x55', # reloadInvMenuGfx
    W_GASHA_MATURITY        = b'\x5c\xc6', # wGashaMaturity
    W_GASHA_MATURITY_H      = b'\x5d\xc6', # wGashaMaturity+1
    OBJ_CLINK_INTERAC       = b'\x69\x4b', # objectCreateClinkInteraction
    RANG_UPDATE_SPEED_ANIM  = b'\x26\x56', # @updateSpeedAndAnimation
    OBJ_GET_REL_OBJ1_VAR    = b'\x1e\x21', # objectGetRelatedObject1Var
    W_ACTIVE_COLLISIONS     = b'\x4f\xcc', # wActiveCollisions
    )

RING_TEXT_SYMBOLS = dict(
    TXT_TERM    = b'\x00',
    TXT_NEWL    = b'\x01',
    TXT_DCT0    = b'\x02',
    TXT_DCT1    = b'\x03',
    TXT_DCT2    = b'\x04',
    TXT_DCT3    = b'\x05',
    TXT_SYMBOL  = b'\x06',
    TXT_JUMP    = b'\x07',
    TXT_TEXTBOX = b'\x08',
    TXT_COLOR   = b'\x09',
    TXT_LINK    = b'\x0a',
    TXT_SETSFX  = b'\x0b',
    TXT_STOP    = b'\x0c\x18',
    TXT_CLOSE   = b'\x0d',
    TXT_PLAYSFX = b'\x0e',
    TXT_CALL    = b'\x0f',
    TXT_CIRCLE  = b'\x10',
    TXT_CLUB    = b'\x11',
    TXT_DIAMOND = b'\x12',
    TXT_SPADE   = b'\x13',
    TXT_HEART   = b'\x14',
    TXT_UP      = b'\x15',
    TXT_DOWN    = b'\x16',
    TXT_LEFT    = b'\x17',
    TXT_RIGHT   = b'\x18',
    TXT_TIMES   = b'\x19',
    TXT_TRIANGLE= b'\x7e',
    TXT_SQUARE  = b'\x7f',

    # NOTE: these aren't actual symbols, but rather are values we'll be
    #       replacing with whatever the user configured the rings to do
    RED_RING_VAL        = b'+100',
    BLUE_RING_VAL       = b' -50',
    GREEN_RING_VAL1     = b' +75',
    GREEN_RING_VAL2     = b' -37',
    CURSE_RING_VAL1     = b'+100',
    CURSE_RING_VAL2     = b'4',

    GOLD_RING_VAL1      = b'+50',
    GOLD_RING_VAL2      = b'+25',
    GOLD_RING_VAL3      = b'4',

    LIGHT_RING_L1_VAL   = b'2',
    LIGHT_RING_L2_VAL   = b'3',
    LUCK_RING_VAL       = b'33',
    HOLY_RING_VAL       = b'+25',
    )

globals().update({name: name for name in set([
    *RING_TEXT_SYMBOLS, *REPLACE_MAP,
    *AGES_REPLACE_MAP, *SEAS_REPLACE_MAP,
    ])})
