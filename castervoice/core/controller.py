# Since Python >= 3.7
import importlib.resources as pkg_resources
import logging
import os
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from dragonfly import get_engine

import casterconfig
from castervoice.core.plugin import PluginManager
from castervoice.core.dependency_manager import DependencyManager
from castervoice.core.context_manager import ContextManager


class Controller:

    """Docstring for Controller. """

    # Class wide singleton instance of Controller
    _controller = None

    def __init__(self, config=None, config_dir=None,
                 plugin_state_dir=None, dev_mode=False):
        """
            `config`: Dictionary or path to file containing configuration.
        """

        self._config_dir = config_dir
        self._config = self.load_config(config, config_dir)

        self._dev_mode = dev_mode

        self.log.info(" ---- Caster: Initializing ----")
        self._engine = self.init_engine()
        self._dependency_manager = DependencyManager(self)

        self._plugin_manager = PluginManager(self, self._config["plugins"],
                                             plugin_state_dir)
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
        """

        Load configuration. If no `caster.yml` exists in `config_dir`
        it is created only if the parent directory of `config_dir`
        is an existing directory.

        :returns: Configuration dictionary

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
                config_file = config_dir + "/caster.yml"
                with open(config_file, "r", encoding='UTF-8') as ymlfile:
                    config_from_file = yaml.load(ymlfile, Loader=Loader)
                    if config_from_file is not None:
                        config_result.update(config_from_file)
            except yaml.YAMLError as error:
                print("Error in configuration file: {}".format(error))
            except FileNotFoundError as error:
                self.log.info("Configuration file was not found in specified "
                              "path '%s': %s ",
                              config_dir, error)
                self.log.info("Attempting to create configuration...")
                self.create_config(config_dir)
                return self.load_config(config, config_dir)

        if "plugins" not in config_result:
            config_result["plugins"] = {}
        if "contexts" not in config_result:
            config_result["contexts"] = []

        return config_result

    def create_config(self, config_dir):
        if not os.path.isdir(config_dir):

            if not os.path.isdir(os.path.dirname(config_dir)):
                raise FileNotFoundError("Configuration directory base path "
                                        "'%s' does not exist!" %
                                        os.path.dirname(config_dir))

            os.mkdir(config_dir)

        config_file = config_dir + "/caster.yml"
        with open(config_file, 'w', encoding='UTF-8') as config_file:
            config_file.write(pkg_resources.read_text(casterconfig,
                                                      'caster.yml'))

        self.log.info("Successfully created configuration in '%s'", config_dir)

    def init_engine(self):
        """Initialize engine from configuration

        :returns: Engine object
        """

        for engine_type in ['kaldi', 'natlink', 'sapi5', 'text']:
            engine_config = self._config["engine"].get(engine_type)
            if engine_config is not None:
                break

        if engine_config is None:
            raise ValueError("Missing `engine` configuration! Received '%s'"
                             % self._config["engine"])

        dragonfly_engine = engine_config.get('options', {})
        dragonfly_engine.update(dict([('name', engine_type)]))

        return get_engine(**dragonfly_engine)

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
