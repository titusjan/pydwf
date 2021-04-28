#! /usr/bin/env python3

"""
This is the "pydwf" support tool that can be executed as "python -m pydwf".
"""

from collections import Counter
import argparse

from pydwf import DigilentWaveformsLibrary
from .dwf_function_signatures import dwf_function_signatures, dwf_version

def show_version():
    """Show DWF library version number."""

    dwf = DigilentWaveformsLibrary()
    print("DWF library version: {}".format(dwf.getVersion()))

def summarize_api():

    class typespec_null:
        def __getattr__(self, name):
            return None

    typespec = typespec_null()

    function_signatures = dwf_function_signatures(typespec)

    categories = {}

    for (name, rettype, params, obsolete_flag) in function_signatures:
        if name.startswith("FDwfAnalogOut"):
            category = "FDwfAnalogOut"
        elif name.startswith("FDwfDevice"):
            category = "FDwfDevice"
        elif name.startswith("FDwfAnalogIn"):
            category = "FDwfAnalogIn"
        elif name.startswith("FDwfDigitalSpi"):
            category = "FDwfDigitalSpi"
        elif name.startswith("FDwfDigitalI2c"):
            category = "FDwfDigitalI2c"
        elif name.startswith("FDwfDigitalCan"):
            category = "FDwfDigitalCan"
        elif name.startswith("FDwfDigitalUart"):
            category = "FDwfDigitalUart"
        elif name.startswith("FDwfDigitalIn"):
            category = "FDwfDigitalIn"
        elif name.startswith("FDwfDigitalOut"):
            category = "FDwfDigitalOut"
        elif name.startswith("FDwfAnalogIO"):
            category = "FDwfAnalogIO"
        elif name.startswith("FDwfEnum"):
            category = "FDwfEnum"
        elif name.startswith("FDwfDigitalIO"):
            category = "FDwfDigitalIO"
        elif name.startswith("FDwfAnalogImpedance"):
            category = "FDwfAnalogImpedance"
        else:
            category = "(miscellaneous)"

        if category not in categories:
            categories[category] = Counter()
        categories[category][obsolete_flag] += 1

    print()
    print("DWF API summary: functions by category")
    print("======================================")
    print()
    print("DWF version: {}".format(dwf_version))
    print()
    total_count_false = 0
    total_count_true = 0
    for category, counter in categories.items():
        count_false = counter[False]
        count_true  = counter[True]
        total_count_false += count_false
        total_count_true  += count_true
        print("{:19}    active {:3}    obsolete {:3}    total {:3}".format(category, count_false, count_true, count_false + count_true))
    print("-------------------    ----------    ------------    ---------")
    print("TOTAL                  active {:3}    obsolete {:3}    total {:3}".format(total_count_false, total_count_true, total_count_false + total_count_true))
    print()

def list_devices(use_obsolete_api: bool, list_configurations: bool):
    """List devices supported by the DWF library."""

    dwf = DigilentWaveformsLibrary()

    num_devices = dwf.enum.count()

    if num_devices == 0:
        print("No Digilent Waveform devices found.")

    for device_index in range(num_devices):

        devtype = dwf.enum.deviceType(device_index)
        is_open = dwf.enum.deviceIsOpened(device_index)
        username = dwf.enum.userName(device_index)
        devicename = dwf.enum.deviceName(device_index)
        serial = dwf.enum.serialNumber(device_index)

        if num_devices == 1:
            header = "Device information for device #{} ({} device found)".format(device_index, num_devices)
        else:
            header = "Device information for device #{} ({} of {} devices found)".format(device_index, device_index+1, num_devices)

        print(header)
        print("=" * len(header))
        print()
        print("  device .......... : {}".format(devtype[0]))
        print("  version ......... : {}".format(devtype[1]))
        print("  open ............ : {}".format(is_open))
        print("  username ........ : {!r}".format(username))
        print("  devicename ...... : {!r}".format(devicename))
        print("  serial .......... : {!r}".format(serial))
        print()
        if use_obsolete_api:

            ai_channels = dwf.enum.analogInChannels(device_index)
            ai_bufsize = dwf.enum.analogInBufferSize(device_index)
            ai_bits = dwf.enum.analogInBits(device_index)
            ai_frequency = dwf.enum.analogInFrequency(device_index)

            print("  Analog-in information (obsolete API)")
            print("  ------------------------------------")
            print()
            print("  number of channels ...... : {!r}".format(ai_channels))
            print("  buffer size ............. : {!r}".format(ai_bufsize))
            print("  bits .................... : {!r}".format(ai_bits))
            print("  frequency ............... : {!r}".format(ai_frequency))
            print()

        if list_configurations:

            configuration_data = {}

            num_config = dwf.enum.configCount(device_index)

            for configuration_index in range(num_config):
                for configuration_parameter in DwfEnumConfigInfo:
                    configuration_parameter_value = dwf.enum.configInfo(configuration_index, configuration_parameter)
                    configuration_data[(configuration_index, configuration_parameter)] = configuration_parameter_value

            print("  Configuration:          {}".format("  ".join("{:8d}".format(configuration_index) for configuration_index in range(num_config))))
            print("  ----------------------  {}".format("  ".join("--------" for configuration_index in range(num_config))))
            for configuration_parameter in DwfEnumConfigInfo:
                print("  {:22}  {}".format(configuration_parameter.name, "  ".join("{:8d}".format(configuration_data[(configuration_index, configuration_parameter)]) for configuration_index in range(num_config))))
            print()


def extract_examples():
    raise NotImplementedError()

def extract_html_documentation():
    raise NotImplementedError()

def extract_pdf_documentation():
    raise NotImplementedError()

def main():

    parser = argparse.ArgumentParser(
        prog = "python -m pydwf",
        description="Utilities for the pydwf package.",
    )
    subparsers = parser.add_subparsers()

    # If no command is given, execute the toplevel parser's "print_help" method.
    parser.set_defaults(execute=lambda args: parser.print_help())

    # Declare the sub-parser for the "version" command.
    parser_version = subparsers.add_parser("version",
        description="Show version of the DWF library.",
        help="show version of the DWF library")
    parser_version.set_defaults(execute=lambda args: show_version())

    # Declare the sub-parser for the "ls" command.

    parser_ls = subparsers.add_parser("ls", aliases=["list", "list-devices"],
        description="List Digilent Waveforms devices.",
        help="list Digilent Waveform devices")
    parser_ls.add_argument('-c', '--list-configurations', action='store_true',
                        help="for each device, printing its configurations", dest='list_configurations')
    parser_ls.add_argument('-u', '--use-obsolete-api', action='store_true',
                        help="for each device, print analog-in parameters obtained using obsolete FDwfEnumAnalogIn* API calls", dest='use_obsolete_api')
    parser_ls.set_defaults(execute=lambda args: list_devices(args.list_configurations, args.use_obsolete_api))

    # Parse command-line arguments.
    args = parser.parse_args()

    # Execute the selected command.
    args.execute(args)

if __name__ == "__main__":
    main()
