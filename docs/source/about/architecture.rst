Architecture
============

Caster provides structured voice commands through grammars which are defined and provided by :doc:`plugins </plugin>`.

.. note::

    In comparison to previous Caster incarnations Caster3 no longer comes with prepackaged voice commands. An initial configured :doc:`/configuration` may provide initial commands of popular Caster Plugins.


The goal of Caster is to provide a ubiquitous frontend to various speech recognition frameworks and engines. Caster does not provide any voice commands itself. Instead a plugin framework can be utilized to bring voice commands and accessibility tooling.

The main advantage of separating the logic of Caster from actual voice commands and their execution is that it allows Caster to focus on features and maintainability while hopefully encouraging a flourishing plugin environment.


Client-Server
-------------

.. note::

    Work in progress (`#14 <https://github.com/Timoses/Caster/issues/14>`_)

Caster aims to support a client-server model in which

* Caster Clients send speech recognition requests to Caster Server,
* Caster Server returns Speech Recognition Results to a target Caster Client and
* targetted Caster Client executes the action.

