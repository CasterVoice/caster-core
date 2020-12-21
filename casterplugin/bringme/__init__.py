
from dragonfly import Grammar

from castervoice import Plugin

from casterplugin.bringme.program import BringMeProgram


class BringMe(Plugin):
    '''Docstring for BringMePlugin.'''

    _instance = None

    def __init__(self, manager):
        super().__init__(manager)

        if self.state is None:
            self.state = dict()

        self._rules = []

    def get_grammars(self):
        grammar = Grammar(name=self._name)
        bring_me_classes = [BringMeProgram]

        for bring_me_class in bring_me_classes:
            bring_me_type = bring_me_class.type

            entities = self.state.pop(bring_me_type, None)
            rule = bring_me_class(entities)
            grammar.add_rule(rule)
            rule.subscribe(self._update_state)
            self._rules.append(rule)

        return [grammar]

    def get_context(self, desired_context=None):
        return None

    def _update_state(self):
        self.state = {}
        for rule in self._rules:
            self.state[rule.type] = rule.entities

        self.persist_state()
