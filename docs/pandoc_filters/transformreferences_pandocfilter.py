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
            # Note: use stderr for debugging
            #sys.stderr.write(code)

            # remove ~. which is only used by sphinx to only display the last component of the listed class/function name
            # i.e., get for pyopenms.MSSpectrum.get
            # TODO think about replicating this behaviour
            code = code.strip('~.')

            # Due to the current structure of C extensions being pulled into the parent module, and the rest being
            # handled as submodules and generated into a subfolder by sphinx
            # https://github.com/OpenMS/pyopenms-docs/blob/8c1f16113f36b5de98001fef2f39ea75f984d07f/docs/source/apidocs/index.rst?plain=1#L14
            # we need to create different links depending on the class/function name. This could be changed in the future
            # if the structure is changed.
            # TODO the following will not work for uppercase submodules like Constants which we still have but should change to lower case
            # otherwise we cannot distinguish from class "namespaces"
            if re.search('(pyopenms\.)[a-z]+\.', code) is not None:
                url = f'https://pyopenms.readthedocs.io/en/latest/apidocs/_autosummary/pyopenmssubmodules/{code}.html'
            else:
                url = f'https://pyopenms.readthedocs.io/en/latest/apidocs/_autosummary/pyopenms/pyopenms.{code}.html'
            return Link(
                        ['ref-link', ['external-link'], [('rel', 'nofollow')]],
                        [Str(code)],
                        [url, code]
                    )
        return None

if __name__ == "__main__":
    toJSONFilter(transformReferences)
