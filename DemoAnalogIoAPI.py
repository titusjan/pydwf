#! /usr/bin/env python3

import time
import argparse
import contextlib
from pydwf import DigilentWaveformLibrary


def demo_analog_io_api(analogIO) -> None:

    # Operations on the AnalogIO instrument:
    #
    # (ok) reset()
    #      configure()
    # (ok) status()
    #
    # (ok) enableInfo() -> Tuple[bool, bool]
    #      enableSet(master_enable: bool)
    # (ok) enableGet() -> bool
    # (ok) enableStatus() -> bool
    #
    # (ok) channelCount() -> int
    # (ok) channelName(channel_index: int) -> Tuple[str, str]
    # (ok) channelInfo(channel_index: int) -> int
    #
    # (ok) channelNodeName(channel_index: int, node_index: int) -> Tuple[str, str]
    # (ok) channelNodeInfo(channel_index: int, node_index: int) -> ANALOGIO
    # (ok) channelNodeSetInfo(channel_index: int, node_index: int) -> Tuple[float, float, int]
    #      channelNodeSet(channel_index: int, node_index: int, node_value: float)
    # (ok) channelNodeGet(channel_index: int, node_index: int) -> float
    # (ok) channelNodeStatusInfo(channel_index: int, node_index: int) -> Tuple[float, float, int]
    # (ok) channelNodeStatus(channel_index: int, node_index: int) -> float

    analogIO.reset()

    (enableSetSupported, enableStatusSupported) = analogIO.enableInfo()

    print("analogIO.enableSet() supported ......... : {}".format(enableSetSupported))
    print("analogIO.enableStatus() supported ...... : {}".format(enableStatusSupported))

    enableGet = analogIO.enableGet()
    print("analogIO.enableGet() ................... : {}".format(enableGet))

    enableStatus = analogIO.enableStatus()
    print("analogIO.enableStatus() ................ : {}".format(enableStatus))

    analogIO.status()

    channel_count = analogIO.channelCount()
    print("Analog IO device has {} channels:".format(channel_count))
    print()

    for channel_index in range(channel_count):
        channel_name = analogIO.channelName(channel_index)
        node_count = analogIO.channelInfo(channel_index)  # Count number of nodes.
        print("Channel #{} ({} of {} channels) named {} has {} nodes:".format(channel_index, channel_index+1, channel_count, channel_name, node_count))
        for node_index in range(node_count):
            node_name        = analogIO.channelNodeName(channel_index, node_index)
            node_info        = analogIO.channelNodeInfo(channel_index, node_index)
            node_set_info    = analogIO.channelNodeSetInfo(channel_index, node_index)
            node_get         = analogIO.channelNodeGet(channel_index, node_index)
            node_status_info = analogIO.channelNodeStatusInfo(channel_index, node_index)
            node_status      = analogIO.channelNodeStatus(channel_index, node_index)
            print("    node_#{} ({} of {}):".format(node_index, node_index + 1, node_count))
            print("        node_name ............. {}".format(node_name))
            print("        node_info ............. {}".format(node_info))
            print("        node_set_info ......... {}".format(node_set_info))
            print("        node_get .............. {}".format(node_get))
            print("        node_status_info ...... {}".format(node_status_info))
            print("        node_status ........... {}".format(node_status))
        print()

    channel_index = 2

    channel_name = analogIO.channelName(channel_index)[0]
    assert channel_name == "USB Monitor"
    for i in range(10):
        analogIO.status()  # Request status update
        usb_volts = analogIO.channelNodeStatus(channel_index, 0)
        usb_amps  = analogIO.channelNodeStatus(channel_index, 1)
        temp      = analogIO.channelNodeStatus(channel_index, 2)
        print("{}: {:.6f} [V] {:.3f} [mA] {:.2f} °C".format(channel_name, usb_volts, usb_amps * 1000.0, temp))
        time.sleep(0.100)

def open_demo_device(dwf, serial_number_sought):

    num_devices = dwf.enum.count()

    if num_devices == 0:
        raise RuntimeError("No Digilent Waveforms devices found.")

    serial_numbers_found = [dwf.enum.serialNumber(device_index) for device_index in range(num_devices)]

    if serial_number_sought is None:

        if num_devices != 1:
            raise RuntimeError("Multiple Digilent Waveforms devices found, specify one. Available devices: {}.".format(
                ", ".join(map(repr, serial_numbers_found))))
        else:
            return dwf.device.open(0)

    else:

        candidates = [device_index for (device_index, device_serial_number) in enumerate(serial_numbers_found) if device_serial_number == serial_number_sought]

        # A serial number was not specified.
        if len(candidates) == 0:
            raise RuntimeError("The specified serial number {} was not found. Available devices: {}.".format(
                repr(serial_number_sought), ", ".join(map(repr, serial_numbers_found))))
        elif len(candidates) != 1:
            raise ValueError("Multiple candidate devices for serial number specified ({}).".format(repr(serial_number_sought)))
        else:
            return dwf.device.open(candidates[0])

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the AnalogIO channels.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    dwf = DigilentWaveformLibrary()

    try:
        with contextlib.closing(open_demo_device(dwf, args.serial_number)) as device:
            demo_analog_io_api(device.analogIO)
    except Exception as exception:
        print("Error:", exception)

if __name__ == "__main__":
    main()
