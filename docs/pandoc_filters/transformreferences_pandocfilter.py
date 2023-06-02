#!/usr/bin/env python3

"""
Pandoc filter to convert API references to html links
"""
import re
from pandocfilters import Str, Link, toJSONFilter

def transformReferences(key, value, _, meta):
    if key == 'Code':
        attr, code = value
        if re.search('[a-zA-Z]+(?=\.)|(?<=\.)[a-zA-Z]+', code) is not None:
            text = code.strip('()')
            if re.search('(pyopenms\.)[a-z]+\.', code) is not None:
                url = f'https://pyopenms.readthedocs.io/en/latest/apidocs/_autosummary/pyopenmssubmodules/{text}.html'
            else:
                text = text.strip('~.')
                url = f'https://pyopenms.readthedocs.io/en/latest/apidocs/_autosummary/pyopenms/pyopenms.{text}.html'
            return Link(
                        ['ref-link', ['external-link'], [('rel', 'nofollow')]],
                        [Str(text)],
                        [url, text]
                    )


if __name__ == "__main__":
    toJSONFilter(transformReferences)
