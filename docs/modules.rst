.. _modules:

=======
Modules
=======

--------
Overview
--------

`CyInstaller` supports package multi python modules into one executable file. It's very useful for
some large or complex application which has multiple entrypoint.

For example, if an application sources structure like:

.. code-block::

  app-root
  |- share
      |- src
      |- docs
      |- test
  |- web
      |- src
          |- server.py
          |- backends
              |- ...
      |- docs
      |- test
  |- schedule
      |- src
          |- server.py
          |- actions
              |- ...
      |- docs
      |- test

That means the app has a share module in 'app-root/share', and two modules have separate entries which
are 'app-root/web/src/server.py' and 'app-root/schedule/src/server.py'.

Now you can use the `modules` option in your `CyInstaller` configration file to package them.

.. note::

  Currently, `CyInstaller` does not support build multi entrypoints in one pipeline.
  So you need to write configration files for each entrypoints.

---------------------
Package and Base Path
---------------------

Mostly module sources is directly in the base path(`module.base`), the base path also is the package
name.

.. code-block::

  app-root
  |- module
      |- __init__.py
      |- src1.py
      |- src2.py
      |- ...

The configration may looks like:

.. code-block:: yaml

  modules:
    - base: module
      package: module
      package_from_base: true # this option is not required as default value is `true`
      ...

For complex application the structure may different, each module has it's own related files such as
documents and unit test etc..

.. code-block::

  app-root
  |- Module1
      |- module1
          |- __init__.py
          |- src1.py
          |- ...
              |- subpackage
                  |- __init__.py
                  |- ...
      |- docs
      |- test

In this case the package not directly from the base path, and the names also are different, for this
example the base path name is **Module1** and the package name is **module1**.

The configration can be:

.. code-block:: yaml

  modules:
    - base: Module1
      package: module1
      package_from_base: false

--------------------
Using PortableSource
--------------------

Alternatively, you can use :ref:`portablesource` to replace the module define. For example:

.. code-block::

  app-root
  |- Module1
      |- module1
          |- __init__.py
          |- src1.py
          |- ...
              |- subpackage
                  |- __init__.py
                  |- ...
      |- docs
      |- test

With `PortableSource` the configration can be:

.. code-block:: yaml

  setup:
    app: CyInstallerApp
    root: .
    sources: Module1::module1/**/*.py
    ...
