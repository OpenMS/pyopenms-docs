#!/usr/bin/env python3

"""
Pandoc filter to convert links to relative html pages
(originally for readthedocs) to point to ipynbs now.
"""
import pandocfilters
from pandocfilters import Str, Link, toJSONFilter, CodeBlock, Para, Code


def transformReferences(key, value, _, meta):
    if key == 'Code':
        attr, content = value
        if content.startswith('~.'):
            text = content[2:]
            return Link(
                        ['ref-link', ['external-link'], [('rel', 'nofollow')]],
                        [Str(text)],
                        [f'https://pyopenms.readthedocs.io/en/latest/apidocs/_autosummary/pyopenms/pyopenms.{text.strip("()")}.html', text]
                    )


if __name__ == "__main__":
    toJSONFilter(transformReferences)
