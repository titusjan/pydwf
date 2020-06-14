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

    analogIn.acquisitionModeSet(ACQMODE.Record)

    analogIn.channelRangeSet(0, 5.0)
    analogIn.channelRangeSet(1, 5.0)

    analogIn.channelEnableSet(0, True)
    #analogIn.channelEnableSet(1, True)

    print_analogIn_info(analogIn)
    print()

    #fs = analogIn.frequencyGet()
    #print("fs:", fs)

    #time.sleep(5.0)

    for repeat in range(10):
        for sampleRate in [1, 2, 5, 10, 20, 50, 100, 200, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]:
            sleep_duration = min(0.1 * 8192 / sampleRate, 0.100)
            analogIn.frequencySet(sampleRate)
            for recordLength in [5.0]:
                analogIn.recordLengthSet(recordLength)

                data_samples = []
                ns = 0

                analogIn.configure(False, True)

                done_count = 0
                while done_count < 3:
                    status = analogIn.status(True)

                    samplesLeft   = analogIn.statusSamplesLeft()
                    samplesValid  = analogIn.statusSamplesValid()
                    indexWrite    = analogIn.statusIndexWrite()
                    autoTriggered = analogIn.statusAutoTriggered()
                    (dAvailable, dLost, dCorrupt) = analogIn.statusRecord()

                    xx = analogIn.statusData(0, dAvailable)
                    data_samples.append(xx)
                    ns += len(xx)

                    print("[{:10}] left {:8} valid {:8} index_write {:8} auto_triggered {:8} d_available {:8} d_lost {:8} d_corrupt {:8}      -- {:8}".format(
                        status.name, samplesLeft, samplesValid, indexWrite, autoTriggered, dAvailable, dLost, dCorrupt, ns))

                    time.sleep(sleep_duration)

                    if status == DwfState.Done:
                        done_count += 1
                    else:
                        done_count = 0

                print()
                time.sleep(0.5)

                data_samples = np.concatenate(data_samples)

                #plt.plot(data_samples, ".", ms=0.1)
                #plt.show()

def main():

    parser = argparse.ArgumentParser(description="Demonstrate AnalogIn usage in Record mode.")
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
