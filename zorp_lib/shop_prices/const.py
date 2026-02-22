# the banks that the patches should apply to
PATCH_BANKS = dict(
    )
AGES_PATCH_BANKS = dict(
    SHOP_PRICE0             = 9,
    SHOP_PRICE1             = 31,
    )

SEAS_PATCH_BANKS = dict(
    SHOP_PRICE0             = 8,
    SHOP_PRICE1             = 30,
    SHOP_PRICE2             = 31,
    SHOP_PRICE3             = 9,
    )

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
