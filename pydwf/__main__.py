#! /usr/bin/env python3

"""This is the "pydwf" support tool that can be executed as "python -m pydwf".
"""

import zipfile
import io
import os
import base64
import argparse
import importlib
from collections import Counter

import pydwf
from pydwf import DigilentWaveformsLibrary, DwfEnumConfigInfo
from pydwf.dwf_function_signatures import dwf_function_signatures, dwf_version

def show_version():
    """Show DWF library version number."""

    dwf = DigilentWaveformsLibrary()
    print("pydwf version ............ : {}".format(pydwf.__version__))
    print("DWF library version ...... : {}".format(dwf.getVersion()))

def list_devices(use_obsolete_api: bool, list_configurations: bool):
    """List devices supported by the DWF library."""

    dwf = DigilentWaveformsLibrary()

    num_devices = dwf.enum.count()

    if num_devices == 0:
        print("No Digilent Waveforms devices found.")

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

def extract_zip_to_directory(target):
    """Extract a directory with auxiliary package data."""
    if os.path.exists(target):
        print()
        print("Unable to unpack '{}', the path already exists.".format(target))
        print()
    else:
        print()
        print("Unpacking '{}' ...".format(target))
        print()

        # We only import "pydwf.auxiliary_package_data" if we actually need to access data from it.
        # It's a very big file; importing it takes a noticable amount of time.
        targets = importlib.import_module("pydwf.auxiliary_package_data").targets

        # Decode and unpack the directory.
        zipfile.ZipFile(io.BytesIO(base64.b64decode(targets[target]))).extractall()

def main():

    parser = argparse.ArgumentParser(
        prog = "python -m pydwf",
        description="Utilities for the pydwf package.",
    )
    subparsers = parser.add_subparsers()

    # If no command is given, execute the toplevel parser's "print_help" method.
    parser.set_defaults(execute=lambda args: parser.print_help())

    # Declare the sub-parser for the "version" command.
    subparser_version = subparsers.add_parser("version",
        description="Show version of the DWF library.",
        help="show version of the DWF library")
    subparser_version.set_defaults(execute=lambda args: show_version())

    # Declare the sub-parser for the "list" command.
    subparser_list = subparsers.add_parser("list", aliases=["ls"],
        description="List Digilent Waveforms devices.",
        help="list Digilent Waveform devices")
    subparser_list.add_argument('-u', '--use-obsolete-api', action='store_true',
                        help="for each device, print analog-in parameters obtained using obsolete FDwfEnumAnalogIn* API calls", dest='use_obsolete_api')
    subparser_list.add_argument('-c', '--list-configurations', action='store_true',
                        help="for each device, printing its configurations", dest='list_configurations')
    subparser_list.set_defaults(execute=lambda args: list_devices(args.use_obsolete_api, args.list_configurations))

    # Declare the sub-parser for the "extract-examples" command.
    subparser_extract_examples = subparsers.add_parser("extract-examples",
        description="Extract pydwf example scripts to 'pydwf-examples' directory.",
        help="extract pydwf example scripts to 'pydwf-examples' directory")
    subparser_extract_examples.set_defaults(execute=lambda args: extract_zip_to_directory("pydwf-examples"))

    # Declare the sub-parser for the "extract-html-docs" command.
    subparser_extract_html = subparsers.add_parser("extract-html-docs",
        description="Extract pydwf HTML documentation to 'pydwf-html-docs' directory.",
        help="extract pydwf HTML documentation to 'pydwf-html-docs' directory")
    subparser_extract_html.set_defaults(execute=lambda args: extract_zip_to_directory("pydwf-html-docs"))

    # Parse command-line arguments.
    args = parser.parse_args()

    # Execute the selected command.
    args.execute(args)

if __name__ == "__main__":
    main()
