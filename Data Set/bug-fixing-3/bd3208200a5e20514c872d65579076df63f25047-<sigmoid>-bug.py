def sigmoid(x, name=None):
    'Computes sigmoid of `x` element-wise.\n\n  Specifically, `y = 1 / (1 + exp(-x))`.\n\n  Args:\n    x: A Tensor with type `float32`, `float64`, `int32`, `complex64`, `int64`,\n      or `qint32`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A Tensor with the same type as `x` if `x.dtype != qint32`\n      otherwise the return type is `quint8`.\n\n  @compatibility(numpy)\n  Equivalent to np.scipy.special.expit\n  @end_compatibility\n  '
    with ops.name_scope(name, 'Sigmoid', [x]) as name:
        x = ops.convert_to_tensor(x, name='x')
        return gen_math_ops._sigmoid(x, name=name)