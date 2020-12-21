import logging
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from dragonfly import get_engine

from castervoice.core.plugin_manager import PluginManager
from castervoice.core.dependency_manager import DependencyManager
from castervoice.core.context_manager import ContextManager


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

    # Class wide instance of Controller
    _controller = None

    def __init__(self):
        """TODO: to be defined. """

        self._log = logging.getLogger("castervoice")

        self._config = self.load_config("config/default.yml")

        self._log.info(" ---- Caster: Initializing ----")
        self._dependency_manager = DependencyManager(self)
        self._engine = self.init_engine()
        self._plugin_manager = PluginManager(self, self._config["plugins"])
        self._context_manager = ContextManager(self, self._config["contexts"])

        self._log.info(" ---- Caster: Loading plugins ----")
        self._plugin_manager.load_plugins()

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
                config = yaml.load(ymlfile, Loader=Loader)
        except yaml.YAMLError as error:
            print("Error in configuration file: {}".format(error))

        for config_element in ["contexts", "plugins"]:
            if config_element not in config:
                config[config_element] = []
        return config

    def init_engine(self):
        """TODO: Docstring for function.

        :arg1: TODO
        :returns: TODO

        """

        return get_engine(**self._config["engine"])

    def listen(self):
        """TODO: Docstring for listen.
        :returns: TODO

        """
        with self._engine.connection():
            self._engine.do_recognition(_on_begin, _on_recognition,
                                        _on_failure)

    @classmethod
    def get(cls):
        """TODO: Docstring for get_controller.

        :returns: TODO

        """
        if cls._controller is None:
            cls._controller = Controller()
        return cls._controller
