
AnalogOut Instrument API
========================

The AnalogOut instrument implements multiple channels of analog output on devices that support it, such as the Analog Discovery and the Analog Discovery 2.

To use the AnalogOut instrument you first need to initialize a DigitalWaveformsLibrary instance.
Next, you open a specific device.
The device's AnalogOut instrument API can now be accessed via its *analogOut* attribute, which is an instance of the AnalogOutAPI class.

For example:

.. code-block:: python

   from pydwf import DigilentWaveformLibrary

   dwf = DigilentWaveformLibrary()

   with dwf.device.open(-1) as device:

       # Get a reference to the device's AnalogIn instrument API.
       analogOut = device.analogOut

       # Use the analog out instrument.
       analogOut.reset()

The AnalogOut instrument is a complicated instrument; there are many parameters that can be used to control its behavior.
We summarize them below.

Version 3.16.3 of the DWF library has 83 'FDwfAnalogOut' functions, 25 of which are obsolete.
