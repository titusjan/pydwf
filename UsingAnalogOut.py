#! /usr/bin/env python3

import argparse
import contextlib

from pydwf import DigilentWaveformLibrary

def demonstrate_usage(serial_number: str) -> None:

    # Version 3.12.1 of the DWF library has 83 'FDwfAnalogOut' functions, 25 of which are obsolete.
    #
    # 58 active functions:
    #
    # [1] count() -> int
    #
    # [2] masterSet        (per channel)   idxMaster: int                                  Set Get
    # [2] triggerSource    (per channel)   trigsrc: TRIGSRC                                Set Get
    # [2] triggerSlope     (per channel)   slope: DwfTriggerSlope                          Set Get
    # [4] run              (per channel)   secRun: float                              Info Set Get Status
    # [3] wait             (per channel)   secWait: float                             Info Set Get
    # [4] repeat           (per channel)   repeat: int                                Info Set Get Status
    # [2] repeatTrigger    (per channel)   repeatTrigger: bool                             Set Get
    # [3] limitation       (per channel)   limit: float                               Info Set Get
    # [2] mode             (per channel)   mode: DwfAnalogOutMode                          Set Get
    # [3] idle             (per channel)   idle: DwfAnalogOutIdle                     Info Set Get
    #
    # nodeInfo         (idxChannel: int) -> List[AnalogOutNode]
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
