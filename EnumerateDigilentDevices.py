#! /usr/bin/env python3

import argparse

from pydwf import DigilentWaveformLibrary, DwfEnumConfigInfo

def main():

    parser = argparse.ArgumentParser(description="Enumerate Digilent Discovery devices.")
    parser.add_argument('-o', '--obsolete', action='store_true',
                        help="for each device, retrieve and show analog-in parameters using obsolete FDwfEnumAnalogIn* API calls", dest='show_obsolete')
    parser.add_argument('-c', '--configurations', action='store_true',
                        help="for each device, show available configurations", dest='list_configurations')

    args = parser.parse_args()

    dwf = DigilentWaveformLibrary()

    num_devices = dwf.enum.count()
    for device_index in range(num_devices):

        print("Device index {} ({} of {} devices):".format(device_index, device_index+1, num_devices))
        print()

        devtype = dwf.enum.deviceType(device_index)
        is_open = dwf.enum.deviceIsOpened(device_index)
        username = dwf.enum.userName(device_index)
        devicename = dwf.enum.deviceName(device_index)
        serial = dwf.enum.serialNumber(device_index)

        print("    device .......... : {}".format(devtype[0]))
        print("    version ......... : {}".format(devtype[1]))
        print("    open ............ : {}".format(is_open))
        print("    username ........ : {!r}".format(username))
        print("    devicename ...... : {!r}".format(devicename))
        print("    serial .......... : {!r}".format(serial))
        print()

        if args.show_obsolete:

            ai_channels = dwf.enum.analogInChannels(device_index)
            ai_bufsize = dwf.enum.analogInBufferSize(device_index)
            ai_bits = dwf.enum.analogInBits(device_index)
            ai_frequency = dwf.enum.analogInFrequency(device_index)

            print("    analog-in info (obsolete API):")
            print()
            print("    number of channels ...... : {!r}".format(ai_channels))
            print("    buffer size ............. : {!r}".format(ai_bufsize))
            print("    bits .................... : {!r}".format(ai_bits))
            print("    frequency ............... : {!r}".format(ai_frequency))
            print()

        if args.list_configurations:

            num_config = dwf.enum.configCount(device_index)
            for configuration_index in range(num_config):

                print("    Configuration index {} ({} of {} configurations):".format(configuration_index,configuration_index+1, num_config))
                print()
                for configuration_parameter in DwfEnumConfigInfo:
                    configuration_parameter_value = dwf.enum.configInfo(configuration_index, configuration_parameter)
                    print("        {:22s} : {:8d}".format(configuration_parameter.name, configuration_parameter_value))
                print()

            print()

if __name__ == "__main__":
    main()
