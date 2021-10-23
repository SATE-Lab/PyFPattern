def sequence_loss(logits, targets, weights, average_across_timesteps=True, average_across_batch=True, softmax_loss_function=None, name=None):
    'Weighted cross-entropy loss for a sequence of logits. Depending on the\n  values of `average_across_timesteps` and `average_across_batch`, the return\n  Tensor will have rank 0, 1, or 2 as these arguments reduce the cross-entropy\n  at each target, which has shape `[batch_size, sequence_length]`, over their\n  respective dimensions. For example, if `average_across_timesteps` is `True`\n  and `average_across_batch` is `False`, then the return Tensor will have shape\n  `[batch_size]`.\n\n  Args:\n    logits: A Tensor of shape\n      `[batch_size, sequence_length, num_decoder_symbols]` and dtype float.\n      The logits correspond to the prediction across all classes at each\n      timestep.\n    targets: A Tensor of shape `[batch_size, sequence_length]` and dtype\n      int. The target represents the true class at each timestep.\n    weights: A Tensor of shape `[batch_size, sequence_length]` and dtype\n      float. `weights` constitutes the weighting of each prediction in the\n      sequence. When using `weights` as masking, set all valid timesteps to 1\n      and all padded timesteps to 0, e.g. a mask returned by `tf.sequence_mask`.\n    average_across_timesteps: If set, sum the cost across the sequence\n      dimension and divide the cost by the total label weight across timesteps.\n    average_across_batch: If set, sum the cost across the batch dimension and\n      divide the returned cost by the batch size.\n    softmax_loss_function: Function (labels, logits) -> loss-batch\n      to be used instead of the standard softmax (the default if this is None).\n      **Note that to avoid confusion, it is required for the function to accept\n      named arguments.**\n    name: Optional name for this operation, defaults to "sequence_loss".\n\n  Returns:\n    A float Tensor of rank 0, 1, or 2 depending on the\n    `average_across_timesteps` and `average_across_batch` arguments. By default,\n    it has rank 0 (scalar) and is the weighted average cross-entropy\n    (log-perplexity) per symbol.\n\n  Raises:\n    ValueError: logits does not have 3 dimensions or targets does not have 2\n                dimensions or weights does not have 2 dimensions.\n  '
    if (len(logits.get_shape()) != 3):
        raise ValueError('Logits must be a [batch_size x sequence_length x logits] tensor')
    if (len(targets.get_shape()) != 2):
        raise ValueError('Targets must be a [batch_size x sequence_length] tensor')
    if (len(weights.get_shape()) != 2):
        raise ValueError('Weights must be a [batch_size x sequence_length] tensor')
    with ops.name_scope(name, 'sequence_loss', [logits, targets, weights]):
        num_classes = array_ops.shape(logits)[2]
        logits_flat = array_ops.reshape(logits, [(- 1), num_classes])
        targets = array_ops.reshape(targets, [(- 1)])
        if (softmax_loss_function is None):
            crossent = nn_ops.sparse_softmax_cross_entropy_with_logits(labels=targets, logits=logits_flat)
        else:
            crossent = softmax_loss_function(labels=targets, logits=logits_flat)
        crossent *= array_ops.reshape(weights, [(- 1)])
        if (average_across_timesteps and average_across_batch):
            crossent = math_ops.reduce_sum(crossent)
            total_size = math_ops.reduce_sum(weights)
            total_size += 1e-12
            crossent /= total_size
        else:
            batch_size = array_ops.shape(logits)[0]
            sequence_length = array_ops.shape(logits)[1]
            crossent = array_ops.reshape(crossent, [batch_size, sequence_length])
        if (average_across_timesteps and (not average_across_batch)):
            crossent = math_ops.reduce_sum(crossent, axis=[1])
            total_size = math_ops.reduce_sum(weights, axis=[1])
            total_size += 1e-12
            crossent /= total_size
        if ((not average_across_timesteps) and average_across_batch):
            crossent = math_ops.reduce_sum(crossent, axis=[0])
            total_size = math_ops.reduce_sum(weights, axis=[0])
            total_size += 1e-12
            crossent /= total_size
        return crossent