
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

The AnalogIn instrument is the most complicated instrument implemented in the DWF library; there are many parameters that can be used to control its behavior.

The AnalogIn instrument state machine
-------------------------------------

(to be written)

The AnalogIn instrument API
---------------------------

Version 3.16.3 of the DWF library has 93 'FDwfAnalogIn' functions, one of which (FDwfAnalogInTriggerSourceInfo) is obsolete.
All of these are available through the AnalogIn API.

Configuration functions
~~~~~~~~~~~~~~~~~~~~~~~

* analogIn.reset()
* analogIn.configure(reconfigure: bool, start: bool)

Status inquiry functions
~~~~~~~~~~~~~~~~~~~~~~~~

* analogIn.status(read_data: bool) -> DwfState

Information on last status() request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* analogIn.statusTime() -> Tuple[int, int, int]
* analogIn.statusSample(channel_index: int) -> float
* analogIn.statusAutoTriggered() -> bool
* analogIn.statusSamplesLeft() -> int
* analogIn.statusSamplesValid() -> int
* analogIn.statusIndexWrite() -> int
* analogIn.statusRecord() -> Tuple[int, int, int]

Retrieving bulk analog-in data 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* analogIn.statusData(channel_index: int, count: int) -> np.ndarray
* analogIn.statusData2(channel_index: int, offset: int, count: int) -> np.ndarray
* analogIn.statusData16(channel_index: int, offset: int, count: int) -> np.ndarray

* analogIn.statusNoise(channel_index: int, count: int) -> Tuple[np.ndarray, np.ndarray]
* analogIn.statusNoise2(channel_index: int, offset: int, count: int) -> Tuple[np.ndarray, np.ndarray]

Acquisition settings
~~~~~~~~~~~~~~~~~~~~

Number of ADC bits
~~~~~~~~~~~~~~~~~~

* analogIn.bitsInfo() -> int

Record length
~~~~~~~~~~~~~

* analogIn.recordLengthSet(length: float)
* analogIn.recordLengthGet() -> float

Sample frequency
~~~~~~~~~~~~~~~~

* analogIn.frequencyInfo() -> Tuple[float, float]
* analogIn.frequencySet(sample_frequency: float)
* analogIn.frequencyGet() -> float

Acquisition buffer size
~~~~~~~~~~~~~~~~~~~~~~~

* analogIn.bufferSizeInfo() -> Tuple[int, int]
* analogIn.bufferSizeSet(buffer_size: int)
* analogIn.bufferSizeGet() -> int

Noise buffer size
~~~~~~~~~~~~~~~~~

* analogIn.noiseSizeInfo() -> int
* analogIn.noiseSizeSet(noise_buffer_active: bool)
* analogIn.noiseSizeGet() -> int

Acquisition mode
~~~~~~~~~~~~~~~~

* analogIn.acquisitionModeInfo() -> List[ACQMODE]
* analogIn.acquisitionModeSet(acquisition_mode: ACQMODE)
* analogIn.acquisitionModeGet() -> ACQMODE

Channel-specific settings
-------------------------

* analogIn.channelCount() -> int

* analogIn.channelEnableSet(channel_index: int, enable: bool)
* analogIn.channelEnableGet(channel_index: int) -> bool

* analogIn.channelFilterInfo() -> List[FILTER]
* analogIn.channelFilterSet(channel_index: int, filter_: FILTER)
* analogIn.channelFilterGet(channel_index: int) -> FILTER

* analogIn.channelRangeInfo() -> Tuple[float, float, float]
* analogIn.channelRangeSteps() -> List[float]
* analogIn.channelRangeSet(channel_index: int, voltsRange: float)
* analogIn.channelRangeGet(channel_index: int) -> float

* analogIn.channelOffsetInfo() -> Tuple[float, float, float]
* analogIn.channelOffsetSet(channel_index: int, voltOffset: float)
* analogIn.channelOffsetGet(channel_index: int) -> float

* analogIn.channelAttenuationSet(channel_index: int, attenuation: float)
* analogIn.channelAttenuationGet(channel_index: int) -> float

* analogIn.channelBandwidthSet(channel_index: int, bandwidth: float)
* analogIn.channelBandwidthGet(channel_index: int) -> float

* analogIn.channelImpedanceSet(channel_index: int, impedance: float)
* analogIn.channelImpedanceGet(channel_index: int) -> float

Triggering
----------

Trigger source
~~~~~~~~~~~~~~

* analogIn.triggerSourceInfo() -> List[TRIGSRC] (OBSOLETE)
* analogIn.triggerSourceSet(trigger_source: TRIGSRC)
* analogIn.triggerSourceGet() -> TRIGSRC

* analogIn.triggerForce()

AnalogIn trigger detector
~~~~~~~~~~~~~~~~~~~~~~~~~

* analogIn.triggerPositionInfo() -> Tuple[float, float, float]
* analogIn.triggerPositionSet(secPosition: float)
* analogIn.triggerPositionGet() -> float
* analogIn.triggerPositionStatus() -> float

* analogIn.triggerAutoTimeoutInfo() -> Tuple[float, float, float]
* analogIn.triggerAutoTimeoutSet(secTimout: float)
* analogIn.triggerAutoTimeoutGet() -> float

* analogIn.triggerHoldOffInfo() -> Tuple[float, float, float]
* analogIn.triggerHoldOffSet(secHoldOff: float)
* analogIn.triggerHoldOffGet() -> float

* analogIn.triggerTypeInfo() -> List[TRIGTYPE]
* analogIn.triggerTypeSet(trigger_type: TRIGTYPE)
* analogIn.triggerTypeGet() -> TRIGTYPE

* analogIn.triggerChannelInfo() -> Tuple[int, int]
* analogIn.triggerChannelSet(channel_index: int)
* analogIn.triggerChannelGet() -> int

* analogIn.triggerFilterInfo() -> List[FILTER]
* analogIn.triggerFilterSet(filter_: FILTER)
* analogIn.triggerFilterGet() -> FILTER

* analogIn.triggerLevelInfo() -> Tuple[float, float, float]
* analogIn.triggerLevelSet(trigger_level: float)
* analogIn.triggerLevelGet() -> float

* analogIn.triggerHysteresisInfo() -> Tuple[float, float, float]
* analogIn.triggerHysteresisSet(trigger_hysteresis: float)
* analogIn.triggerHysteresisGet() -> float

* analogIn.triggerConditionInfo() -> List[DwfTriggerSlope]
* analogIn.triggerConditionSet(trigger_condition: DwfTriggerSlope)
* analogIn.triggerConditionGet() -> DwfTriggerSlope

* analogIn.triggerLengthInfo() -> Tuple[float, float, float]
* analogIn.triggerLengthSet(secLength: float)
* analogIn.triggerLengthGet() -> float

* analogIn.triggerLengthConditionInfo() -> List[TRIGLEN]
* analogIn.triggerLengthConditionSet(trigger_length: TRIGLEN)
* analogIn.triggerLengthConditionGet() -> TRIGLEN

Sampling clock settings
-----------------------

* analogIn.samplingSourceSet(sampling_source: TRIGSRC)
* analogIn.samplingSourceGet() -> TRIGSRC

* analogIn.samplingSlopeSet(sampling_slope: DwfTriggerSlope)
* analogIn.samplingSlopeGet() -> DwfTriggerSlope

* analogIn.samplingDelaySet(sampling_delay: float)
* analogIn.samplingDelayGet() -> float
