import tempfile
import unittest

from castervoice.core.plugin import Plugin


class MockPlugin(Plugin):
    def get_context(self, desired_context=None):
        """

        Well this.

        :param desired_context:  (Default value = None)

        """
        return None


class MockPluginManager():
    # pylint: disable=consider-using-with
    d = tempfile.TemporaryDirectory()
    state_directory = d.name


class TestPlugin(unittest.TestCase):

    def test_initialization(self):
        MockPlugin(None)

    def test_state(self):
        manager = MockPluginManager()
        plugin = MockPlugin(manager)

        state = {'test': 3}
        plugin.state = state
        self.assertEqual(plugin.state, state)

        del plugin
        plugin = MockPlugin(manager)
        self.assertEqual(plugin.state, None)

        plugin.state = state
        plugin.persist_state()

        del plugin
        plugin = MockPlugin(manager)
        self.assertEqual(plugin.state, state)
