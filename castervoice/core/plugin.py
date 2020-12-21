import logging
import os
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Plugin():

    """Docstring for MyClass. """

    def __init__(self, manager):
        """TODO: to be defined. """

        self._id = self.__class__.__module__
        class_name = self.__class__.__name__
        self._name = "{}.{}".format(self._id, class_name)

        self._manager = manager
        self._loaded = False

        self._grammars = []
        self._context = None

        self._state = None
        if self._manager and self._manager.state_directory:
            self._state = PluginState(os.path
                                      .join(self._manager.state_directory,
                                            "%s.state" % (self._id)))

        self._init_context()

    id = property(lambda self: self._id,
                  doc="TODO")

    name = property(lambda self: self._name,
                    doc="TODO")

    log = property(lambda self: logging.getLogger("castervoice.Plugin({})"
                                                  .format(self._name)),
                   doc="TODO")

    def set_state(self, data):
        self._state.data = data

    state = property(lambda self: self._state.data if self._state else None,
                     set_state,
                     doc="TODO")

    def persist_state(self):
        self._state.persist()

    def _init_context(self):
        """Initialize Plugin to its default context.

        The plugin's default context can be overridden by user
        configuration.

        :returns: TODO

        """
        try:
            self._context = self.get_context()
        except NotImplementedError:
            return

    def load(self):
        """Load plugin."""
        if not self._loaded:
            self.log.info("Loading ...")

            assert not self._grammars

            for grammar in self.get_grammars():
                self.log.info("Adding grammar: %s(%s)",
                              self._name, grammar.name)
                self._grammars.append(grammar)

            self.apply_context()

            for grammar in self._grammars:
                grammar.load()

            self._loaded = True

    def unload(self):
        """TODO: Docstring for unload.
        :returns: TODO

        """
        if self._loaded:
            self.log.info("Unloading ...")
            for grammar in self._grammars:
                grammar.unload()
                del grammar

            self._grammars = []
            self._loaded = False

    def enable(self):
        """TODO: Docstring for enable.
        :returns: TODO

        """
        for grammar in self._grammars:
            self.log.info("Enabling grammar: %s(%s)",
                          self._name, grammar.name)
            grammar.enable()

    def disable(self):
        """TODO: Docstring for disable.
        :returns: TODO

        """
        for grammar in self._grammars:
            self.log.info("Disabling grammar: %s(%s)",
                          self._name, grammar.name)
            for rule in grammar.rules:
                rule.disable()
            grammar.disable()

    def get_grammars(self):
        # pylint: disable=no-self-use
        """Gather plugins' grammars.

        :returns: List of `Grammar`s

        """
        return []

    def get_context(self, desired_context=None):
        """Get plugin context.

        The plugin's default context is returned when `desired_context`
        is `None`.
        `None` can be returned to indicate that no default context exists
        for this plugin.

        If `desired_context` is set returns a context object which matches
        the desired context. It is up to the plugin to document which
        context configurations are available.

        :context_name: TODO
        :context_value: TODO
        :returns: Context

        """

        raise NotImplementedError("Plugin '%s' does not provide any"
                                  " contexts" % (self._name))

    def apply_context(self, context=None):
        if context is not None:
            self._context = context

        if self._context is not None:
            self.log.info("Applying context '%s'", self._context)
            for grammar in self._grammars:
                # pylint: disable=W0511
                # TODO: We should not access private `_context` here..
                # -> PR towards Dragonfly to dynamically
                # switch a grammars context.
                grammar._context = self._context  # pylint: disable=W0212

            self._apply_context(context)

    def _apply_context(self, context):
        """TODO: Docstring for _apply_context.

        Can be overridden by child classes.

        :context: TODO
        :returns: TODO

        """


class PluginFile:

    def __init__(self, file_path):

        self._data = None
        self._type = self.__class__.__name__

        try:
            with open(file_path, "r") as ymlfile:
                self._data = yaml.load(ymlfile, Loader=Loader)
        except yaml.YAMLError as error:
            print("Error in {} file: {}".format(self._type, error))
        except FileNotFoundError:
            pass

    def set_data(self, new_data):
        self._data = new_data

    def get_data(self):
        return self._data

    data = property(get_data, set_data)


class PluginState(PluginFile):

    def __init__(self, file_path):
        self._file_path = file_path
        super().__init__(file_path)

    def persist(self):
        with open(self._file_path, 'w') as ymlfile:
            ymlfile.write(yaml.dump(self._data, Dumper=Dumper))
