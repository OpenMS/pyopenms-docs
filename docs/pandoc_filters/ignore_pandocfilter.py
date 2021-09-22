#!/usr/bin/env python3

"""
Pandoc filter to ignore elements when having class ignore:
e.g.
.. code-block:: python
    :class: ignore

    print("Foo")

.. imade:: foo.png
    :class: ignore
"""

from pandocfilters import CodeBlock, Image, Null, toJSONFilter, Str


def ignore(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value
        if "ignore" in classes:
            return Null()  # return Null block
        return CodeBlock(*value)
    if key == 'Image':
        [ident, classes, keyvals], caption, [dest, typef] = value
        if "ignore" in classes:
            return Str("")  # return empty string. Cannot return Block here.
        return Image(*value)


if __name__ == "__main__":
    toJSONFilter(ignore)
