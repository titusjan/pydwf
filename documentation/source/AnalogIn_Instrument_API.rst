.. include:: substitutions.rst

AnalogIn Instrument API
=======================

The AnalogIn instrument implements multiple channels of analog input on devices that support it, such as the Analog Discovery and the Analog Discovery 2.

To use the AnalogIn instrument you first need to initialize a |DigilentWaveformsLibrary| instance.
Next, you open a specific device.
The device's AnalogIn instrument API can now be accessed via its *analogIn* attribute, which is an instance of the AnalogInAPI class.

For example:

.. code-block:: python

   from pydwf import DigilentWaveformsLibrary

   dwf = DigilentWaveformsLibrary()

   with dwf.device.open(-1) as device:

       # Get a reference to the device's AnalogIn instrument API.
       analogIn = device.analogIn

       # Use the AnalogIn instrument.
       analogIn.reset()

The AnalogIn instrument state machine
-------------------------------------

(to be written)

API methods
-----------

The AnalogIn instrument is the most complicated instrument implemented in the DWF library; there are many settings that control its behavior and,
consequently, many functions to control and query those settings.

Version 3.16.3 of the DWF library has 93 'FDwfAnalogIn' functions, one of which (*FDwfAnalogInTriggerSourceInfo*) is obsolete.
All of these are available through the AnalogIn API of the |DigilentWaveformsDevice|.

Configuration functions
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   analogIn.reset()

.. code-block:: python

   analogIn.configure(reconfigure: bool, start: bool)

Status inquiry functions
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   analogIn.status(read_data: bool) -> DwfState

Information on last status() request
""""""""""""""""""""""""""""""""""""

.. code-block:: python

   analogIn.statusTime() -> Tuple[int, int, int]

.. code-block:: python

   analogIn.statusSample(channel_index: int) -> float

.. code-block:: python

   analogIn.statusAutoTriggered() -> bool

.. code-block:: python

   analogIn.statusSamplesLeft() -> int

.. code-block:: python

   analogIn.statusSamplesValid() -> int

.. code-block:: python

   analogIn.statusIndexWrite() -> int

.. code-block:: python

   analogIn.statusRecord() -> Tuple[int, int, int]

Retrieving bulk analog-in status data
"""""""""""""""""""""""""""""""""""""

.. code-block:: python

   analogIn.statusData(channel_index: int, count: int) -> np.ndarray
   analogIn.statusData2(channel_index: int, offset: int, count: int) -> np.ndarray
   analogIn.statusData16(channel_index: int, offset: int, count: int) -> np.ndarray

.. code-block:: python

   analogIn.statusNoise(channel_index: int, count: int) -> Tuple[np.ndarray, np.ndarray]
   analogIn.statusNoise2(channel_index: int, offset: int, count: int) -> Tuple[np.ndarray, np.ndarray]

Acquisition settings
^^^^^^^^^^^^^^^^^^^^

Number of ADC bits
""""""""""""""""""

The raw resolution of the ADC, in bits. This value cannot be changed, only queried.

The Analog Discovery 2 uses an Analog Devices AD9648 two-channel ADC.
It can convert 14-bit samples at a rate of 125 MHz. So for the Analog Discovery 2, the 'bitsInfo' method always returns 14.

.. code-block:: python

   analogIn.bitsInfo() -> int

Record length
"""""""""""""

The length of the record window, in seconds. This value is only used in the "Record" acquisition mode.

A value of 0 (zero) denotes a recording of an indefinite length.

.. code-block:: python

   analogIn.recordLengthSet(length: float)
   analogIn.recordLengthGet() -> float

Sample frequency
""""""""""""""""

The sample frequency of the AnalogIn instrument, in samples per second.

The 'frequencyInfo' method can be used to query the range of possible values for this setting.

.. code-block:: python

   analogIn.frequencyInfo() -> Tuple[float, float]
   analogIn.frequencySet(sample_frequency: float)
   analogIn.frequencyGet() -> float

Acquisition buffer size
"""""""""""""""""""""""

The sample buffer size of the AnalogIn instrument, in samples.

The 'bufferSizeInfo' method can be used to query the range of possible values for this setting.

The maximum buffer size depends on the configuration of the device. For the Analog Discovery 2, for example,
the maximum AnalogIn buffer size can be 512, 2048, 8192, or 16384, depending on the configuration.

When using the "Record" acquisition mode, the buffer size should be left at the default value, which is equal
to the maximum value. In other modes (e.g. Single), the buffer size determines the size of the acquisition window.

.. code-block:: python

   analogIn.bufferSizeInfo() -> Tuple[int, int]
   analogIn.bufferSizeSet(buffer_size: int)
   analogIn.bufferSizeGet() -> int

Noise buffer size
"""""""""""""""""

The noise buffer size of the AnalogInstrument, in samples.

The underlying C API functions for the noise buffer size suggest that it is an independent setting,
but it really isn't.

Setting the noise buffer size to a value 0 disables it completely; setting it to any other value
enables it with the size equal to the size of the sample buffer divided by 8.

In *pydwf*, this behavior is represented by the fact that the *noiseSizeSet* function takes a
boolean parameter instead of an integer parameter.

.. code-block:: python

   analogIn.noiseSizeInfo() -> int
   analogIn.noiseSizeSet(enable_noise_buffer: bool)
   analogIn.noiseSizeGet() -> int

Acquisition mode
""""""""""""""""

.. code-block:: python

   analogIn.acquisitionModeInfo() -> List[ACQMODE]
   analogIn.acquisitionModeSet(acquisition_mode: ACQMODE)
   analogIn.acquisitionModeGet() -> ACQMODE

Channel-specific settings
^^^^^^^^^^^^^^^^^^^^^^^^^

Many settings can be set differently for the AnalogIn channels.

The function *channelCount* queries the number of available channels; all other functions take a *channel_index* argument
that indicates which channel's setting is to be changed. This value should be in the range of 0 to (*channelCount* - 1).

Channel count
"""""""""""""

The number of channels supported by the AnalogIn instrument. This value cannot be changed, only queried.

For the Analog Dicovery 2, the 'channelCount' method always returns 2.

.. code-block:: python

   analogIn.channelCount() -> int

Channel enable/disable
""""""""""""""""""""""

AnalogIn channels can either be enabled or disabled individually.
These functions allow you to set and query their enabled states.

.. code-block:: python

   analogIn.channelEnableSet(channel_index: int, enable: bool)
   analogIn.channelEnableGet(channel_index: int) -> bool

Channel filtering
"""""""""""""""""

.. code-block:: python

   analogIn.channelFilterInfo() -> List[FILTER]
   analogIn.channelFilterSet(channel_index: int, filter_: FILTER)
   analogIn.channelFilterGet(channel_index: int) -> FILTER

Channel range
"""""""""""""

.. code-block:: python

   analogIn.channelRangeInfo() -> Tuple[float, float, float]
   analogIn.channelRangeSteps() -> List[float]
   analogIn.channelRangeSet(channel_index: int, voltsRange: float)
   analogIn.channelRangeGet(channel_index: int) -> float

Channel offset
""""""""""""""

Each channel has a channel offset value, in Volts.

These functions allow you to query the valid range, and to set and get the current offset value.

.. code-block:: python

   analogIn.channelOffsetInfo() -> Tuple[float, float, float]
   analogIn.channelOffsetSet(channel_index: int, voltOffset: float)
   analogIn.channelOffsetGet(channel_index: int) -> float

Channel attenuation
"""""""""""""""""""

.. code-block:: python

   analogIn.channelAttenuationSet(channel_index: int, attenuation: float)
   analogIn.channelAttenuationGet(channel_index: int) -> float

Channel bandwidth
"""""""""""""""""

.. code-block:: python

   analogIn.channelBandwidthSet(channel_index: int, bandwidth: float)
   analogIn.channelBandwidthGet(channel_index: int) -> float

Channel impedance
"""""""""""""""""

.. code-block:: python

   analogIn.channelImpedanceSet(channel_index: int, impedance: float)
   analogIn.channelImpedanceGet(channel_index: int) -> float

Trigger for the AnalogIn instrument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

AnalogIn Trigger source
"""""""""""""""""""""""

Note that analogIn.triggerSourceInfo() is considered obsolete. Use the *triggerInfo* function in the Device API instead.

.. code-block:: python

   analogIn.triggerSourceInfo() -> List[TRIGSRC]       # *** OBSOLETE ***
   analogIn.triggerSourceSet(trigger_source: TRIGSRC)
   analogIn.triggerSourceGet() -> TRIGSRC

Trigger position
""""""""""""""""

.. code-block:: python

   analogIn.triggerPositionInfo() -> Tuple[float, float, float]
   analogIn.triggerPositionSet(secPosition: float)
   analogIn.triggerPositionGet() -> float
   analogIn.triggerPositionStatus() -> float

Force trigger
"""""""""""""

.. code-block:: python

   analogIn.triggerForce()

AnalogIn trigger detector
^^^^^^^^^^^^^^^^^^^^^^^^^

Trigger auto-timeout
""""""""""""""""""""

.. code-block:: python

   analogIn.triggerAutoTimeoutInfo() -> Tuple[float, float, float]
   analogIn.triggerAutoTimeoutSet(secTimout: float)
   analogIn.triggerAutoTimeoutGet() -> float

Trigger holdoff
"""""""""""""""

The trigger holdoff setting is the minimum time (in seconds) for a trigger to be recognized after a previous trigger.

.. code-block:: python

   analogIn.triggerHoldOffInfo() -> Tuple[float, float, float]
   analogIn.triggerHoldOffSet(secHoldOff: float)
   analogIn.triggerHoldOffGet() -> float

Trigger type
""""""""""""

.. code-block:: python

   analogIn.triggerTypeInfo() -> List[TRIGTYPE]
   analogIn.triggerTypeSet(trigger_type: TRIGTYPE)
   analogIn.triggerTypeGet() -> TRIGTYPE

Trigger channel
"""""""""""""""

The AnalogIn trigger detector is sensitive to a specific channel.

These functions return the valid range of values for the trigger channel and set and get the trigger channel.

.. code-block:: python

   analogIn.triggerChannelInfo() -> Tuple[int, int]
   analogIn.triggerChannelSet(channel_index: int)
   analogIn.triggerChannelGet() -> int

Trigger filter
""""""""""""""

.. code-block:: python

   analogIn.triggerFilterInfo() -> List[FILTER]
   analogIn.triggerFilterSet(filter_: FILTER)
   analogIn.triggerFilterGet() -> FILTER

Trigger level
"""""""""""""

The trigger level, in Volt.

.. code-block:: python

   analogIn.triggerLevelInfo() -> Tuple[float, float, float]
   analogIn.triggerLevelSet(trigger_level: float)
   analogIn.triggerLevelGet() -> float

Trigger hysteresis
""""""""""""""""""

The trigger hysteresis, in Volt.

.. code-block:: python

   analogIn.triggerHysteresisInfo() -> Tuple[float, float, float]
   analogIn.triggerHysteresisSet(trigger_hysteresis: float)
   analogIn.triggerHysteresisGet() -> float

Trigger condition
"""""""""""""""""

.. code-block:: python

   analogIn.triggerConditionInfo() -> List[DwfTriggerSlope]
   analogIn.triggerConditionSet(trigger_condition: DwfTriggerSlope)
   analogIn.triggerConditionGet() -> DwfTriggerSlope

Trigger length
""""""""""""""

.. code-block:: python

   analogIn.triggerLengthInfo() -> Tuple[float, float, float]
   analogIn.triggerLengthSet(secLength: float)
   analogIn.triggerLengthGet() -> float

Trigger length condition
""""""""""""""""""""""""

.. code-block:: python

   analogIn.triggerLengthConditionInfo() -> List[TRIGLEN]
   analogIn.triggerLengthConditionSet(trigger_length: TRIGLEN)
   analogIn.triggerLengthConditionGet() -> TRIGLEN

Sampling clock settings
^^^^^^^^^^^^^^^^^^^^^^^

Sampling clock source
"""""""""""""""""""""

.. code-block:: python

   analogIn.samplingSourceSet(sampling_source: TRIGSRC)
   analogIn.samplingSourceGet() -> TRIGSRC

Sampling clock slope
""""""""""""""""""""

.. code-block:: python

   analogIn.samplingSlopeSet(sampling_slope: DwfTriggerSlope)
   analogIn.samplingSlopeGet() -> DwfTriggerSlope

Sampling clock delay
""""""""""""""""""""

.. code-block:: python

   analogIn.samplingDelaySet(sampling_delay: float)
   analogIn.samplingDelayGet() -> float

Example scripts
---------------

AnalogInSimple.py
^^^^^^^^^^^^^^^^^

AnalogInRecordMode.py
^^^^^^^^^^^^^^^^^^^^^
