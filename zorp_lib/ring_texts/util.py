from ..const import BANK_SIZE, TXT_UP, TXT_TERM, TXT_JUMP, TXT_CALL,\
     RING_TEXT_SYMBOLS
from .const import *

def read_ptr16(rom, off):
    rom.seek(off)
    b0, b1 = rom.read(2)
    return b0 | (b1<<8)

def read_ptr24(rom, off, reverse=False):
    rom.seek(off)
    b0, b1, b2 = rom.read(3)
    return BANK_SIZE*(b2 if reverse else b0) + (
        ((b0|(b1<<8) if reverse else (b1|(b2<<8))) & (BANK_SIZE-1))
        )

def replace_text_symbols(text, symbols):
    data, i = "", 0
    while True:
        start = text.find("{{", i)
        if start < 0:
            break
        end = text.find("}}", start)
        data += text[i: start]
        data += symbols[text[start+2: end]].decode(
            encoding='latin-1'
            )
        i = end + 2
    data += text[i:]
    return data

def replace_text_snips(text, snips, symbols):
    data, i = "", 0
    call_opcode = symbols[TXT_CALL].decode("latin-1")
    jump_opcode = symbols[TXT_JUMP].decode("latin-1")
    while True:
        start = text.find("{", i)
        if start < 0:
            break
        end     = text.find("}", start)
        snip_id = snips[text[start+1: end]]['id']
        data   += text[i: start]
        i       = end + 1
        opcode  = (jump_opcode if i+1 == len(text) else call_opcode)
        data   += "%s%s" % (opcode, bytes([snip_id]).decode('latin-1'))
        if i+1 == len(text):
            i += 1

    data += text[i:]
    return data

def compress_text_item(text, text_dict, symbols):
    comp_text, i = b"", 0
    while i < len(text):
        curr_dict_item = None
        curr_found_len = 0

        curr_dict = text_dict
        for j, c in enumerate(text[i:]):
            if c not in curr_dict:
                break

            curr_dict = curr_dict[c]
            if None in curr_dict:
                curr_dict_item = curr_dict[None]
                curr_found_len = j+1

        if not curr_found_len:
            curr_dict_item = text[i].encode('latin-1')
            curr_found_len = 1
            
        comp_text += curr_dict_item
        i += curr_found_len
        if i == len(text) and comp_text[-1] != 0 and comp_text[-2] != 7:
            comp_text += symbols[TXT_TERM]

    return comp_text


def read_text_dict(rom_file, dict_num, is_ages, text_dict=None):
    text_dict       = {} if text_dict is None else text_dict
    dict_num        = max(0, min(3, dict_num))
    text_base1_off  = 0xfcfb3 if is_ages else 0xfcfe2
    text_tbl_off    = 0xfcfe3 if is_ages else 0xfd012

    text_base1 = read_ptr24(rom_file, text_base1_off)
    text_table = read_ptr24(rom_file, text_tbl_off, True)

    dict_ptr   = text_table + read_ptr16(rom_file, text_table + 2*dict_num)
    
    for i in range(256):
        # need to create tree branching at each char
        curr_dict = text_dict
        str_ptr0 = text_base1 + read_ptr16(rom_file, dict_ptr + 2*i)
        str_ptr1 = text_base1 + read_ptr16(rom_file, dict_ptr + 2*(i+1))
        rom_file.seek(str_ptr0)
        text = rom_file.read(str_ptr1-str_ptr0)
        while text.endswith(b'\x00\x00'):
            text = text[:-1]

        if text.endswith(b'\x00') and len(text) > 1:
            if text[-2] not in range(2, 16):
                text = text[:-1]

        for c in text:
            next_dict = curr_dict.setdefault(bytes([c]).decode("latin-1"), {})
            curr_dict = next_dict

        curr_dict[None] = bytes([2+dict_num, i])

    return text_dict


def read_text_dicts(rom_file, is_ages, **kw):
    text_dict = {}
    for i in range(4):
        read_text_dict(rom_file, i, is_ages, text_dict)
    return text_dict

def compress_ring_text(text_dict, text_overrides={}):
    symbols = dict(RING_TEXT_SYMBOLS)
    symbols.update(text_overrides)

    end = symbols[TXT_TERM].decode("latin-1")
    # compress the snips first
    snips = {
        snip_data['id']: dict(id=i+RING_TEXT_SNIPS_INDEX, data='')
        for i, snip_data in enumerate(RING_TEXT_SNIPS)
        }
    name_items, desc_items, snip_items = [], [], []
    for snip_data in RING_TEXT_SNIPS:
        text = replace_text_symbols(snip_data['text']+end, symbols)
        text = replace_text_snips(text, snips, symbols)
        snips[snip_data['id']]['data'] += text
        snip_items.append(text)

    # add the ring name and descriptions to the snips so
    # they can be referenced by other names/descriptions
    snips.update({
        f"{i}_NAME": dict(id=RING_TEXT_NAMES_INDEX+i)
        for i, ring_data in enumerate(RING_TEXT_STRINGS)
        })
    snips.update({
        f"{i}_DESC": dict(id=RING_TEXT_DESCS_INDEX+i)
        for i, ring_data in enumerate(RING_TEXT_STRINGS)
        })

    for ring_data in RING_TEXT_STRINGS:
        name = replace_text_symbols(ring_data['name']+end, symbols)
        name = replace_text_snips(name, snips, symbols)

        desc = replace_text_symbols(ring_data['desc']+end, symbols)
        desc = replace_text_snips(desc, snips, symbols)
        name_items.append(name)
        desc_items.append(desc)

    text_to_index  = {}
    for base, lst in (
            [RING_TEXT_SNIPS_INDEX, snip_items],
            [RING_TEXT_NAMES_INDEX, name_items],
            [RING_TEXT_NAMES_INDEX, desc_items]
            ):
        for i in range(len(lst)):
            text = lst[i]
            if text in text_to_index:
                lst[i] = text_to_index[text]
            else:
                lst[i] = compress_text_item(text, text_dict, symbols)
                text_to_index[text] = base + i

    text_blob = b''
    off_table = []
    # remove duplicates and concatenate
    for base_index, texts in (
            [RING_TEXT_NAMES_INDEX, name_items],
            [RING_TEXT_DESCS_INDEX, desc_items],
            [RING_TEXT_SNIPS_INDEX, snip_items]
            ):
        for i, text_data in enumerate(texts):
            if isinstance(text_data, int):
                off_table.append([base_index + i, off_table[text_data][1]])
            else:
                off_table.append([base_index + i, len(text_blob)])
                text_blob += text_data

    return text_blob, off_table
