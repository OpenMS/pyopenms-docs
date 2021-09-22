#!/usr/bin/env python3

"""
Pandoc filter to convert links to relative html pages
(originally for readthedocs) to point to ipynbs now.
"""

from pandocfilters import Link, toJSONFilter


def transformLink(key, value, _, meta):
    if key == 'Link':
        [ident, classes, keyvals], alttext, [dest, typef] = value
        link, sep, rest = dest.partition("#")  # for anchors
        # TODO better checks? use urllib?
        if not (link.startswith("http://") or link.startswith("https://")
         or link.startswith("ftp://")) and link.endswith(".html"):
            link = link.replace(".html", ".ipynb")
            dest = link + sep + rest
        return Link([ident, classes, keyvals], alttext, [dest, typef])


if __name__ == "__main__":
    toJSONFilter(transformLink)
