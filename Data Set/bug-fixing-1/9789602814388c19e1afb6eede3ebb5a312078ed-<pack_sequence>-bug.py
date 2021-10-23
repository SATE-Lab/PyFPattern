

def pack_sequence(sequences):
    'Packs a list of variable length Tensors\n\n    ``sequences`` should be a list of Tensors of size ``L x *``, where `L` is\n    the length of a sequence and `*` is any number of trailing dimensions,\n    including zero. They should be sorted in the order of decreasing length.\n\n    Example:\n        >>> from torch.nn.utils.rnn import pack_sequence\n        >>> a = torch.tensor([1,2,3])\n        >>> b = torch.tensor([4,5])\n        >>> c = torch.tensor([6])\n        >>> pack_sequence([a, b, c]])\n        PackedSequence(data=tensor([ 1,  4,  6,  2,  5,  3]), batch_sizes=tensor([ 3,  2,  1]))\n\n\n    Arguments:\n        sequences (list[Tensor]): A list of sequences of decreasing length.\n\n    Returns:\n        a :class:`PackedSequence` object\n    '
    return pack_padded_sequence(pad_sequence(sequences), [v.size(0) for v in sequences])
