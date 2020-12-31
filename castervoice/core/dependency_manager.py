import builtins
import importlib
import logging
import os
import site
import subprocess
import sys

from dragonfly import get_current_engine


class DependencyManager():

    """Docstring for MyClass. """

    def __init__(self, controller):
        """TODO: to be defined. """

        self._controller = controller

        if self._controller.dev_mode:
            self.reloader = ModuleReloader()

    log = property(lambda self:
                   logging.getLogger("castervoice.DependencyManager"),
                   doc="TODO")

    def install_package(self, package_config):
        """TODO: Docstring for load_package.

        :package_config: TODO
        :returns: TODO

        """
        pip_pkg = package_config["pip"]

        install_command = [sys.executable, '-m', 'pip', 'install']

        if self._controller.dev_mode:
            install_command.append('-e')

        install_command.append(pip_pkg)
        subprocess.check_call(install_command)

        importlib.invalidate_caches()
        importlib.reload(site)

    def watch_plugin(self, plugin_id, plugin_instance):
        """TODO: Docstring for watch_plugin.

        :arg1: TODO
        :returns: TODO

        """
        self.reloader.watched_plugin_modules[plugin_id] = plugin_instance


class ModuleReloader(importlib.abc.MetaPathFinder):
    """
        Credits:
            Jon Parise: https://github.com/jparise/python-reloader
    """

    def __init__(self):
        self._baseimport = builtins.__import__
        builtins.__import__ = self._import

        self._parent = None

        # Dictionary where key is the module name (e.g.
        # 'casterplugin.dictation') and value contains the entries
        # `module` (module object) and `dependencies`
        # (list of modules which the module depends on)
        self._modules = dict()

        self.watched_plugin_modules = dict()

        get_current_engine().create_timer(self.reload, 10)

    log = property(lambda self:
                   logging.getLogger("castervoice.ModuleReloader"),
                   doc="TODO")

    def __del__(self):
        builtins.__import__ = self._baseimport

    # pylint: disable=too-many-arguments,redefined-builtin
    def _import(self, name, globals=None, locals=None, fromlist=(), level=0):
        """
            __import__() replacement function that tracks module dependencies.
        """
        # Track our current parent module.  This is used to find our current
        # place in the dependency graph.
        parent = self._parent
        self._parent = name

        # Perform the actual import work using the base import function.
        base = self._baseimport(name, globals, locals, fromlist, level)

        if base is not None:
            m = base

            # We manually walk through the imported hierarchy because the
            # import function only returns the top-level package reference for
            # a nested import statement (e.g. 'package' for
            # `import package.module`) when no fromlist has been specified.
            # It's possible that the package might not have all of its
            # descendents as attributes, in which case we fall back to using
            # the immediate ancestor of the module instead.
            if fromlist is None:
                for component in name.split('.')[1:]:
                    try:
                        m = getattr(m, component)
                    except AttributeError:
                        m = sys.modules[m.__name__ + '.' + component]

            module = self._modules.setdefault(name, dict())
            module["module"] = m

            if parent is not None:
                parent_module = self._modules.setdefault(parent, dict())
                # If this is a nested import for a reloadable (source-based)
                # module, we append ourself to our parent's dependency list.
                if hasattr(m, '__file__'):
                    deps = parent_module.setdefault("dependencies", [])
                    deps.append(m)

        # Lastly, we always restore our global _parent pointer.
        self._parent = parent

        return base

    def reload(self):
        """
            Reloads all modules which have been modified since
            the last time. Additionally reloads a plugin if the
            changed module is part of the plugin module/package.
        """
        changed_modules = []
        plugins_to_reload = []

        self.log.debug('Checking for changed modules to be reloaded')

        for name, info in self._modules.items():

            if 'module' not in info or not name:
                continue

            m = info['module']

            # It is a package
            if not hasattr(m, '__file__'):
                continue

            if 'last_changed' not in info:
                self.set_changed_time(name)
                continue

            if os.path.getmtime(m.__file__) > info['last_changed']:
                changed_modules.append(m)
                self.set_changed_time(name)

                for plugin_id, plugin_instance in self. \
                        watched_plugin_modules.items():
                    if str.startswith(name, plugin_id):
                        plugins_to_reload.append(plugin_instance)

        if changed_modules:
            for plugin in plugins_to_reload:
                self.log.info('Disabling and unloading plugin %s', plugin)
                plugin.disable()
                plugin.unload()

            for rel in changed_modules:
                self.log.info('Reloading changed module %s', rel)
                importlib.reload(rel)

            for plugin in plugins_to_reload:
                self.log.info('Reloading plugin module %s', plugin.__module__)
                importlib.reload(sys.modules[plugin.__module__])
                plugin.load()

    def set_changed_time(self, name):
        m = self._modules[name]['module']
        last_changed = os.path.getmtime(m.__file__)
        self._modules[name]['last_changed'] = last_changed
