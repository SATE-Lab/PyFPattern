

def slice(x, start, size):
    'Extracts a slice from a tensor.\n\n    # Arguments\n        x: Input tensor.\n        start: Integer list/tuple or tensor\n            indicating the start indices of the slice\n            along each axis.\n        size: Integer list/tuple or tensor\n            indicating how many dimensions to slice\n            along each axis.\n\n    # Returns\n        A sliced tensor:\n        ```python\n        new_x = x[start[0]: start[0] + size[0], ..., start[-1]: start[-1] + size[-1]]\n        ```\n\n    # Raises\n        ValueError: if the dimension and the size of indices mismatches.\n\n    {{np_implementation}}\n    '
    if (not (len(int_shape(x)) == len(start) == len(size))):
        raise ValueError('The dimension and the size of indices should match.')
    return tf.slice(x, start, size)
