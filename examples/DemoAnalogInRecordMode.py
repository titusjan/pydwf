#! /usr/bin/env python3

import argparse
import contextlib
import time
import numpy as np
from pydwf import DigilentWaveformLibrary, ACQMODE, DwfState
from demo_utilities import open_demo_device, OpenDemoDeviceError

import matplotlib.pyplot as plt

def print_analogIn_info(analogIn):

    print("analogIn.statusSamplesLeft ........ : {}".format(analogIn.statusSamplesLeft()))
    print("analogIn.statusSamplesValid ....... : {}".format(analogIn.statusSamplesValid()))
    print("analogIn.statusIndexWrite ......... : {}".format(analogIn.statusIndexWrite()))
    print("analogIn.statusAutoTriggered ...... : {}".format(analogIn.statusAutoTriggered()))
    print("analogIn.statusRecord ............. : {}".format(analogIn.statusRecord()))

    print("analogIn.recordLengthGet .......... : {}".format(analogIn.recordLengthGet()))
    print("analogIn.frequencyInfo ............ : {}".format(analogIn.frequencyInfo()))
    print("analogIn.frequencyGet ............. : {}".format(analogIn.frequencyGet()))
    print("analogIn.bitsInfo ................. : {}".format(analogIn.bitsInfo()))
    print("analogIn.bufferSizeInfo ........... : {}".format(analogIn.bufferSizeInfo()))
    print("analogIn.bufferSizeGet ............ : {}".format(analogIn.bufferSizeGet()))
    print("analogIn.noiseSizeInfo ............ : {}".format(analogIn.noiseSizeInfo()))
    print("analogIn.noiseSizeGet ............. : {}".format(analogIn.noiseSizeGet()))
    print("analogIn.acquisitionModeInfo ...... : {}".format(analogIn.acquisitionModeInfo()))
    print("analogIn.acquisitionModeGet ....... : {}".format(analogIn.acquisitionModeGet()))
    print()
    print("analogIn.channelCount ....... : {}".format(analogIn.channelCount()))
    print()

    print("analogIn.channelFilterInfo ...... : {}".format(analogIn.channelFilterInfo()))
    print("analogIn.channelRangeInfo ....... : {}".format(analogIn.channelRangeInfo()))
    print("analogIn.channelRangeSteps ...... : {}".format(analogIn.channelRangeSteps()))
    print("analogIn.channelOffsetInfo ...... : {}".format(analogIn.channelOffsetInfo()))
    print()

    for channel_index in range(analogIn.channelCount()):
        print("[{}] analogIn.channelEnableGet ........... : {}".format(channel_index, analogIn.channelEnableGet(channel_index)))
        print("[{}] analogIn.channelFilterGet ........... : {}".format(channel_index, analogIn.channelFilterGet(channel_index)))
        print("[{}] analogIn.channelRangeGet ............ : {}".format(channel_index, analogIn.channelRangeGet(channel_index)))
        print("[{}] analogIn.channelOffsetGet ........... : {}".format(channel_index, analogIn.channelOffsetGet(channel_index)))
        print("[{}] analogIn.channelAttenuationGet ...... : {}".format(channel_index, analogIn.channelAttenuationGet(channel_index)))
        print()

    print("analogIn.triggerSourceGet ............ : {}".format(analogIn.triggerSourceGet()))
    print("analogIn.triggerPositionInfo ......... : {}".format(analogIn.triggerPositionInfo()))
    print("analogIn.triggerPositionGet .......... : {}".format(analogIn.triggerPositionGet()))
    print("analogIn.triggerPositionStatus ....... : {}".format(analogIn.triggerPositionStatus()))
    print("analogIn.triggerAutoTimeoutInfo ...... : {}".format(analogIn.triggerAutoTimeoutInfo()))
    print("analogIn.triggerAutoTimeoutGet ....... : {}".format(analogIn.triggerAutoTimeoutGet()))
    print("analogIn.triggerHoldOffInfo .......... : {}".format(analogIn.triggerHoldOffInfo()))
    print("analogIn.triggerHoldOffGet ........... : {}".format(analogIn.triggerHoldOffGet()))
    print("analogIn.triggerTypeInfo ............. : {}".format(analogIn.triggerTypeInfo()))
    print("analogIn.triggerTypeGet .............. : {}".format(analogIn.triggerTypeGet()))
    print()
    print("analogIn.samplingSourceGet ........... : {}".format(analogIn.samplingSourceGet()))
    print("analogIn.samplingSlopeGet ............ : {}".format(analogIn.samplingSlopeGet()))
    print("analogIn.samplingDelaySet ............ : {}".format(analogIn.samplingDelayGet()))
    print()
    print("analogIn.triggerSourceInfo ........... : {}".format(analogIn.triggerSourceInfo()))

# triggerAutoTimeoutInfo(self) -> Tuple[float, float, float]
# triggerAutoTimeoutSet(self, secTimout: float) -> None
# triggerAutoTimeoutGet(self) -> float
# triggerHoldOffInfo(self) -> Tuple[float, float, float]
# triggerHoldOffSet(self, secHoldOff: float) -> None
# triggerHoldOffGet(self) -> float
# triggerTypeInfo(self) -> List[TRIGTYPE]
# triggerTypeSet(self, trigtype: TRIGTYPE) -> None
# triggerTypeGet(self) -> TRIGTYPE
# triggerChannelInfo(self) -> Tuple[int, int]
# triggerChannelSet(self, idxChannel: int) -> None
# triggerChannelGet(self) -> int
# triggerFilterInfo(self) -> List[FILTER]
# triggerFilterSet(self, filter: FILTER) -> None
# triggerFilterGet(self) -> FILTER
# triggerLevelInfo(self) -> Tuple[float, float, float]
# triggerLevelSet(self, voltsLevel: float) -> None
# triggerLevelGet(self) -> float
# triggerHysteresisInfo(self) -> Tuple[float, float, float]
# triggerHysteresisSet(self, voltsLevel: float) -> None
# triggerHysteresisGet(self) -> float
# triggerConditionInfo(self) -> List[DwfTriggerSlope]
# triggerConditionSet(self, trigger_condition: DwfTriggerSlope) -> None
# triggerConditionGet(self) -> DwfTriggerSlope
# triggerLengthInfo(self) -> Tuple[float, float, float]
# triggerLengthSet(self, secLength: float) -> None
# triggerLengthGet(self) -> float
# triggerLengthConditionInfo(self) -> List[TRIGLEN]
# triggerLengthConditionSet(self, triglen: TRIGLEN) -> None
# triggerLengthConditionGet(self) -> TRIGLEN

# samplingSourceSet(self, trigsrc: TRIGSRC) -> None
# samplingSourceGet(self) -> TRIGSRC
# samplingSlopeSet(self, slope: DwfTriggerSlope) -> None
# samplingSlopeGet(self) -> DwfTriggerSlope
# samplingDelaySet(self, sec: float) -> None
# samplingDelayGet(self) -> float
# triggerSourceInfo(self) -> List[TRIGSRC]


def demo_analog_input_instrument_api_simple(analogIn):
    """Demonstrates the simplest possible use of the analog-in channels.

    This demonstration simply calls the status() function of the AnalogIn instrument, with the 'readdData' argument specified as value False.
    Even though the 'readData' argument is false, the status update requested from the instrument does return up-to-date voltage levels of each
    of the channels.

    This very simple way of querying the current AnalogIn voltages may be sufficient for very simple applications that have no strict requirement
    on sample timing and triggering.
    """

    channel_count = analogIn.channelCount()
    if channel_count == 0:
        print("The device has no analog input channels that can be used for this demo.")
        return

    analogIn.reset()

    analogIn.frequencySet(11050.0)
    fs = analogIn.frequencyGet()
    print("fs:", fs)

    analogIn.acquisitionModeSet(ACQMODE.Record)

    analogIn.recordLengthSet(5.0)

    analogIn.channelRangeSet(0, 5.0)
    analogIn.channelRangeSet(1, 5.0)

    analogIn.channelEnableSet(0, True)
    analogIn.channelEnableSet(1, True)

    print_analogIn_info(analogIn)

    #time.sleep(5.0)

    analogIn.configure(False, True)

    data_samples = []

    while True:
        status = analogIn.status(True)

        samplesLeft   = analogIn.statusSamplesLeft()
        samplesValid  = analogIn.statusSamplesValid()
        indexWrite    = analogIn.statusIndexWrite()
        autoTriggered = analogIn.statusAutoTriggered()
        (dAvailable, dLost, dCorrupt) = analogIn.statusRecord()

        xx = analogIn.statusData(0, dAvailable)

        print("[{}] left {} valid {} index_write {} auto_triggered {} d_available {} d_lost {} d_corrupt {}".format(
            status, samplesLeft, samplesValid, indexWrite, autoTriggered, dAvailable, dLost, dCorrupt))

        print(xx.shape)

        data_samples.append(xx)

        time.sleep(0.010)

        if dAvailable == 0:
            break

    data_samples = np.concatenate(data_samples)

    print(data_samples.shape, data_samples.dtype)

    plt.plot(data_samples, ".")
    plt.show()

def main():

    parser = argparse.ArgumentParser(description="Demonstrate simplest possible AnalogIn usage.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformLibrary()
        with contextlib.closing(open_demo_device(dwf, args.serial_number)) as device:
            demo_analog_input_instrument_api_simple(device.analogIn)
    except OpenDemoDeviceError:
        print("Could not open demo device, exiting.")

if __name__ == "__main__":
    main()
