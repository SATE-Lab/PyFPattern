def retain_outputs(self, indexes):
    'Lets specified output variable nodes keep data arrays.\n\n        By calling this method from :meth:`forward`, the function node can\n        specify which outputs are required for backprop. If this method is not\n        called, no output variables will be marked to keep their data array at\n        the point of returning from :meth:`apply`. The output variables with\n        retained arrays can then be obtained by calling\n        :meth:`get_retained_outputs` from inside :meth:`backward`.\n\n        .. note::\n\n           It is recommended to use this method if the function requires some\n           or all output arrays in backprop. The function can also use output\n           arrays just by keeping references to them directly, although it\n           might affect the performance of later function applications on the\n           output variables.\n\n        Note that **this method must not be called from the outside of\n        :meth:`forward`.**\n\n        Args:\n            indexes (iterable of int): Indexes of output variables that the\n                function will require for backprop.\n\n        '
    self._output_indexes_to_retain = indexes