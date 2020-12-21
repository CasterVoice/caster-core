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

    def install_package(self, package_config):
        """TODO: Docstring for load_package.

        :package_config: TODO
        :returns: TODO

        """
        pip_pkg = package_config["pip"]

        install_command = [sys.executable, '-m', 'pip', 'install']

        if "dev" in package_config:
            install_command.append('-e')

        install_command.append(pip_pkg)
        subprocess.check_call(install_command)

        importlib.invalidate_caches()
        importlib.reload(site)
