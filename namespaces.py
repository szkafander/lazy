# This is a convenience module that has decorators and methods for decorating 
# and mutating namespace methods.
#
# A namespace is a class with only static methods.
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


def _get_methods(class_input):
    """ A rather hacky method to get the methods of a class.
    """
    return [f for f in dir(class_input) 
            if callable(getattr(class_input, f)) and not f.startswith('__')]


def decorate_class_methods(class_input, decorator):
    """ A class decorator that applies a decorator to all of the class' 
    methods.
    
    Args:
        class_input (class) - the class to be decorated.
        decorator (method) - the decorator method to be applied to methods.
    
    Returns:
        This is a class decorator.
    """
    
    class DecoratedClass(class_input):
        pass
    
    for method in _get_methods(DecoratedClass):
        setattr(DecoratedClass, method, 
                decorator(getattr(DecoratedClass, method)))
    
    return DecoratedClass


def _methods_decorator(decorator):
    return lambda x: decorate_class_methods(x, decorator)


def to_factory(function):
    """ A decorator that converts a method to a factory method. Pushes
    evaluation one call deeper. The method is reinitated at every call. This is
    useful to emulate Keras layer behavior.
    
    Args:
        function (method) - the method to convert to a factory method.
    
    Returns:
        A factory method based on function.
    """
    def wrapper(*args, **kwargs):
        def Factory():
            return function(*args, **kwargs)
        return Factory
    return wrapper


def to_callable_factory(function):
    """ The same as to_factory, except the returned factory method is callable
    directly. I.e., instead of using factory_method()(input) to call, you can
    use callable_factory_method(input) to achieve the same behavior. This is
    useful to emulate Keras layer behavior.
    
    Args:
        function (method) - the method to convert to a callable factory method.
    
    Returns:
        A callable factory method based on function.
    """
    def wrapper(*args, **kwargs):
        def CallableFactory(input_arg):
            return function(*args, **kwargs)(input_arg)
        return CallableFactory
    return wrapper


# a class decorator that converts all namespace methods to factory methods
namespace_to_factory = _methods_decorator(to_factory)

# a class decorator that converts all namespace methods to callable factory 
# methods
namespace_to_callable_factory = _methods_decorator(to_callable_factory)


def convert_namespace_to_factory(class_input):
    """ A method that converts a namespace to a namespace with factory methods
    based on the methods of the original namespace.
    
    Args:
        class_input (class): the namespace the methods of which to convert to 
            factory methods
    
    Returns:
        A namespace with factory methods based on the methods of class_input.
    """
    return decorate_class_methods(class_input, to_factory)


def convert_namespace_to_callable_factory(class_input):
    """ The same as convert_namespace_to_factory, except all namespace methods
    will be converted to callable factory methods.
    
    Args:
        class_input (class): the namespace the methods of which to convert to 
            callable factory methods
    
    Returns:
        A namespace with callable factory methods based on the methods of
            class_input.
    """
    return decorate_class_methods(class_input, to_callable_factory)