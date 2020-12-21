from dragonfly import Grammar

from castervoice import Plugin
from castervoice.util.dragonfly import CCRRule

from casterplugin.dictation.alphabet import Alphabet


class DictationPlugin(Plugin):
    '''Docstring for DictationPlugin.'''

    def get_grammars(self):
        grammar = Grammar(name=self._name)
        grammar.add_rule(CCRRule.create(Alphabet()))
        return [grammar]

    def get_context(self, desired_context=None):
        return None
