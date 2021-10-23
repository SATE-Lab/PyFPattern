def rnn(step_function, inputs, initial_states, go_backwards=False, mask=None, constants=None, unroll=False, input_length=None):
    "Iterates over the time dimension of a tensor.\n\n    # Arguments\n        inputs: tensor of temporal data of shape (samples, time, ...)\n            (at least 3D).\n        step_function:\n            Parameters:\n                input: tensor with shape (samples, ...) (no time dimension),\n                    representing input for the batch of samples at a certain\n                    time step.\n                states: list of tensors.\n            Returns:\n                output: tensor with shape (samples, ...) (no time dimension),\n                new_states: list of tensors, same length and shapes\n                    as 'states'.\n        initial_states: tensor with shape (samples, ...) (no time dimension),\n            containing the initial values for the states used in\n            the step function.\n        go_backwards: boolean. If True, do the iteration over\n            the time dimension in reverse order.\n        mask: binary tensor with shape (samples, time),\n            with a zero for every element that is masked.\n        constants: a list of constant values passed at each step.\n        unroll: whether to unroll the RNN or to use a symbolic loop (`scan`).\n        input_length: must be specified if using `unroll`.\n\n    # Returns\n        A tuple (last_output, outputs, new_states).\n            last_output: the latest output of the rnn, of shape (samples, ...)\n            outputs: tensor with shape (samples, time, ...) where each\n                entry outputs[s, t] is the output of the step function\n                at time t for sample s.\n            new_states: list of tensors, latest states returned by\n                the step function, of shape (samples, ...).\n    "
    ndim = inputs.ndim
    assert (ndim >= 3), 'Input should be at least 3D.'
    if unroll:
        if (input_length is None):
            raise Exception('When specifying `unroll=True`, an `input_length` must be provided to `rnn`.')
    axes = ([1, 0] + list(range(2, ndim)))
    inputs = inputs.dimshuffle(axes)
    if (mask is not None):
        if (mask.ndim == (ndim - 1)):
            mask = expand_dims(mask)
        assert (mask.ndim == ndim)
        mask = mask.dimshuffle(axes)
        if (constants is None):
            constants = []
        if unroll:
            indices = list(range(input_length))
            if go_backwards:
                indices = indices[::(- 1)]
            successive_outputs = []
            successive_states = []
            states = initial_states
            for i in indices:
                (output, new_states) = step_function(inputs[i], (states + constants))
                if (len(successive_outputs) == 0):
                    prev_output = zeros_like(output)
                else:
                    prev_output = successive_outputs[(- 1)]
                output = T.switch(mask[i], output, prev_output)
                kept_states = []
                for (state, new_state) in zip(states, new_states):
                    kept_states.append(T.switch(mask[i], new_state, state))
                states = kept_states
                successive_outputs.append(output)
                successive_states.append(states)
            outputs = T.stack(*successive_outputs)
            states = []
            for i in range(len(successive_states[(- 1)])):
                states.append(T.stack(*[states_at_step[i] for states_at_step in successive_states]))
        else:
            initial_output = (step_function(inputs[0], (initial_states + constants))[0] * 0)
            initial_output = T.unbroadcast(initial_output, 0, 1)

            def _step(input, mask, output_tm1, *states):
                (output, new_states) = step_function(input, states)
                output = T.switch(mask, output, output_tm1)
                return_states = []
                for (state, new_state) in zip(states, new_states):
                    return_states.append(T.switch(mask, new_state, state))
                return ([output] + return_states)
            (results, _) = theano.scan(_step, sequences=[inputs, mask], outputs_info=([initial_output] + initial_states), non_sequences=constants, go_backwards=go_backwards)
            if (type(results) is list):
                outputs = results[0]
                states = results[1:]
            else:
                outputs = results
                states = []
    elif unroll:
        indices = list(range(input_length))
        if go_backwards:
            indices = indices[::(- 1)]
        successive_outputs = []
        successive_states = []
        states = initial_states
        for i in indices:
            (output, states) = step_function(inputs[i], states)
            successive_outputs.append(output)
            successive_states.append(states)
        outputs = T.stack(*successive_outputs)
        states = []
        for i in range(len(successive_states[(- 1)])):
            states.append(T.stack(*[states_at_step[i] for states_at_step in successive_states]))
    else:

        def _step(input, *states):
            (output, new_states) = step_function(input, states)
            return ([output] + new_states)
        (results, _) = theano.scan(_step, sequences=inputs, outputs_info=([None] + initial_states), non_sequences=constants, go_backwards=go_backwards)
        if (type(results) is list):
            outputs = results[0]
            states = results[1:]
        else:
            outputs = results
            states = []
    outputs = T.squeeze(outputs)
    last_output = outputs[(- 1)]
    axes = ([1, 0] + list(range(2, outputs.ndim)))
    outputs = outputs.dimshuffle(axes)
    states = [T.squeeze(state[(- 1)]) for state in states]
    return (last_output, outputs, states)