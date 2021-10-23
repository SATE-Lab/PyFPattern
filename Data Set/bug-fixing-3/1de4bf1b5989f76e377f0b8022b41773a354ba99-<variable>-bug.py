def variable(value, dtype=None, name=None):
    "Instantiates a variable and returns it.\n\n    # Arguments\n        value: Numpy array, initial value of the tensor.\n        dtype: Tensor type.\n        name: Optional name string for the tensor.\n\n    # Returns\n        A variable instance (with Keras metadata included).\n\n    # Examples\n    ```python\n        >>> from keras import backend as K\n        >>> val = np.array([[1, 2], [3, 4]])\n        >>> kvar = K.variable(value=val, dtype='float64', name='example_var')\n        >>> K.dtype(kvar)\n        'float64'\n        >>> print(kvar)\n        example_var\n        >>> kvar.eval()\n        array([[ 1.,  2.],\n               [ 3.,  4.]])\n    ```\n    "
    if (dtype is None):
        dtype = floatx()
    if hasattr(value, 'tocoo'):
        sparse_coo = value.tocoo()
        indices = np.concatenate((np.expand_dims(sparse_coo.row, 1), np.expand_dims(sparse_coo.col, 1)), 1)
        v = tf.SparseTensor(indices=indices, values=sparse_coo.data, shape=sparse_coo.shape)
        v._dims = len(sparse_coo.shape)
        v._keras_shape = sparse_coo.shape
        v._uses_learning_phase = False
        return v
    v = tf.Variable(value, dtype=_convert_string_dtype(dtype), name=name)
    if isinstance(value, np.ndarray):
        v._keras_shape = value.shape
    elif hasattr(value, 'get_shape'):
        v._keras_shape = tuple(map(int, value.get_shape()))
    v._uses_learning_phase = False
    return v