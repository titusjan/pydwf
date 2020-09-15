
AnalogIn Instrument API
=======================

The AnalogIn instrument implements multiple channels of analog input on devices that support it, such as the Analog Discovery and the Analog Discovery 2.

To use the AnalogIn instrument you first need to initialize a DigitalWaveformLibrary instance.
Next, you open a specific device.
The device's AnalogIn instrument API can now be accessed via its *analogIn* attribute, which is an instance of the AnalogInAPI class.

For example:

.. code-block:: python

   from pydwf import DigilentWaveformLibrary

   dwf = DigilentWaveformLibrary()

   # Open the first available Digilent device.
   device = dwf.device.open(-1)
   try:
       # Get a reference to the device's AnalogIn instrument API.
       ai = device.analogIn

       # Use the analog in instrument.
       ai.reset()

   finally:
       # Make sure the device is closed.
       device.close()

The AnalogIn instrument is a complicated instrument; there are many parameters that can be used to control its behavior.
We summarize them below.

Version 3.12.2 of the DWF library has 88 'FDwfAnalogIn' functions, 1 of which (FDwfAnalogInTriggerSourceInfo) is obsolete.

Miscellaneous methods (3)
-------------------------

| [1] reset()
| [1] configure(reconfigure: bool, start: bool)
| [1] triggerForce()

Status methods (12)
-------------------

| [1] status(readData: bool) -> DwfState
| [1] statusSamplesLeft() -> int
| [1] statusSamplesValid() -> int
| [1] statusIndexWrite() -> int
| [1] statusRecord() -> Tuple[int, int, int]
| [1] statusAutoTriggered() -> bool
| [1] statusData(idxChannel: int, cdData: int) -> np.ndarray
| [1] statusData2(idxChannel: int, idxData: int, cdData: int) -> np.ndarray
| [1] statusData16(idxChannel: int, idxData: int, cdData: int) -> np.ndarray
| [1] statusNoise(idxChannel: int, cdData: int) -> Tuple[np.ndarray, np.ndarray]
| [1] statusNoise2(idxChannel: int, idxData: int, cdData: int) -> Tuple[np.ndarray, np.ndarray]
| [1] statusSample(idxChannel: int) -> float

Acquisition settings and info methods (16)
------------------------------------------

| [2] recordLength             float            [s]                       Set        Get                         value 0 is used to denote unlimited recording.
| [3] frequency                float            [Hz]      Info            Set        Get                         frequencyInfo() call returns (min, max) range.
| [1] bits                     int              [-]       Info                                                   bitsInfo() call returns single number: number of ADC bits.
| [3] bufferSize               int              [-]       Info            Set        Get                         bufferSizeInfo() returns single number: maximum buffer size.
| [3] noiseSize                int              [-]       Info            Set        Get                         noiseSizeInfo() returns single number: maximum noise buffer size.
| [3] acquisitionMode          ACQMODE          [-]       Info            Set        Get                         acquisitionModeInfo() returns a list of valid ACQMODE values.
| [1] channelCount             int              [-]                                                              channelCount() returns the number of channels.

Per-channel settings (14)
-------------------------

| [2] channelEnable            bool             [-]                       Set        Get
| [3] channelFilter            FILTER           [-]       Info            Set        Get
| [4] channelRange             float            [V]       Info   Steps    Set        Get
| [3] channelOffset            float            [V]       Info            Set        Get
| [2] channelAttenuation       float            [-]                       Set        Get

Trigger settings methods (37)
-----------------------------

| [3] triggerSource            TRIGSRC          [-]       Info            Set        Get                         Note: triggerSourceInfo() is marked OBSOLETE.
| [4] triggerPosition          float            [s]       Info            Set        Get       Status
| [3] triggerAutoTimeout       float            [s]       Info            Set        Get
| [3] triggerHoldOff           float            [s]       Info            Set        Get
| [3] triggerType              TRIGTYPE         [-]       Info            Set        Get
| [3] triggerChannel           int              [-]       Info            Set        Get
| [3] triggerFilter            FILTER           [-]       Info            Set        Get
| [3] triggerLevel             float            [V]       Info            Set        Get
| [3] triggerHysteresis        float            [V]       Info            Set        Get
| [3] triggerCondition         DwfTriggerSlope  [-]       Info            Set        Get
| [3] triggerLength            float            [s]       Info            Set        Get
| [3] triggerLengthCondition   TRIGLEN          [-]       Info            Set        Get

Sampling settings methods (6)
-----------------------------

| [2] samplingSource           TRIGSRC          [-]                       Set        Get
| [2] samplingSlope            DwfTriggerSlope  [-]                       Set        Get
| [2] samplingDelay            float            [s]                       Set        Get
