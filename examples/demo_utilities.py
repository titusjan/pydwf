class DemoDeviceNotFoundError(Exception):
    pass

def find_demo_device(dwf, serial_number_specified):

    # The dwf.enum.count() function builds a table of connected devices that can be queried using the dwf.enum functions.
    num_devices = dwf.enum.count()

    if num_devices == 0:
        print("No Digilent Waveforms devices found.")
        raise DemoDeviceNotFoundError()

    serial_numbers_found = [dwf.enum.serialNumber(device_index) for device_index in range(num_devices)]

    if serial_number_specified is None:
        # A serial number was not specified.
        if num_devices != 1:
            print("Multiple Digilent Waveforms devices found, specify one.")
            print("Available devices: {}.".format(", ".join(map(repr, serial_numbers_found))))
            raise DemoDeviceNotFoundError()
        else:
            # Open the only device.
            return dwf.device.open(0)

    else:
        # A serial number was specified.
        candidates = [device_index for (device_index, device_serial_number) in enumerate(serial_numbers_found) if device_serial_number == serial_number_specified]

        if len(candidates) == 0:
            print("The specified serial number {} was not found.".format(repr(serial_number_specified)))
            print("Available devices: {}.".format(", ".join(map(repr, serial_numbers_found))))
            raise DemoDeviceNotFoundError()
        elif len(candidates) != 1:
            print("Multiple candidate devices for the serial number specified ({}).".format(repr(serial_number_specified)))
            raise DemoDeviceNotFoundError()
        else:
            # Open the single candidate device.
            return dwf.device.open(candidates[0])
