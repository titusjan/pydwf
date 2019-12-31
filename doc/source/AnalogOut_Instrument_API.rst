
AnalogOut Instrument API
========================

The AnalogOut instrument implements multiple channels of analog output on devices that support it, such as the Analog Discovery and the Analog Discovery 2.

To use the AnalogOut instrument you first need to ininitialize a DigitalWaveformLibrary instance.
Next, you open a specific device.
The device's AnalogOut instrument API can now be accessed via its *analogOut* attribute, which is an instance of the AnalogOutAPI class.

For example:

.. code-block:: python

   from pydwf import DigilentWaveformLibrary

   dwf = DigilentWaveformLibrary()

   # Open the first available Digilent device.
   device = dwf.device.open(-1)
   try:
       # Get a reference to the device's AnalogIn instrument API.
       ao = device.analogOut

       # Use the analog in instrument.
       ao.reset()

   finally:
       # Make sure the device is closed.
       device.close()

The AnalogOut instrument is a complicated instrument; there are many parameters that can be used to control its behavior.
We summarize them below.

Version 3.12.2 of the DWF library has 83 'FDwfAnalogOut' functions, 25 of which are obsolete.

| [1] count() -> int
|
| [1] masterSet(idxChannel: int, idxMaster: int)
| [1] masterGet(idxChannel: int) -> int
| [1] triggerSourceSet(idxChannel: int, trigsrc: TRIGSRC)
| [1] triggerSourceGet(idxChannel: int) -> TRIGSRC
| [1] triggerSlopeSet(idxChannel: int, slope: DwfTriggerSlope)
| [1] triggerSlopeGet(idxChannel: int) -> DwfTriggerSlope
| [1] runInfo(idxChannel: int) -> Tuple[float, float]
| [1] runSet(idxChannel: int, secRun: float)
| [1] runGet(idxChannel: int) -> float
| [1] runStatus(idxChannel: int) -> float
| [1] waitInfo(idxChannel: int) -> Tuple[float, float]
| [1] waitSet(idxChannel: int, secWait: float)
| [1] waitGet(idxChannel: int) -> float
| [1] repeatInfo(idxChannel: int) -> Tuple[int, int]
| [1] repeatSet(idxChannel: int, repeat: int)
| [1] repeatGet(idxChannel: int) -> int
| [1] repeatStatus(idxChannel: int) -> int
| [1] repeatTriggerSet(idxChannel: int, repeatTrigger: bool)
| [1] repeatTriggerGet(idxChannel: int, node: AnalogOutNode) -> bool
| [1] limitationInfo(idxChannel: int) -> Tuple[float, float]
| [1] limitationSet(idxChannel: int, limit: float)
| [1] limitationGet(idxChannel: int) -> float
| [1] modeSet(idxChannel: int, mode: DwfAnalogOutMode)
| [1] modeGet(idxChannel: int) -> DwfAnalogOutMode
| [1] idleInfo(idxChannel: int) -> List[DwfAnalogOutIdle]
| [1] idleSet(idxChannel: int, idle: DwfAnalogOutIdle)
| [1] idleGet(idxChannel: int) -> DwfAnalogOutIdle
| [1] nodeInfo(idxChannel: int) -> List[AnalogOutNode]
|
| [1] nodeEnableSet(idxChannel: int, node: AnalogOutNode, enable: bool)
| [1] nodeEnableGet(idxChannel: int, node: AnalogOutNode) -> bool
| [1] nodeFunctionInfo(idxChannel: int, node: AnalogOutNode) -> List[FUNC]
| [1] nodeFunctionSet(idxChannel: int, node: AnalogOutNode, func: FUNC)
| [1] nodeFunctionGet(idxChannel: int, node: AnalogOutNode) -> FUNC
| [1] nodeFrequencyInfo(idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
| [1] nodeFrequencySet(idxChannel: int, node: AnalogOutNode, hzFrequency: float)
| [1] nodeFrequencyGet(idxChannel: int, node: AnalogOutNode) -> float
| [1] nodeAmplitudeInfo(idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
| [1] nodeAmplitudeSet(idxChannel: int, node: AnalogOutNode, vAmplitude: float)
| [1] nodeAmplitudeGet(idxChannel: int, node: AnalogOutNode) -> float
| [1] nodeOffsetInfo(idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
| [1] nodeOffsetSet(idxChannel: int, node: AnalogOutNode, vOffset: float)
| [1] nodeOffsetGet(idxChannel: int, node: AnalogOutNode) -> float
| [1] nodeSymmetryInfo(idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
| [1] nodeSymmetrySet(idxChannel: int, node: AnalogOutNode, percentageSymmetry: float)
| [1] nodeSymmetryGet(idxChannel: int, node: AnalogOutNode) -> float
| [1] nodePhaseInfo(idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
| [1] nodePhaseSet(idxChannel: int, node: AnalogOutNode, degreePhase: float)
| [1] nodePhaseGet(idxChannel: int, node: AnalogOutNode) -> float
| [1] nodeDataInfo(idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
|
| [1] nodeDataSet()
| [1] customAMFMEnableSet(idxChannel: int, enable: bool)
| [1] customAMFMEnableGet(idxChannel: int) -> bool
| [1] reset(idxChannel: int)
| [1] configure(idxChannel: int, start: bool)
| [1] status(idxChannel: int) -> DwfState
| [1] nodePlayStatus(idxChannel: int, node: AnalogOutNode) -> Tuple[int, int, int]
| [1] nodePlayData()
|
| Obsolete functions follow (signatures invalid)
|
| [1] triggerSourceInfo(self) -> None:
| [1] enableSet(self) -> None:
| [1] enableGet(self) -> None:
| [1] functionInfo(self) -> None:
| [1] functionSet(self) -> None:
| [1] functionGet(self) -> None:
| [1] frequencyInfo(self) -> None:
| [1] frequencySet(self) -> None:
| [1] frequencyGet(self) -> None:
| [1] amplitudeInfo(self) -> None:
| [1] amplitudeSet(self) -> None:
| [1] amplitudeGet(self) -> None:
| [1] offsetInfo(self) -> None:
| [1] offsetSet(self) -> None:
| [1] offsetGet(self) -> None:
| [1] symmetryInfo(self) -> None:
| [1] symmetrySet(self) -> None:
| [1] symmetryGet(self) -> None:
| [1] phaseInfo(self) -> None:
| [1] phaseSet(self) -> None:
| [1] phaseGet(self) -> None:
| [1] dataInfo(self) -> None:
| [1] dataSet(self) -> None:
| [1] playStatus(self) -> None:
| [1] playData(self) -> None:
