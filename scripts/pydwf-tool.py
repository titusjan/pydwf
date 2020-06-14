#! /usr/bin/env python3

import argparse

from pydwf import DigilentWaveformLibrary, DwfEnumConfigInfo

def deploy_help_directory():
    pass

def deploy_examples_directory():
    pass

def show_version():
    dwf = DigilentWaveformLibrary()
    print("DWF library version: {!r}".format(dwf.getVersion()))

def summarize_api():
    pass

def enumerate_dwf_devices(use_obsolete_api: bool, list_configurations: bool):

    dwf = DigilentWaveformLibrary()

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

def main():

    parser = argparse.ArgumentParser(description="Enumerate Digilent Waveform devices.")
    parser.add_argument('-c', '--list-configurations', action='store_true',
                        help="for each device, printing its configurations", dest='list_configurations')
    parser.add_argument('-u', '--use-obsolete-api', action='store_true',
                        help="for each device, print analog-in parameters obtained using obsolete FDwfEnumAnalogIn* API calls", dest='use_obsolete_api')

    args = parser.parse_args()

    enumerate_dwf_devices(args.use_obsolete_api, args.list_configurations)


if __name__ == "__main__":
    main()
