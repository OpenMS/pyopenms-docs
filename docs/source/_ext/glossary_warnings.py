from docutils import nodes
from typing import cast
from sphinx import addnodes
from sphinx.errors import SphinxError
from sphinx.domains.std import Glossary
from sphinx.util import logging

logger = logging.getLogger(__name__)

class FindTextNodesVisitor(nodes.SparseNodeVisitor):
    def __init__(self, document, words):
        super().__init__(document)
        self.words = words
        
    def visit_Text(self, node):
        for substring in self.words:
            if substring in node.astext():
                logger.warn(logging.get_node_location(node) + ' Potential glossary terms found in the text node. First match:' + substring)
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
            app.config.forbidden_words.update([" " + w + " " for w in cast(nodes.term, t).astext().split("\n\n")[0].split("\n")])

def check_forbidden_words(app, doctree, docname):
    if (not "_autosummary" in docname):
        visitor = FindTextNodesVisitor(doctree, app.config.forbidden_words)
        doctree.walk(visitor)
        #for node in doctree.findall(nodes.Text):
        #    if any(substring in node.astext() for substring in app.config.forbidden_words):
        #        logger.warn(logging.get_node_location(node) + ' Potential glossary term found in the document.')
                

def setup(app):
    app.add_config_value('forbidden_words', set(), 'env')
    app.connect('doctree-resolved', check_forbidden_words)
    app.connect('doctree-read', collect_glossary_entries_doc)
    #app.add_domain(Glossary)
    return {'version': '0.1'}