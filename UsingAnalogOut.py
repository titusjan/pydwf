#! /usr/bin/env python3

import argparse
import contextlib

from pydwf import DigilentWaveformLibrary

# Version 3.12.1 of the DWF library has 83 'FDwfAnalogOut' functions, 25 of which are obsolete.
#
# 58 active functions:
#
# count() -> int
#
# masterSet        (idxChannel: int, idxMaster: int)
# masterGet        (idxChannel: int) -> int
# triggerSourceSet (idxChannel: int, trigsrc: TRIGSRC)
# triggerSourceGet (idxChannel: int) -> TRIGSRC
# triggerSlopeSet  (idxChannel: int, slope: DwfTriggerSlope)
# triggerSlopeGet  (idxChannel: int) -> DwfTriggerSlope
# runInfo          (idxChannel: int) -> Tuple[float, float]
# runSet           (idxChannel: int, secRun: float)
# runGet           (idxChannel: int) -> float
# runStatus        (idxChannel: int) -> float
# waitInfo         (idxChannel: int) -> Tuple[float, float]
# waitSet          (idxChannel: int, secWait: float)
# waitGet          (idxChannel: int) -> float
# repeatInfo       (idxChannel: int) -> Tuple[int, int]
# repeatSet        (idxChannel: int, repeat: int)
# repeatGet        (idxChannel: int) -> int
# repeatStatus     (idxChannel: int) -> int
# repeatTriggerSet (idxChannel: int, repeatTrigger: bool)
# repeatTriggerGet (idxChannel: int, node: AnalogOutNode) -> bool
# limitationInfo   (idxChannel: int) -> Tuple[float, float]
# limitationSet    (idxChannel: int, limit: float)
# limitationGet    (idxChannel: int) -> float
# modeSet          (idxChannel: int, mode: DwfAnalogOutMode)
# modeGet          (idxChannel: int) -> DwfAnalogOutMode
# idleInfo         (idxChannel: int) -> List[DwfAnalogOutIdle]
# idleSet          (idxChannel: int, idle: DwfAnalogOutIdle)
# idleGet          (idxChannel: int) -> DwfAnalogOutIdle
#
# nodeInfo         (idxChannel: int) -> List[AnalogOutNode]:
#
# nodeEnableSet    (idxChannel: int, node: AnalogOutNode, enable: bool)
# nodeEnableGet    (idxChannel: int, node: AnalogOutNode) -> bool
# nodeFunctionInfo (idxChannel: int, node: AnalogOutNode) -> List[FUNC]
# nodeFunctionSet  (idxChannel: int, node: AnalogOutNode, func: FUNC)
# nodeFunctionGet  (idxChannel: int, node: AnalogOutNode) -> FUNC
# nodeFrequencyInfo(idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
# nodeFrequencySet (idxChannel: int, node: AnalogOutNode, hzFrequency: float)
# nodeFrequencyGet (idxChannel: int, node: AnalogOutNode) -> float
# nodeAmplitudeInfo(idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
# nodeAmplitudeSet (idxChannel: int, node: AnalogOutNode, vAmplitude: float)
# nodeAmplitudeGet (idxChannel: int, node: AnalogOutNode) -> float
# nodeOffsetInfo   (idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
# nodeOffsetSet    (idxChannel: int, node: AnalogOutNode, vOffset: float)
# nodeOffsetGet    (idxChannel: int, node: AnalogOutNode) -> float
# nodeSymmetryInfo (idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
# nodeSymmetrySet  (idxChannel: int, node: AnalogOutNode, percentageSymmetry: float)
# nodeSymmetryGet  (idxChannel: int, node: AnalogOutNode) -> float
# nodePhaseInfo    (idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
# nodePhaseSet     (idxChannel: int, node: AnalogOutNode, degreePhase: float)
# nodePhaseGet     (idxChannel: int, node: AnalogOutNode) -> float
#
# nodeDataInfo(idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
# nodeDataSet()
#
# customAMFMEnableSet(idxChannel: int, enable: bool)
# customAMFMEnableGet(idxChannel: int) -> bool
#
# reset(idxChannel: int)
# configure(idxChannel: int, start: bool)
# status(idxChannel: int) -> DwfState
# nodePlayStatus(idxChannel: int, node: AnalogOutNode) -> Tuple[int, int, int]
# nodePlayData(---UNKNOWN---)

################################################# 25 obsolete functions follow:

# triggerSourceInfo()
#                       enableSet()       enableGet()
# functionInfo()        functionSet()     functionGet()
# frequencyInfo()       frequencySet()    frequencyGet()
# amplitudeInfo()       amplitudeSet()    amplitudeGet()
# offsetInfo()          offsetSet()       offsetGet()
# symmetryInfo()        symmetrySet()     symmetryGet()
# phaseInfo()           phaseSet()        phaseGet()
# dataInfo()            dataSet()
# playStatus()
# playData()

def demonstrate_usage(serial_number: str) -> None:
    # Version 3.12.1 of the DWF library has 19 'FDwfDigitalIO' functions, none of which are obsolete.
    # There are 3 generic functions (reset, configure, and status), and 8 functions that come in 32- and 64-bits variants.

    dwf = DigilentWaveformLibrary()

    with contextlib.closing(dwf.device.openBySerialNumber(serial_number)) as device:

        analogOut = device.analogOut

        # Reset all analog-out channels.
        analogOut.reset(-1)

        num_channels = analogOut.count()

        for channel_index in range(num_channels):

            channel_nodes = analogOut.nodeInfo(channel_index)

            for node in channel_nodes:

                node_function_info = analogOut.nodeFunctionInfo(channel_index, node)
                print(channel_index, node, node_function_info)

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the AnalogOut instrument.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")

    args = parser.parse_args()

    demonstrate_usage(args.serial_number)

if __name__ == "__main__":
    main()
