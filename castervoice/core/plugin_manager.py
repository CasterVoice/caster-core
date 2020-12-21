from importlib import import_module
from inspect import getmembers, isclass
import logging

from castervoice.core.plugin import Plugin


class PluginManager():

    """Docstring for PluginManager. """

    def __init__(self, controller, config):
        """TODO: to be defined.

        :controller: TODO

        """
        self._log = logging.getLogger("castervoice.PluginManager")
        self._controller = controller
        self._plugins = {}

        self.init_plugins(config)

    plugins = property(lambda self: self._plugins,
                       doc="TODO")

    log = property(lambda self: self._log,
                   doc="TODO")

    def init_plugins(self, config):
        """TODO: Docstring for load.

        :config: TODO
        :returns: TODO

        """
        for plugin_config in config:
            plugin_name = plugin_config["name"]

            plugin_module = import_module(plugin_name)

            for name, value in getmembers(plugin_module, isclass):
                if issubclass(value, Plugin) and not value == Plugin:
                    self._log.info("Initializing plugin: %s.%s",
                                   plugin_name, name)
                    plugin_instance = value(self)
                    self._plugins[plugin_name] = plugin_instance

    def load_plugins(self):
        """TODO: Docstring for load_plugins.
        :returns: TODO

        """
        for plugin_name, plugin in self._plugins.items():
            self._log.info("Loading plugin: %s", plugin_name)
            plugin.load()
