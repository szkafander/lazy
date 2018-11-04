# This is a convenience module that has decorators for converting methods
# to lazily evaluated and/or cached methods.
#
# Copyright (c) 2018 Pal Toth
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================


def lazy_evaluation(lazy=True, cached=False):
    """ A decorator that converts a method to a lazily evaluated method. The
    method returns a Data wrapper object. Decorator arguments provide flags for
    caching and lazy evaluation.
    """
    def lazy_eval(function):
        def wrapper(*args, **kwargs):
            def inner():
                return function(*args, **kwargs)
            if cached:
                inner = cached_function(inner)
            if lazy:
                return Data(inner)
            else:
                return Data(function(*args, **kwargs))
        return wrapper
    return lazy_eval


class cached_function:
    """ A decorator that converts a method to cached evaluation.
    It is different from functools.lru_cache in the sense that it does not
    keep a history of calls but rather updates cache every time the arguments
    change. This is better suited for methods that are normally evaluated
    only once, e.g., for computing filter weights or other constants.
    """
    def __init__(self, function):
        self.function = function
        self.args = None
        self.kwargs = None
        self.cache = None
    
    def __call__(self, *args, **kwargs):
        args_changed = self._update_args(*args, **kwargs)
        if self.cache and not args_changed:
            return self.cache
        else:
            print('function run')
            self.cache = self.function(*args, **kwargs)
            return self.cache
    
    def _update_args(self, *args, **kwargs):
        if args == self.args and kwargs == self.kwargs:
            return False
        else:
            self.args = args
            self.kwargs = kwargs
            return True


class Data:
    """ A wrapper class for data that might be lazily evaluated and/or cached.
    
    Args:
        value - instantiate the object from this value. If value is a function,
            Data assumes lazy evaluation. Cached data via the cached_function 
            decorator returns a function ipso facto.
    
    Properties:
        value - returns the stored data. If Data is lazily evaluated, returns a
            the output of a call of the underlying _value attribute.
    """
    def __init__(self, value):
        self._value = value
        if callable(value):
            self.lazy = True
        else:
            self.lazy = False
    
    @property
    def value(self):
        if self.lazy:
            return self._value()
        return self._value