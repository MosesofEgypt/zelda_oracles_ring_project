# the banks that the patches should apply to
PATCH_BANKS = dict(
    RANG_CHECK0 = 7,
    RANG_CHECK1 = 7,
    RANG_TIMER0 = 7,
    RANG_TIMER1 = 7,
    RANG_TIMER2 = 7,
    RANG_TIMER3 = 7,
    )
AGES_PATCH_BANKS = dict()
SEAS_PATCH_BANKS = dict()

PADDING_REPLACE_MAP  = {
    name: b'\x00\x00' for name in set([
        *PATCH_BANKS, *AGES_PATCH_BANKS, *SEAS_PATCH_BANKS
        ])
    }

globals().update({name: name for name in PADDING_REPLACE_MAP})
