from inspect import getmembers, isclass
import copy
import importlib
import logging

from castervoice.core.plugin import Plugin


class PluginManager():

    """Docstring for PluginManager. """

    def __init__(self, controller, config):
        """TODO: to be defined.

        :controller: TODO

        """

        self._initialized = False

        self._controller = controller

        self._plugins = {}

        self._watched_plugin_files = {}

        self._init_plugins(config)

    plugins = property(lambda self: self._plugins.values(),
                       doc="TODO")

    log = property(lambda self: logging.getLogger("castervoice.PluginManager"),
                   doc="TODO")

    def _init_plugins(self, config):
        """Initialize plugins from configuration.

        :config: List of plugin configurations
        :returns: TODO

        """

        if self._initialized:
            return

        local_config = copy.deepcopy(config)

        packages = local_config.pop('packages', [])
        for package_config in packages:
            try:
                self._controller.dependency_manager. \
                    install_package(package_config)
            except Exception:  # pylint: disable=W0703
                self.log.exception("Failed loading package '%s'",
                                   package_config)
                continue

        for plugin_id, plugin_config in local_config.items():
            self.init_plugin(plugin_id, plugin_config)

        self._initialized = True

    def init_plugin(self, plugin_id, plugin_config=None):
        """TODO: Docstring for init_plugin.

        :arg1: TODO
        :returns: TODO

        """

        if plugin_id in self._plugins:
            return

        if plugin_config is not None:
            self.log.warning('Plugin configurations are not implemented yet!')

        try:
            plugin_module = importlib.import_module(plugin_id)
        except ModuleNotFoundError:
            self.log.exception("Failed loading plugin '%s'", plugin_id)

        for name, value in getmembers(plugin_module, isclass):
            if issubclass(value, Plugin) and not value == Plugin \
                    and value.__module__ == plugin_id:
                self.log.info("Initializing plugin: %s.%s",
                              plugin_id, name)
                plugin_instance = value(self)

                # Ensure the plugin correctly set its id
                assert plugin_instance.id == plugin_id

                self._plugins[plugin_id] = plugin_instance

                if self._controller.dev_mode:
                    self._controller.dependency_manager. \
                        watch_plugin(plugin_id, plugin_instance)

    def load_plugins(self):
        """TODO: Docstring for load_plugins.
        :returns: TODO

        """
        for plugin_id, plugin in self._plugins.items():
            self.log.info("Loading plugin: %s", plugin_id)
            plugin.load()

    def unload_plugins(self):
        """TODO: Docstring for unload_plugin.
        :returns: TODO

        """
        for plugin_id, plugin in self._plugins.items():
            self.log.info("Unloading plugin: %s", plugin_id)
            plugin.unload()

    def apply_context(self, plugin_id, context):
        """TODO: Docstring for apply_context.
        :returns: TODO

        """
        self.log.info("Applying context '%s' to plugin '%s'",
                      context, plugin_id)
        self._plugins[plugin_id].apply_context(context)

    def get_context(self, plugin_id, desired_context):
        """TODO: Docstring for get_context.
        :returns: TODO

        """
        return self._plugins[plugin_id].get_context(desired_context)
