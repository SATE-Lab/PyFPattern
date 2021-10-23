def ctc_greedy_decoder(input, blank, name=None):
    "\n    This op is used to decode sequences by greedy policy by below steps:\n\n    1. Get the indexes of max value for each row in input. a.k.a.\n       numpy.argmax(input, axis=0).\n    2. For each sequence in result of step1, merge repeated tokens between two\n       blanks and delete all blanks.\n\n    A simple example as below:\n\n    .. code-block:: text\n\n        Given:\n\n        input.data = [[0.6, 0.1, 0.3, 0.1],\n                      [0.3, 0.2, 0.4, 0.1],\n                      [0.1, 0.5, 0.1, 0.3],\n                      [0.5, 0.1, 0.3, 0.1],\n\n                      [0.5, 0.1, 0.3, 0.1],\n                      [0.2, 0.2, 0.2, 0.4],\n                      [0.2, 0.2, 0.1, 0.5],\n                      [0.5, 0.1, 0.3, 0.1]]\n\n        input.lod = [[4, 4]]\n\n        Then:\n\n        output.data = [[2],\n                       [1],\n                       [3]]\n\n        output.lod = [[2, 1]]\n\n    Args:\n\n        input(Variable): (LoDTensor<float>), the probabilities of\n                         variable-length sequences, which is a 2-D Tensor with\n                         LoD information. It's shape is [Lp, num_classes + 1],\n                         where Lp is the sum of all input sequences' length and\n                         num_classes is the true number of classes. (not\n                         including the blank label).\n        blank(int): the blank label index of Connectionist Temporal\n                    Classification (CTC) loss, which is in thehalf-opened\n                    interval [0, num_classes + 1).\n        name (str): The name of this layer. It is optional.\n\n    Returns:\n        Variable: CTC greedy decode result. If all the sequences in result were\n        empty, the result LoDTensor will be [-1] with LoD [[]] and dims [1, 1].\n\n    Examples:\n        .. code-block:: python\n\n            x = fluid.layers.data(name='x', shape=[8], dtype='float32')\n\n            cost = fluid.layers.ctc_greedy_decoder(input=x, blank=0)\n    "
    helper = LayerHelper('ctc_greedy_decoder', **locals())
    (_, topk_indices) = topk(input, k=1)
    ctc_out = helper.create_variable_for_type_inference(dtype='int64')
    helper.append_op(type='ctc_align', inputs={
        'Input': [topk_indices],
    }, outputs={
        'Output': [ctc_out],
    }, attrs={
        'merge_repeated': True,
        'blank': blank,
    })
    return ctc_out