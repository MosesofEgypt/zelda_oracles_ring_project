import hashlib

from . import const, opcodes, util

from .shared.patches import prepare_shared_patches
from .misc.patches import prepare_misc_patches

from .wallet_size.patches import prepare_wallet_size_patches
from .damage_mods.patches import prepare_damage_modifier_patches
from .gasha_drops.patches import prepare_gasha_drop_patches
from .shop_prices.patches import prepare_shop_price_patches

from .ring_box.patches import prepare_box_menu_patches,\
     prepare_ring_list_reorg_patches, prepare_box_size_patches
from .ring_texts.patches import prepare_ring_text_patches
from .ring_icons.patches import prepare_ring_icon_patches
from .ring_swaps.patches import prepare_ring_swap_patches

from .rings_color.patches import prepare_color_ring_patches
from .rings_hikers.patches import prepare_hikers_ring_patches
from .rings_transform.patches import prepare_transform_ring_patches
from .rings_alchemy.patches import prepare_alchemy_ring_patches
from .rings_victory.patches import prepare_victory_ring_patches
from .rings_mystic_seed.patches import prepare_mystic_seed_ring_patches

from .combo_bombs.patches import prepare_combo_bombs_patches
from .combo_boomerang.patches import prepare_combo_boomerang_patches
from .combo_collision.patches import prepare_combo_collision_patches
from .combo_feather.patches import prepare_combo_feather_patches
from .combo_pickups.patches import prepare_combo_pickups_patches
from .combo_punch.patches import prepare_combo_punch_patches
from .combo_sword.patches import prepare_combo_sword_patches


def detect_game_flavor(rom_file):
    '''
    Determines if the rom is English Ages, English Seasons, or something else.
    '''
    rom_file.seek(const.ROM_SIG_OFFSET)
    sig = rom_file.read(len(const.ROM_SIG_AGES))
    reg = rom_file.read(len(const.ROM_REGION_AGES))
    lan = rom_file.read(len(const.ROM_LANGUAGE_EN))
    ages = seas = False
    full_sig = sig+reg+lan
    if sig not in (const.ROM_SIG_AGES, const.ROM_SIG_SEAS):
        print("ROM name does not match Ages or Seasons.\n"
              f"Expected {const.ROM_SIG_AGES} or {const.ROM_SIG_SEAS}, but got {sig}")
    elif reg not in (const.ROM_REGION_AGES, const.ROM_REGION_SEAS):
        print("ROM region does not match Ages or Seasons.\n"
              f"Expected {const.ROM_REGION_AGES} or {const.ROM_REGION_SEAS}, but got {reg}")
    elif lan == const.ROM_LANGUAGE_JP:
        print("Japanese ROMs are not supported.")
    elif full_sig == const.ROM_SIG_EN_AGES:
        ages = True
    elif full_sig == const.ROM_SIG_EN_SEAS:
        seas = True
    else:
        print("Invalid combination of ROM name, region, and language detected.\n"
              f"Expected {const.ROM_SIG_EN_AGES} or {const.ROM_SIG_EN_SEAS}, but got {full_sig}")

    return ages, seas

def apply_patch(rom_file, name, old, new, offset, *,
                is_ages=False, verify=True,
                replace_map={}, patch_banks={}):
    err_msg = ""
    data_to_find  = (None if old is None else
                     util.serialize_patch(old, replace_map))
    if new is None:
        skip, data_to_write = True, None
    else:
        skip, data_to_write = False, util.serialize_patch(new, replace_map)

    if offset is None:
        offset = util.find_sig(
            rom_file, data_to_find, name, is_ages,
            replace_map, patch_banks
            )

    if skip:
        print(f"\tSkipped({name})\t - {len(data_to_find)} bytes @ {offset}")
        return

    if offset < 0:
        err_msg = "code signature not found"
    elif verify and old is not None:
        # check to ensure the data at the offset is what we expect
        rom_file.seek(offset)
        data_found = rom_file.read(len(data_to_find))
        if data_to_find != data_found:
            err_msg = "data found does not match expected"

        elif len(data_to_find) != len(data_to_write):
            err_msg = "length mismatch between patch(%i) and target(%i)" % (
                len(data_to_write), len(data_to_find)
                )

    if not err_msg:
        rom_file.seek(offset)
        rom_file.write(data_to_write)
        rom_file.flush()

    if err_msg:
        print(f"\tFailure({name})\t - {len(data_to_write)} bytes @ {offset}\n"
              f"\t\t{err_msg}")
    else:
        print(f"\tSuccess({name})\t - {len(data_to_write)} bytes @ {offset}")


def apply_patches(filepath, verify=True):
    # TODO: make this function able to selectively apply patches and
    #       pass the config for those patches to the patch preparers
    with open(filepath, "rb+") as f:
        # pass this around to the patch preparers so they can update it
        is_ages, is_seasons = detect_game_flavor(f)
        if not is_ages and not is_seasons:
            print("\tCannot generate patches(cannot determine if ages or seasons).")
            return

        kwargs = dict(
            rom_file        = f, verify = verify,
            is_ages         = is_ages, is_seasons=is_seasons,
            # keeps track of free space in each bank
            bank_sizes      = {},
            # holds all text replacements that some patches may need
            # to insert into the text data(i.e. ring damage modifiers)
            text_overrides  = {},
            # simply maps the name of each patch to the bank it should be in.
            # this makes searching for patches faster since only 16KB are being
            # searched through, but it also allows our patches to be smaller
            # with significantly lower chance of matching something incorrect.
            patch_banks     = {},
            # maps symbol strings(i.e. func/var names) to a value to replace
            # them with at serialization time. alloc_patch will update this
            # with the bank-relative pointer to any named patches that are
            # applied, so it ends up serving as somewhat of a linker.
            replace_map     = {},
            )

        # update the replace_map with the opcodes and func/var pointers/values
        for module in (const, opcodes):
            replace_map = util.update_replace_map(module, **kwargs)

        # some space used by the garbage is required for the menu
        # patches, so not clearing it isn't really an option.
        util.clear_rom_garbage(
            ages_garbage_map=const.AGES_BANK_GARBAGE,
            seas_garbage_map=const.SEAS_BANK_GARBAGE,
            **kwargs
            )

        # do this only after the garbage has been cleared
        kwargs["bank_sizes"].update(util.get_bank_sizes(f, is_ages))

        for prepare_func in (
                prepare_shared_patches,
                prepare_gasha_drop_patches,
                prepare_misc_patches,
                prepare_wallet_size_patches,
                prepare_damage_modifier_patches,

                prepare_combo_bombs_patches,
                prepare_combo_boomerang_patches,
                prepare_combo_collision_patches,
                prepare_combo_feather_patches,
                prepare_combo_pickups_patches,
                prepare_combo_punch_patches,
                prepare_combo_sword_patches,

                prepare_color_ring_patches,
                prepare_mystic_seed_ring_patches,
                prepare_victory_ring_patches,
                prepare_hikers_ring_patches,
                prepare_alchemy_ring_patches,
                prepare_transform_ring_patches,

                prepare_shop_price_patches,
                prepare_ring_swap_patches,
                # NOTE: box menu patches must come after box size so
                #       the size in the replace_map can be updated
                prepare_box_size_patches,
                prepare_box_menu_patches,
                prepare_ring_icon_patches,
                prepare_ring_list_reorg_patches,

                # NOTE: ring text must come after other patches
                #       so that text overrides can be inserted
                prepare_ring_text_patches,
                ):
            for patch in prepare_func(**kwargs):
                apply_patch(
                    f, *patch, is_ages=is_ages, verify=verify,
                    replace_map=kwargs['replace_map'],
                    patch_banks=kwargs['patch_banks']
                    )

        util.print_bank_free_space(kwargs["bank_sizes"])
