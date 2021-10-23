

def summary(self, line_length=None, positions=None, print_fn=None):
    'Prints a string summary of the network.\n\n        # Arguments\n            line_length: Total length of printed lines\n                (e.g. set this to adapt the display to different\n                terminal window sizes).\n            positions: Relative or absolute positions of log elements\n                in each line. If not provided,\n                defaults to `[.33, .55, .67, 1.]`.\n            print_fn: Print function to use.\n                It will be called on each line of the summary.\n                You can set it to a custom function\n                in order to capture the string summary.\n                It defaults to `print` (prints to stdout).\n        '
    if (not self.built):
        raise ValueError('This model has never been called, thus its weights have not yet been created, so no summary can be displayed. Build the model first (e.g. by calling it on some test data).')
    return print_layer_summary(self, line_length=line_length, positions=positions, print_fn=print_fn)
