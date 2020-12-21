from inspect import getmembers, isclass
import copy
import importlib
import logging
import os

from castervoice.core.plugin.plugin import Plugin


class PluginManager():

    """

    Plugins are managed from the central Plugin Manager.

    Each plugin is referenced by a `plugin_id` which is
    resembled by the plugin's module path (e.g.
    `casterplugin.dictation`).


    """

    def __init__(self, controller, config, state_directory):
        """

        :param controller: Caster controller.
        :param config: Plugins configuration.
        :param state_directory: Directory used for plugin states.

        """

        self._initialized = False

        self._controller = controller

        self._plugins = {}

        self._state_directory = state_directory
        if self._state_directory is not None:
            if not os.path.exists(self._state_directory):
                os.mkdir(self._state_directory)
            elif not os.path.isdir(self._state_directory):
                raise NotADirectoryError("State directory '%s' must be a"
                                         " directory!"
                                         % (self._state_directory))

        self._init_plugins(config)

    plugins = property(lambda self: self._plugins.values(),
                       doc="Retrieve list of initialized plugins.")

    log = property(lambda self: logging.getLogger("castervoice.PluginManager"),
                   doc="Get class logger.")

    state_directory = property(lambda self: self._state_directory,
                               doc="Get plugin state directory.")

    def _init_plugins(self, config):
        """Initialize plugins from configuration.

        :config: List of plugin configurations

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
        """Initialize plugin.

        :param plugin_id: Plugin Id

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
        """Load all initialized plugins."""
        for plugin_id, plugin in self._plugins.items():
            self.log.info("Loading plugin: %s", plugin_id)
            plugin.load()

    def unload_plugins(self):
        """Unload all initialized plugins."""
        for plugin_id, plugin in self._plugins.items():
            self.log.info("Unloading plugin: %s", plugin_id)
            plugin.unload()

    def apply_context(self, plugin_id, context):
        """Apply context to plugin with `plugin_id`

        Overrides existing context.

        :param plugin_id: Plugin Id
        :param context: Context object to be applied

        """
        self.log.info("Applying context '%s' to plugin '%s'",
                      context, plugin_id)
        self._plugins[plugin_id].apply_context(context)

    def get_context(self, plugin_id, desired_context):
        """Get context of plugin with `plugin_id`.

        :param plugin_id: Plugin Id
        :param desired_context: Desired plugin context configuration
        :returns: Context

        """
        return self._plugins[plugin_id].get_context(desired_context)
