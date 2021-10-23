def gaussian(image, sigma=1, output=None, mode='nearest', cval=0, multichannel=None, preserve_range=False, truncate=4.0):
    "Multi-dimensional Gaussian filter.\n\n    Parameters\n    ----------\n    image : array-like\n        Input image (grayscale or color) to filter.\n    sigma : scalar or sequence of scalars, optional\n        Standard deviation for Gaussian kernel. The standard\n        deviations of the Gaussian filter are given for each axis as a\n        sequence, or as a single number, in which case it is equal for\n        all axes.\n    output : array, optional\n        The ``output`` parameter passes an array in which to store the\n        filter output.\n    mode : {'reflect', 'constant', 'nearest', 'mirror', 'wrap'}, optional\n        The `mode` parameter determines how the array borders are\n        handled, where `cval` is the value when mode is equal to\n        'constant'. Default is 'nearest'.\n    cval : scalar, optional\n        Value to fill past edges of input if `mode` is 'constant'. Default\n        is 0.0\n    multichannel : bool, optional (default: None)\n        Whether the last axis of the image is to be interpreted as multiple\n        channels. If True, each channel is filtered separately (channels are\n        not mixed together). Only 3 channels are supported. If `None`,\n        the function will attempt to guess this, and raise a warning if\n        ambiguous, when the array has shape (M, N, 3).\n    preserve_range : bool, optional\n        Whether to keep the original range of values. Otherwise, the input\n        image is converted according to the conventions of `img_as_float`.\n    truncate : float, optional\n        Truncate the filter at this many standard deviations.\n\n    Returns\n    -------\n    filtered_image : ndarray\n        the filtered array\n\n    Notes\n    -----\n    This function is a wrapper around :func:`scipy.ndi.gaussian_filter`.\n\n    Integer arrays are converted to float.\n\n    The multi-dimensional filter is implemented as a sequence of\n    one-dimensional convolution filters. The intermediate arrays are\n    stored in the same data type as the output. Therefore, for output\n    types with a limited precision, the results may be imprecise\n    because intermediate results may be stored with insufficient\n    precision.\n\n    Examples\n    --------\n\n    >>> a = np.zeros((3, 3))\n    >>> a[1, 1] = 1\n    >>> a\n    array([[ 0.,  0.,  0.],\n           [ 0.,  1.,  0.],\n           [ 0.,  0.,  0.]])\n    >>> gaussian(a, sigma=0.4)  # mild smoothing\n    array([[ 0.00163116,  0.03712502,  0.00163116],\n           [ 0.03712502,  0.84496158,  0.03712502],\n           [ 0.00163116,  0.03712502,  0.00163116]])\n    >>> gaussian(a, sigma=1)  # more smoothing\n    array([[ 0.05855018,  0.09653293,  0.05855018],\n           [ 0.09653293,  0.15915589,  0.09653293],\n           [ 0.05855018,  0.09653293,  0.05855018]])\n    >>> # Several modes are possible for handling boundaries\n    >>> gaussian(a, sigma=1, mode='reflect')\n    array([[ 0.08767308,  0.12075024,  0.08767308],\n           [ 0.12075024,  0.16630671,  0.12075024],\n           [ 0.08767308,  0.12075024,  0.08767308]])\n    >>> # For RGB images, each is filtered separately\n    >>> from skimage.data import astronaut\n    >>> image = astronaut()\n    >>> filtered_img = gaussian(image, sigma=1, multichannel=True)\n\n    "
    spatial_dims = guess_spatial_dimensions(image)
    if ((spatial_dims is None) and (multichannel is None)):
        msg = 'Images with dimensions (M, N, 3) are interpreted as 2D+RGB by default. Use `multichannel=False` to interpret as 3D image with last dimension of length 3.'
        warn(RuntimeWarning(msg))
        multichannel = True
    if np.any((np.asarray(sigma) < 0.0)):
        raise ValueError('Sigma values less than zero are not valid')
    if multichannel:
        if (not isinstance(sigma, coll.Iterable)):
            sigma = ([sigma] * (image.ndim - 1))
        if (len(sigma) != image.ndim):
            sigma = np.concatenate((np.asarray(sigma), [0]))
    image = convert_to_float(image, preserve_range)
    return ndi.gaussian_filter(image, sigma, mode=mode, cval=cval, truncate=truncate)