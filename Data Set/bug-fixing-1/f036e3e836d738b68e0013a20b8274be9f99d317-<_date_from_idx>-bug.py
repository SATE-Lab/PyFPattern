

def _date_from_idx(d1, idx, freq):
    '\n    Returns the date from an index beyond the end of a date series.\n    d1 is the datetime of the last date in the series. idx is the\n    index distance of how far the next date should be from d1. Ie., 1 gives\n    the next date from d1 at freq.\n\n    Notes\n    -----\n    This does not do any rounding to make sure that d1 is actually on the\n    offset. For now, this needs to be taken care of before you get here.\n    '
    return (_maybe_convert_period(d1) + (idx * _freq_to_pandas[freq]))
