def tplquad(func, a, b, gfun, hfun, qfun, rfun, args=(), epsabs=1.49e-08, epsrel=1.49e-08):
    '\n    Compute a triple (definite) integral.\n\n    Return the triple integral of ``func(z, y, x)`` from ``x = a..b``,\n    ``y = gfun(x)..hfun(x)``, and ``z = qfun(x,y)..rfun(x,y)``.\n\n    Parameters\n    ----------\n    func : function\n        A Python function or method of at least three variables in the\n        order (z, y, x).\n    a, b : float\n        The limits of integration in x: `a` < `b`\n    gfun : function\n        The lower boundary curve in y which is a function taking a single\n        floating point argument (x) and returning a floating point result:\n        a lambda function can be useful here.\n    hfun : function\n        The upper boundary curve in y (same requirements as `gfun`).\n    qfun : function\n        The lower boundary surface in z.  It must be a function that takes\n        two floats in the order (x, y) and returns a float.\n    rfun : function\n        The upper boundary surface in z. (Same requirements as `qfun`.)\n    args : tuple, optional\n        Extra arguments to pass to `func`.\n    epsabs : float, optional\n        Absolute tolerance passed directly to the innermost 1-D quadrature\n        integration. Default is 1.49e-8.\n    epsrel : float, optional\n        Relative tolerance of the innermost 1-D integrals. Default is 1.49e-8.\n\n    Returns\n    -------\n    y : float\n        The resultant integral.\n    abserr : float\n        An estimate of the error.\n\n    See Also\n    --------\n    quad: Adaptive quadrature using QUADPACK\n    quadrature: Adaptive Gaussian quadrature\n    fixed_quad: Fixed-order Gaussian quadrature\n    dblquad: Double integrals\n    nquad : N-dimensional integrals\n    romb: Integrators for sampled data\n    simps: Integrators for sampled data\n    ode: ODE integrators\n    odeint: ODE integrators\n    scipy.special: For coefficients and roots of orthogonal polynomials\n\n    '

    def ranges0(*args):
        return [qfun(args[1], args[0]), rfun(args[1], args[0])]

    def ranges1(*args):
        return [gfun(args[0]), hfun(args[0])]
    ranges = [ranges0, ranges1, [a, b]]
    return nquad(func, ranges, args=args, opts={
        'epsabs': epsabs,
        'epsrel': epsrel,
    })