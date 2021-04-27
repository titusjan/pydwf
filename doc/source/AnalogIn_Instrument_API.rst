
AnalogIn Instrument API
=======================

The AnalogIn instrument implements multiple channels of analog input on devices that support it, such as the Analog Discovery and the Analog Discovery 2.

To use the AnalogIn instrument you first need to initialize a DigitalWaveformLibrary instance.
Next, you open a specific device.
The device's AnalogIn instrument API can now be accessed via its *analogIn* attribute, which is an instance of the AnalogInAPI class.

For example:

.. code-block:: python

   from pydwf import DigilentWaveformsLibrary

   dwf = DigilentWaveformsLibrary()

   with dwf.device.open(-1) as device:

       # Get a reference to the device's AnalogIn instrument API.
       analogIn = device.analogIn

       # Use the analog in instrument.
       analogIn.reset()

The AnalogIn instrument is a complicated instrument; there are many parameters that can be used to control its behavior.
We summarize them below.

Version 3.16.3 of the DWF library has 93 'FDwfAnalogIn' functions, one of which (FDwfAnalogInTriggerSourceInfo) is obsolete.
