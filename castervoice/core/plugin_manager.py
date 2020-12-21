from importlib import import_module
from inspect import getmembers, isclass
import hashlib
import logging
import pkgutil

from dragonfly import get_current_engine

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

        self._watched_plugin_files = {}

        self.init_plugins(config)

    plugins = property(lambda self: self._plugins,
                       doc="TODO")

    log = property(lambda self: self._log,
                   doc="TODO")

    def init_plugins(self, config):
        """Initialize plugins from configuration.

        :config: List of plugin configurations
        :returns: TODO

        """
        for plugin_config in config:

            plugin_name = plugin_config["name"]

            dev_mode = False
            if "dev" in plugin_config:
                dev_mode = True

            try:
                plugin_module = import_module(plugin_name)
            except ModuleNotFoundError:
                self._log.info("Missing dependency for plugin '%s';"
                               " trying to resolve",
                               plugin_name)
                self._controller.dependency_manager \
                    .resolve_plugin(plugin_config, bool(dev_mode))
                plugin_module = import_module(plugin_name)

            for name, value in getmembers(plugin_module, isclass):
                if issubclass(value, Plugin) and not value == Plugin:
                    self._log.info("Initializing plugin: %s.%s",
                                   plugin_name, name)
                    plugin_instance = value(self)
                    self._plugins[plugin_name] = plugin_instance

                    if bool(dev_mode):
                        self.watch_plugin(plugin_name, plugin_module.__path__)

        if bool(self._watched_plugin_files):
            get_current_engine().create_timer(self._watch_plugin_files, 10)

    def load_plugins(self):
        """TODO: Docstring for load_plugins.
        :returns: TODO

        """
        for plugin_name, plugin in self._plugins.items():
            self._log.info("Loading plugin: %s", plugin_name)
            plugin.load()

    def apply_context(self, plugin_name, context):
        """TODO: Docstring for apply_context.
        :returns: TODO

        """
        self._log.info("Applying context '%s' to plugin '%s'",
                       context, plugin_name)
        self._plugins[plugin_name].apply_context(context)

    def watch_plugin(self, plugin_name, plugin_path):
        for file_path in self._watch_get_files_from_path(plugin_path):
            if file_path not in self._watched_plugin_files:
                self._watched_plugin_files[file_path] = \
                    {"plugins": [],
                     "hash": get_md5_hash(file_path)}
            if plugin_name not in \
                    self._watched_plugin_files[file_path]["plugins"]:
                self._watched_plugin_files[file_path]["plugins"] \
                    .append(plugin_name)

    # pylint: disable=W0511
    # TODO: move this into a utility library
    def _watch_get_files_from_path(self, plugin_path, files=None):
        """Returns all module files from a path.

        Appends to `files` if it is not empty.

        """
        if files is None:
            files = []

        files.append("{}/__init__.py".format(plugin_path[0]))

        for mod in pkgutil.walk_packages(plugin_path):
            path = "{}/{}".format(plugin_path[0], mod.name)
            if mod.ispkg:
                self._watch_get_files_from_path([path], files)
            else:
                files.append("{}.py".format(path))

        return files

    def _watch_plugin_files(self):
        for file_path in self._watched_plugin_files:
            new_md5 = get_md5_hash(file_path)
            if new_md5 != self._watched_plugin_files[file_path]["hash"]:
                for plugin_name in self \
                        ._watched_plugin_files[file_path]["plugins"]:
                    self._log.info("Reloading plugin '%s' due"
                                   " to changed file '%s'.",
                                   plugin_name, file_path)
                    self._plugins[plugin_name].reload()
                    self._watched_plugin_files[file_path]["hash"] = new_md5


# pylint: disable=W0511
# TODO: move this into a utility library
#       rename to get_file_md5_hash
def get_md5_hash(file_path):
    m = hashlib.md5()
    with open(file_path, 'rb') as handle:
        m.update(handle.read())
    return m.hexdigest()
