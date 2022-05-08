Features
========

.. contents:: Contents
    :local:

State
-----

Plugins are provided with a state store which is persisted between Caster restarts. This can be useful if a plugin benefits from caching data or requires persisting other data.

Note that stored data is presently not encrypted.


Configuration
-------------

Plugins can themselves define how they may be :doc:`configured </configuration>` by the user.
