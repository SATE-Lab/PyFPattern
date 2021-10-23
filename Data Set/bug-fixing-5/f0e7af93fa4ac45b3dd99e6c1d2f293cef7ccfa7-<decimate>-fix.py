def decimate(x, q, n=None, ftype='iir', axis=(- 1), zero_phase=True):
    "\n    Downsample the signal after applying an anti-aliasing filter.\n\n    By default, an order 8 Chebyshev type I filter is used. A 30 point FIR\n    filter with Hamming window is used if `ftype` is 'fir'.\n\n    Parameters\n    ----------\n    x : array_like\n        The signal to be downsampled, as an N-dimensional array.\n    q : int\n        The downsampling factor. When using IIR downsampling, it is recommended\n        to call `decimate` multiple times for downsampling factors higher than\n        13.\n    n : int, optional\n        The order of the filter (1 less than the length for 'fir'). Defaults to\n        8 for 'iir' and 20 times the downsampling factor for 'fir'.\n    ftype : str {'iir', 'fir'} or ``dlti`` instance, optional\n        If 'iir' or 'fir', specifies the type of lowpass filter. If an instance\n        of an `dlti` object, uses that object to filter before downsampling.\n    axis : int, optional\n        The axis along which to decimate.\n    zero_phase : bool, optional\n        Prevent phase shift by filtering with `filtfilt` instead of `lfilter`\n        when using an IIR filter, and shifting the outputs back by the filter's\n        group delay when using an FIR filter. The default value of ``True`` is\n        recommended, since a phase shift is generally not desired.\n\n        .. versionadded:: 0.18.0\n\n    Returns\n    -------\n    y : ndarray\n        The down-sampled signal.\n\n    See Also\n    --------\n    resample : Resample up or down using the FFT method.\n    resample_poly : Resample using polyphase filtering and an FIR filter.\n\n    Notes\n    -----\n    The ``zero_phase`` keyword was added in 0.18.0.\n    The possibility to use instances of ``dlti`` as ``ftype`` was added in\n    0.18.0.\n    "
    x = np.asarray(x)
    q = operator.index(q)
    if (n is not None):
        n = operator.index(n)
    if (ftype == 'fir'):
        if (n is None):
            half_len = (10 * q)
            n = (2 * half_len)
        (b, a) = (firwin((n + 1), (1.0 / q), window='hamming'), 1.0)
    elif (ftype == 'iir'):
        if (n is None):
            n = 8
        system = dlti(*cheby1(n, 0.05, (0.8 / q)))
        (b, a) = (system.num, system.den)
    elif isinstance(ftype, dlti):
        system = ftype._as_tf()
        (b, a) = (system.num, system.den)
    else:
        raise ValueError('invalid ftype')
    sl = ([slice(None)] * x.ndim)
    a = np.asarray(a)
    if (a.size == 1):
        b = (b / a)
        if zero_phase:
            y = resample_poly(x, 1, q, axis=axis, window=b)
        else:
            n_out = ((x.shape[axis] // q) + bool((x.shape[axis] % q)))
            y = upfirdn(b, x, up=1, down=q, axis=axis)
            sl[axis] = slice(None, n_out, None)
    else:
        if zero_phase:
            y = filtfilt(b, a, x, axis=axis)
        else:
            y = lfilter(b, a, x, axis=axis)
        sl[axis] = slice(None, None, q)
    return y[tuple(sl)]