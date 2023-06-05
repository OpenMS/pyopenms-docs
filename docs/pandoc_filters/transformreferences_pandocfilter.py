#!/usr/bin/env python3

"""
Pandoc filter to convert API references to html links
"""
import re
import sys
from pandocfilters import Str, Link, toJSONFilter

def transformReferences(key, value, fmt, meta):
    if key == 'Code':
        [[ident, classes, kvs], code] = value
        kvs = {key: value for key, value in kvs}
        role = kvs.get("role", "")
        if role[0:3] == "py:":
            sys.stderr.write(code)
            if re.search('(pyopenms\.)[a-z]+\.', code) is not None:
                url = f'https://pyopenms.readthedocs.io/en/latest/apidocs/_autosummary/pyopenmssubmodules/{code}.html'
            else:
                code = code.strip('~.')
                url = f'https://pyopenms.readthedocs.io/en/latest/apidocs/_autosummary/pyopenms/pyopenms.{code}.html'
            return Link(
                        ['ref-link', ['external-link'], [('rel', 'nofollow')]],
                        [Str(code)],
                        [url, code]
                    )
        return None

if __name__ == "__main__":
    toJSONFilter(transformReferences)
