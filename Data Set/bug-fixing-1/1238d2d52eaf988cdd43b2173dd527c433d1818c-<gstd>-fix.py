

def gstd(a, axis=0, ddof=1):
    'Calculate the geometric standard deviation of an array\n\n    The geometric standard deviation describes the spread of a set of numbers\n    where the geometric mean is preferred. It is a multiplicative factor, and\n    so a dimensionless quantity.\n\n    It is defined as the exponent of the standard deviation of ``log(a)``.\n    Mathematically the population geometric standard deviation can be\n    evaluated as::\n\n        gstd = exp(std(log(a)))\n\n    .. versionadded:: 1.3.0\n\n    Parameters\n    ----------\n    a : array_like\n        An array like object containing the sample data.\n    axis : int, tuple or None, optional\n        Axis along which to operate. Default is 0. If None, compute over\n        the whole array `a`.\n    ddof : int, optional\n        Degree of freedom correction in the calculation of the\n        geometric standard deviation. Default is 1.\n\n    Returns\n    -------\n    ndarray or float\n        An array of the geometric standard deviation. If `axis` is None or `a`\n        is a 1d array a float is returned.\n\n    Notes\n    -----\n    As the calculation requires the use of logarithms the geometric standard\n    deviation only supports strictly positive values. Any non-positive or\n    infinite values will raise a `ValueError`.\n    The geometric standard deviation is sometimes confused with the exponent of\n    the standard deviation, ``exp(std(a))``. Instead the geometric standard\n    deviation is ``exp(std(log(a)))``.\n    The default value for `ddof` is different to the default value (0) used\n    by other ddof containing functions, such as ``np.std`` and ``np.nanstd``.\n\n    Examples\n    --------\n    Find the geometric standard deviation of a log-normally distributed sample.\n    Note that the standard deviation of the distribution is one, on a\n    log scale this evaluates to approximately ``exp(1)``.\n\n    >>> from scipy.stats import gstd\n    >>> np.random.seed(123)\n    >>> sample = np.random.lognormal(mean=0, sigma=1, size=1000)\n    >>> gstd(sample)\n    2.7217860664589946\n\n    Compute the geometric standard deviation of a multidimensional array and\n    of a given axis.\n\n    >>> a = np.arange(1, 25).reshape(2, 3, 4)\n    >>> gstd(a, axis=None)\n    2.2944076136018947\n    >>> gstd(a, axis=2)\n    array([[1.82424757, 1.22436866, 1.13183117],\n           [1.09348306, 1.07244798, 1.05914985]])\n    >>> gstd(a, axis=(1,2))\n    array([2.12939215, 1.22120169])\n\n    The geometric standard deviation further handles masked arrays.\n\n    >>> a = np.arange(1, 25).reshape(2, 3, 4)\n    >>> ma = np.ma.masked_where(a > 16, a)\n    >>> ma\n    masked_array(\n      data=[[[1, 2, 3, 4],\n             [5, 6, 7, 8],\n             [9, 10, 11, 12]],\n            [[13, 14, 15, 16],\n             [--, --, --, --],\n             [--, --, --, --]]],\n      mask=[[[False, False, False, False],\n             [False, False, False, False],\n             [False, False, False, False]],\n            [[False, False, False, False],\n             [ True,  True,  True,  True],\n             [ True,  True,  True,  True]]],\n      fill_value=999999)\n    >>> gstd(ma, axis=2)\n    masked_array(\n      data=[[1.8242475707663655, 1.2243686572447428, 1.1318311657788478],\n            [1.0934830582350938, --, --]],\n      mask=[[False, False, False],\n            [False,  True,  True]],\n      fill_value=999999)\n    '
    a = np.asanyarray(a)
    log = (ma.log if isinstance(a, ma.MaskedArray) else np.log)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', RuntimeWarning)
            return np.exp(np.std(log(a), axis=axis, ddof=ddof))
    except RuntimeWarning as w:
        if np.isinf(a).any():
            raise ValueError('Infinite value encountered. The geometric standard deviation is defined for strictly positive values only.')
        a_nan = np.isnan(a)
        a_nan_any = a_nan.any()
        if ((a_nan_any and np.less_equal(np.nanmin(a), 0)) or ((not a_nan_any) and np.less_equal(a, 0).any())):
            raise ValueError('Non positive value encountered. The geometric standard deviation is defined for strictly positive values only.')
        elif ('Degrees of freedom <= 0 for slice' == str(w)):
            raise ValueError(w)
        else:
            return np.exp(np.std(log(a, where=(~ a_nan)), axis=axis, ddof=ddof))
    except TypeError:
        raise ValueError('Invalid array input. The inputs could not be safely coerced to any supported types')
