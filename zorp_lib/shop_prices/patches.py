from ..const import *
from .const import *
from .. import util
from . import asm, const


def prepare_shop_price_patches(**kw):
    patch_data = []
    if kw.get("is_ages"):
        patch_data.extend([
            [SHOP_PRICE1, asm.AGES_NEW_SHOP_PRICE1_ASM, asm.AGES_ORIG_SHOP_PRICE1_ASM],
            [SHOP_PRICE0, asm.AGES_NEW_SHOP_PRICE0_ASM, asm.AGES_ORIG_SHOP_PRICE0_ASM],
            ])
    else:
        patch_data.extend([
            [SHOP_PRICE3, asm.SEAS_NEW_SHOP_PRICE3_ASM, asm.SEAS_ORIG_SHOP_PRICE3_ASM],
            [SHOP_PRICE2, asm.SEAS_NEW_SHOP_PRICE2_ASM, asm.SEAS_ORIG_SHOP_PRICE2_ASM],
            [SHOP_PRICE1, asm.SEAS_NEW_SHOP_PRICE1_ASM, asm.SEAS_ORIG_SHOP_PRICE1_ASM],
            [SHOP_PRICE0, asm.SEAS_NEW_SHOP_PRICE0_ASM, asm.SEAS_ORIG_SHOP_PRICE0_ASM],
            ])
    util.update_patch_banks(const, **kw)
    util.update_replace_map(const, **kw)
    return [util.alloc_patch(*args, **kw) for args in patch_data]
