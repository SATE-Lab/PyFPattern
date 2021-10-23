

def logsumexp(x, axis=None, keepdims=False):
    'Computes log(sum(exp(elements across dimensions of a tensor))).\n\n    This function is more numerically stable than log(sum(exp(x))).\n    It avoids overflows caused by taking the exp of large inputs and\n    underflows caused by taking the log of small inputs.\n\n    # Arguments\n        x: A tensor or variable.\n        axis: An integer, the axis to reduce over.\n        keepdims: A boolean, whether to keep the dimensions or not.\n            If `keepdims` is `False`, the rank of the tensor is reduced\n            by 1. If `keepdims` is `True`, the reduced dimension is\n            retained with length 1.\n\n    # Returns\n        The reduced tensor.\n    '
    axis = _normalize_axis(axis, ndim(x))
    return tf.reduce_logsumexp(x, axis=axis, keep_dims=keepdims)
