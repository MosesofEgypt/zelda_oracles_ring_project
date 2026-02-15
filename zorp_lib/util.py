import hashlib
from . import const, opcodes

def to_bytes(val, size=None):
    return int.to_bytes(
        val, signed=(val<0), byteorder='little', length=(
            (1+(val not in range(-0x8000, 0x10000)))
            if size is None else size
            ),
        )

def val_to_str(val, max_len=3, percent=True, pad=True):
    '''
    Converts an int to a byte string to be substituted into the game text.
    '''
    string = b"%i" % int(abs(val)*(100 if percent else 1))
    prefix = (
        (b" "*(max_len - len(string)) if pad else b"") +
        (b""  if not percent else
         b"+" if val > 0 else
         b"-")
        )
    return prefix + string

def pad_for_bank(size, bank, is_ages=True):
    '''
    Returns a size-length string of pad bytes.
    NOTE: Ages always uses 0x00 as the padding char, while
          Seasons increments it to match the bank number.
    '''
    return [bytes([0 if is_ages else bank])*size]

def pad_for_asm(patch_parts, patch_name, is_ages=False,
                replace_map=None, patch_banks=None,
                ):
    '''
    Returns a string of pad bytes as long as the serialized patch.
    '''
    bank    = patch_banks[patch_name]
    data    = serialize_patch(patch_parts, replace_map)
    return pad_for_bank(len(data), bank, is_ages)

def clear_rom_garbage(
        rom_file, ages_garbage_map=(), seas_garbage_map=(),
        is_ages=False, verify=True, **kwargs
        ):
    '''
    Searches for sections of garbage data and replaces them with padding.
    '''
    garbage_dct = ages_garbage_map if is_ages else seas_garbage_map
    for bank in sorted(garbage_dct):
        for info in garbage_dct[bank]:
            size  = info.get("size", len(info.get("data", [])))
            start = bank*const.BANK_SIZE + info["start"]

            status, err = "Success", ""
            clear_data = b'\x00'*size
            if verify:
                rom_file.seek(start)
                clear_md5 = hashlib.md5(clear_data).hexdigest()
                good_md5  = info.get(
                    "md5", hashlib.md5(info.get("data", b'')).hexdigest()
                    )
                file_md5  = hashlib.md5(rom_file.read(size)).hexdigest()
                if clear_md5 == file_md5:
                    status = "Skipped"
                elif file_md5 != good_md5:
                    err = "\n\t\tMD5 checksum mismatch(%s vs %s)" % (
                        good_md5, file_md5
                        )
                    status = "Failure" 

            print("\t%s clearing garbage data(bank: %02x, offset: 0x%04x, bytes: %i)%s"%
                  (status, bank, info["start"], size, err))

            if status == "Success":
                rom_file.seek(start)
                rom_file.write(clear_data)


def update_patch_banks(module, patch_banks, is_ages=False, **kw):
    '''
    Updates patch_banks with values defined in the provided module.
    '''
    for name, include in ([
            ["PATCH_BANKS",      True],
            ["AGES_PATCH_BANKS", is_ages],
            ["SEAS_PATCH_BANKS", not is_ages],
            ]):
        banks = getattr(module, name, {})
        include and patch_banks.update(banks)
    return patch_banks


def update_replace_map(module, replace_map, is_ages=False, **kw):
    '''
    Updates replace_map with replacements defined in the provided module.
    Any symbols not in replace_map, the modules PADDING_REPLACE_MAP will
    be used to set a default value(sometimes necessary for calculating
    the size of a patch before writing it).
    '''
    for k, v in getattr(module, "PADDING_REPLACE_MAP", {}).items():
        replace_map.setdefault(k, v)

    for name, include in ([
            ["REPLACE_MAP",      True],
            ["AGES_REPLACE_MAP", is_ages],
            ["SEAS_REPLACE_MAP", not is_ages],
            ]):
        replacements = getattr(module, name, {})
        include and replace_map.update(replacements)
    return replace_map


def get_bank_sizes(rom_file, is_ages=False):
    pad_starts = (const.AGES_BANK_PAD_STARTS if is_ages else
                  const.SEAS_BANK_PAD_STARTS)
    # if searching for padding, this is a reference table for how much
    # padding is available in each bank for each game. the method of
    # searching backward for padding may falsely return true if all
    # padding is skipped, but a matching string is found in the code
    bank_sizes = {}
    for bank in range(const.MAX_BANKS):
        start, end = 0, 0
        if bank in pad_starts:
            pad     = pad_for_bank(1, bank, is_ages)[0]
            start   = pad_starts[bank]
            size    = const.BANK_SIZE - start

            rom_file.seek(start + bank*const.BANK_SIZE)
            data = rom_file.read(size)
            i = 0
            while data[i] != pad[0] and start < size:
                i += 1

            # search to find the first non-pad char
            start, i = start+i, 0
            for i in range(size):
                if data[i] != pad[0]:
                    i -= 1
                    break

            end = i + start + 1

        bank_sizes[bank] = [start, end, end]

    return bank_sizes


def serialize_patch(patch_parts, replace_map):
    '''
    Converts a patch to its serialized bytes form.
    Handles replacing symbols and calculating relative jumps.
    '''
    try:
        
        patch_data  = []
        rel_jumps   = {}
        labels      = {}
        off         = 0
        is_rel_jump = False
        for i, v in enumerate(patch_parts):
            if is_rel_jump:
                # skip the offset byte since it will be handled elsewhere
                is_rel_jump = False
                continue
            elif isinstance(v, opcodes.Label):
                # record label for later use
                if v in labels:
                    raise ValueError(f"Label '{v}' redefined.")
                labels[v] = off
                continue

            is_rel_jump = v in opcodes.JR_OPCODES

            v = replace_map.get(v, v)
            if isinstance(v, int):
                v = to_bytes(v)

            patch_data.append(v)
            off += len(v)

            if is_rel_jump and i+1 < len(patch_parts):
                off, v = off+1, patch_parts[i+1]

                # relative jump will need to be calculated here
                if isinstance(v, str):
                    rel_jumps[len(patch_data)] = [off, v]
                elif isinstance(v, int):
                    v = to_bytes(v)

                patch_data.append(v)

        # calculate relative jumps
        for idx in sorted(rel_jumps):
            src_off, label = rel_jumps[idx]
            if label not in labels:
                raise ValueError(f"No Label named '{label}' found."
                                 "Cannot calculate relative jump")
            off = labels[label] - src_off
            if off not in range(-128, 128):
                raise ValueError("Relative jump offset {off} too large.")

            patch_data[idx] = to_bytes(off)

        return b''.join(patch_data)
    except Exception:
        print(patch_parts)
        print(patch_data)
        raise

def find_sig(rom_file, sig, sig_name, is_ages=False,
             replace_map=None, patch_banks=None,
             bank_end=const.BANK_SIZE, search_start=0
             ):
    '''
    Searches the bank backwards for the first instance of sig.
    Returns the absolute offset, or -1 if it can't be found.
    '''
    file_start = search_start + patch_banks[sig_name] * const.BANK_SIZE

    if isinstance(sig, (list, tuple)):
        sig = serialize_patch(sig, replace_map)

    rom_file.seek(file_start)
    data    = rom_file.read(bank_end - search_start)
    # we reverse these to search backwards to check padding first
    offset  = data[::-1].find(sig[::-1])
    if offset >= 0:
        offset = (
            # add the start offset of where the data was read
            file_start +
            # adjust to be relative to the start
            len(data) - (offset + len(sig))
            )

    return offset

def offset_abs_to_rel(offset):
    '''
    Converts a file/absolute pointer to a bank-relative pointer.
    '''
    if offset >= 0:
        offset = (
            (offset%const.BANK_SIZE) +
            # bank0 is always mapped to the range [0x0000 - 0x3fFF],
            # while the current bank is mapped to [0x4000 - 0x7fFF]
            (const.BANK_SIZE if offset >= const.BANK_SIZE else 0)
            )
    return offset

def offset_rel_to_abs(offset, bank):
    '''
    Converts a bank-relative pointer to a file/absolute pointer.
    '''
    offset = offset%const.BANK_SIZE
    bank = 1 if bank == 0 else bank
    return offset + (bank-1)*const.BANK_SIZE

def print_bank_free_space(bank_sizes):
    '''
    Prints a small table showing the per-bank free space
    before and after all patches have been applied
    '''
    print("\nPrevious/Current per-bank free space:")
    print("\tbank\tstart\tpre-end\tcur-end\tpre-len\tcur-len")
    for bank in sorted(bank_sizes):
        start, curr_end, init_end = bank_sizes[bank]
        if start != curr_end and start != init_end:
            print(f"\t{bank}\t{start}\t{init_end}\t{curr_end}"
                  f"\t{init_end-start}\t{curr_end-start}")
    print("\tbank\tstart\tpre-end\tcur-end\tpre-len\tcur-len\n")

def alloc_patch(name, new, old=None, *, rom_file, bank_sizes,
                is_ages=False, replace_map=None, patch_banks=None, **kw):
    '''
    Searches bank for the offset of the old code being overwritten.
    If old is None(no existing code to overwrite), then patch offset
    will be the furthest spot in the bank padding that can hold it.

    If written to padding, bank_sizes will be updated with the new size.
    Updates replace_map with the determined offset(-1 if it wasnt found).

    NOTE: If there is no code being overwritten(or the old code can't
          be found in the bank), then the bank will first be searched
          for the new code. If found, that offset will be used instead.
    '''
    pad        = None if old else pad_for_asm(
        new, name, is_ages, replace_map, patch_banks
        )
    bank_sizes = {} if bank_sizes is None else bank_sizes
    bank       = patch_banks[name]
    start, end, _ = (
        [0, const.BANK_SIZE, const.BANK_SIZE] if pad is None else
        bank_sizes.setdefault(bank, [0, const.BANK_SIZE, const.BANK_SIZE])
        )

    # see if the new sig exists if the code was inserted into padding
    off = -1 if pad is None else find_sig(
        rom_file, new, name, is_ages, replace_map, patch_banks
        )
    skip = off >= 0

    if not skip:
        off = find_sig(rom_file, old or pad, name, is_ages,
                       replace_map, patch_banks, end, start)
        skip = off < 0

    if skip:
        off = find_sig(
            rom_file, new, name, is_ages, replace_map, patch_banks
            )
        if off >= 0:
            old, new = new, None

    if off < 0:
        msg = ("" if old else
               f"(not enough slack space in bank{bank})")
        print(f"\tCannot generate {name} patch{msg}.")
    else:
        rel_off = offset_abs_to_rel(off)
        # NOTE: need to do modulus since the address of banks 1 and higher
        #       starts at 0x4000, which will throw off our calculations.
        if pad and not skip:
            bank_sizes[bank][:-1] = [start, rel_off%const.BANK_SIZE]

        replace_map[name] = to_bytes(rel_off, 2)

    return [name, old or pad, new, off]
