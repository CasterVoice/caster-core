from dragonfly.grammar.context import LogicAndContext
from dragonfly import (
        AppContext,
        Context as DragonflyContext
        )


class Context(DragonflyContext):

    """Docstring for myclass. """

    def __init__(self, manager, config):
        """TODO: to be defined. """

        super().__init__()

        self._str = config.pop("name")
        self._name = self._str
        self._enabled = True

        self._contexts = []

        executable = config.pop("executable", None)
        title = config.pop("title", None)
        if title is not None or executable is not None:
            self._contexts.append(AppContext(executable=executable,
                                             title=title))

        # Apply plugin specific contexts
        for plugin_id, desired_context in config.items():
            try:
                plugin_context = manager.get_plugin_context(plugin_id,
                                                            desired_context)
                self._contexts.append(plugin_context)

            except Exception as error:  # pylint: disable=W0703
                manager.log.exception("Error while applying plugin specific"
                                      " context in context '%s'."
                                      " Unable to get context for plugin"
                                      " %s: %s" % (self._name, plugin_id,
                                                   error))

    def matches(self, executable, title, handle):
        return self._enabled and LogicAndContext(*self._contexts) \
            .matches(executable, title, handle)
