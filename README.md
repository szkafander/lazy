# lazy
A trivial Python utility for converting methods to lazily evaluated and/or cached methods.

## Usage
```
import lazy

@lazy.lazy_evaluation(lazy=True, cached=True)
def your_method...
```
The decorated method returns a Data wrapper object. Lazily evaluated and/or cached data can be accessed by the `value` property of the returned Data object.
