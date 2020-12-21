Plugins
=======

.. toctree::
   :glob:
   :titlesonly:

   plugin/*

.. automodule:: castervoice.core.plugin


Plugins can be used by adding plugin packages to the :doc:`configuration file</configuration>` which are installed
automatically when *Caster* starts.

For example, the following will install `Timoses Caster Plugins`_ package:


.. _Timoses Caster Plugins: https://github.com/Timoses/caster-plugins

.. code-block:: yaml

    plugins:
      packages:
        - pip: "https://github.com/Timoses/caster-plugins"


Once the package is included its plugins can be referenced in plugin list of a context section within the :doc:`configuration file</configuration>` like so:

.. code-block:: yaml


    contexts:
      - name: global
        plugins:
          - castercontrol
