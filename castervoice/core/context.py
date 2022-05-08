from dragonfly.grammar.context import LogicAndContext
from dragonfly import (
        AppContext,
        Context as DragonflyContext
        )


class Context(DragonflyContext):

    def __init__(self, name, manager):
        """TODO: to be defined. """

        super().__init__()

        self._str = name
        self._name = self._str
        self._enabled = True

        self._contexts = []

        self.manager = manager

    def matches(self, executable, title, handle):
        return self._enabled and LogicAndContext(*self._contexts) \
            .matches(executable, title, handle)


class ConfigContext(Context):

    """Interpret context from Caster configuration"""

    def __init__(self, manager, config):
        """TODO: to be defined. """

        super().__init__(config.pop("name"), manager)

        executable = config.pop("executable", None)
        title = config.pop("title", None)
        if title is not None or executable is not None:
            self._contexts.append(AppContext(executable=executable,
                                             title=title))

        # Apply plugin specific contexts
        for plugin_id, desired_state in config.items():

            self._contexts.append(
                    PluginContext(manager, plugin_id, desired_state))


class PluginContext(Context):

    """Lazily loads plugin contexts on matching

    Plugin contexts may not be available at start up
    while plugins are still loaded sequentially.

    """

    def __init__(self, manager, plugin_id, desired_state):

        super().__init__(plugin_id, manager)

        self._plugin_id = plugin_id
        self._desired_state = desired_state

        self._loaded = False

    def load(self):
        try:
            plugin_context = self.manager \
                .get_plugin_context(self._plugin_id,
                                    self._desired_state)
            self._contexts.append(plugin_context)

        except Exception as error:  # pylint: disable=W0703
            self.manager.log.exception(
                    "Error while applying plugin specific"
                    f" context in context '{self._name}'."
                    " Unable to get context for plugin"
                    f" {self._plugin_id}: {error}")

    def matches(self, executable, title, handle):
        if not self._loaded:
            self.load()
            self._loaded = True

        return super().matches(executable, title, handle)
