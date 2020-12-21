import logging
import re

from dragonfly import (
        DictList, MappingRule, Function,
        DictListRef, Literal, Dictation
    )


class BringMeBase(MappingRule):

    """Docstring for BringMeBase. """

    type = "base"

    def __init__(self, entities):
        """TODO: to be defined. """

        self._entities = DictList('bring_me_base')

        if isinstance(entities, dict):
            self._entities.set(entities)

        self.mapping = {
            "bring me <entity>":
                Function(self.bring_me),
            "<entity_type> to bring me as <entity_name>":
                Function(self.bring_me_as),
            "remove <entity_name> from bring me":
                Function(self.bring_me_remove)
        }

        self.extras = [
            DictListRef("entity", self._entities),
            Literal(self.type, "entity_type"),
            Dictation("entity_name").apply(lambda key:
                                           re.sub(r'[^A-Za-z\'\s]+', '', key)
                                           .lower())
        ]

        self._subscribers = []

        super().__init__()

    entities = property(lambda self: self._entities.copy(),
                        doc='TODO')

    log = property(lambda self: logging.getLogger("casterplugin.{}"
                                                  .format(self)),
                   doc='TODO')

    def __str__(self):
        return self.__class__.__name__

    def subscribe(self, callback):
        """TODO: callback is called everytime the entities are altered by the user.
        :returns: TODO

        """
        self._subscribers.append(callback)

    def bring_me(self, entity):
        """TODO: Docstring for bring_me.
        :returns: TODO

        """
        self._bring_me(entity)

    def bring_me_as(self, entity_type, entity_name):
        """TODO: Docstring for bring_me_as.
        :returns: TODO

        """
        assert entity_type == self.type
        self.log.info('Bringing you %s as "%s"', entity_type, entity_name)
        self._bring_me_as(entity_name)
        for subscriber in self._subscribers:
            subscriber()

    def bring_me_remove(self, entity_name):
        self.log.info('Removing "%s" from BringMe', entity_name)
        self._entities.pop(str(entity_name))
        for subscriber in self._subscribers:
            subscriber()

    def _bring_me(self, entity):
        raise NotImplementedError("Please bring me something!")

    def _bring_me_as(self, entity_name):
        raise NotImplementedError("Let me bring new stuff!")
