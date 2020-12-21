import subprocess


class DependencyManager():

    """Docstring for MyClass. """

    def __init__(self, controller):
        """TODO: to be defined. """

    def resolve_plugin(self, plugin_config, dev_mode=False):
        """Resolve plugin dependencies.

        :plugin_config: TODO
        :returns: TODO

        """
        if "pip" in plugin_config:
            self.resolve_pip(plugin_config["pip"], dev_mode)

    def resolve_pip(self, pip_config, dev_mode=False):
        """TODO: Docstring for resolve_pip.
        :returns: TODO

        """
        command = ['pip', 'install']
        if dev_mode:
            command.append('-e')
        command.append(pip_config.get('url'))

        install = subprocess.Popen(command)
        install.wait()
