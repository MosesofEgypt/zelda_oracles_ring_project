from .const import *
from .. import util
from .util import read_ptr16, read_ptr24, compress_ring_text, read_text_dicts
from . import asm, const


def prepare_ring_text_patches(**kw):
    rom_file = kw["rom_file"]
    ring_text_data, ring_off_table = compress_ring_text(
        read_text_dicts(**kw), kw.get("text_overrides", {})
        )

    text_tbl_off    = 0x74000 if kw.get("is_ages") else 0x71c00
    text_base2_off  = 0xfcfcb if kw.get("is_ages") else 0xfcffa
    text_tbl_off    = 0xfcfe3 if kw.get("is_ages") else 0xfd012
    max_text_size   =    1400 if kw.get("is_ages") else 1423

    text_base2          = read_ptr24(rom_file, text_base2_off)
    text_table          = read_ptr24(rom_file, text_tbl_off, True)
    ring_ptrs_group_off = text_table + read_ptr16(
        rom_file, text_table + (RING_TEXT_GROUP + 4)*2
        )
    text_ptrs_off = ring_ptrs_group_off + (RING_TEXT_NAMES_INDEX)*2
    ring_text_off = text_base2 + read_ptr16(rom_file, text_ptrs_off)

    new_ptrs = [ring_text_off + off - text_base2
                for _, off in ring_off_table]
    ptrs_data = bytes(
        (new_ptrs[i//2] >> 8) if i%2 else (new_ptrs[i//2] & 0xFF)
        for i in range(len(new_ptrs)*2) # x2 for each byte
        )

    text_ptrs_data, snips_ptrs_data = ptrs_data[:256], ptrs_data[256:]

    patch_data  = []

    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    if len(ring_text_data) > max_text_size:
        print("\tFailure preparing ring text update.\n"
              "\t\tPatch data is %i bytes too large to fit." %
              (len(ring_text_data) - max_text_size))
    else:
        patch_data.extend([util.alloc_patch(*args, **kw) for args in (
            [TEXT_SNIPS2, snips_ptrs_data],
            [TEXT_SNIPS1, asm.TEXT_SNIPS1_ASM],
            [TEXT_SNIPS0, asm.NEW_TEXT_SNIPS0_ASM, asm.ORIG_TEXT_SNIPS0_ASM],
            )])
        patch_data.extend([
            ["RING_TEXT_PTRS", None, text_ptrs_data, text_ptrs_off],
            ["RING_TEXT",      None, ring_text_data, ring_text_off],
            ])

    return patch_data
