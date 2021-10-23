

def separable_conv2d(input, depthwise_filter, pointwise_filter, strides, padding, rate=None, name=None, data_format=None):
    '2-D convolution with separable filters.\n\n  Performs a depthwise convolution that acts separately on channels followed by\n  a pointwise convolution that mixes channels.  Note that this is separability\n  between dimensions `[1, 2]` and `3`, not spatial separability between\n  dimensions `1` and `2`.\n\n  In detail,\n\n      output[b, i, j, k] = sum_{di, dj, q, r]\n          input[b, strides[1] * i + di, strides[2] * j + dj, q] *\n          depthwise_filter[di, dj, q, r] *\n          pointwise_filter[0, 0, q * channel_multiplier + r, k]\n\n  `strides` controls the strides for the depthwise convolution only, since\n  the pointwise convolution has implicit strides of `[1, 1, 1, 1]`.  Must have\n  `strides[0] = strides[3] = 1`.  For the most common case of the same\n  horizontal and vertical strides, `strides = [1, stride, stride, 1]`.\n  If any value in `rate` is greater than 1, we perform atrous depthwise\n  convolution, in which case all values in the `strides` tensor must be equal\n  to 1.\n\n  Args:\n    input: 4-D `Tensor` with shape according to `data_format`.\n    depthwise_filter: 4-D `Tensor` with shape\n      `[filter_height, filter_width, in_channels, channel_multiplier]`.\n      Contains `in_channels` convolutional filters of depth 1.\n    pointwise_filter: 4-D `Tensor` with shape\n      `[1, 1, channel_multiplier * in_channels, out_channels]`.  Pointwise\n      filter to mix channels after `depthwise_filter` has convolved spatially.\n    strides: 1-D of size 4.  The strides for the depthwise convolution for\n      each dimension of `input`.\n    padding: A string, either `\'VALID\'` or `\'SAME\'`.  The padding algorithm.\n      See the @{tf.nn.convolution$comment here}\n    rate: 1-D of size 2. The dilation rate in which we sample input values\n      across the `height` and `width` dimensions in atrous convolution. If it is\n      greater than 1, then all values of strides must be 1.\n    name: A name for this operation (optional).\n    data_format: The data format for input. Either "NHWC" (default) or "NCHW".\n\n  Returns:\n    A 4-D `Tensor` with shape according to \'data_format\'. For\n      example, with data_format="NHWC", shape is [batch, out_height,\n      out_width, out_channels].\n  '
    with ops.name_scope(name, 'separable_conv2d', [input, depthwise_filter, pointwise_filter]) as name:
        input = ops.convert_to_tensor(input, name='tensor_in')
        depthwise_filter = ops.convert_to_tensor(depthwise_filter, name='depthwise_filter')
        pointwise_filter = ops.convert_to_tensor(pointwise_filter, name='pointwise_filter')
        pointwise_filter_shape = pointwise_filter.get_shape().with_rank(4)
        pointwise_filter_shape[0].assert_is_compatible_with(1)
        pointwise_filter_shape[1].assert_is_compatible_with(1)
        if (rate is None):
            rate = [1, 1]

        def op(input_converted, _, padding):
            return nn_ops.depthwise_conv2d_native(input=input_converted, filter=depthwise_filter, strides=strides, padding=padding, data_format=data_format, name='depthwise')
        depthwise = nn_ops.with_space_to_batch(input=input, filter_shape=array_ops.shape(depthwise_filter), dilation_rate=rate, padding=padding, data_format=data_format, op=op)
        return nn_ops.conv2d(depthwise, pointwise_filter, [1, 1, 1, 1], padding='VALID', data_format=data_format, name=name)
