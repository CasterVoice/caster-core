import logging

from dragonfly import Grammar


class Plugin():

    """Docstring for MyClass. """

    def __init__(self, manager):
        """TODO: to be defined. """

        self._name = self.__class__.__module__ + '.' + self.__class__.__name__

        self._log = logging.getLogger("castervoice.Plugin({})"
                                      .format(self._name))

        self._manager = manager
        self._loaded = False

        self._rules = []
        self._grammar = None

        self.init_rules()

    def init_rules(self):
        """Initialize plugin grammar rules.

        :returns: TODO

        """

        for rule in self.get_rules():
            self._log.info("Instantiating rule: %s(%s)", self._name, rule.name)
            self._rules.append(rule)

    def load(self):
        """Load plugin."""
        if not self._loaded:
            self._grammar = Grammar(self._name)
            for rule in self._rules:
                self._grammar.add_rule(rule)
            self._loaded = True

        if not self._grammar.loaded:
            self._grammar.load()

    def get_rules(self):
        # pylint: disable=no-self-use
        """TODO: Docstring for get_rules.
        :returns: TODO

        """
        return []
