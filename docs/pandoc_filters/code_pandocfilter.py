#!/usr/bin/env python

"""
Pandoc filter to convert code blocks of certain language classes to code class
"""

from pandocfilters import *

def addCodeClass(key, value, format, meta):
  if key == 'CodeBlock':
    [[ident, classes, keyvals], code] = value
    if "python" in classes:
      classes.remove("python")
      classes.append("code")
    return CodeBlock([ident, classes, keyvals], code)

if __name__ == "__main__":
  toJSONFilter(addCodeClass)