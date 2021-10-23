

def cumprod(x, axis=0, exclusive=False, reverse=False, name=None):
    'Compute the cumulative product of the tensor `x` along `axis`.\n\n  By default, this op performs an inclusive cumprod, which means that the\n  first\n  element of the input is identical to the first element of the output:\n  ```prettyprint\n  tf.cumprod([a, b, c]) ==> [a, a * b, a * b * c]\n  ```\n\n  By setting the `exclusive` kwarg to `True`, an exclusive cumprod is\n  performed\n  instead:\n  ```prettyprint\n  tf.cumprod([a, b, c], exclusive=True) ==> [0, a, a * b]\n  ```\n\n  By setting the `reverse` kwarg to `True`, the cumprod is performed in the\n  opposite direction:\n  ```prettyprint\n  tf.cumprod([a, b, c], reverse=True) ==> [a * b * c, b * c, c]\n  ```\n  This is more efficient than using separate `tf.reverse` ops.\n\n  The `reverse` and `exclusive` kwargs can also be combined:\n  ```prettyprint\n  tf.cumprod([a, b, c], exclusive=True, reverse=True) ==> [b * c, c, 0]\n  ```\n\n  Args:\n    x: A `Tensor`. Must be one of the following types: `float32`, `float64`,\n       `int64`, `int32`, `uint8`, `uint16`, `int16`, `int8`, `complex64`,\n       `complex128`, `qint8`, `quint8`, `qint32`, `half`.\n    axis: A `Tensor` of type `int32` (default: 0).\n    reverse: A `bool` (default: False).\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor`. Has the same type as `x`.\n  '
    with ops.name_scope(name, 'Cumprod', [x]) as name:
        x = ops.convert_to_tensor(x, name='x')
        return gen_math_ops.cumprod(x, axis, exclusive=exclusive, reverse=reverse, name=name)