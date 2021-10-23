

def cross_entropy(input, target, weight=None, size_average=True):
    'This criterion combines `log_softmax` and `nll_loss` in one single class.\n\n    See :class:`torch.nn.CrossEntropyLoss` for details.\n\n    Args:\n        input: Variable :math:`(N, C)` where `C = number of classes`\n        target: Variable :math:`(N)` where each value is `0 <= targets[i] <= C-1`\n        weight (Tensor, optional): a manual rescaling weight given to each\n                class. If given, has to be a Tensor of size "nclasses"\n        size_average (bool, optional): By default, the losses are averaged\n                over observations for each minibatch. However, if the field\n                sizeAverage is set to False, the losses are instead summed\n                for each minibatch.\n    '
    return nll_loss(log_softmax(input), target, weight, size_average)
