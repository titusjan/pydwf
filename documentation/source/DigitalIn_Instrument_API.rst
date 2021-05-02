.. include:: substitutions.rst

DigitalIn Instrument API
========================

The DigitalIn instrument implements multiple channels of digital input on devices that support it, such as the Analog Discovery, Analog Discovery 2, and Digital Discovery.

To use the DigitalIn instrument you first need to initialize a |DigilentWaveformsLibrary| instance.
Next, you open a specific device.
The device's DigitalIn instrument API can now be accessed via its *digitalIn* attribute, which is an instance of the DigitalInAPI class.

For example:

.. code-block:: python

   from pydwf import DigilentWaveformsLibrary

   dwf = DigilentWaveformsLibrary()

   with dwf.device.open(-1) as device:

       # Get a reference to the device's DigitalIn instrument API.
       digitalIn = device.digitalIn

       # Use the DigitalOut instrument.
       digitalIn.reset()

The DigitalIn instrument state machine
---------------------------------------

(to be written)

API methods
-----------

The DigitalIn instrument is complicated; there are many settings that control its behavior and, consequently,
many functions to control and query those settings.

Version 3.16.3 of the DWF library has 55 'FDwfDigitalIn' functions, 2 of which (*FDwfDigitalInMixedSet*, *FDwfDigitalInTriggerSourceInfo*) are obsolete.
All of these are available through the DigitalIn API of |pydwf|.

Instrument configuration
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   digitalIn.reset()
   digitalIn.configure(reconfigure: bool, start: bool)

Status inquiry
^^^^^^^^^^^^^^

.. code-block:: python

   digitalIn.status(readData: bool) -> DwfState

.. code-block:: python

   digitalIn.statusSamplesLeft() -> int
   digitalIn.statusSamplesValid() -> int
   digitalIn.statusIndexWrite() -> int
   digitalIn.statusAutoTriggered() -> bool
   digitalIn.statusData(count_bytes: int) -> np.ndarray
   digitalIn.statusData2(first_sample: int, count_bytes: int) -> np.ndarray
   digitalIn.statusNoise2(first_sample: int, count_bytes: int) -> np.ndarray
   digitalIn.statusRecord() -> Tuple[int, int, int]
   digitalIn.statusTime() -> Tuple[int, int, int]

Timing configuration
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   digitalIn.internalClockInfo() -> float

.. code-block:: python

   digitalIn.clockSourceInfo() -> List[DwfDigitalInClockSource]
   digitalIn.clockSourceSet(clock_source: DwfDigitalInClockSource)
   digitalIn.clockSourceGet() -> DwfDigitalInClockSource

.. code-block:: python

   digitalIn.dividerInfo() -> int
   digitalIn.dividerSet(div: int)
   digitalIn.dividerGet() -> int

Channel configuration
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   digitalIn.bitsInfo() -> int

.. code-block:: python

   digitalIn.sampleFormatSet(nBits: int)
   digitalIn.sampleFormatGet() -> int

.. code-block:: python

   digitalIn.inputOrderSet(dioFirst: bool)

.. code-block:: python

   digitalIn.bufferSizeInfo() -> int
   digitalIn.bufferSizeSet(nSize: int)
   digitalIn.bufferSizeGet() -> int

.. code-block:: python

   digitalIn.sampleModeInfo() -> List[DwfDigitalInSampleMode]
   digitalIn.sampleModeSet(sample_mode: DwfDigitalInSampleMode)
   digitalIn.sampleModeGet() -> DwfDigitalInSampleMode

.. code-block:: python

   digitalIn.sampleSensibleSet(compression_bits: int)
   digitalIn.sampleSensibleGet() -> int

.. code-block:: python

   digitalIn.acquisitionModeInfo() -> List[ACQMODE]
   digitalIn.acquisitionModeSet(acquisition_mode: ACQMODE)
   digitalIn.acquisitionModeGet() -> ACQMODE

Trigger configuration
^^^^^^^^^^^^^^^^^^^^^

Note: this function is obsolete.

.. code-block:: python

   digitalIn.triggerSourceInfo() -> List[TRIGSRC]

.. code-block:: python

   digitalIn.triggerSourceSet(trigger_source: TRIGSRC)
   digitalIn.triggerSourceGet() -> TRIGSRC
   digitalIn.triggerSlopeSet(trigger_slope: DwfTriggerSlope)
   digitalIn.triggerSlopeGet() -> DwfTriggerSlope

.. code-block:: python

   digitalIn.triggerPositionInfo() -> int
   digitalIn.triggerPositionSet(samples_after_trigger: int)
   digitalIn.triggerPositionGet() -> int

.. code-block:: python

   digitalIn.triggerPrefillSet(samples_before_trigger: int)
   digitalIn.triggerPrefillGet() -> int

.. code-block:: python

   digitalIn.triggerAutoTimeoutInfo() -> Tuple[float, float, float]
   digitalIn.triggerAutoTimeoutSet(secTimout: float)
   digitalIn.triggerAutoTimeoutGet() -> float

.. code-block:: python

   digitalIn.triggerInfo() -> Tuple[int, int, int, int]
   digitalIn.triggerSet(fsLevelLow: int, fsLevelHigh: int, fsEdgeRise: int, fsEdgeFall: int)
   digitalIn.triggerGet() -> Tuple[int, int, int, int]

.. code-block:: python

   digitalIn.triggerResetSet(fsLevelLow: int, fsLevelHigh: int, fsEdgeRise: int, fsEdgeFall: int)
   digitalIn.triggerCountSet(count: int, restart: int)
   digitalIn.triggerLengthSet(secMin: float, secMax: float, idxSync: int)
   digitalIn.triggerMatchSet(pin: int, mask: int, value: int, bitstuffing: int)

Miscellaneous functionality
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note: this function is obsolete.

.. code-block:: python

   digitalIn.mixedSet(enable: bool)
