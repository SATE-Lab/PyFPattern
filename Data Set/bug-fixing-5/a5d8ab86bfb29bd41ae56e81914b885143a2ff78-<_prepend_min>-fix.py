def _prepend_min(arr, pad_amt, num, axis=(- 1)):
    '\n    Prepend `pad_amt` minimum values along `axis`.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to prepend.\n    num : int\n        Depth into `arr` along `axis` to calculate minimum.\n        Range: [1, `arr.shape[axis]`] or None (entire axis)\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt` values prepended along `axis`. The\n        prepended region is the minimum of the first `num` values along\n        `axis`.\n\n    '
    if (pad_amt == 0):
        return arr
    if (num == 1):
        return _prepend_edge(arr, pad_amt, axis)
    if (num is not None):
        if (num >= arr.shape[axis]):
            num = None
    min_slice = _slice_first(arr.shape, num, axis=axis)
    min_chunk = arr[min_slice].min(axis=axis, keepdims=True)
    return _do_prepend(arr, min_chunk.repeat(pad_amt, axis), axis=axis)