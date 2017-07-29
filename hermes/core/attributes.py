import typing

"""
   Copyright 2017 David B. Bracewell

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__attribute_decoders = {}


def set_encoder(attribute: str, encoder: typing.Callable) -> None:
    """
    Sets the encoder for the given attribute
    :param attribute: The attribute to set the encoder for
    :param encoder: The encoder
    :return: None
    """
    if encoder is not None:
        __attribute_decoders[attribute.lower()] = encoder


def get_decoder(attribute: str) -> typing.Callable:
    """
    Gets the encoder for the given attribute
    :param attribute: the attribute to get the encoder for
    :return: Callable method for decoding the value of the given attribute
    """
    attribute = attribute.lower()
    if attribute in __attribute_decoders and __attribute_decoders[attribute] is not None:
        return __attribute_decoders[attribute]
    return lambda x: x
