# -*- coding: utf-8 -*-
import numpy as np



def moveaxis(ndarray, axis_src, axis_dst) :
    '''
    '''
    ndarray = np.asanyarray(ndarray)
    if axis_src == axis_dst :
        return ndarray.view()
    else :
        step = np.sign(axis_dst - axis_src)
        for axis in range(axis_src, axis_dst, step) :
            ndarray = np.swapaxes(ndarray, axis, axis + step)
        return ndarray



def zero_elimination(ndarray) :
    '''
    '''
    ndarray = np.asfarray(ndarray)
    ndarray[ndarray == 0] = np.finfo(ndarray.dtype).eps
    return ndarray



def rolling_window(array, window=(0,), asteps=None, wsteps=None, axes=None, toend=True):
    """Create a view of `array` which for every point gives the n-dimensional
    neighbourhood of size window. New dimensions are added at the end of
    `array` or after the corresponding original dimension.
    
    Parameters
    ----------
    array : array_like
        Array to which the rolling window is applied.
    window : int or tuple
        Either a single integer to create a window of only the last axis or a
        tuple to create it for the last len(window) axes. 0 can be used as a
        to ignore a dimension in the window.
    asteps : tuple
        Aligned at the last axis, new steps for the original array, ie. for
        creation of non-overlapping windows. (Equivalent to slicing result)
    wsteps : int or tuple (same size as window)
        steps for the added window dimensions. These can be 0 to repeat values
        along the axis.
    axes: int or tuple
        If given, must have the same size as window. In this case window is
        interpreted as the size in the dimension given by axes. IE. a window
        of (2, 1) is equivalent to window=2 and axis=-2.       
    toend : bool
        If False, the new dimensions are right after the corresponding original
        dimension, instead of at the end of the array. Adding the new axes at the
        end makes it easier to get the neighborhood, however toend=False will give
        a more intuitive result if you view the whole array.
    
    Returns
    -------
    A view on `array` which is smaller to fit the windows and has windows added
    dimensions (0s not counting), ie. every point of `array` is an array of size
    window.
    
    Examples
    --------
    >>> a = np.arange(9).reshape(3,3)
    >>> rolling_window(a, (2,2))
    array([[[[0, 1],
             [3, 4]],
            [[1, 2],
             [4, 5]]],
           [[[3, 4],
             [6, 7]],
            [[4, 5],
             [7, 8]]]])
    
    Or to create non-overlapping windows, but only along the first dimension:
    >>> rolling_window(a, (2,0), asteps=(2,1))
    array([[[0, 3],
            [1, 4],
            [2, 5]]])
    
    Note that the 0 is discared, so that the output dimension is 3:
    >>> rolling_window(a, (2,0), asteps=(2,1)).shape
    (1, 3, 2)
    
    This is useful for example to calculate the maximum in all (overlapping)
    2x2 submatrixes:
    >>> rolling_window(a, (2,2)).max((2,3))
    array([[4, 5],
           [7, 8]])
           
    Or delay embedding (3D embedding with delay 2):
    >>> x = np.arange(10)
    >>> rolling_window(x, 3, wsteps=2)
    array([[0, 2, 4],
           [1, 3, 5],
           [2, 4, 6],
           [3, 5, 7],
           [4, 6, 8],
           [5, 7, 9]])
    """
    array = np.asarray(array)
    orig_shape = np.asarray(array.shape)
    window = np.atleast_1d(window).astype(int) # maybe crude to cast to int...
    
    if axes is not None:
        axes = np.atleast_1d(axes)
        w = np.zeros(array.ndim, dtype=int)
        for axis, size in zip(axes, window):
            w[axis] = size
        window = w
    
    # Check if window is legal:
    if window.ndim > 1:
        raise ValueError("`window` must be one-dimensional.")
    if np.any(window < 0):
        raise ValueError("All elements of `window` must be larger then 1.")
    if len(array.shape) < len(window):
        raise ValueError("`window` length must be less or equal `array` dimension.") 

    _asteps = np.ones_like(orig_shape)
    if asteps is not None:
        asteps = np.atleast_1d(asteps)
        if asteps.ndim != 1:
            raise ValueError("`asteps` must be either a scalar or one dimensional.")
        if len(asteps) > array.ndim:
            raise ValueError("`asteps` cannot be longer then the `array` dimension.")
        # does not enforce alignment, so that steps can be same as window too.
        _asteps[-len(asteps):] = asteps
        
        if np.any(asteps < 1):
             raise ValueError("All elements of `asteps` must be larger then 1.")
    asteps = _asteps
    
    _wsteps = np.ones_like(window)
    if wsteps is not None:
        wsteps = np.atleast_1d(wsteps)
        if wsteps.shape != window.shape:
            raise ValueError("`wsteps` must have the same shape as `window`.")
        if np.any(wsteps < 0):
             raise ValueError("All elements of `wsteps` must be larger then 0.")

        _wsteps[:] = wsteps
        _wsteps[window == 0] = 1 # make sure that steps are 1 for non-existing dims.
    wsteps = _wsteps

    # Check that the window would not be larger then the original:
    if np.any(orig_shape[-len(window):] < window * wsteps):
        raise ValueError("`window` * `wsteps` larger then `array` in at least one dimension.")

    new_shape = orig_shape # just renaming...
    
    # For calculating the new shape 0s must act like 1s:
    _window = window.copy()
    _window[_window==0] = 1
    
    new_shape[-len(window):] += wsteps - _window * wsteps
    new_shape = (new_shape + asteps - 1) // asteps
    # make sure the new_shape is at least 1 in any "old" dimension (ie. steps
    # is (too) large, but we do not care.
    new_shape[new_shape < 1] = 1
    shape = new_shape
    
    strides = np.asarray(array.strides)
    strides *= asteps
    new_strides = array.strides[-len(window):] * wsteps
    
    # The full new shape and strides:
    if toend:
        new_shape = np.concatenate((shape, window))
        new_strides = np.concatenate((strides, new_strides))
    else:
        _ = np.zeros_like(shape)
        _[-len(window):] = window
        _window = _.copy()
        _[-len(window):] = new_strides
        _new_strides = _
        
        new_shape = np.zeros(len(shape)*2, dtype=int)
        new_strides = np.zeros(len(shape)*2, dtype=int)
        
        new_shape[::2] = shape
        new_strides[::2] = strides
        new_shape[1::2] = _window
        new_strides[1::2] = _new_strides
    
    new_strides = new_strides[new_shape != 0]
    new_shape = new_shape[new_shape != 0]
    
    return np.lib.stride_tricks.as_strided(array, shape=new_shape, strides=new_strides)



def shape_index(shape, index) :
    if len(shape) == 0 :
        return ()
    else :
        q, r = divmod(index, shape[-1])
        return shape_index(shape[0 : -1], q) + (r,)
    
def plain_index(shape, multi_index) :
    if len(multi_index) == 0 :
        return 0
    else :
        return multi_index[-1] + shape[-1] * plain_index(shape[0 : -1], multi_index[0 : -1])
    
def max_multi_index(shape) :
    index = ()
    for k in range(len(shape)) :
        index += (shape[k] - 1,)
    return index
        
class ChainIndex :
    def __init__(self, shape, index=0) :
        self.shape = shape
        self.index = index
        self.multi_index = shape_index(self.shape, self.index)
        self.is_valid = 0 <= index and index < plain_index(self.shape, max_multi_index(self.shape))
        
    def next(self) :
        return ChainIndex(self.shape, self.index + 1)
    
    def prev(self) :
        return ChainIndex(self.shape, self.index - 1)
    
    
    
def mirroring_crop(spectrogram, axis=-1) :
    spectrogram = np.asfarray(spectrogram)
    tmp = np.swapaxes(spectrogram, axis, -1)
    Nfft = spectrogram.shape[-1]
    half = Nfft // 2
    tmp = tmp[... , 0 : half]
    return np.swapaxes(tmp, axis, -1), half



def polygon(x, y, mesh, default=0, dtype=np.float64) :
    '''
    (x - x1) / (x2 - x1) = (y - y1) / (y2 - y1) -->
    --> y = [(y2 - y1) / (x2 - x1)] * x - [(y2 - y1) / (y2 - y1)] * x1 + y1
    '''
    def line(x, y, mesh, lb=np.less, rb=np.less_equal) :
        cn = np.logical_and( lb(x[0], mesh), rb(mesh, x[1]) )
        fn = lambda t: ((y[1] - y[0]) * (t - x[0]) / (x[1] - x[0])) + y[0]
        return cn, fn
        
    it = np.nditer([ rolling_window(x, window=2), rolling_window(y, window=2) ],
                    ['external_loop'], [['readonly'], ['readonly']])
    
    cn = np.array([])
    fn = np.array([])
    first = True
    for xi, yi in it :
        ci, fi = line(xi, yi, mesh, lb=np.less_equal if first else np.less, rb=np.less_equal)
        cn = np.append(cn, ci)
        fn = np.append(fn, fi)
        first = False
        
    cn = cn.reshape((-1, mesh.size))
    fn = np.append(fn, default)
    return np.piecewise(mesh.astype(dtype), cn, fn)