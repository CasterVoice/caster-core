Transition to Caster3
=====================

.. note::

    Work in progress

Differences to Caster2
----------------------

* Caster3 is modular. `caster-core` supplies usability features while the actual grammars and rules for speech recognition are supplied by plugins.
* The focus of Caster3 is to provide the glue which holds together speech recognition engines and speech recognition frameworks.
  While speech recognition frameworks such as Dragonfly tightly couple speech recognition engines, grammars and bound actions Caster3
  seeks to find a lighter coupling between these components.
  This allows Caster3 to focus on usability.

