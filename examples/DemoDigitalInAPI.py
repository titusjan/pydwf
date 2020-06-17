#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary
from demo_utilities import open_demo_device, OpenDemoDeviceError

def demo_digital_in_api(digitalIn):
    """Demonstrate the DigitalOut functionality.

    # Version 3.12.2 of the DWF library has 54 'FDwfDigitalIn' functions, 2 of which (FDwfDigitalInMixedSet, FDwfDigitalInTriggerSourceInfo) are obsolete.
    #
    # reset()
    # configure(reconfigure: bool, start: bool)
    #
    # status(readData: bool) -> DwfState
    # statusSamplesLeft() -> int
    # statusSamplesValid() -> int
    # statusIndexWrite() -> int
    # statusAutoTriggered() -> bool
    # statusData(idxChannel: int, cdData: int) -> np.ndarray
    # statusData2(idxChannel: int, idxData: int, cdData: int) -> np.ndarray
    # statusNoise2(idxChannel: int, idxData: int, cdData: int) -> np.ndarray
    # statusRecord(idxChannel: int, idxData: int, cdData: int) -> np.ndarray
    #
    # internalClockInfo() -> float
    #
    # clockSourceInfo()
    # clockSourceSet()
    # clockSourceGet()
    #
    # dividerInfo() -> int
    # dividerSet(div: int)
    # dividerGet() -> int
    #
    # bitsInfo() -> int
    # sampleFormatSet()
    # sampleFormatGet()
    # inputOrderSet()
    # bufferSizeInfo()
    # bufferSizeSet()
    # bufferSizeGet()
    # sampleModeInfo()
    # sampleModeSet()
    # sampleModeGet()
    # sampleSensibleSet()
    # sampleSensibleGet()
    # acquisitionModeInfo()
    # acquisitionModeSet()
    # acquisitionModeGet()
    # triggerSourceSet(trigsrc: TRIGSRC)
    # triggerSourceGet() -> TRIGSRC
    # triggerSlopeSet(slope: DwfTriggerSlope)
    # triggerSlopeGet() -> DwfTriggerSlope
    # triggerPositionInfo()
    # triggerPositionSet()
    # triggerPositionGet()
    # triggerPrefillSet()
    # triggerPrefillGet()
    # triggerAutoTimeoutInfo() -> Tuple[float, float, float]
    # triggerAutoTimeoutSet(secTimout: float)
    # triggerAutoTimeoutGet() -> float
    # triggerInfo() -> Tuple[int, int, int, int]
    # triggerSet(fsLevelLow: int, fsLevelHigh: int, fsEdgeRise: int, fsEdgeFall: int)
    # triggerGet() -> Tuple[int, int, int, int]
    # triggerResetSet(fsLevelLow: int, fsLevelHigh: int, fsEdgeRise: int, fsEdgeFall: int)
    # triggerCountSet()
    # triggerLengthSet()
    # triggerMatchSet()
    # mixedSet()
    # triggerSourceInfo()



    """

    digitalIn.reset()

    print("===== DigitalIn instrument, fixed information =====")
    print()

    print("    Number of available input bits ...... : {}".format(digitalIn.bitsInfo()))
    print("    Clock ............................... : {} [Hz]".format(digitalIn.internalClockInfo()))
    print("    Possible clock sources .............. : {{{}}}".format(", ".join(cs.name for cs in digitalIn.clockSourceInfo())))

    print("    Divider range (max) ................. : {}".format(digitalIn.dividerInfo()))
    print("    Possible acquisition modes .......... : {{{}}}".format(", ".join(cs.name for cs in digitalIn.acquisitionModeInfo())))
    #print("    Waiting time range (min, max) ................... : {} [s]".format(digitalOut.waitInfo()))
    #print("    Repeat range (min, max) ......................... : {}".format(digitalOut.repeatInfo()))

    #minmax = None
    #for channel_index in range(channel_count):
    #    divider_info = digitalOut.dividerInfo(channel_index)
    #    if channel_index == 0:
    #        minmax = divider_info
    #   else:
    #        assert minmax == divider_info

    #print("    Channel divider range (all channels) ............ : {}".format(minmax))

    #minmax = None
    #for channel_index in range(channel_count):
    #    counter_info = digitalOut.counterInfo(channel_index)
    #    if channel_index == 0:
    #        minmax = counter_info
    #    else:
    #        assert minmax == counter_info

    #print("    Channel counter range (all channels) ............ : {}".format(minmax))

    #bufsize = None
    #for channel_index in range(channel_count):
    #    data_info = digitalOut.dataInfo(channel_index)
    #    if channel_index == 0:
    #        bufsize = data_info
    #    else:
    #        assert bufsize == data_info

    #print("    Channel pattern buffer size (all channels) ...... : {}".format(bufsize))

    #print()

    #print("===== DigitalOut instrument, settings =====")
    #print()

    #print("    Trigger source ........... : {}".format(digitalOut.triggerSourceGet().name))
    #print("    Running time ............. : {}".format(digitalOut.runGet()))
    #print("    Waiting time ............. : {}".format(digitalOut.waitGet()))
    #print("    Repeat count ............. : {}".format(digitalOut.repeatGet()))
    #print("    Trigger slope ............ : {}".format(digitalOut.triggerSlopeGet().name))
    #print("    Repeat trigger ........... : {}".format(digitalOut.repeatTriggerGet()))
    #print()

    #print("===== DigitalOut instrument, status =====")
    #print()
    #print("    Running time status ...... : {}".format(digitalOut.runStatus()))
    #print("    Repeat count status ...... : {}".format(digitalOut.repeatStatus()))

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the DigitalIn (logic analyzer) functionality.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")
    args = parser.parse_args()

    try:
        dwf = DigilentWaveformLibrary()
        with contextlib.closing(open_demo_device(dwf, args.serial_number)) as device:
            demo_digital_out_api(device.digitalIn)
    except OpenDemoDeviceError:
        print("Could not open demo device, exiting.")

if __name__ == "__main__":
    main()
