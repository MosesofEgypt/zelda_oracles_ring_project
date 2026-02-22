
# the banks that the patches should apply to
PATCH_BANKS = dict(
    ENTRYPOINT              = 0,
    MAIN_LOOP               = 0,
    MAIN_LOOP1              = 0,

    RING_PALETTE0           = 5,
    RING_PALETTE1           = 5,
    RING_PALETTE2           = 5,
    RING_PALETTE3           = 5,
    RING_PALETTE4           = 5,
    RING_PALETTE5           = 5,
    RING_PALETTE6           = 5,

    # sprite updates
    GBOY_COLOR_RING_ICON    = 28,
    RUPEE_RING_ICON         = 28,
    SLAYERS_RING_ICON       = 28,
    SIGN_RING_ICON          = 28,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
