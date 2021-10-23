def doit(self, **kwargs):
    from sympy.matrices.expressions import Inverse
    deep = kwargs.get('deep', True)
    if deep:
        args = [arg.doit(**kwargs) for arg in self.args]
    else:
        args = self.args
    (base, exp) = args
    while isinstance(base, MatPow):
        exp = (exp * base.args[1])
        base = base.args[0]
    if (exp.is_zero and base.is_square):
        if isinstance(base, MatrixBase):
            return base.func(Identity(base.shape[0]))
        return Identity(base.shape[0])
    elif (isinstance(base, ZeroMatrix) and exp.is_negative):
        raise ValueError('Matrix determinant is 0, not invertible.')
    elif isinstance(base, (Identity, ZeroMatrix)):
        return base
    elif (isinstance(base, MatrixBase) and (exp.is_number or (exp.is_negative is not None) or (base.det() != 0))):
        if (exp is S.One):
            return base
        return (base ** exp)
    elif ((exp is S((- 1))) and base.is_square):
        return Inverse(base).doit(**kwargs)
    elif (exp is S.One):
        return base
    return MatPow(base, exp)