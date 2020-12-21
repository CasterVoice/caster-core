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


class Controller:

    """Docstring for Controller. """

    # Class wide singleton instance of Controller
    _controller = None

    def __init__(self, config=None, config_dir=None,
                 dev_mode=False):
        """
            `config`: Dictionary or path to file containing configuration.
        """

        self._config_dir = config_dir
        self._config = self.load_config(config, config_dir)

        self._dev_mode = dev_mode

        self.log.info(" ---- Caster: Initializing ----")
        self._engine = self.init_engine()
        self._dependency_manager = DependencyManager(self)

        self._plugin_manager = PluginManager(self, self._config["plugins"])
        self._context_manager = ContextManager(self, self._config["contexts"])

        self.log.info(" ---- Caster: Loading plugins ----")
        self._plugin_manager.load_plugins()

        Controller._controller = self

    plugin_manager = property(lambda self: self._plugin_manager,
                              doc="TODO")

    dependency_manager = property(lambda self: self._dependency_manager,
                                  doc="TODO")

    engine = property(lambda self: self._engine,
                      doc="TODO")

    dev_mode = property(lambda self: self._dev_mode,
                        doc="Boolean indicating wether development"
                            " mode is active")

    log = property(lambda self: logging.getLogger("castervoice"))

    def load_config(self, config, config_dir):
        """TODO: Docstring for load_config.
        :returns: TODO

        """

        if config is None and config_dir is None:
            self.log.warning("No configuration to load for Controller")
            return None

        config_result = {}

        if isinstance(config, dict):
            self.log.info("Loading configuration: %s", config)
            config_result.update(config)

        if isinstance(config_dir, str):
            try:
                with open(config_dir + "/caster.yml", "r") as ymlfile:
                    config_result.update(yaml.load(ymlfile, Loader=Loader))
            except yaml.YAMLError as error:
                print("Error in configuration file: {}".format(error))

        if "plugins" not in config_result:
            config_result["plugins"] = dict()
        if "contexts" not in config_result:
            config_result["contexts"] = []

        return config_result

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
