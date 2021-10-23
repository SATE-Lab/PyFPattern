def standardize_weights(y, sample_weight=None, class_weight=None, sample_weight_mode=None):
    'Performs sample weight validation and standardization.\n\n    Everything gets normalized to a single sample-wise (or timestep-wise)\n    weight array.\n\n    # Arguments\n        y: Numpy array of model targets to be weighted.\n        sample_weight: User-provided `sample_weight` argument.\n        class_weight: User-provided `class_weight` argument.\n        sample_weight_mode: One of `None` or `"temporal"`.\n            `"temporal"` indicated that we expect 2D weight data\n            that will be applied to the last 2 dimensions of\n            the targets (i.e. we are weighting timesteps, not samples).\n\n    # Returns\n        A Numpy array of target weights, one entry per sample to weight.\n\n    # Raises\n        ValueError: In case of invalid user-provided arguments.\n    '
    if (sample_weight_mode is not None):
        if (sample_weight_mode != 'temporal'):
            raise ValueError(('"sample_weight_mode should be None or "temporal". Found: ' + str(sample_weight_mode)))
        if (len(y.shape) < 3):
            raise ValueError((('Found a sample_weight array for an input with shape ' + str(y.shape)) + '. Timestep-wise sample weighting (use of sample_weight_mode="temporal") is restricted to outputs that are at least 3D, i.e. that have a time dimension.'))
        if ((sample_weight is not None) and (len(sample_weight.shape) != 2)):
            raise ValueError((('Found a sample_weight array with shape ' + str(sample_weight.shape)) + '. In order to use timestep-wise sample weighting, you should pass a 2D sample_weight array.'))
    elif ((sample_weight is not None) and (len(sample_weight.shape) != 1)):
        raise ValueError((('Found a sample_weight array with shape ' + str(sample_weight.shape)) + '. In order to use timestep-wise sample weights, you should specify sample_weight_mode="temporal" in compile(). If you just mean to use sample-wise weights, make sure your sample_weight array is 1D.'))
    if ((sample_weight is not None) and (class_weight is not None)):
        warnings.warn('Found both `sample_weight` and `class_weight`: `class_weight` argument will be ignored.')
    if (sample_weight is not None):
        if (len(sample_weight.shape) > len(y.shape)):
            raise ValueError(((('Found a sample_weight with shape' + str(sample_weight.shape)) + '.Expected sample_weight with rank less than or equal to ') + str(len(y.shape))))
        if (y.shape[:sample_weight.ndim] != sample_weight.shape):
            raise ValueError((((('Found a sample_weight array with shape ' + str(sample_weight.shape)) + ' for an input with shape ') + str(y.shape)) + '. sample_weight cannot be broadcast.'))
        return sample_weight
    elif isinstance(class_weight, dict):
        if (len(y.shape) > 2):
            raise ValueError('`class_weight` not supported for 3+ dimensional targets.')
        if (y.shape[1] > 1):
            y_classes = np.argmax(y, axis=1)
        elif (y.shape[1] == 1):
            y_classes = np.reshape(y, y.shape[0])
        else:
            y_classes = y
        weights = np.asarray([class_weight[cls] for cls in y_classes if (cls in class_weight)])
        if (len(weights) != len(y_classes)):
            existing_classes = set(y_classes)
            existing_class_weight = set(class_weight.keys())
            raise ValueError(('`class_weight` must contain all classes in the data. The classes %s exist in the data but not in `class_weight`.' % (existing_classes - existing_class_weight)))
        return weights
    elif (sample_weight_mode is None):
        return np.ones((y.shape[0],), dtype=K.floatx())
    else:
        return np.ones((y.shape[0], y.shape[1]), dtype=K.floatx())