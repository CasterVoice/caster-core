import importlib
import logging
import site
import subprocess
import sys


class DependencyManager():

    """Docstring for MyClass. """

    def __init__(self):
        """TODO: to be defined. """

        self._log = logging.getLogger("mycastervoice.DependencyManager")

    def install_plugin(self, plugin_config, dev_mode=False):
        """TODO: Docstring for install_plugin.

        :plugin_config: Plugin configuration
        :dev_mode: Install plugin in development mode
        :returns: Module object

        """
        plugin_name = plugin_config.get("name", None)

        if plugin_name is None:
            self._log.error("'name' required for plugin configuration: %s",
                            plugin_config)
            return None

        try:
            plugin_module = importlib.import_module(plugin_name)
        except ModuleNotFoundError:
            self._log.info("Missing dependency for plugin '%s';"
                           " trying to resolve", plugin_name)
            pip_url = plugin_config["pip"]["url"]

            install_command = [sys.executable, '-m', 'pip', 'install']
            if dev_mode:
                install_command.append('-e')
            install_command.append(pip_url)
            subprocess.check_call(install_command)

            importlib.invalidate_caches()
            importlib.reload(site)
        finally:
            plugin_module = importlib.import_module(plugin_name)

        return plugin_module
