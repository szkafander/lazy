# This is a layer grouper class. It allows grouping Tensorflow ops into keras
# layers without having to inherit from keras.models.Model. This allows keeping
# the .input and .output attributes, as well as for usage in functional API
# Models.
#
# Copyright (c) 2019 Pal Toth
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


from tensorflow import Tensor

from tensorflow.keras.models import Model
from typing import Callable


class LayerGroup:

    def __init__(self, name: str, op: Callable) -> None:
        """ 
        Constructor.

        Specify a name and an op. The name will appear in model summaries
        and model graphs as specified here. The op argument is a Callable that
        takes a Tensor and returns a Tensor.

        :param name: The name of the layer group. Use CamelCase for consistency
            with Keras layer names.
        :type name: str
        :param op: A Callable that takes a Tensor and returns a Tensor. The
            returned tensor should represent a connected graph that you would 
            normally pass to keras.models.Model as an output.
        :type op: Callable
        
        """
        self.name = name
        self.op = op

    def __call__(self, input_tensor: Tensor) -> Tensor:
        """ When a LayerGroup instance is called on a Tensor, it returns the 
        Tensor output of a Keras model. Use the LayerGroup instance as you
        would normally use a Keras layer.

        :param input_tensor: The input Tensor of the wrapped model.
        :type input_tensor: tensorflow.Tensor
        :returns: The Tensor result of self.op(input_tensor), but with 
            self.name as layer name.
        :rtype: tensorflow.Tensor
        
        """
        class GroupWrapper(Model): pass
        GroupWrapper.__name__ = self.name

        return GroupWrapper(
                        inputs=[input_tensor],
                        outputs=[self.op(input_tensor)]
                    )(input_tensor)
