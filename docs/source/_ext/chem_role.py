from docutils.nodes import math


def chem_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    latex = rf'\ce{{{text}}}'
    node = math(rawtext, latex, **options)
    return [node], []
