#!/usr/bin/env python3

"""
Pandoc filter to ignore elements when having class ignore:
e.g.
.. code-block:: python
    :class: ignore

    print("Foo")
"""

from pandocfilters import *

def ignore(key, value, format, meta):
  if key == 'CodeBlock':
    [[ident, classes, keyvals], code] = value
    #sys.stderr.write(str(classes))
    if "ignore" in classes:
      return Null()
    return CodeBlock([ident, classes, keyvals], code)

if __name__ == "__main__":
  toJSONFilter(ignore)