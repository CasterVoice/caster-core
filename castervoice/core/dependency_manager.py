import subprocess


class DependencyManager():

    """Docstring for MyClass. """

    def __init__(self, controller):
        """TODO: to be defined. """

    def resolve_plugin(self, plugin_config):
        """Resolve plugin dependencies.

        :plugin_config: TODO
        :returns: TODO

        """
        if "pip" in plugin_config:
            self.resolve_pip(plugin_config["pip"])

    def resolve_pip(self, pip_url):
        """TODO: Docstring for resolve_pip.
        :returns: TODO

        """
        install = subprocess.Popen(['pip', 'install', pip_url])
        install.wait()
