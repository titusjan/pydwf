
AnalogOut Instrument API
========================

The AnalogOut instrument implements multiple channels of analog output on devices that support it, such as the Analog Discovery and the Analog Discovery 2.

To use the AnalogOut instrument you first need to initialize a DigitalWaveformsLibrary instance.
Next, you open a specific device.
The device's AnalogOut instrument API can now be accessed via its *analogOut* attribute, which is an instance of the AnalogOutAPI class.

For example:

.. code-block:: python

   from pydwf import DigilentWaveformsLibrary

   dwf = DigilentWaveformsLibrary()

   with dwf.device.open(-1) as device:

       # Get a reference to the device's AnalogOut instrument API.
       analogOut = device.analogOut

       # Use the AnalogOut instrument.
       analogOut.reset()

The AnalogOut instrument state machine
--------------------------------------

(to be written)

Channels and nodes
------------------

(to be written)

API methods
-----------

The AnalogOut instrument is a complicated instrument; there are many parameters that can be used to control its behavior.
We summarize them below.

Version 3.16.3 of the DWF library has 83 'FDwfAnalogOut' functions, 25 of which are obsolete.
All of these are available through the AnalogIn API of *pydwf*.

Miscellaneus functions
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   analogOut.count() -> int

.. code-block:: python

   analogOut.reset(channel_index: int)

.. code-block:: python

   analogOut.configure(channel_index: int, start: bool)

.. code-block:: python

   analogOut.customAMFMEnableSet(channel_index: int, enable: bool)
   analogOut.customAMFMEnableGet(channel_index: int) -> bool

.. code-block:: python

   analogOut.status(channel_index: int) -> DwfState
   analogOut.nodePlayStatus(channel_index: int, node: AnalogOutNode) -> Tuple[int, int, int]
   analogOut.nodePlayData(channel_index:int, node: AnalogOutNode, data: np.ndarray)

.. code-block:: python

   analogOut.masterSet(channel_index: int, idxMaster: int)
   analogOut.masterGet(channel_index: int) -> int

Triggering
^^^^^^^^^^

.. code-block:: python

   analogOut.triggerSourceSet(channel_index: int, trigger_source: TRIGSRC)
   analogOut.triggerSourceGet(channel_index: int) -> TRIGSRC

.. code-block:: python

   analogOut.triggerSlopeSet(channel_index: int, trigger_slope: DwfTriggerSlope)
   analogOut.triggerSlopeGet(channel_index: int) -> DwfTriggerSlope

Run duration, wait duration, and repeats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   analogOut.runInfo(channel_index: int) -> Tuple[float, float]
   analogOut.runSet(channel_index: int, secRun: float)
   analogOut.runGet(channel_index: int) -> float
   analogOut.runStatus(channel_index: int) -> float

.. code-block:: python

   analogOut.waitInfo(channel_index: int) -> Tuple[float, float]
   analogOut.waitSet(channel_index: int, secWait: float)
   analogOut.waitGet(channel_index: int) -> float

.. code-block:: python

   analogOut.repeatInfo(channel_index: int) -> Tuple[int, int]
   analogOut.repeatSet(channel_index: int, repeat: int)
   analogOut.repeatGet(channel_index: int) -> int
   analogOut.repeatStatus(channel_index: int) -> int

.. code-block:: python

   analogOut.repeatTriggerSet(channel_index: int, repeatTrigger: bool)
   analogOut.repeatTriggerGet(channel_index: int) -> bool

Analog Output settings
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   analogOut.modeSet(channel_index: int, mode: DwfAnalogOutMode)
   analogOut.modeGet(channel_index: int) -> DwfAnalogOutMode

.. code-block:: python

   analogOut.limitationInfo(channel_index: int) -> Tuple[float, float]
   analogOut.limitationSet(channel_index: int, limit: float)
   analogOut.limitationGet(channel_index: int) -> float

.. code-block:: python

   analogOut.idleInfo(channel_index: int) -> List[DwfAnalogOutIdle]
   analogOut.idleSet(channel_index: int, idle: DwfAnalogOutIdle)
   analogOut.idleGet(channel_index: int) -> DwfAnalogOutIdle

AnalogOut node functions
^^^^^^^^^^^^^^^^^^^^^^^^

Query available signal nodes
""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.nodeInfo(channel_index: int) -> List[AnalogOutNode]

Node enable/disable setting
"""""""""""""""""""""""""""

.. code-block:: python

   analogOut.nodeEnableSet(channel_index: int, node: AnalogOutNode, enable: bool)
   analogOut.nodeEnableGet(channel_index: int, node: AnalogOutNode) -> bool

Node signal function (waveform) setting
"""""""""""""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.nodeFunctionInfo(channel_index: int, node: AnalogOutNode) -> List[FUNC]
   analogOut.nodeFunctionSet(channel_index: int, node: AnalogOutNode, func: FUNC)
   analogOut.nodeFunctionGet(channel_index: int, node: AnalogOutNode) -> FUNC

Node signal frequency setting
"""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.nodeFrequencyInfo(channel_index: int, node: AnalogOutNode) -> Tuple[float, float]
   analogOut.nodeFrequencySet(channel_index: int, node: AnalogOutNode, hzFrequency: float)
   analogOut.nodeFrequencyGet(channel_index: int, node: AnalogOutNode) -> float

Node signal amplitude setting
"""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.nodeAmplitudeInfo(channel_index: int, node: AnalogOutNode) -> Tuple[float, float]
   analogOut.nodeAmplitudeSet(channel_index: int, node: AnalogOutNode, vAmplitude: float)
   analogOut.nodeAmplitudeGet(channel_index: int, node: AnalogOutNode) -> float

Node signal offset setting
""""""""""""""""""""""""""

.. code-block:: python

   analogOut.nodeOffsetInfo(channel_index: int, node: AnalogOutNode) -> Tuple[float, float]
   analogOut.nodeOffsetSet(channel_index: int, node: AnalogOutNode, vOffset: float)
   analogOut.nodeOffsetGet(channel_index: int, node: AnalogOutNode) -> float

Node signal symmetry setting
""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.nodeSymmetryInfo(channel_index: int, node: AnalogOutNode) -> Tuple[float, float]
   analogOut.nodeSymmetrySet(channel_index: int, node: AnalogOutNode, percentageSymmetry: float)
   analogOut.nodeSymmetryGet(channel_index: int, node: AnalogOutNode) -> float

Node signal phase setting
"""""""""""""""""""""""""

.. code-block:: python

   analogOut.nodePhaseInfo(channel_index: int, node: AnalogOutNode) -> Tuple[float, float]
   analogOut.nodePhaseSet(channel_index: int, node: AnalogOutNode, degreePhase: float)
   analogOut.nodePhaseGet(channel_index: int, node: AnalogOutNode) -> float

.. code-block:: python

   analogOut.nodeDataInfo(channel_index: int, node: AnalogOutNode) -> Tuple[float, float]
   analogOut.nodeDataSet(channel_index: int, node: AnalogOutNode, data: np.ndarray)

Obsolete functions
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   analogOut.triggerSourceInfo() -> List[TRIGSRC]

.. code-block:: python

   analogOut.enableSet(channel_index: int, enable: bool)
   analogOut.enableGet(channel_index: int) -> bool

Signal function (waveform) setting (OBSOLETE)
"""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.functionInfo(channel_index: int) -> List[FUNC]
   analogOut.functionSet(channel_index: int, func: FUNC)
   analogOut.functionGet(channel_index: int) -> FUNC

Signal frequency setting (OBSOLETE)
"""""""""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.frequencyInfo(channel_index: int) -> Tuple[float, float]
   analogOut.frequencySet(channel_index: int, hzFrequency: float)
   analogOut.frequencyGet(channel_index: int) -> float

Signal amplitude setting (OBSOLETE)
"""""""""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.amplitudeInfo(channel_index: int) -> Tuple[float, float]
   analogOut.amplitudeSet(channel_index: int, vAmplitude: float)
   analogOut.amplitudeGet(channel_index: int) -> float

Signal offset setting (OBSOLETE)
""""""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.offsetInfo(channel_index: int) -> Tuple[float, float]
   analogOut.offsetSet(channel_index: int, vOffset: float)
   analogOut.offsetGet(channel_index: int) -> float

Signal symmetry setting (OBSOLETE)
""""""""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.symmetryInfo(channel_index: int) -> Tuple[float, float]
   analogOut.symmetrySet(channel_index: int, percentageSymmetry: float)
   analogOut.symmetryGet(channel_index: int) -> float

Signal phase setting (OBSOLETE)
"""""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.phaseInfo(channel_index: int) -> Tuple[float, float]
   analogOut.phaseSet(channel_index: int, degreePhase: float)
   analogOut.phaseGet(channel_index: int) -> float

Arbitrary signal playback (OBSOLETE)
""""""""""""""""""""""""""""""""""""

.. code-block:: python

   analogOut.dataInfo(channel_index: int) -> Tuple[int, int]
   analogOut.dataSet(channel_index: int, data: np.ndarray)
   analogOut.playStatus(channel_index: int)  -> Tuple[int, int, int]
   analogOut.playData(channel_index: int, data: np.ndarray)

Example scripts
---------------

AnalogOutSimple.py
^^^^^^^^^^^^^^^^^^

AnalogOutContinuousPlay.py
^^^^^^^^^^^^^^^^^^^^^^^^^^
