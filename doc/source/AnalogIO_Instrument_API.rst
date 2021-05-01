
AnalogIO Instrument API
=======================

The AnalogIO instrument implements analog I/O on devices that support it, such as the Analog Discovery and the Analog Discovery 2.

The Analog I/O functionality, despite its name, does not overlap with the functionality of the AnalogIn and AnalogOut instruments.
It cannot be used to control signals to the analog signal outputs or to monitor the analog signal inputs.

Instead, the Analog I/O functionality provides control of the positive and negative voltage supplies on devices that support it,
as well as monitoring of several analog status indicators of the devices, such as voltages, currents, and temperatures.

To use the AnalogIO instrument you first need to initialize a DigitalWaveformsLibrary instance.
Next, you open a specific device.
The device's AnalogIO instrument API can now be accessed via its *analogIO* attribute, which is an instance of the AnalogIOAPI class.

For example:

.. code-block:: python

   from pydwf import DigilentWaveformsLibrary

   dwf = DigilentWaveformLibrary()

   with dwf.device.open(-1) as device:

       # Get a reference to the device's AnalogIO instrument API.
       analogIO = device.analogIO

       # Use the analog I/O instrument.
       analogIO.reset()

Channels and nodes
------------------

API methods
-----------

Version 3.16.3 of the DWF library has 17 'FDwfAnalogIO' functions. All of these are available through the AnalogIO API of *pydwf*.

Example scripts
---------------

AnalogIO.py
^^^^^^^^^^^

The *pydwf* example script *AnalogIO.py* demonstrates use of the AnalogIO instrument.

It first lists all AnalogIO channels and nodes.

Next, it continuously monitors the voltage, current, and temperature of the *USB Monitor* channel.
