import unittest

from castervoice.core.plugin import Plugin


class MockPlugin(Plugin):
    def get_context(self, desired_context=None):
        """

        Well this.

        :param desired_context:  (Default value = None)

        """
        return None


class TestPlugin(unittest.TestCase):

    def test_initialization(self):
        MockPlugin(None)
