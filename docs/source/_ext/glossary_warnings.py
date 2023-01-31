from docutils import nodes
from typing import cast
from sphinx import addnodes
from sphinx.util import logging

logger = logging.getLogger(__name__)


class FindTextNodesVisitor(nodes.SparseNodeVisitor):

    def __init__(self, document, words):
        super().__init__(document)
        self.words = words

    def visit_Text(self, node):
        for substring in self.words:
            if substring in node.astext():
                logger.warn(logging.get_node_location(node) +
                  ' Potential glossary terms found in the text node. First match:' +
                  substring)
                break

    def visit_literal_block(self, node):
        self.in_literal_block = True
        raise nodes.SkipChildren

    def visit_term(self, node):
        self.in_term = True
        raise nodes.SkipChildren


def collect_glossary_entries_doc(app, doctree):
    for glossary in doctree.findall(addnodes.glossary):
        definition_list = cast(nodes.definition_list, glossary[0])
        for t in definition_list:
            app.config.forbidden_words.update(
                [" " + w + " " 
                    for w in cast(nodes.term, t).astext().split("\n\n")[0].split("\n")])


def check_forbidden_words(app, doctree, docname):
    if ("_autosummary" not in docname):
        visitor = FindTextNodesVisitor(doctree, app.config.forbidden_words)
        doctree.walk(visitor)


def setup(app):
    app.add_config_value('forbidden_words', set(), 'env')
    app.connect('doctree-resolved', check_forbidden_words)
    app.connect('doctree-read', collect_glossary_entries_doc)
    return {'version': '0.1'}
