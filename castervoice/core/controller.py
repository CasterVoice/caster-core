import logging
import unittest
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


class Controller():

    """Docstring for Controller. """

    # Class wide instance of Controller
    _controller = None

    def __init__(self, config=None):
        """
            `config`: Dictionary or path to file containing configuration.
        """

        self._log = logging.getLogger("castervoice")

        if config is None:
            self._log.warning("Loading Controller without configuration")
        self._config = self.load_config(config)

        self._log.info(" ---- Caster: Initializing ----")
        self._dependency_manager = DependencyManager()
        self._engine = self.init_engine()
        self._plugin_manager = PluginManager(self, self._config["plugins"])
        self._context_manager = ContextManager(self, self._config["contexts"])

        self._log.info(" ---- Caster: Loading plugins ----")
        self._plugin_manager.load_plugins()

    plugin_manager = property(lambda self: self._plugin_manager,
                              doc="TODO")

    dependency_manager = property(lambda self: self._dependency_manager,
                                  doc="TODO")

    engine = property(lambda self: self._engine,
                      doc="TODO")

    def load_config(self, config_path_or_dict):
        """TODO: Docstring for load_config.
        :returns: TODO

        """

        self._log.info("Loading configuration: %s", config_path_or_dict)

        if isinstance(config_path_or_dict, dict):
            config = config_path_or_dict
        else:
            try:
                with open(config_path_or_dict + "/caster.yml", "r") as ymlfile:
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

    def listen(self, on_begin=None, on_recognition=None, on_failure=None):
        """TODO: Docstring for listen.
        :returns: TODO

        """
        with self._engine.connection():
            self._engine.do_recognition(on_begin, on_recognition, on_failure)

    @classmethod
    def get(cls):
        """TODO: Docstring for get_controller.

        :returns: TODO

        """
        return cls._controller


class TestController(unittest.TestCase):
    # pylint: disable=import-outside-toplevel

    def test_speech_recogition(self):
        import sys
        from io import StringIO
        config = {'engine': {'name': 'text'}}
        controller = Controller(config)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            controller.engine.speak("test words")
            output = out.getvalue().strip()
            self.assertEqual('test words', output)
        finally:
            sys.stdout = saved_stdout
