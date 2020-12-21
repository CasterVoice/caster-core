import sys
from subprocess import Popen

from dragonfly import Window

from casterplugin.bringme.base import BringMeBase


class BringMeProgram(BringMeBase):

    """Docstring for MyClass. """

    type = "program"

    def _bring_me(self, entity):
        """TODO: Docstring for bring_me.
        :returns: TODO

        """
        if sys.platform == "darwin":
            Popen(['open', '-a', entity])
        else:
            Popen(entity)

    def _bring_me_as(self, entity_name):
        """TODO: Docstring for bring_me_as.
        :returns: TODO

        """
        program = Window.get_foreground().executable
        self._entities.update({str(entity_name): str(program)})
