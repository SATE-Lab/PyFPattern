

def bernoulli_nll(x, y):
    'Computes the negative log-likelihood of a Bernoulli distribution.\n\n    This function calculates the negative log-likelihood of a Bernoulli\n    distribution.\n\n    .. math::\n\n        -\\log B(x; p) = -\\sum_i \\{x_i \\log(p_i) + (1 - x_i)\\log(1 - p_i)\\},\n\n    where :math:`p = \\sigma(y)`, :math:`\\sigma(\\cdot)` is a sigmoid\n    function, and :math:`B(x; p)` is a Bernoulli distribution.\n\n    .. note::\n\n       As this function uses a sigmoid function, you can pass a result of\n       fully-connected layer (that means :class:`Linear`) to this function\n       directly.\n\n    Args:\n        x (~chainer.Variable): Input variable.\n        y (~chainer.Variable): A variable representing the parameter of\n            Bernoulli distribution.\n\n    Returns:\n        ~chainer.Variable: A variable representing negative log-likelihood.\n\n    '
    assert isinstance(x, variable.Variable)
    assert isinstance(y, variable.Variable)
    return (sum.sum(softplus.softplus(y)) - sum.sum((x * y)))
