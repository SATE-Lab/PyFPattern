def monkey_patch_variable():

    def unique_tmp_name():
        return unique_name.generate('tmp')

    def safe_get_dtype(var):
        try:
            dtype = var.dtype
        except:
            raise ValueError('Cannot get data type from %s', var.name)
        return dtype

    def current_block(var):
        if in_dygraph_mode():
            return default_main_program().global_block()
        return var.block.program.current_block()

    def create_new_tmp_var(block, dtype):
        tmp_name = unique_tmp_name()
        return block.create_var(name=tmp_name, dtype=dtype)

    def create_tensor(block, value, dtype, shape):
        value = float(value)
        var = create_new_tmp_var(block, dtype)
        block.append_op(type='fill_constant', outputs={
            'Out': [var],
        }, attrs={
            'dtype': var.dtype,
            'shape': shape,
            'value': value,
            'force_cpu': force_init_on_cpu(),
        }, stop_gradient=True)
        var.stop_gradient = True
        return var

    def create_scalar(block, value, dtype):
        return create_tensor(block, value, dtype, shape=[1])

    def create_tensor_with_batchsize(ref_var, value, dtype):
        assert isinstance(ref_var, Variable)
        value = float(value)
        block = current_block(ref_var)
        var = create_new_tmp_var(block, dtype)
        batch_dim = (- 1)
        for (i, d) in enumerate(ref_var.shape):
            if (d < 0):
                batch_dim = i
                break
        assert (batch_dim != (- 1))
        block.append_op(type='fill_constant_batch_size_like', outputs={
            'Out': [var],
        }, inputs={
            'Input': [ref_var],
        }, attrs={
            'shape': ref_var.shape,
            'value': value,
            'input_dim_idx': batch_dim,
            'output_dim_idx': batch_dim,
        }, stop_gradient=True)
        var.stop_gradient = True
        return var

    def astype(self, dtype):
        '\n        **Notes**:\n            **The variable must be a** :ref:`api_fluid_Tensor`\n\n        Cast a variable to a specified data type.\n\n        Args:\n\n            self(Variable): The source variable\n\n            dtype: The target data type\n\n        Returns:\n            Variable: Variable with new dtype\n\n        Examples:\n            In Static Graph Mode:\n\n            .. code-block:: python\n\n                import paddle.fluid as fluid\n\n                startup_prog = fluid.Program()\n                main_prog = fluid.Program()\n                with fluid.program_guard(startup_prog, main_prog):\n                    original_variable = fluid.data(name = "new_variable", shape=[2,2], dtype=\'float32\')\n                    new_variable = original_variable.astype(\'int64\')\n                    print("new var\'s dtype is: {}".format(new_variable.dtype))\n\n            In Dygraph Mode:\n\n            .. code-block:: python\n\n                import paddle.fluid as fluid\n                import numpy as np\n\n                x = np.ones([2, 2], np.float32)\n                with fluid.dygraph.guard():\n                    original_variable = fluid.dygraph.to_variable(x)\n                    print("original var\'s dtype is: {}, numpy dtype is {}".format(original_variable.dtype, original_variable.numpy().dtype))\n                    new_variable = original_variable.astype(\'int64\')\n                    print("new var\'s dtype is: {}, numpy dtype is {}".format(new_variable.dtype, new_variable.numpy().dtype))\n\n        '
        block = current_block(self)
        out = create_new_tmp_var(block, dtype)
        block.append_op(type='cast', inputs={
            'X': [self],
        }, outputs={
            'Out': [out],
        }, attrs={
            'in_dtype': self.dtype,
            'out_dtype': out.dtype,
        })
        return out

    def _scalar_elementwise_op_(var, scale, bias):
        block = current_block(var)
        out = create_new_tmp_var(block, var.dtype)
        block.append_op(type='scale', inputs={
            'X': [var],
        }, outputs={
            'Out': [out],
        }, attrs={
            'scale': scale,
            'bias': bias,
        })
        return out

    def _scalar_elementwise_add_(var, value):
        return _scalar_elementwise_op_(var, 1.0, value)

    def _scalar_elementwise_sub_(var, value):
        return _scalar_elementwise_op_(var, 1.0, (- value))

    def _scalar_elementwise_rsub_(var, value):
        return _scalar_elementwise_op_(var, (- 1.0), value)

    def _scalar_elementwise_mul_(var, value):
        return _scalar_elementwise_op_(var, value, 0.0)

    def _scalar_elementwise_div_(var, value):
        return _scalar_elementwise_op_(var, (1.0 / value), 0.0)

    def _elemwise_method_creator_(method_name, op_type, reverse=False, scalar_method=None):

        def __impl__(self, other_var):
            if ((scalar_method is not None) and (not ((op_type == 'elementwise_div') and (self.dtype in _supported_int_dtype_)))):
                if isinstance(other_var, float):
                    if (self.dtype in _supported_int_dtype_):
                        assert (other_var == int(other_var)), 'float value {} cannot convert to integer'.format(other_var)
                    return scalar_method(self, other_var)
                elif isinstance(other_var, int):
                    return scalar_method(self, float(other_var))
            lhs_dtype = safe_get_dtype(self)
            if (not isinstance(other_var, Variable)):
                if reverse:
                    has_batch_size = False
                    for elem in self.shape:
                        if (elem < 0):
                            has_batch_size = True
                            break
                    if (not has_batch_size):
                        other_var = create_tensor(current_block(self), other_var, dtype=lhs_dtype, shape=self.shape)
                    else:
                        other_var = create_tensor_with_batchsize(self, other_var, lhs_dtype)
                else:
                    other_var = create_scalar(current_block(self), value=other_var, dtype=lhs_dtype)
            rhs_dtype = safe_get_dtype(other_var)
            if (lhs_dtype != rhs_dtype):
                other_var = astype(other_var, lhs_dtype)
            if reverse:
                tmp = self
                self = other_var
                other_var = tmp
            out = create_new_tmp_var(current_block(self), dtype=lhs_dtype)
            current_block(self).append_op(type=op_type, inputs={
                'X': [self],
                'Y': [other_var],
            }, outputs={
                'Out': out,
            }, attrs={
                'axis': (- 1),
            })
            return out
        comment = OpProtoHolder.instance().get_op_proto(op_type).comment
        __impl__.__doc__ = '\n        {0}\n        Args:\n            self(Variable): left hand variable\n            other_var(Variable|float|int): right hand variable\n\n        Returns:\n            Variable\n        '.format(comment)
        __impl__.__name__ = method_name
        return __impl__
    for (method_name, op_type, reverse, scalar_method) in (('__add__', 'elementwise_add', False, _scalar_elementwise_add_), ('__radd__', 'elementwise_add', False, _scalar_elementwise_add_), ('__sub__', 'elementwise_sub', False, _scalar_elementwise_sub_), ('__rsub__', 'elementwise_sub', True, _scalar_elementwise_rsub_), ('__mul__', 'elementwise_mul', False, _scalar_elementwise_mul_), ('__rmul__', 'elementwise_mul', False, _scalar_elementwise_mul_), ('__div__', 'elementwise_div', False, _scalar_elementwise_div_), ('__truediv__', 'elementwise_div', False, _scalar_elementwise_div_), ('__rdiv__', 'elementwise_div', True, None), ('__rtruediv__', 'elementwise_div', True, None), ('__pow__', 'elementwise_pow', False, None), ('__rpow__', 'elementwise_pow', True, None), ('__floordiv__', 'elementwise_floordiv', False, None), ('__mod__', 'elementwise_mod', False, None), ('__eq__', 'equal', False, None), ('__ne__', 'not_equal', False, None), ('__lt__', 'less_than', False, None), ('__le__', 'less_equal', False, None), ('__gt__', 'greater_than', False, None), ('__ge__', 'greater_equal', False, None)):
        setattr(Variable, method_name, _elemwise_method_creator_(method_name, op_type, reverse, scalar_method))
        setattr(core.VarBase, method_name, _elemwise_method_creator_(method_name, op_type, reverse, scalar_method))
    Variable.astype = astype
    setattr(core.VarBase, 'astype', astype)