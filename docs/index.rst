=====
About
=====

.. container:: twocol

    .. container:: leftside

        .. image:: _static/images/welcome.png
            :alt: CyInstaller welcome

    .. container:: rightside

        CyInstaller is a lightweight CLI tools to compile and package your application
        to a single executable file with related distribution files.

        CyInstaller use `Cython`_ to compile application's source codes, then package
        files with `PyInstaller`_.

----------
Installing
----------

Install and update using `pip`_:

.. code-block:: text

    pip install -U CyInstaller

----------
Quickstart
----------

Add a `setup.yml` in your project, then execute the `CyInstaller` cli command:

.. code-block:: text

    CyInstaller

CyInstaller default use `setup.yml` as the config file. If use another file,
just execute the `CyInstaller` command with it as a parameter.

.. code-block:: text

    CyInstaller 'path/to/the/file'

To write the configuration file, please see the :ref:`configration`.

-----
Links
-----

* Releases: https://pypi.org/project/CyInstaller/
* Code: https://github.com/solardiax/cyinstaller
* Issue tracker: https://github.com/solardiax/cyinstaller/issues

.. _Cython: https://cython.org/
.. _PyInstaller: https://www.pyinstaller.org/
.. _pip: https://pip.pypa.io/en/stable/quickstart/

.. toctree::
    :maxdepth: 2
    :hidden:

    configuration

.. toctree::
    :maxdepth: 2
    :hidden:

    portablesource


.. toctree::
    :maxdepth: 2
    :hidden:

    modules