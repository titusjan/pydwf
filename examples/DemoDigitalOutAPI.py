#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary
from demo_utilities import open_demo_device, OpenDemoDeviceError

def demo_digital_out_api(digitalOut) -> None:
    """Demonstrate the DigitalOut functionality.

    The DigitalOut API has 46 methods.

    Generic instrument functions:

    - reset()
    - configure(start: bool)
    - status() -> DwfState

    Global DigitalOut settings:

    - internalClockInfo() -> float

    - triggerSourceInfo() -> List[TRIGSRC]       NOTE: OBSOLETE!
    - triggerSourceSet(trigsrc: TRIGSRC)
    - triggerSourceGet() -> TRIGSRC

    - runInfo() -> Tuple[float, float]
    - runSet(secRun: float)
    - runGet() -> float
    - runStatus() -> float

    - waitInfo() -> Tuple[float, float]
    - waitSet(secWait: float)
    - waitGet() -> float

    - repeatInfo() -> Tuple[int, int]
    - repeatSet(repeat: int)
    - repeatGet() -> int
    - repeatStatus() -> int

    - triggerSlopeSet(slope: DwfTriggerSlope)
    - triggerSlopeGet() -> DwfTriggerSlope

    - repeatTriggerSet(repeatTrigger: bool)
    - repeatTriggerGet() -> bool

    Count the number of channels:

    - count() -> int

    Per-channel settings:

    - enableSet(idxChannel: int, enable: bool)
    - enableGet(idxChannel: int) -> bool

    - outputInfo(idxChannel: int) -> List[DwfDigitalOutOutput]
    - outputSet(idxChannel: int, v: DwfDigitalOutOutput)
    - outputGet(idxChannel: int) -> DwfDigitalOutOutput

    - typeInfo(idxChannel: int) -> List[DwfDigitalOutType]
    - typeSet(idxChannel: int, v: DwfDigitalOutType)
    - typeGet(idxChannel: int) -> DwfDigitalOutType

    - idleInfo(idxChannel: int) -> List[DwfDigitalOutIdle]
    - idleSet(idxChannel: int, idle_mode: DwfDigitalOutIdle)
    - idleGet(idxChannel: int) -> DwfDigitalOutIdle

    - dividerInfo(idxChannel: int) -> Tuple[int, int]
    - dividerInitSet(idxChannel: int, divider_init: int)
    - dividerInitGet(idxChannel: int) -> int
    - dividerSet(idxChannel: int, divider: int)
    - dividerGet(idxChannel: int) -> int

    - counterInfo(idxChannel: int) -> Tuple[int, int]
    - counterInitSet(idxChannel: int, high: bool, counter_init: int)
    - counterInitGet(idxChannel: int) -> Tuple[int, int]
    - counterSet(idxChannel: int, low_count: int, high_count: int)
    - counterGet(idxChannel: int) -> Tuple[int, int]

    - dataInfo(idxChannel: int) -> int
    - dataSet(idxChannel: int, bits: str, tristate: bool=False)

    """

    digitalOut.reset()

    print("===== DigitalOut instrument, fixed information =====")
    print()

    channel_count = digitalOut.count()

    print("    Clock ........................................... : {} [Hz]".format(digitalOut.internalClockInfo()))
    print("    Number of channels .............................. : {}".format(channel_count))
    print("    Possible trigger sources ........................ : {{{}}}".format(", ".join(ts.name for ts in digitalOut.triggerSourceInfo())))
    print("    Running time range (min, max) ................... : {} [s]".format(digitalOut.runInfo()))
    print("    Waiting time range (min, max) ................... : {} [s]".format(digitalOut.waitInfo()))
    print("    Repeat range (min, max) ......................... : {}".format(digitalOut.repeatInfo()))

    options = None
    for channel_index in range(channel_count):
        channel_output_info = digitalOut.outputInfo(channel_index)
        if channel_index == 0:
            options = channel_output_info
        else:
            assert options == channel_output_info

    print("    Channel output options (all channels) ........... : {{{}}}".format(", ".join(option.name for option in options)))

    options = None
    for channel_index in range(channel_count):
        channel_type_info = digitalOut.typeInfo(channel_index)
        if channel_index == 0:
            options = channel_type_info
        else:
            assert options == channel_type_info

    print("    Channel type options (all channels) ............. : {{{}}}".format(", ".join(option.name for option in options)))

    options = None
    for channel_index in range(channel_count):
        channel_idle_info = digitalOut.idleInfo(channel_index)
        if channel_index == 0:
            options = channel_idle_info
        else:
            assert options == channel_idle_info

    print("    Channel idle options (all channels) ............. : {{{}}}".format(", ".join(option.name for option in options)))

    minmax = None
    for channel_index in range(channel_count):
        divider_info = digitalOut.dividerInfo(channel_index)
        if channel_index == 0:
            minmax = divider_info
        else:
            assert minmax == divider_info

    print("    Channel divider range (all channels) ............ : {}".format(minmax))

    minmax = None
    for channel_index in range(channel_count):
        counter_info = digitalOut.counterInfo(channel_index)
        if channel_index == 0:
            minmax = counter_info
        else:
            assert minmax == counter_info

    print("    Channel counter range (all channels) ............ : {}".format(minmax))

    bufsize = None
    for channel_index in range(channel_count):
        data_info = digitalOut.dataInfo(channel_index)
        if channel_index == 0:
            bufsize = data_info
        else:
            assert bufsize == data_info

    print("    Channel pattern buffer size (all channels) ...... : {}".format(bufsize))

    print()

    print("===== DigitalOut instrument, settings =====")
    print()

    print("    Trigger source ........... : {}".format(digitalOut.triggerSourceGet().name))
    print("    Running time ............. : {}".format(digitalOut.runGet()))
    print("    Waiting time ............. : {}".format(digitalOut.waitGet()))
    print("    Repeat count ............. : {}".format(digitalOut.repeatGet()))
    print("    Trigger slope ............ : {}".format(digitalOut.triggerSlopeGet().name))
    print("    Repeat trigger ........... : {}".format(digitalOut.repeatTriggerGet()))
    print()

    print("===== DigitalOut instrument, status =====")
    print()
    print("    Running time status ...... : {}".format(digitalOut.runStatus()))
    print("    Repeat count status ...... : {}".format(digitalOut.repeatStatus()))

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the DigitalOut (pattern generator) functionality.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")
    args = parser.parse_args()

    try:
        dwf = DigilentWaveformLibrary()
        with contextlib.closing(open_demo_device(dwf, args.serial_number)) as device:
            demo_digital_out_api(device.digitalOut)
    except OpenDemoDeviceError:
        print("Could not open demo device, exiting.")

if __name__ == "__main__":
    main()
