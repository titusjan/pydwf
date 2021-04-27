
AnalogIO Instrument API
=======================

The AnalogIO instrument implements analog I/O on devices that support it, such as the Analog Discovery and the Analog Discovery 2.

The Analog I/O functionality does not overlap with the functionality of the AnalogIn and AnalogOut instruments. It cannot be used
to control signals to the analog signal outputs or to monitor the analog signal inputs.

Instead, the Analog I/O functionality provides control of the positive and negative voltage supplies on devices that support it,
as well as monitoring of several analog status indicators of the devices, such as voltages, currents, and temperatures.

To use the AnalogIO instrument you first need to initialize a DigitalWaveformsLibrary instance.
Next, you open a specific device.
The device's AnalogIO instrument API can now be accessed via its *analogIO* attribute, which is an instance of the AnalogIOAPI class.

For example:

.. code-block:: python

   from pydwf import DigilentWaveformLibrary

   dwf = DigilentWaveformLibrary()

   with dwf.device.open(-1) as device:

       # Get a reference to the device's AnalogIO instrument API.
       analogIO = device.analogIO

       # Use the analog I/O instrument.
       analogIO.reset()

The AnalogOut instrument is a complicated instrument; there are many parameters that can be used to control its behavior.
We summarize them below.

Version 3.16.3 of the DWF library has 17 'FDwfAnalogIO' functions. All of these are available through PyDWF.

Channels and nodes
------------------


