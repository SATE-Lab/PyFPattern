

def conv1d(input, weight, bias=None, stride=1, padding=0, dilation=1, groups=1):
    'Applies a 1D convolution over an input signal composed of several input\n    planes.\n\n    See :class:`~torch.nn.Conv1d` for details and output shape.\n\n    Args:\n        input: input tensor of shape (minibatch x in_channels x iW)\n        weight: filters of shape (out_channels, in_channels, kW)\n        bias: optional bias of shape (out_channels)\n        stride: the stride of the convolving kernel, default 1\n\n    Examples:\n        >>> filters = autograd.Variable(torch.randn(33, 16, 3))\n        >>> inputs = autograd.Variable(torch.randn(20, 16, 50))\n        >>> F.conv1d(inputs)\n    '
    f = ConvNd(_single(stride), _single(padding), _single(dilation), False, _single(0), groups)
    return (f(input, weight, bias) if (bias is not None) else f(input, weight))
