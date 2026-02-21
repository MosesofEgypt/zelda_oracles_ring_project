from ..const import RING_TEXT_SYMBOLS, TXT_DCT0, TXT_DCT1, TXT_DCT2, TXT_DCT3, TXT_NEWL
from .const import *
from .. import util
from . import asm, const


def update_mappings(portal_box_level=3, **kw):
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)

    portal_box_level = min(4,  max(0, portal_box_level))
    kw["replace_map"].update(
        PORTAL_BOX_LEVEL = util.to_bytes(portal_box_level)
        )

def prepare_box_size_patches(
        box_size_l1=3, box_size_l2=5, box_size_l3_add=5,
        **kw
        ):
    update_mappings(**kw)
    portal_box_level = kw["replace_map"][PORTAL_BOX_LEVEL][0]

    # I'm capping these to 9 since i don't wanna fuck with rewriting the
    # text to support an additional char for "10"
    box_size_l1     = min(9, max(0, box_size_l1))
    box_size_l2     = min(9, max(0, box_size_l2))
    box_size_l3_add = min(5, max(0, box_size_l3_add))

    offset_l1        = 3*(min(5, box_size_l1) + 1)
    offset_l2        = 3*(min(5, box_size_l2) + 1)

    new_box_capacity0_asm = list(asm.ORIG_BOX_CAPACITY0_ASM)
    new_box_capacity1_asm = list(asm.ORIG_BOX_CAPACITY1_ASM)
    new_box_capacity2_asm = list(asm.ORIG_BOX_CAPACITY2_ASM)
    # okay so, this is a shitload of fuck, but basically we're replacing some
    # of the compressed strings in the ring box descriptions. this means we're
    # dealing with lots of dict indices and messy messy shit. it also means it
    # won't work if anyone has rebuilt the rom with newly compressed strings,
    # but at that point they can handle adding the strings their damn selves.
    if kw.get("is_ages"):
        all_entry       = [RING_TEXT_SYMBOLS[TXT_DCT2], 0xd2]
        _all_entry      = [RING_TEXT_SYMBOLS[TXT_DCT2], 0x51]
        all_newl_entry  = [RING_TEXT_SYMBOLS[TXT_DCT1], 0x8c]
        ring_entry      = [RING_TEXT_SYMBOLS[TXT_DCT0], 0x45]
        rings_entry     = [RING_TEXT_SYMBOLS[TXT_DCT0], 0x29]

        orig_box_capacity3_asm = asm.AGES_ORIG_BOX_CAPACITY3_ASM
        orig_box_capacity4_asm = asm.AGES_ORIG_BOX_CAPACITY4_ASM

        new_box_capacity3_asm = list(orig_box_capacity3_asm)
        new_box_capacity4_asm = list(orig_box_capacity4_asm)

        new_box_capacity4_asm[8]     = b"seed"
        new_box_capacity4_asm[11]   += b" "
        if box_size_l1 < 2:
            new_box_capacity3_asm[17:19] = ring_entry
            new_box_capacity4_asm[ 9:11] = ring_entry
        else:
            new_box_capacity3_asm[17:19] = rings_entry
            new_box_capacity4_asm[ 9:11] = rings_entry

        if box_size_l2 < 2:
            new_box_capacity3_asm[39:41] = ring_entry
            new_box_capacity4_asm[24]    = new_box_capacity4_asm[24][1:]
            new_box_capacity4_asm[24]   += b" "
        else:
            new_box_capacity3_asm[39:41] = rings_entry

        if portal_box_level <= 1:
            new_box_capacity3_asm[16] = bytes([all_entry[0][0],
                                               all_entry[1]])
            new_box_capacity3_asm[19]   += b" "
            new_box_capacity4_asm[5:8]   = [*all_newl_entry, b""]
            new_box_capacity4_asm[11]   += b" "
        else:
            new_box_capacity3_asm[16:17] = b"%i" % box_size_l1
            new_box_capacity3_asm[19]   += b"  "
            new_box_capacity4_asm[5:7]   = [b" ", (b"%i" % box_size_l1)]

        if portal_box_level <= 2:
            new_box_capacity3_asm[37:39] = all_entry
            new_box_capacity4_asm[18:21] = [*all_newl_entry, b""]
            new_box_capacity4_asm[17]    = b"Holds"
            new_box_capacity4_asm[24]   += b"  "
        else:
            new_box_capacity3_asm[37:39] = [(b"%i" % box_size_l2), b" "]
            new_box_capacity4_asm[18:20] = [(b"%i" % box_size_l2), b""]
            new_box_capacity4_asm[24]   += b" "

        if portal_box_level <= 3:
            new_box_capacity3_asm[59:63] = (
                b"all",
                RING_TEXT_SYMBOLS[TXT_DCT0], 0x29,
                b"! "
                )
            new_box_capacity4_asm[30]  = b"Holds all"
            new_box_capacity4_asm[35] += b" "
        else:
            new_box_capacity3_asm[59:63] = (
                b"5",
                RING_TEXT_SYMBOLS[TXT_DCT0], 0x29,
                b"!   "
                )
            new_box_capacity4_asm[30]  = b"Holds %i" % (5+box_size_l3_add)
            new_box_capacity4_asm[35] += b" " * (2 + (box_size_l3_add < 5))
    else:
        all_entry   = [RING_TEXT_SYMBOLS[TXT_DCT3], 0x81]
        all__entry  = [RING_TEXT_SYMBOLS[TXT_DCT2], 0x07]
        ring_entry  = [RING_TEXT_SYMBOLS[TXT_DCT0], 0x2a]
        rings_entry = [RING_TEXT_SYMBOLS[TXT_DCT0], 0x13]

        orig_box_capacity3_asm = asm.SEAS_ORIG_BOX_CAPACITY3_ASM
        orig_box_capacity4_asm = asm.SEAS_ORIG_BOX_CAPACITY4_ASM

        new_box_capacity3_asm = list(orig_box_capacity3_asm)
        new_box_capacity4_asm = list(orig_box_capacity4_asm)

        if box_size_l1 < 2:
            new_box_capacity3_asm[19:21] = ring_entry
            new_box_capacity4_asm[14:16] = ring_entry
        else:
            new_box_capacity3_asm[19:21] = rings_entry
            new_box_capacity4_asm[14:16] = rings_entry
            new_box_capacity4_asm[13]    = b""

        if box_size_l2 < 2:
            new_box_capacity3_asm[42:44] = ring_entry
            new_box_capacity4_asm[34]    = new_box_capacity4_asm[34][1:]
            new_box_capacity4_asm[34]   += b" "
        else:
            new_box_capacity3_asm[42:44] = rings_entry

        if portal_box_level <= 1:
            new_box_capacity3_asm[17:19] = all_entry
            new_box_capacity4_asm[8:11]  = (
                RING_TEXT_SYMBOLS[TXT_NEWL],
                *all__entry,
                )
            new_box_capacity4_asm[13]    = b""
        else:
            new_box_capacity3_asm[17:19] = [b"",  (b"%i" % box_size_l1)]
            new_box_capacity3_asm[21]   += b" "
            new_box_capacity4_asm[8:10]  = [b" ", (b"%i" % box_size_l1)]

        if portal_box_level <= 2:
            new_box_capacity3_asm[40:42] = all_entry
            new_box_capacity4_asm[26:28] = all_entry
        else:
            new_box_capacity3_asm[40:42] = [(b"%i" % box_size_l2), b" "]
            new_box_capacity4_asm[26:28] = [(b"%i" % box_size_l2), b""]
            new_box_capacity4_asm[34]   += b" "

        if new_box_capacity4_asm[13] == b"":
            new_box_capacity4_asm[16]   += b" "

        if portal_box_level <= 3:
            new_box_capacity3_asm[63:67] = (
                b"all",
                RING_TEXT_SYMBOLS[TXT_DCT0], 0x13,
                b"! "
                )
            new_box_capacity4_asm[43]  = b"s all"
            new_box_capacity4_asm[50] += b" "
        else:
            new_box_capacity3_asm[63:67] = (
                b"5",
                RING_TEXT_SYMBOLS[TXT_DCT0], 0x13,
                b"!   "
                )
            new_box_capacity4_asm[43]  = b"s %i" % (5+box_size_l3_add)
            new_box_capacity4_asm[50] += b" " * (2 + (box_size_l3_add < 5))

    new_box_capacity0_asm[6]  = box_size_l1
    new_box_capacity1_asm[7]  = new_box_capacity1_asm[5] + offset_l1
    new_box_capacity1_asm[8]  = 3*(5 - min(4, box_size_l1))
    new_box_capacity2_asm[1]  = 1 + offset_l1

    new_box_capacity0_asm[7]  = box_size_l2
    new_box_capacity1_asm[9]  = new_box_capacity1_asm[5] + offset_l2
    new_box_capacity1_asm[10] = 3*(5 - min(4, box_size_l2))
    new_box_capacity2_asm[7]  = 1 + offset_l2

    new_box_capacity0_asm[-1]  = 5 + box_size_l3_add

    patch_data = [
        [BOX_CAPACITY4, new_box_capacity4_asm, orig_box_capacity4_asm],
        [BOX_CAPACITY3, new_box_capacity3_asm, orig_box_capacity3_asm],
        [BOX_CAPACITY2, new_box_capacity2_asm, asm.ORIG_BOX_CAPACITY2_ASM],
        [BOX_CAPACITY1, new_box_capacity1_asm, asm.ORIG_BOX_CAPACITY1_ASM],
        [BOX_CAPACITY0, new_box_capacity0_asm, asm.ORIG_BOX_CAPACITY0_ASM],
        ]
    return [util.alloc_patch(*args, **kw) for args in patch_data]

def prepare_ring_list_reorg_patches(**kw):
    update_mappings(**kw)
    patch_data = [
        [RING_MAP_TABLE,           asm.RING_MAP_TABLE_ASM],
        [GET_SELECTED_RING1,       asm.GET_SELECTED_RING1_ASM],
        [DRAW_RING1,               asm.DRAW_RING1_ASM],
        [DRAW_RING_BOX1,           asm.DRAW_RING_BOX1_ASM],
        [IS_RING_IN_BOX1,          asm.IS_RING_IN_BOX1_ASM],
        [SEL_RING_FROM_LIST1,      asm.SEL_RING_FROM_LIST1_ASM],
        [SHOULD_DRAW_RING1,        asm.SHOULD_DRAW_RING1_ASM],
        [GET_RING_BOX_SPRITE_OFF1, asm.GET_RING_BOX_SPRITE_OFF1_ASM],
        [EQUIP_RING1,              asm.EQUIP_RING1_ASM],
        [DRAW_INV_RING_BOX1,       asm.DRAW_INV_RING_BOX1_ASM],
        [DRAW_RING_BOX_CURSOR1,    asm.DRAW_RING_BOX_CURSOR1_ASM],
        [DRAW_RING_BOX,            asm.NEW_DRAW_RING_BOX_ASM,             asm.ORIG_DRAW_RING_BOX_ASM],
        [RING_BOX_CURSOR_MOVED1,   asm.RING_BOX_CURSOR_MOVED1_ASM],
        [INV_RING_BOX_CURSOR_MOVED1,asm.INV_RING_BOX_CURSOR_MOVED1_ASM],
        [SUBMENU1_DRAW_CURSOR1,    asm.SUBMENU1_DRAW_CURSOR1_ASM],
        [DRAW_EQUIP1,              asm.DRAW_EQUIP1_ASM],
        [DRAW_RING_BOX_CURSOR,     asm.NEW_DRAW_RING_BOX_CURSOR_ASM,      asm.ORIG_DRAW_RING_BOX_CURSOR_ASM],
        [SUBSCREEN1_MAIN,          asm.NEW_SUBSCREEN1_MAIN_ASM,           asm.ORIG_SUBSCREEN1_MAIN_ASM],
        [SUBMENU1_DRAW_CURSOR,     asm.NEW_SUBMENU1_DRAW_CURSOR_ASM,      asm.ORIG_SUBMENU1_DRAW_CURSOR_ASM],
        [DRAW_INV_RING_BOX,        asm.NEW_DRAW_INV_RING_BOX_ASM,         asm.ORIG_DRAW_INV_RING_BOX_ASM],
        [INV_RING_BOX_CURSOR_MOVED,asm.NEW_INV_RING_BOX_CURSOR_MOVED_ASM, asm.ORIG_INV_RING_BOX_CURSOR_MOVED_ASM],
        [RING_BOX_CURSOR_MOVED,    asm.NEW_RING_BOX_CURSOR_MOVED_ASM,     asm.ORIG_RING_BOX_CURSOR_MOVED_ASM],
        [SEL_RING_FROM_LIST,       asm.NEW_SEL_RING_FROM_LIST_ASM,        asm.ORIG_SEL_RING_FROM_LIST_ASM],
        [DISP_RING_BOX_TEXT,       asm.NEW_DISP_RING_BOX_TEXT_ASM,        asm.ORIG_DISP_RING_BOX_TEXT_ASM],
        [IS_RING_IN_BOX,           asm.NEW_IS_RING_IN_BOX_ASM,            asm.ORIG_IS_RING_IN_BOX_ASM],
        [GET_RING_BOX_SPRITE_OFF,  asm.NEW_GET_RING_BOX_SPRITE_OFF_ASM,   asm.ORIG_GET_RING_BOX_SPRITE_OFF_ASM],
        [SHOULD_DRAW_RING0,        asm.NEW_SHOULD_DRAW_RING0_ASM,         asm.ORIG_SHOULD_DRAW_RING0_ASM],
        [DRAW_RING0,               asm.NEW_DRAW_RING0_ASM,                asm.ORIG_DRAW_RING0_ASM],
        [SET_SELECTED_RING,        asm.NEW_SET_SELECTED_RING_ASM,         asm.ORIG_SET_SELECTED_RING_ASM],
        [DRAW_CARRIED,             asm.NEW_DRAW_CARRIED_ASM,              asm.ORIG_DRAW_CARRIED_ASM],
        [EQUIP_RING,               asm.NEW_EQUIP_RING_ASM,                asm.ORIG_EQUIP_RING_ASM],
        [DRAW_EQUIP0,              asm.NEW_DRAW_EQUIP0_ASM,               asm.ORIG_DRAW_EQUIP0_ASM],
        [DRAW_EQUIP2,              asm.NEW_DRAW_EQUIP2_ASM,               asm.ORIG_DRAW_EQUIP2_ASM],
        ]
    return [util.alloc_patch(*args, **kw) for args in patch_data]

def prepare_box_menu_patches(**kw):
    update_mappings(**kw)
    patch_data = [
        [OPEN_MENU1,     asm.OPEN_MENU1_ASM],
        [OPEN_MENU0,     asm.NEW_OPEN_MENU0_ASM, asm.ORIG_OPEN_MENU0_ASM],
        [RING_BOX_MENU1, asm.RING_BOX_MENU1_ASM],
        [RING_BOX_MENU0, asm.NEW_RING_BOX_MENU0_ASM, asm.ORIG_RING_BOX_MENU0_ASM],
        ]
    return [util.alloc_patch(*args, **kw) for args in patch_data]
