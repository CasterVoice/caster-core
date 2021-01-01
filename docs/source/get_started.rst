Get started
===========

.. toctree::
   :glob:
   :titlesonly:
   :hidden:

   get_started/*


Installation
------------

1. `Install Python Pip <https://pip.pypa.io/en/stable/installing/>`_.

2. Install Caster::

    pip install 'git+https://github.com/CasterVoice/caster-core.git'

3. Configure Caster::

   Run

   .. code::

       python -m castervoice

   This will create a file `config/caster.yml` which contains the :doc:`/configuration` for Caster.
   Engines must be :doc:`configured </configuration>` and may provide :doc:`special configuration options </configuration/engine>`.

4. Follow steps for one of the :doc:`/get_started/engines` which you configured in the previous step.


Usage
-----

Caster can be started with the following::

    python -m castervoice

To list available options execute::

    python -m castervoice --help


.. _Caster3 here: https://github.com/Timoses/Caster/archive/caster3.zip
.. _Caster3 repository: https://github.com/Timoses/Caster
.. _KAG model: https://github.com/daanzu/kaldi-active-grammar/releases
