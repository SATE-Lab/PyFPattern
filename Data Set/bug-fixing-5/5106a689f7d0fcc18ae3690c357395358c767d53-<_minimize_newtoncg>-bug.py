def _minimize_newtoncg(fun, x0, args=(), jac=None, hess=None, hessp=None, callback=None, xtol=1e-05, eps=_epsilon, maxiter=None, disp=False, return_all=False, **unknown_options):
    '\n    Minimization of scalar function of one or more variables using the\n    Newton-CG algorithm.\n\n    Note that the `jac` parameter (Jacobian) is required.\n\n    Options\n    -------\n    disp : bool\n        Set to True to print convergence messages.\n    xtol : float\n        Average relative error in solution `xopt` acceptable for\n        convergence.\n    maxiter : int\n        Maximum number of iterations to perform.\n    eps : float or ndarray\n        If `jac` is approximated, use this value for the step size.\n\n    '
    _check_unknown_options(unknown_options)
    if (jac is None):
        raise ValueError('Jacobian is required for Newton-CG method')
    f = fun
    fprime = jac
    fhess_p = hessp
    fhess = hess
    avextol = xtol
    epsilon = eps
    retall = return_all
    x0 = asarray(x0).flatten()
    (fcalls, f) = wrap_function(f, args)
    (gcalls, fprime) = wrap_function(fprime, args)
    hcalls = 0
    if (maxiter is None):
        maxiter = (len(x0) * 200)
    xtol = (len(x0) * avextol)
    update = [(2 * xtol)]
    xk = x0
    if retall:
        allvecs = [xk]
    k = 0
    old_fval = f(x0)
    old_old_fval = None
    float64eps = numpy.finfo(numpy.float64).eps
    warnflag = 0
    while ((numpy.add.reduce(numpy.abs(update)) > xtol) and (k < maxiter)):
        b = (- fprime(xk))
        maggrad = numpy.add.reduce(numpy.abs(b))
        eta = numpy.min([0.5, numpy.sqrt(maggrad)])
        termcond = (eta * maggrad)
        xsupi = zeros(len(x0), dtype=x0.dtype)
        ri = (- b)
        psupi = (- ri)
        i = 0
        dri0 = numpy.dot(ri, ri)
        if (fhess is not None):
            A = fhess(*((xk,) + args))
            hcalls = (hcalls + 1)
        k2 = 0
        cg_maxiter = (20 * len(x0))
        while ((numpy.add.reduce(numpy.abs(ri)) > termcond) and (k2 < cg_maxiter)):
            if (fhess is None):
                if (fhess_p is None):
                    Ap = approx_fhess_p(xk, psupi, fprime, epsilon)
                else:
                    Ap = fhess_p(xk, psupi, *args)
                    hcalls = (hcalls + 1)
            else:
                Ap = numpy.dot(A, psupi)
            Ap = asarray(Ap).squeeze()
            curv = numpy.dot(psupi, Ap)
            if (0 <= curv <= (3 * float64eps)):
                break
            elif (curv < 0):
                if (i > 0):
                    break
                else:
                    xsupi = ((dri0 / (- curv)) * b)
                    break
            alphai = (dri0 / curv)
            xsupi = (xsupi + (alphai * psupi))
            ri = (ri + (alphai * Ap))
            dri1 = numpy.dot(ri, ri)
            betai = (dri1 / dri0)
            psupi = ((- ri) + (betai * psupi))
            i = (i + 1)
            dri0 = dri1
            k2 += 1
        if (k2 >= cg_maxiter):
            break
        pk = xsupi
        gfk = (- b)
        try:
            (alphak, fc, gc, old_fval, old_old_fval, gfkp1) = _line_search_wolfe12(f, fprime, xk, pk, gfk, old_fval, old_old_fval)
        except _LineSearchError:
            warnflag = 2
            break
        update = (alphak * pk)
        xk = (xk + update)
        if (callback is not None):
            callback(xk)
        if retall:
            allvecs.append(xk)
        k += 1
    fval = old_fval
    if (warnflag == 2):
        msg = _status_message['pr_loss']
        if disp:
            print(('Warning: ' + msg))
            print(('         Current function value: %f' % fval))
            print(('         Iterations: %d' % k))
            print(('         Function evaluations: %d' % fcalls[0]))
            print(('         Gradient evaluations: %d' % gcalls[0]))
            print(('         Hessian evaluations: %d' % hcalls))
    elif (k >= maxiter):
        warnflag = 1
        msg = _status_message['maxiter']
        if disp:
            print(('Warning: ' + msg))
            print(('         Current function value: %f' % fval))
            print(('         Iterations: %d' % k))
            print(('         Function evaluations: %d' % fcalls[0]))
            print(('         Gradient evaluations: %d' % gcalls[0]))
            print(('         Hessian evaluations: %d' % hcalls))
    elif (k2 >= cg_maxiter):
        warnflag = 3
        msg = "Warning: CG iterations didn't converge.  The Hessian is not positive definite."
        if disp:
            print(('Warning: ' + msg))
            print(('         Current function value: %f' % fval))
            print(('         Iterations: %d' % k))
            print(('         Function evaluations: %d' % fcalls[0]))
            print(('         Gradient evaluations: %d' % gcalls[0]))
            print(('         Hessian evaluations: %d' % hcalls))
    else:
        msg = _status_message['success']
        if disp:
            print(msg)
            print(('         Current function value: %f' % fval))
            print(('         Iterations: %d' % k))
            print(('         Function evaluations: %d' % fcalls[0]))
            print(('         Gradient evaluations: %d' % gcalls[0]))
            print(('         Hessian evaluations: %d' % hcalls))
    result = OptimizeResult(fun=fval, jac=gfk, nfev=fcalls[0], njev=gcalls[0], nhev=hcalls, status=warnflag, success=(warnflag == 0), message=msg, x=xk, nit=k)
    if retall:
        result['allvecs'] = allvecs
    return result