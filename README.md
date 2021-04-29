# pydwf

This is *pydwf*, a Python 3 wrapper for the Digilent Waveforms library to control the *Discovery*
line of multi-function lab devices. It fully implements all functionality offered by the underlying
C library (over 400 functions!) in an easy-to-use Python API.

The package offers a convenient command line tool that can be used, among other things, to list
the available Digilent devices and their configurations. The package comes with documentation
(still sparse but improving) and ready-to-run, well-written examples (already very useful)
demonstrating how to use the package to perform useful measurements.

Like the DWF library, the package supports Windows, Linux (Intel and AMD), and macOS.

## Project hosting

The project is hosted on github:

https://github.com/sidneycadot/pydwf/

## Installation using *pip*

The installable package is hosted on PyPI:

https://pypi.org/project/pydwf/

This makes it possible to install it using the standard pip tool:

```sh
pip install pydwf
```

A working installation of the  Digilent Adept and DWF libraries is a prerequisite for using *pydwf*.
If the Waveforms GUI application provided by Digilent works, you're good to go.

After installing *pydwf*, the following command will show the version of pydwf and the underlying
DWF library:

```sh
python -m pydwf version
```

The following command will list all Discovery devices connected to the system, and list their
configurations:

```sh
python -m pydwf list -c
```

## Documentation

The project documentation will be hosted on readthedocs in the near future.

For now, the documentation can easily be installed locally after installing the package,
by executing the following command:

```python
python -m pydwf extract-html-docs
```

This will create a local directory called *pydwf-docs-html* containing the project documentation.

## Examples

For now, the documentation can easily be installed locally after installing the package,
by executing the following command:

```python
python -m pydwf extract-examples
```
This will create a local directory called *pydwf-examples* containing the Python examples that show off the
capabilities of the Dicovery devices and *pydwf*. These examples should provide a good starting point to
implement your own scripts that use your Discovery devices.
