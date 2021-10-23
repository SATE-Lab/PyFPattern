def __rmod__(self, other):
    'Returns `other` modulo `self`.\n\n    Args:\n      other: Another Dimension, or a value accepted by `as_dimension`.\n\n    Returns:\n      A Dimension whose value is `other` modulo `self`.\n    '
    try:
        other = as_dimension(other)
    except (TypeError, ValueError):
        return NotImplemented
    return (other % self)