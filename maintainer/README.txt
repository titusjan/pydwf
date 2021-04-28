
In my modest opinion, Python packaging is in a terrible state.

* Too many tools.

  distutils
  setuptools
  wheel
  build
  twine
  poetry
  pip

* No clear central source of truth. Documents point to each other.

* Documentation by tutorial.

  Where is a full list of all things that can go in setup.cfg,
  and what their effect is?

* No way to incorporate examples and documentation (HTML, PDF) into
  the distributed modules.


Building
========

To build a package, execute this command in the top-level project directory:

python3 -m build -n

This makes three directories:

    build
    pydwf.egg-info
    dist

This depends on:
    setup.cfg
    pyproject.toml
    LICENSE
    README.md
    pydwf/*

The 'dist' directory will contain the two desired build artefacts:

  dist/pydwf-<version>.tar.gz                -- source package
  dist/pydwf-<version>-py3-none-any.whl      -- wheel file (for binary installation)

Uploading to PyPI
=================

python3 -m twine upload -u reddish -p "<password>" dist/*
