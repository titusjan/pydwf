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
    print("channel count: {}".format(channel_count))

    for channel_index in range(channel_count):
        channel_name = analogIO.channelName(channel_index)
        node_count = analogIO.channelInfo(channel_index)  # Count number of nodes.
        print("channel_index {} channel_name {} node_count {}".format(channel_index, channel_name, node_count))
        for node_index in range(node_count):
            node_name        = analogIO.channelNodeName(channel_index, node_index)
            node_info        = analogIO.channelNodeInfo(channel_index, node_index)
            node_set_info    = analogIO.channelNodeSetInfo(channel_index, node_index)
            node_get         = analogIO.channelNodeGet(channel_index, node_index)
            node_status_info = analogIO.channelNodeStatusInfo(channel_index, node_index)
            node_status      = analogIO.channelNodeStatus(channel_index, node_index)
            print("    node_index {} node_name {} node_info {} node_set_info {} node_get {} node_status_info {} node_status {}".format(node_index, node_name, node_info, node_set_info, node_get, node_status_info, node_status))

    while True:
        analogIO.status()  # Request status update
        usb_volts = analogIO.channelNodeStatus(2, 0)
        usb_amps  = analogIO.channelNodeStatus(2, 1)
        temp      = analogIO.channelNodeStatus(2, 2)
        print("{:.6f} [V] {:.3f} [mA] {:.2f} °C".format(usb_volts, usb_amps * 1000.0, temp))
        time.sleep(0.100)

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the AnalogIO channels.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")

    args = parser.parse_args()

    dwf = DigilentWaveformLibrary()
    with contextlib.closing(dwf.device.openBySerialNumber(args.serial_number)) as device:
        demo_analog_io_api(device.analogIO)

if __name__ == "__main__":
    main()
