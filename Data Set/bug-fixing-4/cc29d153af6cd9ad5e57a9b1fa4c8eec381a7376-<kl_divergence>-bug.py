def kl_divergence(dist1, dist2):
    'Computes Kullback-Leibler divergence.\n\n    For two continuous distributions :math:`p(x), q(x)`, it is expressed as\n\n    .. math::\n        D_{KL}(p||q) = \\int p(x) \\log \\frac{p(x)}{q(x)} dx\n\n    For two discrete distributions :math:`p(x), q(x)`, it is expressed as\n\n    .. math::\n        D_{KL}(p||q) = \\sum_x p(x) \\log \\frac{p(x)}{q(x)}\n\n    Args:\n        dist1(:class:`~chainer.Distribution`): Distribution to calculate KL\n            divergence :math:`p`. This is the first (left) operand of the KL\n            divergence.\n        dist2(:class:`~chainer.Distribution`): Distribution to calculate KL\n            divergence :math:`q`. This is the second (right) operand of the KL\n            divergence.\n\n    Returns:\n        ~chainer.Variable: Output variable representing kl divergence\n        :math:`D_{KL}(p||q)`.\n\n    Using `register_kl`, we can define behavior of `kl_divergence` for any two\n    distributions.\n\n    '
    return _KLDIVERGENCE[(type(dist1), type(dist2))](dist1, dist2)