import logging
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from dragonfly import get_engine

from castervoice.core.plugin_manager import PluginManager
from castervoice.core.dependency_manager import DependencyManager


logging.basicConfig(level="INFO")


def _on_begin():
    print("Speech start detected.")


def _on_recognition(words):
    message = u"Recognized: %s" % u" ".join(words)

    print(message)


def _on_failure():
    print("Sorry, what was that?")


class Controller():

    """Docstring for Controller. """

    def __init__(self):
        """TODO: to be defined. """

        self._log = logging.getLogger("castervoice")

        self._config = self.load_config("user_config_dir/caster.yml")

        self._log.info(" ---- Caster: Initializing ----")
        self._dependency_manager = DependencyManager(self)
        self._engine = self.init_engine()
        self._plugin_manager = PluginManager(self, self._config["plugins"])

        self._log.info(" ---- Caster: Loading plugins ----")
        self._plugin_manager.load_plugins()

        with self._engine.connection():
            self._engine.do_recognition(_on_begin, _on_recognition,
                                        _on_failure)

    plugin_manager = property(lambda self: self._plugin_manager,
                              doc="TODO")

    dependency_manager = property(lambda self: self._dependency_manager,
                                  doc="TODO")

    def load_config(self, config_path):
        """TODO: Docstring for load_config.
        :returns: TODO

        """

        self._log.info("Loading configuration: %s", config_path)

        try:
            with open(config_path, "r") as ymlfile:
                cfg = yaml.load(ymlfile, Loader=Loader)
        except yaml.YAMLError as error:
            print("Error in configuration file: {}".format(error))

        return cfg

    def init_engine(self):
        """TODO: Docstring for function.

        :arg1: TODO
        :returns: TODO

        """

        return get_engine(**self._config["engine"])
