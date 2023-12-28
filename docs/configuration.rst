.. _configuration:

=============
Configuration
=============

--------
Overview
--------

CyInstaller use yaml file (default is `setup.yml`) as configuration.

The config file may looks like:

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
      cython_binaries: true
      hiddenimports:
        - ...
      auto_hiddenimports: true
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

-----------------
Detail of Options
-----------------

+---------------------------+----------------+-------------------------------------------------------------------------+
| Option                    | Type           | Description                                                             |
+===========================+================+=========================================================================+
| name                      | str            | The name of app, will used as output packaged file's name.              |
|                           |                |                                                                         |
|                           |                | Default is **CyInstallerApp**.                                          |
+---------------------------+----------------+-------------------------------------------------------------------------+
| root                      | str            | The working path of CyInstaller, default is current path.               |
|                           |                |                                                                         |
|                           |                | Default is **.**.                                                       |
+---------------------------+----------------+-------------------------------------------------------------------------+
| modules                   | (optional)     | The modules list to compile and package.                                |
+---------------------------+----------------+-------------------------------------------------------------------------+
| modules.base              | str            | The base path of module related to `setup.root`,                        |
+---------------------------+----------------+-------------------------------------------------------------------------+
| module.package            | str            | The base package name of module,                                        |
|                           |                | this will used to detect `Cython` output for `PyInstaller`.             |
+---------------------------+----------------+-------------------------------------------------------------------------+
| module.package_from_base  | boolean        | If false the module's `Cython` output will base from                    |
|                           |                | a path named by the `module.package` not `module.base`.                 |
|                           |                |                                                                         |
|                           |                | Default is **true**.                                                    |
+---------------------------+----------------+-------------------------------------------------------------------------+
| module.compiles           | list           | The module's source files for `Cython` to compile,                      |
|                           |                | the files can be python scripts or any others can be supported.         |
|                           |                |                                                                         |
|                           |                | See :ref:`portablesource`.                                              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| module.packages           | list           | The module's source files for `PyInstaller` to package,                 |
|                           |                | the files can only be python scripts.                                   |
|                           |                |                                                                         |
|                           |                | See :ref:`portablesource`.                                              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| module.binaries           | list           | The modules' binary files for `PyInstaller` to package.                 |
|                           |                |                                                                         |
|                           |                | See :ref:`portablesource`.                                              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| module.data               | list           | The modules' data files for `PyInstaller` to package.                   |
|                           |                |                                                                         |
|                           |                | See :ref:`portablesource`.                                              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| module.relates            | list           | The modules' related files will copy to output dist.                    |
|                           |                |                                                                         |
|                           |                | See :ref:`portablesource`.                                              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| compiles                  | list           | The global source files for `Cython` to compile,                        |
|                           |                | the fields can be python scripts or any others can be supported.         |
|                           |                |                                                                         |
|                           |                | See :ref:`portablesource`.                                              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| packages                  | list           | The global source files for `PyInstaller` to package,                   |
|                           |                | the files can only be python scripts.                                   |
|                           |                |                                                                         |
|                           |                | See :ref:`portablesource`.                                              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| binaries                  | list           | The global binary files for `PyInstaller` to package,                   |
|                           |                |                                                                         |
|                           |                | See :ref:`portablesource`.                                              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| datas                     | list           | The global data files for `PyInstaller` to package,                     |
|                           |                |                                                                         |
|                           |                | See :ref:`portablesource`.                                              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| relates                   | list           | The global related files will copy to output dist.                      |
|                           |                |                                                                         |
|                           |                | See :ref:`portablesource`.                                              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| cython_binaries           | true           | Whether should use `Cython` outputs as `PyInstaller` binaries.          |
|                           |                |                                                                         |
|                           |                | Default is **true**.                                                    |
+---------------------------+----------------+-------------------------------------------------------------------------+
| hiddenimports             | list           | The full name list of packages of `PyInstaller` hiddenimports.          |
+---------------------------+----------------+-------------------------------------------------------------------------+
| auto_hiddenimports        | true           | Whether auto scan all python scripts defined by                         |
|                           |                | `compiles`, `packages`, `module.compiles` and `module.packages`.        |
|                           |                |                                                                         |
|                           |                | Default is **true**.                                                    |
+---------------------------+----------------+-------------------------------------------------------------------------+
| entrypoint                | str            | The entrypoint file of your application.                                |
|                           |                | The entrypoint should be a python script, and should be executed        |
|                           |                | directly from python cli like 'python entrypoint.py'.                   |
+---------------------------+----------------+-------------------------------------------------------------------------+
| stage                     | (optional)     | The building stage options for `Cython` and `PyInstaller`.              |
+---------------------------+----------------+-------------------------------------------------------------------------+
| stage.path                | str            | The related path of current path to store stage temporary files.        |
|                           |                |                                                                         |
|                           |                | Default is **_build**.                                                  |
+---------------------------+----------------+-------------------------------------------------------------------------+
| stage.debug               | str            | whether enable or disable debug.                                        |
|                           |                | if true all process files will remained for debug.                      |
|                           |                |                                                                         |
|                           |                | Default is **true**.                                                    |
+---------------------------+----------------+-------------------------------------------------------------------------+
| stage.cython.path         | str            | The `Cython` output path related to `stage.path`                        |
|                           |                |                                                                         |
|                           |                | Default is **cython**.                                                  |
+---------------------------+----------------+-------------------------------------------------------------------------+
| stage.cython.path_tmp     | str            | The `Cython` temp output path related to `stage.path`                   |
|                           |                |                                                                         |
|                           |                | Default is **compile**.                                                 |
+---------------------------+----------------+-------------------------------------------------------------------------+
| stage.cython.options      | dict           | The options use to execute `Cython` compile.                            |
|                           |                |                                                                         |
|                           |                | See `Cython Default Options`_.                                          |
+---------------------------+----------------+-------------------------------------------------------------------------+
| stage.cyinstaller.path    | str            | The `PyInstaller` output path related to `stage.path`                   |
|                           |                |                                                                         |
|                           |                | Default is **package**.                                                 |
+---------------------------+----------------+-------------------------------------------------------------------------+
| stage.cyinstaller.template| str            | The template file to execute `PyInstaller`.                             |
|                           |                |                                                                         |
|                           |                | If this value is not set, will use a default template to execute.       |
|                           |                |                                                                         |
|                           |                | See `PyInstaller Default Template`_.                                    |
+---------------------------+----------------+-------------------------------------------------------------------------+
| dist                      | str            | The path for dist output, can be a path related to `root`               |
|                           |                | or a absolute path                                                      |
|                           |                |                                                                         |
|                           |                | Default is **target**.                                                  |
+---------------------------+----------------+-------------------------------------------------------------------------+


----------------------
Cython Default Options
----------------------

The default options used for `Cython` to execute `cythonize` compile is:

.. code-block:: yaml

    compiler_directives:
        always_allow_keywords: true
    nthreads: 1
    language_level: 3

----------------------------
PyInstaller Default Template
----------------------------

The default template for `PyInstaller` is:

.. code-block::

    app_name = ${app_name}

    sources = ${sources}
    datas = ${datas}
    binaries = ${binaries}
    hiddenimports = ${hiddenimports}

    a = Analysis(sources,
                 pathex=[],
                 binaries=binaries,
                 datas=datas,
                 hiddenimports=hiddenimports,
                 hookspath=[],
                 runtime_hooks=[],
                 excludes=[],
                 win_no_prefer_redirects=False,
                 win_private_assemblies=False,
                 cipher=None,
                 noarchive=False)

    pyz = PYZ(a.pure, a.zipped_data,
                 cipher=None)

    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              [],
              name=app_name,
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              upx_exclude=[],
              runtime_tmpdir=None,
              console=True)

The `PyInstaller` template file support following placeholder:

================ ============================================================================================
Placeholder      Description
================ ============================================================================================
${app_name}      Placeholder for `app` defined in `CyInstaller` configuration file.
${sources}       Placeholder for `entrypoint` defined in `CyInstaller` configuration file.
${datas}         Placeholder for calculated data files mapping defined in `CyInstaller` configuration file.
${binaries}      Placeholder for calculated binary files mapping defined in `CyInstaller` configuration file.
${hiddenimports} Placeholder for calculated hiddenimports defined in `CyInstaller` configuration file.
================ ============================================================================================
