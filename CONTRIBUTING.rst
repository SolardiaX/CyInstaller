================================
HOW TO CONTRIBUTE TO CYINSTALLER
================================

Thank you for considering contributing to CyInstaller!


----------------
Reporting issues
----------------

Include the following information in your post:

- Describe what you expected to happen.
- If possible, include a minimal reproducible example to help us identify
  the issue. This also helps check that the issue is not with your own code.
- Describe what actually happened. Include the full traceback if there was
  an exception.
- List your Python, Cython, PyInstaller and OS versions.
  If possible, check if this issue is already fixed in the latest releases
  or the latest code in the repository.

------------------
Submitting patches
------------------

If there is not an open issue for what you want to submit, prefer opening
one for discussion before working on a PR.
You can work on any issue that doesn't have an open PR linked to it or a
maintainer assigned to it.
These show up in the sidebar. No need to ask if you can work on an issue
that interests you.

Include the following in your patch:
Include the following in your patch:

-   Use `Black`_ to format your code. This and other tools will run
    automatically if you install `pre-commit`_ using the instructions
    below.
-   Include tests if your patch adds or changes code. Make sure the test
    fails without your patch.
-   Update any relevant docs pages and docstrings. Docs pages and
    docstrings should be wrapped at 72 characters.
-   Add an entry in ``CHANGES.rst``. Use the same style as other
    entries. Also include ``.. versionchanged::`` inline changelogs in
    relevant docstrings.

.. _Black: https://black.readthedocs.io
.. _pre-commit: https://pre-commit.com