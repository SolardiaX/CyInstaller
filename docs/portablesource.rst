.. _portablesource:

==============
PortableSource
==============

--------
Overview
--------

`Cython` and `PyInstaller` support related or absolute file, but they have some different to deal with the files.

For example, `CyInstaller` use `Cython`'s `cythonize api`_ to compile sources, the method can take two arguments,
`module_list` and `exclude` which support glob pattern.

Similarly, when execute `PyInstaller` to package your application, the `datas` and `binaries` parameters must be a
tuple list, each tuple has two element, the source and the mapping dist path. See `PyInstaller` document
`Adding files to the bundle`_.

`CyInstaller` use a string expression `PortableSource` to handle those files whether they are related or absolute
or even need to be excluded. It's looks like:

.. code-block::

    [!][portable-base-dir::]the/path/to/file-or-glob[->target-dir]

Take a look at this:

.. code-block::

    [!][portable-base-dir::]the/path/to/file-or-glob

Generally, if ignore the **::** it's just a standard python glob pattern.

| If the str starts with **!** means the source is an exclude pattern. Exclude pattern will ignore
| **target-mapping-dir** cause it will do nothing.
| **portable-base-dir** is the base dir of source, but when `CyInstaller` copy it to the dist or building
  with `PyInstaller` it will be ignored. If it's not specified, will use the parent path of
  `the/path/to/file-or-glob` as the `portable-base-dir`.
| **the/path/to/file-or-glob** is the remained parts of a standard pattern.

**::target-mapping-dir** is the dist dir, will used as mapping dist for `datas` and `binaries` of `PyInstaller`.
It also be used to copy relates file to the distribution path. If it's not specified, will use the parent path of
`the/path/to/file-or/glob`.

--------
Examples
--------

.. code-block::

    "src/app/server.py"
    # A file from current working dir or module base, see `root` or `module.base` in configration.

    "src/app/**/__init__.py"
    # A python glob pattern which will include all `__init__.py` file in `src/app` and all sub directories.

    "!src/app/**/__init__.py"
    # A python glob pattern which will exclude all `__main__.py` file in `src/app` and all sub directories.

    "/home/cyinstaller::config.env"
    # The file in `/home/cyinstaller` which may copy to `dist` when used as `relates`,
    # or mapping as ('/home/cyinstaller/config.env', '.') when used as `datas`, `binaries`.

    "/home/cyinstaller::config.env->config"
    # Simply like previous example, but will use `config/` as the dist path.
    # or mapping as ('/home/cyinstaller/config.env', 'config')

    "/home/cyinstaller::datas/**/*.dat"
    # The files in `/home/cyinstaller/datas` which may copy to the path `datas/` of `dist` when used as `relates`,
    # or a tuple list mapping as:
    # [('/home/cyinstaller/datas/base.dat', 'datas'), ('/home/cyinstaller/datas/i/i.dat', 'datas/i')]
    # when used as `datas` or `binaries`.

    "/home/cyinstaller::datas/**/*.dat->static"
    # Simply like previous example, but will use `static/` as the dist path.
    # or a tuple list mapping as:
    # [('/home/cyinstaller/datas/base.dat', 'static/datas'), ('/home/cyinstaller/datas/a/1.dat', 'static/datas/a')]

.. _cythonize api: https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html
.. _Adding files to the bundle: https://pyinstaller.readthedocs.io/en/stable/spec-files.html#adding-files-to-the-bundle
