#! /usr/bin/env python3

import argparse
import contextlib
from typing import Optional

from pydwf import DigilentWaveformLibrary

def enum_list_to_str(elist):
    return "{} ({})".format(type(elist[0]).__name__, ", ".join("{}:{}".format(e.name, e.value) for e in elist))

def print_info(digitalOut, num_channels: Optional[int]):

        internal_clock = digitalOut.internalClockInfo()
        trigger_source_info = digitalOut.triggerSourceInfo()
        trigger_source_setting = digitalOut.triggerSourceGet()
        run_info = digitalOut.runInfo()
        run_setting = digitalOut.runGet()
        run_status = digitalOut.runGet()
        wait_info = digitalOut.waitInfo()
        wait_setting = digitalOut.waitGet()
        repeat_info = digitalOut.repeatInfo()
        repeat_setting = digitalOut.repeatGet()
        repeat_status = digitalOut.repeatStatus()
        trigger_slope_setting = digitalOut.triggerSlopeGet()
        repeat_trigger_setting = digitalOut.repeatTriggerGet()
        channel_count = digitalOut.count()

        print("Instrument-level settings")
        print("=========================")
        print()

        print("internal clock ........................ : {} [Hz]".format(internal_clock))
        print("trigger source info (DEPRECATED) ...... : {}".format(enum_list_to_str(trigger_source_info)))
        print("trigger source setting ................ : {}".format(trigger_source_setting))
        print("run info .............................. : {}".format(run_info))
        print("run setting ........................... : {}".format(run_setting))
        print("run status ............................ : {}".format(run_status))
        print("wait info ............................. : {} [s]".format(wait_info))
        print("wait setting .......................... : {} [s]".format(wait_setting))
        print("repeat info ........................... : {}".format(repeat_info))
        print("repeat setting ........................ : {}".format(repeat_setting))
        print("repeat status ......................... : {}".format(repeat_status))
        print("trigger slope setting ................. : {}".format(trigger_slope_setting))
        print("repeat trigger setting ................ : {}".format(repeat_trigger_setting))
        print()

        print("channel count ......................... : {}".format(channel_count))
        print()

        if num_channels is not None:
            display_channel_count = min(channel_count, num_channels)
        else:
            display_channel_count = channel_count

        for channel_index in range(display_channel_count):

            channel_enable_setting = digitalOut.enableGet(channel_index)
            channel_output_info = digitalOut.outputInfo(channel_index)
            channel_output_setting = digitalOut.outputGet(channel_index)
            channel_type_info = digitalOut.typeInfo(channel_index)
            channel_type_setting = digitalOut.typeGet(channel_index)
            channel_idle_info = digitalOut.idleInfo(channel_index)
            channel_idle_setting = digitalOut.idleGet(channel_index)
            channel_divider_info = digitalOut.dividerInfo(channel_index)
            channel_divider_setting = digitalOut.dividerGet(channel_index)
            channel_divider_init_setting = digitalOut.dividerInitGet(channel_index)
            channel_counter_info = digitalOut.counterInfo(channel_index)
            channel_counter_setting = digitalOut.counterGet(channel_index)
            channel_counter_init_setting = digitalOut.counterInitGet(channel_index)
            channel_data_info = digitalOut.dataInfo(channel_index)

            channel_title = "Channel #{} ({} of {})".format(channel_index, channel_index + 1, channel_count)

            print(channel_title)
            print("=" * len(channel_title))
            print()
            print("enable setting ............ : {}".format(channel_enable_setting))
            print("output info ............... : {}".format(enum_list_to_str(channel_output_info)))
            print("output setting ............ : {}".format(channel_output_setting))
            print("type info ................. : {}".format(enum_list_to_str(channel_type_info)))
            print("type setting .............. : {}".format(channel_type_setting))
            print("idle info ................. : {}".format(enum_list_to_str(channel_idle_info)))
            print("idle setting .............. : {}".format(channel_idle_setting))
            print("divider info .............. : {}".format(channel_divider_info))
            print("divider setting ........... : {}".format(channel_divider_setting))
            print("divider init setting ...... : {}".format(channel_divider_init_setting))
            print("counter info .............. : {}".format(channel_counter_info))
            print("counter setting ........... : {}".format(channel_counter_setting))
            print("counter init setting ...... : {}".format(channel_counter_init_setting))
            print("data info ................. : {}".format(channel_data_info))
            print()

def demonstrate_usage(serial_number: str, num_channels: Optional[int]) -> None:

    # Version 3.12.1 of the DWF library has 46 'FDwfDigitalOut' functions, 1 of which (FDwfDigitalOutTriggerSourceInfo) is obsolete.
    #
    # [1] reset()
    # [1] configure(start: bool)
    # [1] status() -> DwfState
    #
    # [1] internalClock    float                  [Hz]   Info
    # [3] triggerSource    TRIGSRC                [-]    Info Set Get              // NOTE: triggerSourceInfo() is obsolete.
    # [4] run              float                  [s]    Info Set Get Status
    # [3] wait             float                  [s]    Info Set Get
    # [4] repeat           int                    [-]    Info Set Get Status
    # [2] triggerSlope     DwfTriggerSlope        [-]         Set Get
    # [2] repeatTrigger    bool                   [-]         Set Get
    # [1] count()          int                    [-]                              // counts number of channels
    #
    # ====== Per channel:
    #
    # [2] enable           bool                   [-]         Set Get
    # [3] output           DwfDigitalOutOutput    [-]    Info Set Get
    # [3] type             DwfDigitalOutType      [-]    Info Set Get
    # [3] idle             DwfDigitalOutIdle      [-]    Info Set Get
    # [5] divider          int                    [-]    Info Set Get InitSet InitGet
    # [5] counter          int                    [-]    Info Set Get InitSet InitGet
    # [2] data             string                 [-]    Info Set

    dwf = DigilentWaveformLibrary()

    with contextlib.closing(dwf.device.openBySerialNumber(serial_number)) as device:

        digitalOut = device.digitalOut

        digitalOut.reset()

        print_info(digitalOut, num_channels)

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the DigitalOut instrument.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")
    parser.add_argument('-n', '--num-channels', type=int, help="display only the first n channels")

    args = parser.parse_args()

    demonstrate_usage(args.serial_number, args.num_channels)

if __name__ == "__main__":
    main()
