

def concat_examples(batch, device=None, padding=None):
    'Concatenates a list of examples into array(s).\n\n    This function converts an "array of tuples" into a "tuple of arrays".\n    Specifically, given a list of examples each of which consists of\n    a list of elements, this function first makes an array\n    by taking the element in the same position from each example\n    and concatenates them along the newly-inserted first axis\n    (called `batch dimension`) into one array.\n    It repeats this for all positions and returns the resulting arrays.\n\n    The output type depends on the type of examples in ``batch``.\n    For instance, consider each example consists of two arrays ``(x, y)``.\n    Then, this function concatenates ``x`` \'s into one array, and ``y`` \'s\n    into another array, and returns a tuple of these two arrays. Another\n    example: consider each example is a dictionary of two entries whose keys\n    are ``\'x\'`` and ``\'y\'``, respectively, and values are arrays. Then, this\n    function concatenates ``x`` \'s into one array, and ``y`` \'s into another\n    array, and returns a dictionary with two entries ``x`` and ``y`` whose\n    values are the concatenated arrays.\n\n    When the arrays to concatenate have different shapes, the behavior depends\n    on the ``padding`` value. If ``padding`` is ``None`` (default), it raises\n    an error. Otherwise, it builds an array of the minimum shape that the\n    contents of all arrays can be substituted to. The padding value is then\n    used to the extra elements of the resulting arrays.\n\n    .. admonition:: Example\n\n       >>> import numpy as np\n       >>> from chainer import dataset\n       >>> x = [([1, 2], 1),\n       ...      ([3, 4], 2),\n       ...      ([5, 6], 3)]\n       >>> dataset.concat_examples(x)\n       (array([[1, 2],\n              [3, 4],\n              [5, 6]]), array([1, 2, 3]))\n       >>>\n       >>> y = [(np.array([1, 2]), 0),\n       ...      (np.array([3]), 1),\n       ...      (np.array([]), 2)]\n       >>> dataset.concat_examples(y, padding=100)\n       (array([[  1,   2],\n              [  3, 100],\n              [100, 100]]), array([0, 1, 2]))\n       >>>\n       >>> z = [(np.array([1, 2]), np.array([0])),\n       ...      (np.array([3]), np.array([])),\n       ...      (np.array([]), np.array([2]))]\n       >>> dataset.concat_examples(z, padding=(100, 200))\n       (array([[  1,   2],\n              [  3, 100],\n              [100, 100]]), array([[  0],\n              [200],\n              [  2]]))\n       >>> w = [{\'feature\': np.array([1, 2]), \'label\': 0},\n       ...      {\'feature\': np.array([3, 4]), \'label\': 1},\n       ...      {\'feature\': np.array([5, 6]), \'label\': 2}]\n       >>> dataset.concat_examples(w)  # doctest: +SKIP\n       {\'feature\': array([[1, 2],\n              [3, 4],\n              [5, 6]]), \'label\': array([0, 1, 2])}\n\n    Args:\n        batch (list): A list of examples. This is typically given by a dataset\n            iterator.\n        device (int): Device ID to which each array is sent. Negative value\n            indicates the host memory (CPU). If it is omitted, all arrays are\n            left in the original device.\n        padding: Scalar value for extra elements. If this is None (default),\n            an error is raised on shape mismatch. Otherwise, an array of\n            minimum dimensionalities that can accommodate all arrays is\n            created, and elements outside of the examples are padded by this\n            value.\n\n    Returns:\n        Array, a tuple of arrays, or a dictionary of arrays. The type depends\n        on the type of each example in the batch.\n\n    '
    if (len(batch) == 0):
        raise ValueError('batch is empty')
    first_elem = batch[0]
    if isinstance(first_elem, tuple):
        result = []
        if (not isinstance(padding, tuple)):
            padding = ([padding] * len(first_elem))
        for i in six.moves.range(len(first_elem)):
            result.append(to_device(device, _concat_arrays([example[i] for example in batch], padding[i])))
        return tuple(result)
    elif isinstance(first_elem, dict):
        result = {
            
        }
        if (not isinstance(padding, dict)):
            padding = {key: padding for key in first_elem}
        for key in first_elem:
            result[key] = to_device(device, _concat_arrays([example[key] for example in batch], padding[key]))
        return result
    else:
        return to_device(device, _concat_arrays(batch, padding))
