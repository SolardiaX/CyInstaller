CyInstaller
===========

CyInstaller is a lightweight CLI tools to compile and package your application
to a single executable file with related distribution files.

CyInstaller use `Cython`_ to compile application's source codes, then package
files with `PyInstaller`_.

Installing
----------

Install and update using `pip`_:

.. code-block:: text

    pip install -U CyInstaller

Quickstart
----------

Add a `setup.yml` in your project, then execute the `CyInstaller` cli command:

.. code-block:: text

    CyInstaller --file setup.yml

CyInstaller default use `setup.yml` as the config file. If use another file,
just execute the `CyInstaller` command with it as a parameter.

.. code-block:: text

    CyInstaller --file 'path/to/the/file'

Configuration
-------------

A yaml configration may looks like:

.. code-block:: yaml

    setup:
      app: CyInstallerApp
      root: .
      modules:
        - base: Common
          package: common
          package_from_base: false
          compiles:
            - ...
          packages:
            - ...
          binaries:
            - ...
          datas:
            - ...
          relates:
        - base: Backend
          ...
      compiles:
          - ...
      packages:
          - ...
      datas:
        - ...
      relates:
        - ...
      cython_binaries: true/false
      hiddenimports:
        - ...
      auto_hiddenimports: true/false
      entrypoint: app.py

      stage:
        path: _build
        debug: true/false
        cython:
          path: cython
          path_tmp: compile
          options:
            ...
        pyinstaller:
          path: package
          template: setup.spec

      dist: target

Detail for each options see the `configration guidelines`_.

.. _configration guidelines: https://github.com/solardiax/cyinstaller/blob/master/docs/configuration.rst

Links
-----

* Releases: https://pypi.org/project/CyInstaller/
* Code: https://github.com/solardiax/cyinstaller
* Issue tracker: https://github.com/solardiax/cyinstaller/issues

.. _Cython: https://cython.org/
.. _PyInstaller: https://www.pyinstaller.org/
.. _pip: https://pip.pypa.io/en/stable/quickstart/
