#!/usr/bin/env python3

"""
Pandoc filter to convert divs with class="admonition" to ipynb
"""

from pandocfilters import toJSONFilter, RawBlock, Div, stringify

# from: https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions
# admonition is a special case with arbitrary header
admonition_types = ["attention", "caution", "danger", "error", "hint",
                    "important", "note", "tip", "warning", "admonition"]
# keywords in arbitrary admonition header
admonition_subtypes = ["goal"]
# colors and icons for admonition_types (without "admonition") and subtypes
admonition_colors = {"notfound": "#FFA07A",
                     "attention": "#FFA07A",
                     "caution": "#FFA07A",
                     "danger": "#CD5C5C",
                     "error": "#CD5C5C",
                     "hint": "#F0F8FF",
                     "important": "#FFA500",
                     "note": "#BDE5F8",
                     "tip": "#F0E68C",
                     "warning": "#FFA07A",
                     "goal": "#98FB98"}

admonition_icons = {"notfound": "fas fa-exclamation",
                    "attention": "fas fa-exclamation",
                    "caution": "fas fa-exclamation-triangle",
                    "danger": "fas fa-exclamation-triangle",
                    "error": "fas fa-bomb",
                    "hint": "far fa-lightbulb",
                    "important": "fas fa-exclamation",
                    "note": "far fa-sticky-note",
                    "tip": "far fa-lightbulb",
                    "warning": "fas fa-exclamation-triangle",
                    "goal": "far fa-check-square"}


def html(x):
    return RawBlock('html', x)


def admonitions(key, value, fmt, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if any(item in classes for item in admonition_types) and fmt == "ipynb":
            header = stringify(contents[0])
            admonition_subtype = "notfound"
            if "admonition" not in classes:
                admonition_subtype = header.lower()
            else:
                for subtype in admonition_subtypes:
                    if subtype in header.lower():
                        admonition_subtype = subtype
                        break
            newcontents = [html('<div style="background-color: '
                                + admonition_colors[admonition_subtype]
                                + '; margin: 10px 0px; padding:12px;"><p style="font-size: x-large"><i class="'
                                + admonition_icons[admonition_subtype] + '"></i> <b>'
                                + header + '</b></p>')] + contents[1:] + [html('</div>')]
            return Div([ident, classes, kvs], newcontents)


if __name__ == "__main__":
    toJSONFilter(admonitions)
