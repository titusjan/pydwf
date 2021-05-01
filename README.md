# pydwf

This is *pydwf*, a Python wrapper for the Digilent Waveforms library to control their line of
multi-function lab devices. It fully implements all functionality offered by the underlying
C library (over 400 functions!) in an easy-to-use Python API.

The package offers a convenient command line tool that can be used, among other things, to list
the available Digilent devices and their configurations. The package comes with documentation
(still sparse, but improving) and ready-to-run, well-written examples (already very useful),
demonstrating how to use *pydwf* to perform useful measurements.

Like the DWF library, the *pydwf* package supports Windows, Linux (Intel and AMD), and macOS.

## Supported devices

The *pydwf* package has been extensively tested with the Analog Discovery 2 and Digital Discovery
devices. It should also work with other devices, like the legacy Analog Discovery, the Electronics
Explorer board, and the new Analog Discovery Pro devices, but these haven't been tested.

If you have such a device and encounter issues, please let me know.

## Dependencies

The *pydwf* package is Python 3 only.

It requires the Digilent Adept and Digilent Waveforms packages to be installed on your computer.

Furthermore, it depends on the *numpy* package to handle the large amounts of data that travel
between the PC and the devices.

Some of the examples depend on the *matplotlib* library, but *pydwf* itself will work without it.

## Project hosting

The project repository and issue tracker are hosted on github:

https://github.com/sidneycadot/pydwf/

## Installation using *pip*

The installable package is hosted on PyPI:

https://pypi.org/project/pydwf/

This allows installation using the standard *pip* (or *pip3*) tool:

```
pip install pydwf
```

A working installation of the Digilent Adept and DWF libraries is a prerequisite for using *pydwf*.
If the Waveforms GUI application provided by Digilent works, you're good to go.

After installing *pydwf*, the following command will show the version of *pydwf* and the underlying
DWF library:

```
python -m pydwf version
```

The following command will list all Discovery devices connected to the system, and list their
configurations:

```
python -m pydwf list -c
```

## Documentation

The project documentation will be hosted on readthedocs in the near future.

For now, the documentation can easily be installed locally after installing the package
by executing the following command:

```
python -m pydwf extract-html-docs
```

This will create a local directory called *pydwf-docs-html* containing the project documentation in HTML format.

Please note that the documentation is not yet complete — it's a big API!

## Examples

The Python examples can easily be installed locally after installing the package
by executing the following command:

```
python -m pydwf extract-examples
```

This will create a local directory called *pydwf-examples* containing the Python examples that
show off the capabilities of the Discovery devices and *pydwf*.

These examples should provide a good starting point for your own Python scripts that control
Digilent Waveforms devices.
