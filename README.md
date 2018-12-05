# lazy
A subset of a growing collection of productivity tools that I use when working with Keras layers. Useful for manipulating namespaces (classes with only static methods). Has methods for converting functions to lazily evaluated and/or cached methods. Has methods to convert functions to a few sorts of factory methods. Useful for e.g., converting a namespace of neural network topologies to objects that mimic the behavior of Keras layers.

## Usage
```
import lazy

@lazy.lazy_evaluation(lazy=True, cached=True)
def your_method...
```
The decorated method returns a Data wrapper object. Lazily evaluated and/or cached data can be accessed by the `value` property of the returned Data object.

```
import namespaces

@namespaces.namespace_to_callable_factory
class MyNetworks:
    def network1(*args, **kwargs):
        ...
        return keras.layers.some_layer(some_args)(input)
    
    def network2(*args, **kwargs):
        ...
        return keras.layers.some_layer(some_args)(input)
```

The decorated namespace methods will mimic the behavior of Keras layers. Each method should return a model defined by using the functional API.
