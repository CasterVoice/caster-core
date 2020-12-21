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
        self._context = None

        self.init_rules()
        self.init_context()

    def init_rules(self):
        """Initialize plugin grammar rules.

        :returns: TODO

        """

        for rule in self.get_rules():
            self._log.info("Instantiating rule: %s(%s)", self._name, rule.name)
            self._rules.append(rule)

    def init_context(self):
        """Initialize Plugin to its default context.

        The plugin's default context can be overridden by user
        configuration.

        :returns: TODO

        """
        try:
            self._context = self.get_context()
        except NotImplementedError:
            return

    def load(self):
        """Load plugin."""
        if not self._loaded:
            self._grammar = Grammar(self._name)
            for rule in self._rules:
                self._grammar.add_rule(rule)
            self._loaded = True

        if not self._grammar.loaded:
            self._grammar.load()

        if self._context is not None:
            # pylint: disable=W0511
            # TODO: We should not access private `_context` here..
            # -> PR towards Dragonfly to dynamically
            # switch a grammars context.
            self._grammar._context = self._context  # pylint: disable=W0212

    def get_rules(self):
        # pylint: disable=no-self-use
        """Gather grammar rules from plugin.

        :returns: List of `Rule`s

        """
        return []

    def get_context(self, desired_context=None):
        """Get plugin context.

        The plugin's default context is returned when `desired_context`
        is `None`.
        `None` can be returned to indicate that no default context exists
        for this plugin.

        If `desired_context` is set returns a context object which matches
        the desired context. It is up to the plugin to document which
        context configurations are available.

        :context_name: TODO
        :context_value: TODO
        :returns: Context

        """

        raise NotImplementedError("Plugin '%s' does not provide any"
                                  " contexts" % (self._name))

    def apply_context(self, context):
        self._context = context
        if self._grammar is not None:
            # pylint: disable=W0511
            # TODO: We should not access private `_context` here..
            # -> PR towards Dragonfly to dynamically
            # switch a grammars context.
            self._grammar._context = context  # pylint: disable=W0212
