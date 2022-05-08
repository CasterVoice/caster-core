Plugins
=======

.. toctree::
   :glob:
   :titlesonly:

   plugin/*

.. automodule:: castervoice.core.plugin


Plugins can be used by adding plugin packages to the :doc:`configuration file</configuration>` which are installed
automatically when *Caster* starts.

For example, the following will install `CasterVoice Caster Plugins`_ package:


.. _CasterVoice Caster Plugins: https://github.com/CasterVoice/caster-plugins

.. code-block:: yaml

    plugins:
      packages:
        - pip: "git+https://github.com/CasterVoice/caster-plugins.git"


Once the package is included its plugins can be referenced in the plugins list of a context section within the :doc:`configuration file</configuration>` like so:

.. code-block:: yaml


    contexts:
      - name: global
        plugins:
          - casterplugin.castercontrol
