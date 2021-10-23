

def background_gradient(self, cmap='PuBu', low=0, high=0, axis=0, subset=None):
    "\n        Color the background in a gradient according to\n        the data in each column (optionally row).\n        Requires matplotlib.\n\n        .. versionadded:: 0.17.1\n\n        Parameters\n        ----------\n        cmap: str or colormap\n            matplotlib colormap\n        low, high: float\n            compress the range by these values.\n        axis: int or str\n            1 or 'columns' for columnwise, 0 or 'index' for rowwise\n        subset: IndexSlice\n            a valid slice for ``data`` to limit the style application to\n\n        Returns\n        -------\n        self : Styler\n\n        Notes\n        -----\n        Tune ``low`` and ``high`` to keep the text legible by\n        not using the entire range of the color map. These extend\n        the range of the data by ``low * (x.max() - x.min())``\n        and ``high * (x.max() - x.min())`` before normalizing.\n        "
    subset = _maybe_numeric_slice(self.data, subset)
    subset = _non_reducing_slice(subset)
    self.apply(self._background_gradient, cmap=cmap, subset=subset, axis=axis, low=low, high=high)
    return self
