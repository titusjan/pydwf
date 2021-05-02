.. include:: substitutions.rst

DigitalOut Instrument API
=========================

The DigitalOut instrument implements multiple channels of digital input on devices that support it, such as the Analog Discovery, Analog Discovery 2, and Digital Discovery.

To use the DigitalOut instrument you first need to initialize a |DigilentWaveformsLibrary| instance.
Next, you open a specific device.
The device's DigitalOut instrument API can now be accessed via its *digitalOut* attribute, which is an instance of the DigitalOutAPI class.

For example:

.. code-block:: python

   from pydwf import DigilentWaveformsLibrary

   dwf = DigilentWaveformsLibrary()

   with dwf.device.open(-1) as device:

       # Get a reference to the device's DigitalOut instrument API.
       digitalOut = device.digitalOut

       # Use the DigitalOut instrument.
       digitalOut.reset()

The DigitalOut instrument state machine
---------------------------------------

(to be written)

API methods
-----------

The DigitalOut instrument is complicated; there are many settings that control its behavior and, consequently, many functions to
control and query those settings.

Version 3.16.3 of the DWF library has 48 'FDwfDigitalOut' functions, one of which (*FDwfDigitalOutTriggerSourceInfo*) is obsolete.
All of these are available through the DigitalOut API of |pydwf|.

Configuration functions
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   digitalOut.reset()
   digitalOut.configure(start: bool)

Status function
^^^^^^^^^^^^^^^

.. code-block:: python

   digitalOut.status() -> DwfState

Trigger functions
^^^^^^^^^^^^^^^^^

This function is obsolete.

.. code-block:: python

   digitalOut.triggerSourceInfo() -> List[TRIGSRC]

.. code-block:: python

   digitalOut.triggerSlopeSet(trigger_slope: DwfTriggerSlope)
   digitalOut.triggerSlopeGet() -> DwfTriggerSlope

.. code-block:: python

   digitalOut.triggerSourceSet(trigger_source: TRIGSRC)
   digitalOut.triggerSourceGet() -> TRIGSRC

Pattern functions
^^^^^^^^^^^^^^^^^

.. code-block:: python

   digitalOut.runInfo() -> Tuple[float, float]
   digitalOut.runSet(secRun: float)
   digitalOut.runGet() -> float
   digitalOut.runStatus() -> float

.. code-block:: python

   digitalOut.waitInfo() -> Tuple[float, float]
   digitalOut.waitSet(secWait: float)
   digitalOut.waitGet() -> float

.. code-block:: python

   digitalOut.repeatInfo() -> Tuple[int, int]
   digitalOut.repeatSet(repeat: int)
   digitalOut.repeatGet() -> int
   digitalOut.repeatStatus() -> int

.. code-block:: python

   digitalOut.repeatTriggerSet(repeatTrigger: bool)
   digitalOut.repeatTriggerGet() -> bool

Channel Count
^^^^^^^^^^^^^

.. code-block:: python

   digitalOut.count() -> int

Channel enable/disable
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   digitalOut.enableSet(channel_index: int, enable: bool)
   digitalOut.enableGet(channel_index: int)

Channel output
^^^^^^^^^^^^^^

.. code-block:: python

   digitalOut.typeInfo(channel_index: int) -> List[DwfDigitalOutType]
   digitalOut.typeSet(channel_index: int, output_type: DwfDigitalOutType)
   digitalOut.typeGet(channel_index: int) -> DwfDigitalOutType

.. code-block:: python

   digitalOut.outputInfo(channel_index: int) -> List[DwfDigitalOutOutput]
   digitalOut.outputSet(channel_index: int, output_value: DwfDigitalOutOutput)
   digitalOut.outputGet(channel_index: int) -> DwfDigitalOutOutput

.. code-block:: python

   digitalOut.idleInfo(channel_index: int) -> List[DwfDigitalOutIdle]
   digitalOut.idleSet(channel_index: int, idle_mode: DwfDigitalOutIdle)
   digitalOut.idleGet(channel_index: int) -> DwfDigitalOutIdle

Channel timing
^^^^^^^^^^^^^^

.. code-block:: python

   digitalOut.internalClockInfo() -> float

.. code-block:: python

   digitalOut.dividerInfo(channel_index: int) -> Tuple[int, int]
   digitalOut.dividerInitSet(channel_index: int, divider_init: int)
   digitalOut.dividerInitGet(channel_index: int) -> int
   digitalOut.dividerSet(channel_index: int, divider: int)
   digitalOut.dividerGet(channel_index: int) -> int

.. code-block:: python

   digitalOut.counterInfo(channel_index: int) -> Tuple[int, int]
   digitalOut.counterInitSet(channel_index: int, high: bool, counter_init: int)
   digitalOut.counterInitGet(channel_index: int) -> Tuple[int, int]
   digitalOut.counterSet(channel_index: int, low_count: int, high_count: int)
   digitalOut.counterGet(channel_index: int) -> Tuple[int, int]

Channel pattern data management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   digitalOut.dataInfo(channel_index: int) -> int
   digitalOut.dataSet(channel_index: int, bits: str, tristate: bool=False)

   digitalOut.playDataSet(rg_bits: int, bits_per_sample: int, count_of_samples: int)
   digitalOut.playRateSet(rate_hz: float)
