import logging

from dragonfly.grammar.context import LogicOrContext, LogicAndContext

from castervoice.core.context import Context


class ContextManager():

    """Docstring for ContextManager. """

    def __init__(self, controller, config):
        """TODO: to be defined.

        :config: TODO

        """
        self._log = logging.getLogger("castervoice.ContextManager")

        self._controller = controller

        self._config = config
        self._contexts = {}
        self.init_contexts(self._config)

    log = property(lambda self: self._log,
                   doc="TODO")

    def init_contexts(self, config):
        """TODO: Docstring for init_contexts.

        :config: TODO
        :returns: TODO

        """
        plugin_contexts = {}
        for context_config in config:
            try:
                context_name = context_config["name"]
            except KeyError:
                self._log.exception("Configured context requires a name!")
                return

            self._log.info("Initializing context: %s", context_name)

            context_plugins = context_config.pop("plugins", [])
            extends = context_config.pop("extends", None)

            context = Context(self, context_config)

            if isinstance(extends, str):
                extended_context = self._contexts.get(extends)
                if extended_context:
                    self._contexts[context_name] = \
                        LogicAndContext(extended_context, context)
            else:
                self._contexts[context_name] = context

            for plugin_name in context_plugins:
                if plugin_name not in plugin_contexts:
                    plugin_contexts[plugin_name] = []
                plugin_contexts[plugin_name] \
                    .append(self._contexts[context_name])

        # Plugins may be present in various contexts
        for plugin_name in plugin_contexts:
            plugin_manager = self._controller.plugin_manager
            plugin_manager \
                .apply_context(plugin_name,
                               LogicOrContext(*plugin_contexts[plugin_name]))

    def get_plugin_context(self, plugin_name, desired_context):
        """TODO: Docstring for get_plugin_context.
        :returns: TODO

        """
        return self._controller.plugin_manager.plugins[plugin_name] \
            .get_context(desired_context)
