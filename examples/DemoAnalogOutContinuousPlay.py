#! /usr/bin/env python3

import argparse
import contextlib
import time
import numpy as np
from pydwf import DigilentWaveformsLibrary, AnalogOutNode, FUNC
from demo_utilities import find_demo_device, DemoDeviceNotFoundError


class sampler:
    def __init__(self, fs, channel):
        self.fs = fs
        self.channel = channel
        self.k = 0

    def get_samples(self, n: int):
        t = np.arange(self.k, self.k + n) / self.fs
        if self.channel == 0:
            data = np.mod(t * 400.0 * 2 * np.pi, 1.02)
        else:
            data = np.mod(t * 400.0 * 2 * np.pi, 1.0201)

        self.k += n

        return data

def demo_analog_output_instrument_api(analogOut):

    # count(self) -> int
    #
    # masterSet(self, idxChannel: int, idxMaster: int)
    # masterGet(self, idxChannel: int) -> int
    #
    # triggerSourceSet(self, idxChannel: int, trigsrc: TRIGSRC)
    # triggerSourceGet(self, idxChannel: int) -> TRIGSRC
    # triggerSlopeSet(self, idxChannel: int, slope: DwfTriggerSlope)
    # triggerSlopeGet(self, idxChannel: int) -> DwfTriggerSlope
    # runInfo(self, idxChannel: int) -> Tuple[float, float]
    # runSet(self, idxChannel: int, secRun: float)
    # runGet(self, idxChannel: int) -> float
    # runStatus(self, idxChannel: int) -> float
    # waitInfo(self, idxChannel: int) -> Tuple[float, float]
    # waitSet(self, idxChannel: int, secWait: float)
    # waitGet(self, idxChannel: int) -> float
    # repeatInfo(self, idxChannel: int) -> Tuple[int, int]
    # repeatSet(self, idxChannel: int, repeat: int)
    # repeatGet(self, idxChannel: int) -> int
    # repeatStatus(self, idxChannel: int) -> int
    # repeatTriggerSet(self, idxChannel: int, repeatTrigger: bool)
    # repeatTriggerGet(self, idxChannel: int, node: AnalogOutNode) -> bool
    # limitationInfo(self, idxChannel: int) -> Tuple[float, float]
    # limitationSet(self, idxChannel: int, limit: float)
    # limitationGet(self, idxChannel: int) -> float
    # modeSet(self, idxChannel: int, mode: DwfAnalogOutMode)
    # modeGet(self, idxChannel: int) -> DwfAnalogOutMode
    # idleInfo(self, idxChannel: int) -> List[DwfAnalogOutIdle]
    # idleSet(self, idxChannel: int, idle: DwfAnalogOutIdle)
    # idleGet(self, idxChannel: int) -> DwfAnalogOutIdle
    # nodeInfo(self, idxChannel: int) -> List[AnalogOutNode]
    # nodeEnableSet(self, idxChannel: int, node: AnalogOutNode, enable: bool)
    # nodeEnableGet(self, idxChannel: int, node: AnalogOutNode) -> bool
    # nodeFunctionInfo(self, idxChannel: int, node: AnalogOutNode) -> List[FUNC]
    # nodeFunctionSet(self, idxChannel: int, node: AnalogOutNode, func: FUNC)
    # nodeFunctionGet(self, idxChannel: int, node: AnalogOutNode) -> FUNC
    # nodeFrequencyInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
    # nodeFrequencySet(self, idxChannel: int, node: AnalogOutNode, hzFrequency: float)
    # nodeFrequencyGet(self, idxChannel: int, node: AnalogOutNode) -> float
    # nodeAmplitudeInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
    # nodeAmplitudeSet(self, idxChannel: int, node: AnalogOutNode, vAmplitude: float)
    # nodeAmplitudeGet(self, idxChannel: int, node: AnalogOutNode) -> float
    # nodeOffsetInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
    # nodeOffsetSet(self, idxChannel: int, node: AnalogOutNode, vOffset: float)
    # nodeOffsetGet(self, idxChannel: int, node: AnalogOutNode) -> float
    # nodeSymmetryInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
    # nodeSymmetrySet(self, idxChannel: int, node: AnalogOutNode, percentageSymmetry: float)
    # nodeSymmetryGet(self, idxChannel: int, node: AnalogOutNode) -> float
    # nodePhaseInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
    # nodePhaseSet(self, idxChannel: int, node: AnalogOutNode, degreePhase: float)
    # nodePhaseGet(self, idxChannel: int, node: AnalogOutNode) -> float
    # nodeDataInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]
    # nodeDataSet(self, idxChannel: int, node: AnalogOutNode, data: np.ndarray)
    # nodePlayStatus(self, idxChannel: int, node: AnalogOutNode) -> Tuple[int, int, int]
    # nodePlayData(self, idxChannel:int,  node: AnalogOutNode, data: np.ndarray)
    #
    # customAMFMEnableSet(self, idxChannel: int, enable: bool)
    # customAMFMEnableGet(self, idxChannel: int) -> bool
    #
    # reset(self, idxChannel: int)
    # configure(self, idxChannel: int, start: bool)
    # status(self, idxChannel: int) -> DwfState

    channel_count = analogOut.count()

    if channel_count == 0:
        print("The device has no analog output channels that can be used for this demo.")
        return

    analogOut.reset(-1)

    print("Number of channels ............. : {}".format(channel_count))
    print()

    for channel_index in range(channel_count):

        print("Channel #{}:".format(channel_index))
        print()
        print("    masterGet .................. : {}".format(analogOut.masterGet(channel_index)))
        print("    triggerSourceGet ........... : {}".format(analogOut.triggerSourceGet(channel_index)))
        print("    triggerSlopeGet ............ : {}".format(analogOut.triggerSlopeGet(channel_index)))
        print("    runInfo .................... : {}".format(analogOut.runInfo(channel_index)))
        print("    runGet ..................... : {}".format(analogOut.runGet(channel_index)))
        print("    runStatus .................. : {}".format(analogOut.runStatus(channel_index)))
        print("    waitInfo ................... : {}".format(analogOut.waitInfo(channel_index)))
        print("    waitGet .................... : {}".format(analogOut.waitGet(channel_index)))
        print("    repeatInfo ................. : {}".format(analogOut.repeatInfo(channel_index)))
        print("    repeatGet .................. : {}".format(analogOut.repeatGet(channel_index)))
        print("    repeatStatus ............... : {}".format(analogOut.repeatStatus(channel_index)))
        print("    repeatTriggerGet ........... : {}".format(analogOut.repeatTriggerGet(channel_index)))
        print("    limitationInfo ............. : {}".format(analogOut.limitationInfo(channel_index)))
        print("    limitationGet .............. : {}".format(analogOut.limitationGet(channel_index)))
        print("    modeGet .................... : {}".format(analogOut.modeGet(channel_index)))
        print("    customAMFMEnableGet ........ : {}".format(analogOut.customAMFMEnableGet(channel_index)))
        print()

        nodes = analogOut.nodeInfo(channel_index)

        print("    nodeInfo ................... : {}".format(nodes))
        print()

        for node in nodes:

            print("    Node ...... : {}".format(node))
            print()
            print("        nodeEnableGet .......... : {}".format(analogOut.nodeEnableGet(channel_index, node)))
            print("        nodeFunctionInfo ....... : {}".format(analogOut.nodeFunctionInfo(channel_index, node)))
            print("        nodeFunctionGet ........ : {}".format(analogOut.nodeFunctionGet(channel_index, node)))
            print("        nodeFrequencyInfo ...... : {}".format(analogOut.nodeFrequencyInfo(channel_index, node)))
            print("        nodeFrequencyGet ....... : {}".format(analogOut.nodeFrequencyGet(channel_index, node)))
            print("        nodeAmplitudeInfo ...... : {}".format(analogOut.nodeAmplitudeInfo(channel_index, node)))
            print("        nodeAmplitudeGet ....... : {}".format(analogOut.nodeAmplitudeGet(channel_index, node)))
            print("        nodeOffsetInfo ......... : {}".format(analogOut.nodeOffsetInfo(channel_index, node)))
            print("        nodeOffsetGet .......... : {}".format(analogOut.nodeOffsetGet(channel_index, node)))
            print("        nodeSymmetryInfo ....... : {}".format(analogOut.nodeSymmetryInfo(channel_index, node)))
            print("        nodeSymmetryGet ........ : {}".format(analogOut.nodeSymmetryGet(channel_index, node)))
            print("        nodePhaseInfo .......... : {}".format(analogOut.nodePhaseInfo(channel_index, node)))
            print("        nodePhaseGet ........... : {}".format(analogOut.nodePhaseGet(channel_index, node)))
            print("        nodeDataInfo ........... : {}".format(analogOut.nodeDataInfo(channel_index, node)))
            print("        nodePlayStatus ......... : {}".format(analogOut.nodePlayStatus(channel_index, node)))

            print()

    CH1 = 0
    CH2 = 1

    fs = 500000.0

    #analogOut.runSet(CH1, 1000)
    #analogOut.repeatSet(CH1, 1000)

    #analogOut.runSet(CH2, 1000)
    #analogOut.repeatSet(CH2, 1000)

    analogOut.nodeEnableSet(CH1, AnalogOutNode.Carrier, True)
    analogOut.nodeFunctionSet(CH1, AnalogOutNode.Carrier, FUNC.Play)
    analogOut.nodeFrequencySet(CH1, AnalogOutNode.Carrier, fs)

    analogOut.nodeEnableSet(CH2, AnalogOutNode.Carrier, True)
    analogOut.nodeFunctionSet(CH2, AnalogOutNode.Carrier, FUNC.Play)
    analogOut.nodeFrequencySet(CH2, AnalogOutNode.Carrier, fs)

    sampler_ch1 = sampler(fs, 0)
    sampler_ch2 = sampler(fs, 1)

    data = sampler_ch1.get_samples(4000)
    analogOut.nodePlayData(CH1, AnalogOutNode.Carrier, data)

    data = sampler_ch2.get_samples(4000)
    analogOut.nodePlayData(CH2, AnalogOutNode.Carrier, data)

    analogOut.masterSet(CH2, CH1)
    analogOut.configure(CH1, True) # start

    while True:

        ch1_status = analogOut.status(CH1)
        ch2_status = analogOut.status(CH2)

        (ch1_dataFree, ch1_dataLost, ch1_dataCorrupted) = analogOut.nodePlayStatus(CH1, AnalogOutNode.Carrier)
        (ch2_dataFree, ch2_dataLost, ch2_dataCorrupted) = analogOut.nodePlayStatus(CH2, AnalogOutNode.Carrier)

        if ch1_dataLost != 0 or ch1_dataCorrupted != 0 or ch2_dataLost != 0 or ch2_dataCorrupted != 0:
            print("ch1 status: {:10} {:10} {:10} ch2 status: {:10} {:10} {:10}".format(
                ch1_dataFree, ch1_dataLost, ch1_dataCorrupted,
                ch2_dataFree, ch2_dataLost, ch2_dataCorrupted))

        feed_ch1 = 0
        feed_ch2 = 0

        if ch1_dataFree > ch2_dataFree:
            if ch1_dataFree > 1000:
                feed_ch1 = ch1_dataFree
        else:
            if ch2_dataFree > 1000:
                feed_ch2 = ch2_dataFree

        if feed_ch1 > 0:
            data = sampler_ch1.get_samples(feed_ch1)
            analogOut.nodePlayData(CH1, AnalogOutNode.Carrier, data)

        if feed_ch2 > 0:
            data = sampler_ch2.get_samples(feed_ch2)
            analogOut.nodePlayData(CH2, AnalogOutNode.Carrier, data)

def main():

    parser = argparse.ArgumentParser(description="Demonstrate AnalogOut usage, continuous playback.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformsLibrary()
        with find_demo_device(dwf, args.serial_number) as device:
            demo_analog_output_instrument_api(device.analogOut)
    except DemoDeviceNotFoundError:
        print("Could not find demo device, exiting.")

if __name__ == "__main__":
    main()
