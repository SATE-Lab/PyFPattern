def list_arguments(self):
    "List all the arguments in the symbol.\n\n        A\n        ~~~~\n        >>> a = mxnet.sym.var('a')\n        >>> b = mxnet.sym.var('b')\n        >>> c = a + b\n        >>> c.list_arguments\n        ['a', 'b']\n        ~~~~\n\n        Returns\n        -------\n        args : list of string\n            List containing the names of all the arguments required to compute the symbol.\n        "
    size = ctypes.c_uint()
    sarr = ctypes.POINTER(ctypes.c_char_p)()
    check_call(_LIB.MXSymbolListArguments(self.handle, ctypes.byref(size), ctypes.byref(sarr)))
    return [py_str(sarr[i]) for i in range(size.value)]