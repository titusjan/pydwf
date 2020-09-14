"""Python binding for the DWF (Digilent Waveforms) shared library.

This binding is based on the C header file "dwf.h", version 3.14.3, as extracted from the Linux package;
size = 48046 bytes; md5sum = cdc0e93efaf1d82d7a1a8c1d5a4e68a0670fc8ba690cbe0f848444c6f1458682.

Open issues:

- In dwf.h, function FDwfDigitalInInputOrderSet, parameter 'fDioFirst' is a bool. This doesn't exist in C.
- There's a bunch of lines in dwf.h with trailing spaces.
- The DEVVER enum type has 2 values with integer 2, is that intentional?
- The DwfState enum type has 2 values with integer 3, is that intentional?
- FDwfAnalogInTriggerForce not documented in the PDF?
- FDwfAnalogInTriggerHoldOffInfo: parameter is called 'pnStep' rather than 'pnSteps'.

(Some of these were addressed in an email response; cross-reference.)
"""

import sys
import ctypes
import enum
import numpy as np
from typing import Optional, Tuple, List

from .dwf_function_signatures import dwf_function_signatures


HDWF_NONE = 0  # HDWF value representing a bad device handle.

_RESULT_SUCCESS = 1  # This value is returned by all API calls in case of success. (This used to be a boolean in earlier versions of the library).

@enum.unique
class ENUMFILTER(enum.Enum):
    """Device enumeration filter constants, represented as type 'int'."""
    All        = 0
    EExplorer  = 1
    Discovery  = 2
    Discovery2 = 3
    DDiscovery = 4

@enum.unique
class DEVID(enum.Enum):
    """Device ID constants, represented as type 'int'."""
    EExplorer  = 1
    Discovery  = 2
    Discovery2 = 3
    DDiscovery = 4

# Note: enum values are not unique.
class DEVVER(enum.Enum):
    """Device version, represented as type 'int'."""
    EExplorerC = 2  # Duplicate enum value with DiscoveryB (historical)
    EExplorerE = 4
    EExplorerF = 5
    DiscoveryA = 1
    DiscoveryB = 2  # Duplicate enum value with EExplorerC (historical)
    DiscoveryC = 3

@enum.unique
class TRIGSRC(enum.Enum):
    """Trigger source, represented as type 'unsigned char'."""
    None_             = 0
    PC                = 1
    DetectorAnalogIn  = 2
    DetectorDigitalIn = 3
    AnalogIn          = 4
    DigitalIn         = 5
    DigitalOut        = 6
    AnalogOut1        = 7
    AnalogOut2        = 8
    AnalogOut3        = 9
    AnalogOut4        = 10
    External1         = 11
    External2         = 12
    External3         = 13
    External4         = 14
    High              = 15
    Low               = 16

# Note: the enum values are not unique.
class DwfState(enum.Enum):
    """Instrument states, represented as type 'unsigned char'."""
    Ready     = 0
    Config    = 4
    Prefill   = 5
    Armed     = 1
    Wait      = 7
    Triggered = 3
    Running   = 3  # Duplicate value, but there is no state 6. Typo?
    Done      = 2

@enum.unique
class DwfEnumConfigInfo(enum.Enum):
    """Enum configuration info, represented as type 'int'."""
    AnalogInChannelCount   = 1
    AnalogOutChannelCount  = 2
    AnalogIOChannelCount   = 3
    DigitalInChannelCount  = 4
    DigitalOutChannelCount = 5
    DigitalIOChannelCount  = 6
    AnalogInBufferSize     = 7
    AnalogOutBufferSize    = 8
    DigitalInBufferSize    = 9
    DigitalOutBufferSize   = 10

@enum.unique
class ACQMODE(enum.Enum):
    """Acquisition modes, represented as type 'int'."""
    Single     = 0
    ScanShift  = 1
    ScanScreen = 2
    Record     = 3
    Overs      = 4
    Single1    = 5

@enum.unique
class FILTER(enum.Enum):
    """Analog acquisition filter, represented as type 'int'."""
    Decimate = 0
    Average  = 1
    MinMax   = 2

@enum.unique
class TRIGTYPE(enum.Enum):
    """Analog in trigger mode, represented as type 'int'."""
    Edge       = 0
    Pulse      = 1
    Transition = 2

@enum.unique
class DwfTriggerSlope(enum.Enum):
    """Trigger slope, represented as type 'int'."""
    Rise   = 0
    Fall   = 1
    Either = 2

@enum.unique
class TRIGLEN(enum.Enum):
    """Analog in trigger length condition, represented as type 'int'."""
    Less    = 0
    Timeout = 1
    More    = 2

@enum.unique
class DWFERC(enum.Enum):
    """Error codes for DWF public API, represented as type 'int'."""
    NoErc             = 0     # No error occurred
    UnknownError      = 1     # Unknown error
    ApiLockTimeout    = 2     # API waiting on pending API timed out
    AlreadyOpened     = 3     # Device already opened
    NotSupported      = 4     # Device not supported
    InvalidParameter0 = 0x10  # Invalid parameter sent in API call
    InvalidParameter1 = 0x11  # Invalid parameter sent in API call
    InvalidParameter2 = 0x12  # Invalid parameter sent in API call
    InvalidParameter3 = 0x13  # Invalid parameter sent in API call
    InvalidParameter4 = 0x14  # Invalid parameter sent in API call

@enum.unique
class FUNC(enum.Enum):
    """Analog out signal types, represented as type 'unsigned char'."""
    DC        = 0
    Sine      = 1
    Square    = 2
    Triangle  = 3
    RampUp    = 4
    RampDown  = 5
    Noise     = 6
    Pulse     = 7
    Trapezium = 8
    SinePower = 9
    Custom    = 30
    Play      = 31

@enum.unique
class ANALOGIO(enum.Enum):
    """Analog I/O channel node types, represented as type 'unsigned char'."""
    Enable      = 1
    Voltage     = 2
    Current     = 3
    Power       = 4
    Temperature = 5
    Dmm         = 6
    Range       = 7
    Measure     = 8
    Time        = 9
    Frequency   = 10

@enum.unique
class AnalogOutNode(enum.Enum):
    """Analog Out node type, represented as type 'int'."""
    Carrier = 0
    FM      = 1
    AM      = 2

@enum.unique
class DwfAnalogOutMode(enum.Enum):
    """Analog Out mode, represented as type 'int'."""
    Voltage = 0
    Current = 1

@enum.unique
class DwfAnalogOutIdle(enum.Enum):
    """Analog Out idle state, represented as type 'int'."""
    Disable  = 0
    Offset   = 1
    Initial  = 2

@enum.unique
class DwfDigitalInClockSource(enum.Enum):
    """Digital In clock source, represented as type 'int'."""
    Internal = 0
    External = 1

@enum.unique
class DwfDigitalInSampleMode(enum.Enum):
    """Digital In sample mode, represented as type 'int'."""
    Simple = 0
    # alternate samples: noise|sample|noise|sample|...
    # where noise is more than 1 transition between 2 samples
    Noise  = 1

@enum.unique
class DwfDigitalOutOutput(enum.Enum):
    """Digital Out output mode, represented as type 'int'."""
    PushPull   = 0
    OpenDrain  = 1
    OpenSource = 2
    ThreeState = 3  # For custom and random.

@enum.unique
class DwfDigitalOutType(enum.Enum):
    """Digital Out type, represented as type 'int'."""
    Pulse  = 0
    Custom = 1
    Random = 2
    ROM    = 3

@enum.unique
class DwfDigitalOutIdle(enum.Enum):
    """Digital Out idle mode, represented as type 'int'."""
    Init = 0
    Low  = 1
    High = 2
    Zet  = 3

@enum.unique
class DwfAnalogImpedance(enum.Enum):
    """Analog Impedance measurement setting, represented as type 'int'."""
    Impedance           =  0  # Ohms
    ImpedancePhase      =  1  # Radians
    Resistance          =  2  # Ohms
    Reactance           =  3  # Ohms
    Admittance          =  4  # Siemens
    AdmittancePhase     =  5  # Radians
    Conductance         =  6  # Siemens
    Susceptance         =  7  # Siemens
    SeriesCapactance    =  8  # Farad
    ParallelCapacitance =  9  # Farad
    SeriesInductance    = 10  # Henry
    ParallelInductance  = 11  # Henry
    Dissipation         = 12  # factor
    Quality             = 13  # factor

@enum.unique
class DwfParam(enum.Enum):
    """Parameter setting, represented as type 'int'."""
    UsbPower      = 2 # 1 keep the USB power enabled even when AUX is connected, Analog Discovery 2
    LedBrightness = 3 # LED brightness 0 ... 100%, Digital Discovery
    OnClose       = 4 # 0 continue, 1 stop, 2 shutdown
    AudioOut      = 5 # 0 disable / 1 enable audio output, Analog Discovery 1, 2
    UsbLimit      = 6 # 0..1000 mA USB power limit, -1 no limit, Analog Discovery 1, 2


class _typespec_ctypes:
    """The class members given below map the type specifications as given in the 'dwf_function_signatures' variable to ctypes types."""

    c_bool                      = ctypes.c_bool  # Note: use of type 'bool' in dwf.h is probably not intentional.

    c_char                      = ctypes.c_char
    c_char_ptr                  = ctypes.POINTER(c_char)
    c_char_array_16             = c_char * 16
    c_char_array_32             = c_char * 32
    c_char_array_512            = c_char * 512

    c_short                     = ctypes.c_short
    c_short_ptr                 = ctypes.POINTER(c_short)

    c_int                       = ctypes.c_int
    c_int_ptr                   = ctypes.POINTER(c_int)

    c_unsigned_char             = ctypes.c_ubyte
    c_unsigned_char_ptr         = ctypes.POINTER(c_unsigned_char)

    c_unsigned_short            = ctypes.c_ushort
    c_unsigned_short_ptr        = ctypes.POINTER(c_unsigned_short)

    c_unsigned_int              = ctypes.c_uint
    c_unsigned_int_ptr          = ctypes.POINTER(c_unsigned_int)

    c_unsigned_long_long        = ctypes.c_ulonglong
    c_unsigned_long_long_ptr    = ctypes.POINTER(c_unsigned_long_long)

    c_double                    = ctypes.c_double
    c_double_ptr                = ctypes.POINTER(c_double)
    c_double_array_32           = c_double * 32

    c_void_ptr                  = ctypes.c_void_p

    HDWF                        = c_int  # Handle
    HDWF_ptr                    = ctypes.POINTER(HDWF)

    DWFERC                      = c_int
    DWFERC_ptr                  = ctypes.POINTER(DWFERC)

    ENUMFILTER                  = c_int

    TRIGSRC                     = c_unsigned_char
    TRIGSRC_ptr                 = ctypes.POINTER(TRIGSRC)

    FUNC                        = c_unsigned_char
    FUNC_ptr                    = ctypes.POINTER(FUNC)

    DEVID                       = c_int
    DEVID_ptr                   = ctypes.POINTER(DEVID)

    DEVVER                      = c_int
    DEVVER_ptr                  = ctypes.POINTER(DEVVER)

    ACQMODE                     = c_int
    ACQMODE_ptr                 = ctypes.POINTER(ACQMODE)

    ANALOGIO                    = c_unsigned_char
    ANALOGIO_ptr                = ctypes.POINTER(ANALOGIO)

    FILTER                      = c_int
    FILTER_ptr                  = ctypes.POINTER(FILTER)

    TRIGTYPE                    = c_int
    TRIGTYPE_ptr                = ctypes.POINTER(TRIGTYPE)

    TRIGLEN                     = c_int
    TRIGLEN_ptr                 = ctypes.POINTER(TRIGLEN)

    DwfState                    = c_unsigned_char
    DwfState_ptr                = ctypes.POINTER(DwfState)

    DwfAnalogOutMode            = c_int
    DwfAnalogOutMode_ptr        = ctypes.POINTER(DwfAnalogOutMode)

    DwfAnalogOutIdle            = c_int
    DwfAnalogOutIdle_ptr        = ctypes.POINTER(DwfAnalogOutIdle)

    DwfTriggerSlope             = c_int
    DwfTriggerSlope_ptr         = ctypes.POINTER(DwfTriggerSlope)

    DwfDigitalInClockSource     = c_int
    DwfDigitalInClockSource_ptr = ctypes.POINTER(DwfDigitalInClockSource)

    DwfDigitalInSampleMode      = c_int
    DwfDigitalInSampleMode_ptr  = ctypes.POINTER(DwfDigitalInSampleMode)

    DwfDigitalOutOutput         = c_int
    DwfDigitalOutOutput_ptr     = ctypes.POINTER(DwfDigitalOutOutput)

    DwfDigitalOutType           = c_int
    DwfDigitalOutType_ptr       = ctypes.POINTER(DwfDigitalOutType)

    DwfDigitalOutIdle           = c_int
    DwfDigitalOutIdle_ptr       = ctypes.POINTER(DwfDigitalOutIdle)

    DwfParam                    = c_int
    DwfEnumConfigInfo           = c_int
    DwfAnalogImpedance          = c_int

    AnalogOutNode               = c_int


class DigilentWaveformLibraryError(RuntimeError):
    """This class represents an error as reported back by one of the DWF API functions."""
    def __init__(self, code: Optional[DWFERC], msg: Optional[str]) -> None:
        self.code = code
        self.msg = msg

    def __str__(self) -> str:
        if self.code is None:
            error_string = "DWF Error (unspecified)"
        else:
            error_string = "DWF Error {!r} ({})".format(self.code.name, self.code.value)

        if self.msg is not None:
            error_string = "{}: {!r}".format(error_string, self.msg.strip())

        return error_string


class DigilentWaveformLibrary:
    """Provides access to the DWF shared library functions.

    Version 3.14.3 of the DWF library has 5 miscellaneous functions, none of which are obsolete, that are
    wrapped as DigilentWaveformLibrary methods:

        FDwfGetLastError, FDwfGetLastErrorMsg, FDwfGetVersion, FDwfParamSet, and FDwfParamGet.

    These five functions are wrapped as methods of the DigilentWaveformLibrary class.

    In addition, the following two private helper methods are provided for the Python wrapper itself:

    - The _annotate_function_signatures static method.
    - The _exception() method.

    """
    def __init__(self) -> None:
        """Initializes a DigilentWaveformLibrary instance.

        This function instantiates a ctypes library, type-annotates its functions, and instantiates 'enum' and 'device' fields
        that can be used to access the device enumeration and device functions of the API.
        """
        if sys.platform.startswith("win"):
            lib = ctypes.cdll.dwf
        elif sys.platform.startswith("darwin"):
            lib = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            lib = ctypes.cdll.LoadLibrary("libdwf.so")

        self._annotate_function_signatures(lib)

        self._lib = lib

        self.enum = DigilentWaveformLibrary.EnumAPI(self)
        self.device = DigilentWaveformLibrary.DeviceAPI(self)

    @staticmethod
    def _annotate_function_signatures(lib: ctypes.CDLL) -> None:
        """Adds 'ctype' return type and parameter type annotations for all known functions in the DWF shared library."""

        function_signatures = dwf_function_signatures(_typespec_ctypes)

        for (name, restype, argtypes, obsolete_flag) in function_signatures:
            argtypes = [argtype for (argname, argtype) in argtypes]
            try:
                func = getattr(lib, name)
                func.restype = restype
                func.argtypes = argtypes
            except AttributeError:
                # Ignore functions that cannot be found.
                pass

    def _exception(self) -> DigilentWaveformLibraryError:
        """Returns an exception describing the most recent error.

        This function is used by the Python API to make an informative `DigilentWaveformLibraryError` exception in case a DWF library function fails.

        Returns:
            A DigilentWaveformLibraryError exception describing the error reported by the last DWF library call.
        """
        return DigilentWaveformLibraryError(self.getLastError(), self.getLastErrorMsg())

    def getLastError(self) -> DWFERC:
        """Returns the last error code in the calling process.

        The error code is cleared when other API functions are called and is only set when an API function fails during execution.

        Returns:
            Error code of last API call.

        Raises:
            DigilentWaveformLibraryError: the last error code cannot be retrieved.
        """
        c_dwferc = _typespec_ctypes.DWFERC()
        result = self._lib.FDwfGetLastError(c_dwferc)
        if result != _RESULT_SUCCESS:
            # If the FDwfGetLastError call itself fails, we cannot get a proper error code or message.
            raise DigilentWaveformLibraryError(None, "FDwfGetLastError() failed.")
        dwferc = DWFERC(c_dwferc.value)
        return dwferc

    def getLastErrorMsg(self) -> str:
        """Returns the last error message.

        Returns:
            Error message of the last API call.
            It may consist of a chain of messages, separated by a newline character, that describe the events leading to the failure.

        Raises:
            DigilentWaveformLibraryError: the last error message cannot be retrieved.
        """
        c_error_message = ctypes.create_string_buffer(512)
        result = self._lib.FDwfGetLastErrorMsg(c_error_message)
        if result != _RESULT_SUCCESS:
            raise DigilentWaveformLibraryError(None, None)
        error_message = c_error_message.value.decode()
        return error_message

    def getVersion(self) -> str:
        """Returns the library version string.

        Returns:
            Version string, composed of major, minor, and build numbers (e.g., "3.14.3").

        Raises:
            DigilentWaveformLibraryError: the library version string cannot be retrieved.
        """
        c_version = ctypes.create_string_buffer(32)
        result = self._lib.FDwfGetVersion(c_version)
        if result != _RESULT_SUCCESS:
            raise self._exception()
        version = c_version.value.decode()
        return version

    def paramSet(self, parameter: DwfParam, value: int) -> None:
        """Sets a default parameter value.

        Parameters are settings of a specific DigilentWaveformsDevice.
        Different DigilentWaveformsDevice instances can have different values for each of the possible DwfParam parameters.

        This method sets parameter values at the library level.
        They are used as default parameters for devices that are opened subsequently.

        Note:
            The parameter values are not checked to make sure they correspond to a valid value
            for the specific parameter.

        Args:
            parameter: The parameter to set.
            value: The desired parameter value.

        Raises:
            DigilentWaveformLibraryError: the parameter value cannot be set.
        """
        result = self._lib.FDwfParamSet(parameter.value, value)
        if result != _RESULT_SUCCESS:
            raise self._exception()

    def paramGet(self, parameter: DwfParam) -> int:
        """Returns a default parameter value.

        Parameters are settings of a specific DigilentWaveformsDevice.
        Different DigilentWaveformsDevice instances can have different values for each of the possible DwfParam parameters.

        This method retrieves parameter values at the library level.
        They are used as default parameters for devices that are opened subsequently.

        Args:
            parameter: The parameter to get.

        Returns:
            The retrieved parameter value.

        Raises:
            DigilentWaveformLibraryError: the parameter value cannot be retrieved.
        """
        c_value = _typespec_ctypes.c_int()
        result = self._lib.FDwfParamGet(parameter.value, c_value)
        if result != _RESULT_SUCCESS:
            raise self._exception()
        value = c_value.value
        return value

    class EnumAPI:
        """Encapsulates the 'FDwfEnum' API calls.

        Version 3.14.3 of the DWF library has 12 'FDwfEnum' functions, 4 of which are obsolete.

        These functions are used to discover all connected, compatible devices.
        """

        def __init__(self, dwf: 'DigilentWaveformLibrary') -> None:
            self._dwf = dwf

        def count(self, enumfilter: Optional[ENUMFILTER]=None) -> int:
            """Builds an internal list of detected devices filtered by the 'enumfilter' argument, and return the count of detected devices.

            This function must be called before using other enum functions because they obtain information about enumerated devices from this list,
            indexed by the device index.

            Note:
                This method can take several seconds to complete.

            Args:
                enumfilter: Specify which devices to enumerate. If not specified, enumerate all devices.

            Returns:
                The number of devices detected.

            Raises:
                DigilentWaveformLibraryError: the devices cannot be enumerated.
            """
            if enumfilter is None:
                enumfilter = ENUMFILTER.All

            c_device_count = _typespec_ctypes.c_int()
            result = self._dwf._lib.FDwfEnum(enumfilter.value, c_device_count)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            device_count = c_device_count.value
            return device_count

        def deviceType(self, device_index: int)-> Tuple[DEVID, DEVVER]:
            """Returns the device ID and version ID of the selected device.

            The DEVVER value 2 is unfortunately used for two different enum values: EExplorerC and DiscoveryB.
            We try to remove the ambiguity by returning EExplorerC if DEVID is EExplorer, and DiscoveryB otherwise.
            Unfortunately, this doesn't work due to the way Python Enums work.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).

            Returns:
                A tuple of the DEVID and DEVVER of the device selected by the 'device_index' parameter.

            Raises:
                DigilentWaveformLibraryError: the device type and version cannot be retrieved.
            """
            c_device_id = _typespec_ctypes.DEVID()
            c_device_revision = _typespec_ctypes.DEVVER()
            result = self._dwf._lib.FDwfEnumDeviceType(device_index, c_device_id, c_device_revision)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            device_id = DEVID(c_device_id.value)
            if c_device_revision.value == 2:
                # There is ambiguity in the proper enum value. Decide based on the value of device_id.
                if device_id == DEVID.EExplorer:
                    device_revision = DEVVER.EExplorerC
                else:
                    device_revision = DEVVER.DiscoveryB
            else:
                # No ambiguity.
                device_revision = DEVVER(c_device_revision.value)
            return (device_id, device_revision)

        def deviceIsOpened(self, device_index: int) -> bool:
            """Checks if the specified device is already opened by this or any other process.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).

            Returns:
                True if the device is already opened, False otherwise.

            Raises:
                DigilentWaveformLibraryError: the open state of the device cannot be retrieved.
            """
            c_is_used = _typespec_ctypes.c_int()
            result = self._dwf._lib.FDwfEnumDeviceIsOpened(device_index, c_is_used)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            is_used = bool(c_is_used.value)
            return is_used

        def userName(self, device_index: int) -> str:
            """Retrieves the username of the selected device.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).

            Returns:
                Username of the device, which is a short name denoting the device type (e.g., "Discovery2", "DDiscovery").

            Raises:
                DigilentWaveformLibraryError: the user name of the device cannot be retrieved.
            """
            c_username = ctypes.create_string_buffer(32)
            result = self._dwf._lib.FDwfEnumUserName(device_index, c_username)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            username = c_username.value.decode()
            return username

        def deviceName(self, device_index: int) -> str:
            """Retrieves the devicename of the selected device.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).

            Returns:
                Device name of the device, which is a long name denoting the device type (e.g., "Analog Discovery 2", "Digital Discovery").

            Raises:
                DigilentWaveformLibraryError: the device name of the device cannot be retrieved.
            """
            c_devicename = ctypes.create_string_buffer(32)
            result = self._dwf._lib.FDwfEnumDeviceName(device_index, c_devicename)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            devicename = c_devicename.value.decode()
            return devicename

        def serialNumber(self, device_index: int) -> str:
            """Retrieves the 12-digit, unique serial number of the enumerated device.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).

            Returns:
                The 12 hex-digit unique serial number of the device. The 'SN:' prefix returned by the underlying API function is discarded.

            Raises:
                DigilentWaveformLibraryError: the serial number of the device cannot be retrieved.
                ValueError: the serial number returned by the library isn't of the form 'SN:XXXXXXXXXXXX'.
            """
            c_serial = ctypes.create_string_buffer(32)
            result = self._dwf._lib.FDwfEnumSN(device_index, c_serial)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            serial = c_serial.value.decode()
            if not serial.startswith("SN:"):
                raise ValueError("Bad serial number string received: {!r}".format(serial))
            serial = serial[3:]
            if len(serial) != 12:
                raise ValueError("Serial number isn't 12 characters: {!r}".format(serial))
            return serial

        def configCount(self, device_index: int) -> int:
            """Builds an internal list of detected configurations for the selected device.

            This function must be called before using other FDwfEnumConfigInfo functions because they obtain information about
            configurations from the list, as indexed by the configuration index.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).

            Returns:
                The count of configurations of the device.

            Raises:
                DigilentWaveformLibraryError: the configuration list of the device cannot be retrieved.
            """
            c_config_count = _typespec_ctypes.c_int()
            result = self._dwf._lib.FDwfEnumConfig(device_index, c_config_count)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            config_count = c_config_count.value
            return config_count

        def configInfo(self, config_index: int, info: DwfEnumConfigInfo) -> int:
            """Returns information about the configuration.

            Args:
                config_index: Zero-based index of the previously enumerated configuration (see the EnumAPI.configCount() method).
                info: Selects which configuration parameter to retrieve.

            Returns:
                The integer value of the selected configuration parameter, of the selected configuration.

            Raises:
                DigilentWaveformLibraryError: the configuration info of the device cannot be retrieved.
            """
            c_configuration_parameter_value = _typespec_ctypes.c_int()
            result = self._dwf._lib.FDwfEnumConfigInfo(config_index, info.value, c_configuration_parameter_value)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            configuration_parameter_value = c_configuration_parameter_value.value
            return configuration_parameter_value

        def analogInChannels(self, device_index: int) -> int:
            """Counts analog input channels of the selected device.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).

            Returns:
                The number of analog input channels of the device.

            Note: This function is OBSOLETE. Use EnumAPI.configInfo(config_index, DwfEnumConfigInfo.AnalogInChannelCount) or AnalogInAPI.channelCount() instead.

            Raises:
                DigilentWaveformLibraryError: the analog-in channel count of the device cannot be retrieved.
            """
            c_channels = _typespec_ctypes.c_int()
            result = self._dwf._lib.FDwfEnumAnalogInChannels(device_index, c_channels)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            channels = c_channels.value
            return channels

        def analogInBufferSize(self, device_index: int) -> int:
            """Retrieve analog input buffer size of the selected device.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).

            Returns:
                The analog input buffer size of the selected device.

            Note: This function is OBSOLETE. Use EnumAPI.configInfo(idxConfig, DwfEnumConfigInfo.AnalogInBufferSize) instead.

            Raises:
                DigilentWaveformLibraryError: the analog-in buffer size of the device cannot be retrieved.
            """
            c_buffer_size = _typespec_ctypes.c_int()
            result = self._dwf._lib.FDwfEnumAnalogInBufferSize(device_index, c_buffer_size)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            buffer_size = c_buffer_size.value
            return buffer_size

        def analogInBits(self, device_index: int) -> int:
            """Retrieve analog input bit resolution of the selected device.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).

            Returns:
                The analog input bit resolution of the selected device.

            Note: This function is OBSOLETE. Use AnalogInAPI.bitsInfo() instead.

            Raises:
                DigilentWaveformLibraryError: the analog-in bit resolution of the device cannot be retrieved.
            """
            c_num_bits = _typespec_ctypes.c_int()
            result = self._dwf._lib.FDwfEnumAnalogInBits(device_index, c_num_bits)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            num_bits = c_num_bits.value
            return num_bits

        def analogInFrequency(self, device_index: int) -> float:
            """Retrieve the analog input sample frequency of the selected device.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).

            Returns:
                The analog input sample frequency of the selected device, in samples per second.

            Note: This function is OBSOLETE. The frequency of the analog input channels is now configurable.
                  Use `AnalogInAPI.frequencyInfo()`, `AnalogInAPI.frequencyGet()`, and `AnalogInAPI.frequencySet()` instead.

            Check: check if this function returns the maximum analog input sample rate, or the currently configured
                analog input sample rate.

            Raises:
                DigilentWaveformLibraryError: the analog input sample frequency of the device cannot be retrieved.
            """
            c_sample_frequency = _typespec_ctypes.c_double()
            result = self._dwf._lib.FDwfEnumAnalogInFrequency(device_index, c_sample_frequency)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            sample_frequency = c_sample_frequency.value
            return sample_frequency

    class DeviceAPI:
        """Implements the 'FDwfDevice' API calls.

        Version 3.14.3 of the DWF library has 15 'FDwfDevice' functions, none of which are obsolete.

        The 'open' and 'closeAll' methods are implemented here, since they are not associated to a specific previously opened device.
        The 12 remaining library functions are implemented as methods of the DigilentWaveformDevice class.

        The 'open' method wraps two different library calls: 'FDwfDeviceOpen' and 'FDwfDeviceConfigOpen'.
        These API calls open either the default configuration, or an explicitly specified configuration of the device.
        In the open() method defined below, the decision on which underlying library function to call is made based
        on the value of the'config_index' parameter.

        The DeviceAPI class also provides the openBySerialNumber() convenience method.
        This the recommended way to open a specific device.
        """

        def __init__(self, dwf: 'DigilentWaveformLibrary') -> None:
            self._dwf = dwf

        def open(self, device_index: int, config_index: Optional[int]=None) -> 'DigilentWaveformDevice':
            """Opens a device identified by the enumeration index and retrieve a handle.

            Note:
                This method takes approximately 2 seconds to complete.

            Args:
                device_index: Zero-based index of the previously enumerated device (see the EnumAPI.count() method).
                              To automatically enumerate all connected devices and open the first discovered device, use device_index=-1.
                config_index: Zero-based index of the device configuration to use. If None, open the default device configuration.

            Returns:
                The DigilentWaveformDevice created as a result of this call.

            Raises:
                DigilentWaveformLibraryError: the specified device or configuration cannot be opened.
            """
            c_hdwf = _typespec_ctypes.HDWF()
            if config_index is None:
                result = self._dwf._lib.FDwfDeviceOpen(device_index, c_hdwf)
            else:
                result = self._dwf._lib.FDwfDeviceConfigOpen(device_index, config_index, c_hdwf)
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()
            hdwf = c_hdwf.value
            return DigilentWaveformDevice(self._dwf, hdwf)

        def closeAll(self) -> None:
            """Closes all opened devices by the calling process.

            Note that this function does not close all devices across all processes.

            Raises:
                DigilentWaveformLibraryError: the close all operation failed.
            """
            result = self._dwf._lib.FDwfDeviceCloseAll()
            if result != _RESULT_SUCCESS:
                raise self._dwf._exception()

        def openBySerialNumber(self, serial_number_sought: str) -> 'DigilentWaveformDevice':
            """Opens a device identified by its serial number.

            Note:
                This is a convenience method that doesn't directly encapsulate a single function call of the library.

            Note:
                This method takes several seconds to complete.

            Args:
                serial_number_sought: The serial number of the device to be opened.
                                      Digilent device serial numbers consist of 12 hexadecimal digits.

            Returns:
                The DigilentWaveformDevice instance created as a result of this call.

            Raises:
                DigilentWaveformLibraryError: an error occurred in the underlying API.
                ValueError: the serial number specified was not found or it was found more than once (unlikely).
            """
            num_devices = self._dwf.enum.count()  # Perform a device enumeration.
            candidates = [device_index for device_index in range(num_devices) if self._dwf.enum.serialNumber(device_index) == serial_number_sought]

            if len(candidates) != 1:
                raise ValueError("Cannot open Digilent device by serial number {!r}: {} candidates.".format(serial_number_sought, len(candidates)))

            # We found a unique candidate. Open it.
            device_index = candidates[0]
            return self.open(device_index)


class DigilentWaveformDevice:
    """A DigilentWaveformDevice represents a single Digilent measurement device.

    A DigitalWaveform device consists of multiple sub-modules (instruments, protocols,
    and/or measurements); e.g. Analog In, Analog Out, Digital In, and Digital Out.

    The DigilentWaveformDevice class wraps API functions that refer to a specific device,
    but not to a specific instrument, protocol, or measurement in the device.

    This class implements 12 of the 15 FDwfDevice functions provided by the C API, namely,
    the 12 functions that refer to a specific open device.
    The other 3 FDwfDevice functions are wrapped at the DigilentWaveformLibrary library level.

    It also includes 11 sub-APIs to address the various instruments inside the device.
    Those can be reached via fields of the DigilentWaveformDevice instance.
    """

    def __init__(self, dwf: DigilentWaveformLibrary, hdwf: int) -> None:
        """Initialize a DigilentWaveformDevice with the specified dwf handle value.

        Note:
            The user should not make DigilentWaveformDevice instances directly.
            Use DigilentWaveformLibrary.device.open() or DigilentWaveformLibrary.device.openBySerialNumber()
            to obtain a valid DigilentWaveformDevice.

        Args:
            dwf: The DigilentWaveformLibrary instance used to make calls to the underlying library.
            hdwf: the device to open.
        """
        self._dwf = dwf
        self._hdwf = hdwf
        self.analogIn = DigilentWaveformDevice.AnalogInAPI(self)
        self.analogOut = DigilentWaveformDevice.AnalogOutAPI(self)
        self.analogIO = DigilentWaveformDevice.AnalogIOAPI(self)
        self.digitalIO = DigilentWaveformDevice.DigitalIOAPI(self)
        self.digitalIn = DigilentWaveformDevice.DigitalInAPI(self)
        self.digitalOut = DigilentWaveformDevice.DigitalOutAPI(self)
        self.digitalUart = DigilentWaveformDevice.DigitalUartAPI(self)
        self.digitalSpi = DigilentWaveformDevice.DigitalSpiAPI(self)
        self.digitalI2c = DigilentWaveformDevice.DigitalI2cAPI(self)
        self.digitalCan = DigilentWaveformDevice.DigitalCanAPI(self)
        self.analogImpedance = DigilentWaveformDevice.AnalogImpedanceAPI(self)

    def close(self) -> None:
        """Closes an interface handle when access to the device is no longer needed.

        Once this function returns, the DigilentWaveformDevice can no longer be used to access the device.

        Raises:
            DigilentWaveformLibraryError: the device cannot be closed.
        """
        result = self._dwf._lib.FDwfDeviceClose(self._hdwf)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()

    def autoConfigureSet(self, auto_configure: int) -> None:
        """Enables or disables the AutoConfig setting for a specific device.

        When this setting is enabled, the device is automatically configured every time an instrument parameter is set.
        For example, when AutoConfigure is enabled, FDwfAnalogOutConfigure does not need to be called after FDwfAnalogOutRunSet.
        This adds latency to every Set function; just as much latency as calling the corresponding Configure function directly afterward.
        With value 3 the analog-out configuration will be applied dynamically, without stopping the instrument.

        Args:
            auto_configure: Value for this option; 0: disable, 1: enable, 3: dynamic.

        Raises:
            DigilentWaveformLibraryError: the value cannot be set.
        """
        result = self._dwf._lib.FDwfDeviceAutoConfigureSet(self._hdwf, auto_configure)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()

    def autoConfigureGet(self) -> int:
        """Returns the AutoConfig setting of the device.

        Returns:
            The auto-configure setting; 0: disable, 1: enable, 3: dynamic.

        Raises:
            DigilentWaveformLibraryError: the value cannot be retrieved.
        """

        c_auto_configure = _typespec_ctypes.c_int()
        result = self._dwf._lib.FDwfDeviceAutoConfigureGet(self._hdwf, c_auto_configure)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()
        auto_configure = c_auto_configure.value
        return auto_configure

    def reset(self) -> None:
        """Resets and configures (by default, having auto configure enabled) all device and instrument parameters to default values.

        Raises:
            DigilentWaveformLibraryError: the device cannot be reset.
        """
        result = self._dwf._lib.FDwfDeviceReset(self._hdwf)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()

    def enableSet(self, enable: bool) -> None:
        """Enables or disables the device.

        Args:
            enable: True for enable, False for disable.

        Raises:
            DigilentWaveformLibraryError: the device's enabled state cannot be set.
        """
        result = self._dwf._lib.FDwfDeviceEnableSet(self._hdwf, enable)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()

    def triggerInfo(self) -> List[TRIGSRC]:
        """Returns the supported trigger source options for the global trigger bus.

        Returns:
            A list of available trigger sources.

        Raises:
            DigilentWaveformLibraryError: the list of supported trigger sources cannot be retrieved.
        """
        c_trigger_source_bitset = _typespec_ctypes.c_int()
        result = self._dwf._lib.FDwfDeviceTriggerInfo(self._hdwf, c_trigger_source_bitset)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()
        trigger_source_bitset = c_trigger_source_bitset.value
        trigger_source_list = [trigger_source for trigger_source in TRIGSRC if trigger_source_bitset & (1 << trigger_source.value)]
        return trigger_source_list

    def triggerSet(self, pin_index: int, trigger_source: TRIGSRC) -> None:
        """Configures the trigger I/O pin with a specific trigger source option.

        Args:
            pin_index: The pin_index to configure.
            trigger_source: The trigger source to select.

        Raises:
            DigilentWaveformLibraryError: the trigger source cannot be set.
        """
        result = self._dwf._lib.FDwfDeviceTriggerSet(self._hdwf, pin_index, trigger_source.value)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()

    def triggerGet(self, pin_index: int) -> TRIGSRC:
        """Returns the selected trigger source for a trigger I/O pin.

        The trigger source can be "none", an internal instrument, or an external trigger.

        Args:
            pin_index: The pin for which to obtain the selected trigger source.

        Returns:
           The trigger source setting for the selected pin.

        Raises:
            DigilentWaveformLibraryError: the trigger source cannot be retrieved.
        """
        c_trigger_source = _typespec_ctypes.TRIGSRC()
        result = self._dwf._lib.FDwfDeviceTriggerGet(self._hdwf, pin_index, c_trigger_source)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()
        trigger_source = TRIGSRC(c_trigger_source.value)
        return trigger_source

    def triggerPC(self) -> None:
        """Generates one pulse on the PC trigger line.

        Raises:
            DigilentWaveformLibraryError: the PC trigger line cannot be pulsed.
        """
        result = self._dwf._lib.FDwfDeviceTriggerPC(self._hdwf)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()

    def triggerSlopeInfo(self) -> List[DwfTriggerSlope]:
        """Returns the supported trigger slope options.

        Returns:
            A list of possible TriggerSlope values.

        Note:
            This function is not documented in the API reference PDF.

        Raises:
            DigilentWaveformLibraryError: the trigger slope options cannot be retrieved.
        """
        c_slope_bitset = _typespec_ctypes.c_int()
        result = self._dwf._lib.FDwfDeviceTriggerSlopeInfo(self._hdwf, c_slope_bitset)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()
        slope_bitset = c_slope_bitset.value
        slope_list = [slope for slope in DwfTriggerSlope if slope_bitset & (1 << slope.value)]
        return slope_list

    def paramSet(self, parameter: DwfParam, value: int) -> None:
        """Configures a device parameter.

        Args:
            parameter: The device parameter to configure.
            value: The value to assign to the parameter.

        Raises:
            DigilentWaveformLibraryError: the specified device parameter cannot be set to the specified value.
        """
        result = self._dwf._lib.FDwfDeviceParamSet(self._hdwf, parameter.value, value)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()

    def paramGet(self, parameter: DwfParam) -> int:
        """Retrieves a device parameter.

        Args:
            parameter: The device parameter to query.

        Returns:
            The integer value of the parameter.

        Raises:
            DigilentWaveformLibraryError: the specified device parameter cannot be retrieved.
        """
        c_value = _typespec_ctypes.c_int()
        result = self._dwf._lib.FDwfDeviceParamGet(self._hdwf, parameter.value, c_value)
        if result != _RESULT_SUCCESS:
            raise self._dwf._exception()
        value = c_value.value
        return value


    class AnalogInAPI:
        """Provides wrappers for the 'FDwfAnalogIn' API calls.

        Version 3.14.3 of the DWF library has 93 'FDwfAnalogIn' functions, 1 of which (FDwfAnalogInTriggerSourceInfo) is obsolete.
        """

        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def reset(self) -> None:
            """Resets and configures (by default, having auto configure enabled) all AnalogIn instrument parameters to default values."""
            result = self._device._dwf._lib.FDwfAnalogInReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def configure(self, reconfigure: bool, start: bool) -> None:
            """Configure the instrument and start or stop the acquisition.

            To reset the Auto trigger timeout, set reconfigure to True.
            """
            result = self._device._dwf._lib.FDwfAnalogInConfigure(self._device._hdwf, reconfigure, start)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerForce(self) -> None:
            # TODO: not documented in PDF ??
            result = self._device._dwf._lib.FDwfAnalogInTriggerForce(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def status(self, readData: bool) -> DwfState:
            """Check the state of the acquisition.

            To read the data from the device, set readData to True.
            For single acquisition mode, the data will be read only when the acquisition is finished.
            """
            c_status_ = _typespec_ctypes.DwfState()
            result = self._device._dwf._lib.FDwfAnalogInStatus(self._device._hdwf, readData, c_status_)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            status_ = DwfState(c_status_.value)
            return status_

        def statusSamplesLeft(self) -> int:
            """Retrieve the number of samples left in the acquisition."""
            c_samplesLeft = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInStatusSamplesLeft(self._device._hdwf, c_samplesLeft)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            samplesLeft = c_samplesLeft.value
            return samplesLeft

        def statusTime(self) -> Tuple[int, int, int]:
            """Retrieve timestamp of status."""
            c_sec_utc = _typespec_ctypes.c_uint()
            c_tick = _typespec_ctypes.c_uint()
            c_ticks_per_second = _typespec_ctypes.c_uint()
            result = self._device._dwf._lib.FDwfAnalogInStatusTime(self._device._hdwf, c_sec_utc, c_tick, c_ticks_per_second)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            sec_utc = c_sec_utc.value
            tick = c_tick.value
            ticks_per_second = c_ticks_per_second.value
            return (sec_utc, tick, ticks_per_second)

        def statusSamplesValid(self) -> int:
            """Retrieve the number of valid/acquired data samples."""
            c_samplesValid = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInStatusSamplesValid(self._device._hdwf, c_samplesValid)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            samplesValid = c_samplesValid.value
            return samplesValid

        def statusIndexWrite(self) -> int:
            """Retrieve the buffer write pointer.

            This is needed in ScanScreen acquisition mode to display the scan bar.
            """
            c_indexWrite = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInStatusIndexWrite(self._device._hdwf, c_indexWrite)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            indexWrite = c_indexWrite.value
            return indexWrite

        def statusAutoTriggered(self) -> bool:
            """Verify if the acquisition is auto triggered."""
            c_auto_triggered = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInStatusAutoTriggered(self._device._hdwf, c_auto_triggered)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            auto_triggered = bool(c_auto_triggered.value)
            return auto_triggered

        def statusData(self, idxChannel: int, cdData: int) -> np.ndarray:
            """Retrieve the acquired data samples from the specified idxChannel on the AnalogIn instrument.

            It copies the data samples to the provided buffer.
            """
            samples = np.empty(cdData, dtype=np.float64)
            result = self._device._dwf._lib.FDwfAnalogInStatusData(self._device._hdwf, idxChannel, samples.ctypes.data_as(_typespec_ctypes.c_double_ptr), cdData)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            return samples

        def statusData2(self, idxChannel: int, idxData: int, cdData: int) -> np.ndarray:
            """Retrieve the acquired data samples from the specified idxChannel on the AnalogIn instrument.

            It copies the data samples to the provided buffer.
            """
            samples = np.empty(cdData, dtype=np.float64)
            result = self._device._dwf._lib.FDwfAnalogInStatusData2(self._device._hdwf, idxChannel, samples.ctypes.data_as(_typespec_ctypes.c_double_ptr), idxData, cdData)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            return samples

        def statusData16(self, idxChannel: int, idxData: int, cdData: int) -> np.ndarray:
            samples = np.empty(cdData, dtype=np.int16)
            result = self._device._dwf._lib.FDwfAnalogInStatusData16(self._device._hdwf, idxChannel, samples.ctypes.data_as(_typespec_ctypes.c_short_ptr), idxData, cdData)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            return samples

        def statusNoise(self, idxChannel: int, cdData: int) -> Tuple[np.ndarray, np.ndarray]:
            """Retrieve the acquired data samples from the specified idxChannel on the AnalogIn instrument.

            It copies the data samples to the provided buffer.
            """
            c_rgdMin = np.empty(cdData, dtype=np.float64)
            c_rgdMax = np.empty(cdData, dtype=np.float64)
            result = self._device._dwf._lib.FDwfAnalogInStatusNoise(self._device._hdwf, idxChannel, c_rgdMin.ctypes.data_as(_typespec_ctypes.c_double_ptr), c_rgdMax.ctypes.data_as(_typespec_ctypes.c_double_ptr), cdData)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            return (c_rgdMin, c_rgdMax)

        def statusNoise2(self, idxChannel: int, idxData: int, cdData: int) -> Tuple[np.ndarray, np.ndarray]:
            """Retrieve the acquired data samples from the specified idxChannel on the AnalogIn instrument.

            It copies the data samples to the provided buffer.
            """
            rgdMin = np.empty(cdData, dtype=np.float64)
            rgdMax = np.empty(cdData, dtype=np.float64)
            result = self._device._dwf._lib.FDwfAnalogInStatusNoise2(self._device._hdwf, idxChannel, rgdMin.ctypes.data_as(_typespec_ctypes.c_double_ptr), rgdMax.ctypes.data_as(_typespec_ctypes.c_double_ptr), idxData, cdData)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            return (rgdMin, rgdMax)

        def statusSample(self, idxChannel: int) -> float:
            """Get the last ADC conversion sample from the specified idxChannel on the AnalogIn instrument."""
            c_dVoltSample = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInStatusSample(self._device._hdwf, idxChannel, c_dVoltSample)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            dVoltSample = c_dVoltSample.value
            return dVoltSample

        def statusRecord(self) -> Tuple[int, int, int]:
            """Retrieve information about the recording process.

            Data loss occurs when the device acquisition is faster than the read process to PC.
            In this case, the device recording buffer is filled and data samples are overwritten.
            Corrupt samples indicate that the samples have been overwritten by the acquisition process during the previous read.
            In this case, try optimizing the loop process for faster execution or reduce the acquisition frequency or record length
            to be less than or equal to the device buffer size (record length <= buffersize/frequency).
            """
            c_dataAvailable = _typespec_ctypes.c_int()
            c_dataLost = _typespec_ctypes.c_int()
            c_dataCorrupt = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInStatusRecord(self._device._hdwf, c_dataAvailable, c_dataLost, c_dataCorrupt)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            dataAvailable = c_dataAvailable.value
            dataLost = c_dataLost.value
            dataCorrupt = c_dataCorrupt.value
            return (dataAvailable, dataLost, dataCorrupt)

        def recordLengthSet(self, length: float) -> None:
            """Set the Record length in seconds.

            With length of zero, the recording will run indefinitely.
            """
            result = self._device._dwf._lib.FDwfAnalogInRecordLengthSet(self._device._hdwf, length)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def recordLengthGet(self) -> float:
            """Get the current Record length in seconds."""
            c_length = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInRecordLengthGet(self._device._hdwf, c_length)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            length = c_length.value
            return length

        # Acquisition configuration:

        def frequencyInfo(self) -> Tuple[float, float]:
            """Retreive the minimum and maximum (ADC frequency) settable sample frequency."""
            c_hzMin = _typespec_ctypes.c_double()
            c_hzMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInFrequencyInfo(self._device._hdwf, c_hzMin, c_hzMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            hzMin = c_hzMin.value
            hzMax = c_hzMax.value
            return (hzMin, hzMax)

        def frequencySet(self, hzFrequency: float) -> None:
            """Set the sample frequency for the instrument."""
            result = self._device._dwf._lib.FDwfAnalogInFrequencySet(self._device._hdwf, hzFrequency)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def frequencyGet(self) -> float:
            """Read the configured sample frequency.

            The AnalogIn ADC always runs at maximum frequency, but the method in which the samples are stored can be
            individually configured for each channel with the `channelFilterSet` function.
            """
            c_hzFrequency = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInFrequencyGet(self._device._hdwf, c_hzFrequency)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            hzFrequency = c_hzFrequency.value
            return hzFrequency

        def bitsInfo(self) -> int:
            """Retrieve the number of bits used by the AnalogIn ADC."""
            c_num_bits = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInBitsInfo(self._device._hdwf, c_num_bits)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            num_bits = c_num_bits.value
            return num_bits

        def bufferSizeInfo(self) -> Tuple[int, int]:
            """Returns the minimum and maximum allowable buffer size for the instrument."""
            c_nSizeMin = _typespec_ctypes.c_int()
            c_nSizeMax = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInBufferSizeInfo(self._device._hdwf, c_nSizeMin, c_nSizeMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nSizeMin = c_nSizeMin.value
            nSizeMax = c_nSizeMax.value
            return (nSizeMin, nSizeMax)

        def bufferSizeSet(self, nSize: int) -> None:
            """Adjust the AnalogIn instrument buffer size."""
            result = self._device._dwf._lib.FDwfAnalogInBufferSizeSet(self._device._hdwf, nSize)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def bufferSizeGet(self) -> int:
            """Return the used AnalogIn instrument buffer size."""
            c_nSize = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInBufferSizeGet(self._device._hdwf, c_nSize)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nSize = c_nSize.value
            return nSize

        def noiseSizeInfo(self) -> int:
            """Return the maximum noise buffer size for the instrument."""
            c_nSizeMax = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInNoiseSizeInfo(self._device._hdwf, c_nSizeMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nSizeMax = c_nSizeMax.value
            return nSizeMax

        def noiseSizeSet(self, nSize: int) -> None:
            result = self._device._dwf._lib.FDwfAnalogInNoiseSizeSet(self._device._hdwf, nSize)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def noiseSizeGet(self) -> int:
            """Return the used AnalogIn noise buffer size.

            This is automatically adjusted according to the sample buffer size. For instance, having maximum buffer
            size of 8192 and noise buffer size of 512, setting the sample buffer size to 4096 the noise buffer size will be 256.
            """
            c_nSize = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInNoiseSizeGet(self._device._hdwf, c_nSize)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nSize = c_nSize.value
            return nSize

        def acquisitionModeInfo(self) -> List[ACQMODE]:
            """Returns the supported AnalogIn acquisition modes.

            Single : Perform a single buffer acquisition and rearm the instrument for next capture after the data is fetched
                     to host using the `status` function.

            ScanShift : Perform a continuous acquisition in FIFO style.
                        The trigger setting is ignored.
                        The last sample is at the end of the buffer.
                        The `statusSamplesValid` function is used to show the number of the acquired samples,
                          which will grow until reaching the buffer size.
                        Then, the waveform "picture" is shifted for every new sample.

            ScanScreen : Perform continuous acquisition circularly writing samples into the buffer.
                         The trigger setting is ignored.
                         The IndexWrite shows the buffer write position.
                         This is similar to a heart monitor display.

            Record : Perform acquisition for length of time set by `recordLengthSet`.

            Single1 : Perform a single buffer acquisition.
            """

            c_acquisition_mode_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInAcquisitionModeInfo(self._device._hdwf, c_acquisition_mode_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            acquisition_mode_bitset = c_acquisition_mode_bitset.value
            acquisiton_mode_list = [acquisiton_mode for acquisiton_mode in ACQMODE if acquisition_mode_bitset & (1 << acquisiton_mode.value)]
            return acquisiton_mode_list

        def acquisitionModeSet(self, acquisition_mode: ACQMODE) -> None:
            """Set the acquisition mode."""
            result = self._device._dwf._lib.FDwfAnalogInAcquisitionModeSet(self._device._hdwf, acquisition_mode.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def acquisitionModeGet(self) -> ACQMODE:
            """Get the acquisition mode."""
            c_acquisition_mode = _typespec_ctypes.ACQMODE()
            result = self._device._dwf._lib.FDwfAnalogInAcquisitionModeGet(self._device._hdwf, c_acquisition_mode)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            acquisition_mode = ACQMODE(c_acquisition_mode.value)
            return acquisition_mode

        # Channel configuration:

        def channelCount(self) -> int:
            """Read the number of AnalogIn channels of the device."""
            c_channel_count = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInChannelCount(self._device._hdwf, c_channel_count)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            channel_count = c_channel_count.value
            return channel_count

        def channelEnableSet(self, idxChannel: int, enable: bool) -> None:
            """Enable or disable the specified AnalogIn channel."""
            result = self._device._dwf._lib.FDwfAnalogInChannelEnableSet(self._device._hdwf, idxChannel, enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def channelEnableGet(self, idxChannel: int) -> bool:
            """Get the current enable/disable status of the specified AnalogIn channel."""
            c_enable = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInChannelEnableGet(self._device._hdwf, idxChannel, c_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            enable = bool(c_enable.value)
            return enable

        def channelFilterInfo(self) -> List[FILTER]:
            c_filter_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInChannelFilterInfo(self._device._hdwf, c_filter_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            filter_bitset = c_filter_bitset.value
            filter_list = [filter_ for filter_ in FILTER if filter_bitset & (1 << filter_.value)]
            return filter_list

        def channelFilterSet(self, idxChannel: int, filter_: FILTER) -> None:
            result = self._device._dwf._lib.FDwfAnalogInChannelFilterSet(self._device._hdwf, idxChannel, filter_.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def channelFilterGet(self, idxChannel: int) -> FILTER:
            c_filter = _typespec_ctypes.FILTER()
            result = self._device._dwf._lib.FDwfAnalogInChannelFilterGet(self._device._hdwf, idxChannel, c_filter)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            filter_ = FILTER(c_filter.value)
            return filter_

        def channelRangeInfo(self) -> Tuple[float, float, float]:
            c_voltsMin = _typespec_ctypes.c_double()
            c_voltsMax = _typespec_ctypes.c_double()
            c_nSteps = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInChannelRangeInfo(self._device._hdwf, c_voltsMin, c_voltsMax, c_nSteps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            voltsMin = c_voltsMin.value
            voltsMax = c_voltsMax.value
            nSteps = c_nSteps.value
            return (voltsMin, voltsMax, nSteps)

        def channelRangeSteps(self) -> List[float]:
            c_rgVoltsStep = _typespec_ctypes.c_double_array_32()
            c_nSteps = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInChannelRangeSteps(self._device._hdwf, c_rgVoltsStep, c_nSteps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nSteps = c_nSteps.value
            rgVoltsStep = [c_rgVoltsStep[index] for index in range(nSteps)]
            return rgVoltsStep

        def channelRangeSet(self, idxChannel: int, voltsRange: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInChannelRangeSet(self._device._hdwf, idxChannel, voltsRange)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def channelRangeGet(self, idxChannel: int) -> float:
            c_voltsRange = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInChannelRangeGet(self._device._hdwf, idxChannel, c_voltsRange)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            voltsRange = c_voltsRange.value
            return voltsRange

        def channelOffsetInfo(self) -> Tuple[float, float, float]:
            c_voltsMin = _typespec_ctypes.c_double()
            c_voltsMax = _typespec_ctypes.c_double()
            c_nSteps = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInChannelOffsetInfo(self._device._hdwf, c_voltsMin, c_voltsMax, c_nSteps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            voltsMin = c_voltsMin.value
            voltsMax = c_voltsMax.value
            nSteps = c_nSteps.value
            return (voltsMin, voltsMax, nSteps)

        def channelOffsetSet(self, idxChannel: int, voltOffset: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInChannelOffsetSet(self._device._hdwf, idxChannel, voltOffset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def channelOffsetGet(self, idxChannel: int) -> float:
            c_voltOffset = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInChannelOffsetGet(self._device._hdwf, idxChannel, c_voltOffset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            voltOffset = c_voltOffset.value
            return voltOffset

        def channelAttenuationSet(self, idxChannel: int, attenuation: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInChannelAttenuationSet(self._device._hdwf, idxChannel, attenuation)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def channelAttenuationGet(self, idxChannel: int) -> float:
            c_attenuation = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInChannelAttenuationGet(self._device._hdwf, idxChannel, c_attenuation)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            attenuation = c_attenuation.value
            return attenuation

        def channelBandwidthSet(self, idxChannel: int, bandwidth: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInChannelBandwidthSet(self._device._hdwf, idxChannel, bandwidth)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def channelBandwidthGet(self, idxChannel: int) -> float:
            c_bandwidth = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInChannelBandwidthGet(self._device._hdwf, idxChannel, c_bandwidth)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            bandwidth = c_bandwidth.value
            return bandwidth

        def channelImpedanceSet(self, idxChannel: int, impedance: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInChannelImpedanceSet(self._device._hdwf, idxChannel, impedance)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def channelImpedanceGet(self, idxChannel: int) -> float:
            c_impedance = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInChanneImpedanceGet(self._device._hdwf, idxChannel, c_impedance)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            impedance = c_impedance.value
            return impedance

        # Trigger configuration:

        def triggerSourceSet(self, trigger_source: TRIGSRC) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerSourceSet(self._device._hdwf, trigger_source.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerSourceGet(self) -> TRIGSRC:
            c_trigger_source = _typespec_ctypes.TRIGSRC()
            result = self._device._dwf._lib.FDwfAnalogInTriggerSourceGet(self._device._hdwf, c_trigger_source)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_source = TRIGSRC(c_trigger_source.value)
            return trigger_source

        def triggerPositionInfo(self) -> Tuple[float, float, float]:
            c_secMin = _typespec_ctypes.c_double()
            c_secMax = _typespec_ctypes.c_double()
            c_nSteps = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerPositionInfo(self._device._hdwf, c_secMin, c_secMax, c_nSteps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secMin = c_secMin.value
            secMax = c_secMax.value
            nSteps = c_nSteps.value
            return (secMin, secMax, nSteps)

        def triggerPositionSet(self, secPosition: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerPositionSet(self._device._hdwf, secPosition)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerPositionGet(self) -> float:
            c_secPosition = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerPositionGet(self._device._hdwf, c_secPosition)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secPosition = c_secPosition.value
            return secPosition

        def triggerPositionStatus(self) -> float:
            c_secPosition = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerPositionStatus(self._device._hdwf, c_secPosition)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secPosition = c_secPosition.value
            return secPosition

        def triggerAutoTimeoutInfo(self) -> Tuple[float, float, float]:
            c_secMin = _typespec_ctypes.c_double()
            c_secMax = _typespec_ctypes.c_double()
            c_nSteps = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerAutoTimeoutInfo(self._device._hdwf, c_secMin, c_secMax, c_nSteps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secMin = c_secMin.value
            secMax = c_secMax.value
            nSteps = c_nSteps.value
            return (secMin, secMax, nSteps)

        def triggerAutoTimeoutSet(self, secTimout: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerAutoTimeoutSet(self._device._hdwf, secTimout)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerAutoTimeoutGet(self) -> float:
            c_secTimeout = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerAutoTimeoutGet(self._device._hdwf, c_secTimeout)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secTimeout = c_secTimeout.value
            return secTimeout

        def triggerHoldOffInfo(self) -> Tuple[float, float, float]:
            # TODO: Typo 'nStep' (corrected)
            c_secMin = _typespec_ctypes.c_double()
            c_secMax = _typespec_ctypes.c_double()
            c_nSteps = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerHoldOffInfo(self._device._hdwf, c_secMin, c_secMax, c_nSteps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secMin = c_secMin.value
            secMax = c_secMax.value
            nSteps = c_nSteps.value
            return (secMin, secMax, nSteps)

        def triggerHoldOffSet(self, secHoldOff: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerHoldOffSet(self._device._hdwf, secHoldOff)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerHoldOffGet(self) -> float:
            c_secHoldOff = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerHoldOffGet(self._device._hdwf, c_secHoldOff)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secHoldOff = c_secHoldOff.value
            return secHoldOff

        def triggerTypeInfo(self) -> List[TRIGTYPE]:
            c_trigger_type_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInTriggerTypeInfo(self._device._hdwf, c_trigger_type_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_type_bitset = c_trigger_type_bitset.value
            trigger_type_list = [trigger_type for trigger_type in TRIGTYPE if trigger_type_bitset & (1 << trigger_type.value)]
            return trigger_type_list

        def triggerTypeSet(self, trigger_type: TRIGTYPE) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerTypeSet(self._device._hdwf, trigger_type.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerTypeGet(self) -> TRIGTYPE:
            c_trigger_type = _typespec_ctypes.TRIGTYPE()
            result = self._device._dwf._lib.FDwfAnalogInTriggerTypeGet(self._device._hdwf, c_trigger_type)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_type = TRIGTYPE(c_trigger_type.value)
            return trigger_type

        def triggerChannelInfo(self) -> Tuple[int, int]:
            c_idxMin = _typespec_ctypes.c_int()
            c_idxMax = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInTriggerChannelInfo(self._device._hdwf, c_idxMin, c_idxMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            idxMin = c_idxMin.value
            idxMax = c_idxMax.value
            return (idxMin, idxMax)

        def triggerChannelSet(self, idxChannel: int) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerChannelSet(self._device._hdwf, idxChannel)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerChannelGet(self) -> int:
            c_idxChannel = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInTriggerChannelGet(self._device._hdwf, c_idxChannel)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            idxChannel = c_idxChannel.value
            return idxChannel

        def triggerFilterInfo(self) -> List[FILTER]:
            c_filter_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInTriggerFilterInfo(self._device._hdwf, c_filter_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            filter_bitset = c_filter_bitset.value
            filter_list = [filter_ for filter_ in FILTER if filter_bitset & (1 << filter_.value)]
            return filter_list

        def triggerFilterSet(self, filter_: FILTER) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerFilterSet(self._device._hdwf, filter_.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerFilterGet(self) -> FILTER:
            c_filter = _typespec_ctypes.FILTER()
            result = self._device._dwf._lib.FDwfAnalogInTriggerFilterGet(self._device._hdwf, c_filter)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            filter_ = FILTER(c_filter.value)
            return filter_

        def triggerLevelInfo(self) -> Tuple[float, float, float]:
            c_voltsMin = _typespec_ctypes.c_double()
            c_voltsMax = _typespec_ctypes.c_double()
            c_nSteps = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerLevelInfo(self._device._hdwf, c_voltsMin, c_voltsMax, c_nSteps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            voltsMin = c_voltsMin.value
            voltsMax = c_voltsMax.value
            nSteps = c_nSteps.value
            return (voltsMin, voltsMax, nSteps)

        def triggerLevelSet(self, voltsLevel: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerLevelSet(self._device._hdwf, voltsLevel)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerLevelGet(self) -> float:
            c_voltsLevel = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerLevelGet(self._device._hdwf, c_voltsLevel)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            voltsLevel = c_voltsLevel.value
            return voltsLevel

        def triggerHysteresisInfo(self) -> Tuple[float, float, float]:
            c_voltsMin = _typespec_ctypes.c_double()
            c_voltsMax = _typespec_ctypes.c_double()
            c_nSteps = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerHysteresisInfo(self._device._hdwf, c_voltsMin, c_voltsMax, c_nSteps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            voltsMin = c_voltsMin.value
            voltsMax = c_voltsMax.value
            nSteps = c_nSteps.value
            return (voltsMin, voltsMax, nSteps)

        def triggerHysteresisSet(self, voltsLevel: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerHysteresisSet(self._device._hdwf, voltsLevel)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerHysteresisGet(self) -> float:
            c_voltsHysteresis = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerHysteresisGet(self._device._hdwf, c_voltsHysteresis)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            voltsHysteresis = c_voltsHysteresis.value
            return voltsHysteresis

        def triggerConditionInfo(self) -> List[DwfTriggerSlope]:
            c_trigger_condition_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInTriggerConditionInfo(self._device._hdwf, c_trigger_condition_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_condition_bitset = c_trigger_condition_bitset.value
            trigger_condition_list = [trigger_condition for trigger_condition in DwfTriggerSlope if trigger_condition_bitset & (1 << trigger_condition.value)]
            return trigger_condition_list

        def triggerConditionSet(self, trigger_condition: DwfTriggerSlope) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerConditionSet(self._device._hdwf, trigger_condition.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerConditionGet(self) -> DwfTriggerSlope:
            c_trigger_condition = _typespec_ctypes.DwfTriggerSlope()
            result = self._device._dwf._lib.FDwfAnalogInTriggerConditionGet(self._device._hdwf, c_trigger_condition)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_condition = c_trigger_condition.value
            return DwfTriggerSlope(trigger_condition)

        def triggerLengthInfo(self) -> Tuple[float, float, float]:
            c_secMin = _typespec_ctypes.c_double()
            c_secMax = _typespec_ctypes.c_double()
            c_nSteps = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerLengthInfo(self._device._hdwf, c_secMin, c_secMax, c_nSteps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secMin = c_secMin.value
            secMax = c_secMax.value
            nSteps = c_nSteps.value
            return (secMin, secMax, nSteps)

        def triggerLengthSet(self, secLength: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerLengthSet(self._device._hdwf, secLength)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerLengthGet(self) -> float:
            c_secLength = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInTriggerLengthGet(self._device._hdwf, c_secLength)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secLength = c_secLength.value
            return secLength

        def triggerLengthConditionInfo(self) -> List[TRIGLEN]:
            c_triglen_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInTriggerLengthConditionInfo(self._device._hdwf, c_triglen_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            triglen_bitset = c_triglen_bitset.value
            triglen_list = [triglen for triglen in TRIGLEN if triglen_bitset & (1 << triglen.value)]
            return triglen_list

        def triggerLengthConditionSet(self, trigger_length: TRIGLEN) -> None:
            result = self._device._dwf._lib.FDwfAnalogInTriggerLengthConditionSet(self._device._hdwf, trigger_length.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerLengthConditionGet(self) -> TRIGLEN:
            c_trigger_length = _typespec_ctypes.TRIGLEN()
            result = self._device._dwf._lib.FDwfAnalogInTriggerLengthConditionGet(self._device._hdwf, c_trigger_length)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_length = TRIGLEN(c_trigger_length.value)
            return trigger_length

        def samplingSourceSet(self, sampling_source: TRIGSRC) -> None:
            """Configure the AnalogIn acquisition data sampling source."""
            result = self._device._dwf._lib.FDwfAnalogInSamplingSourceSet(self._device._hdwf, sampling_source.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def samplingSourceGet(self) -> TRIGSRC:
            """Return the configured sampling source."""
            c_sampling_source = _typespec_ctypes.TRIGSRC()
            result = self._device._dwf._lib.FDwfAnalogInSamplingSourceGet(self._device._hdwf, c_sampling_source)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            sampling_source = TRIGSRC(c_sampling_source.value)
            return sampling_source

        def samplingSlopeSet(self, sampling_slope: DwfTriggerSlope) -> None:
            """Set the sampling slope for the instrument."""
            result = self._device._dwf._lib.FDwfAnalogInSamplingSlopeSet(self._device._hdwf, sampling_slope.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def samplingSlopeGet(self) -> DwfTriggerSlope:
            """Return the sampling for the instrument."""
            c_sampling_slope = _typespec_ctypes.DwfTriggerSlope()
            result = self._device._dwf._lib.FDwfAnalogInSamplingSlopeGet(self._device._hdwf, c_sampling_slope)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            sampling_slope = DwfTriggerSlope(c_sampling_slope.value)
            return sampling_slope

        def samplingDelaySet(self, sampling_delay: float) -> None:
            """Set the sampling delay for the instrument, in seconds."""
            result = self._device._dwf._lib.FDwfAnalogInSamplingDelaySet(self._device._hdwf, sampling_delay)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def samplingDelayGet(self) -> float:
            """Return the configured sampling delay, in seconds."""
            c_sampling_delay = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogInSamplingDelayGet(self._device._hdwf, c_sampling_delay)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            sampling_delay = c_sampling_delay.value
            return sampling_delay

        def triggerSourceInfo(self) -> List[TRIGSRC]:
            """Get analog-in trigger source info.

            Note: This function is OBSOLETE. Use the generic DeviceAPI.triggerInfo() method instead.
            """
            c_trigger_source_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogInTriggerSourceInfo(self._device._hdwf, c_trigger_source_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_source_bitset = c_trigger_source_bitset.value
            trigger_source_list = [trigger_source for trigger_source in TRIGSRC if trigger_source_bitset & (1 << trigger_source.value)]
            return trigger_source_list


    class AnalogOutAPI:
        """Provides wrappers for the 'FDwfAnalogOut' API functions.

        Version 3.14.3 of the DWF library has 83 'FDwfAnalogOut' functions, 25 of which are obsolete.
        """

        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def count(self) -> int:
            c_cChannel = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutCount(self._device._hdwf, c_cChannel)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            cChannel = c_cChannel.value
            return cChannel

        def masterSet(self, idxChannel: int, idxMaster: int) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutMasterSet(self._device._hdwf, idxChannel, idxMaster)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def masterGet(self, idxChannel: int) -> int:
            c_idxMaster = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutMasterGet(self._device._hdwf, idxChannel, c_idxMaster)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            idxMaster = c_idxMaster.value
            return idxMaster

        def triggerSourceSet(self, idxChannel: int, trigger_source: TRIGSRC) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutTriggerSourceSet(self._device._hdwf, idxChannel, trigger_source.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerSourceGet(self, idxChannel: int) -> TRIGSRC:
            c_trigger_source = _typespec_ctypes.TRIGSRC()
            result = self._device._dwf._lib.FDwfAnalogOutTriggerSourceGet(self._device._hdwf, idxChannel, c_trigger_source)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_source = TRIGSRC(c_trigger_source.value)
            return trigger_source

        def triggerSlopeSet(self, idxChannel: int, trigger_slope: DwfTriggerSlope) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutTriggerSlopeSet(self._device._hdwf, idxChannel, trigger_slope.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerSlopeGet(self, idxChannel: int) -> DwfTriggerSlope:
            c_trigger_slope = _typespec_ctypes.DwfTriggerSlope()
            result = self._device._dwf._lib.FDwfAnalogOutTriggerSlopeGet(self._device._hdwf, idxChannel, c_trigger_slope)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_slope = DwfTriggerSlope(c_trigger_slope.value)
            return trigger_slope

        def runInfo(self, idxChannel: int) -> Tuple[float, float]:
            c_secMin = _typespec_ctypes.c_double()
            c_secMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutRunInfo(self._device._hdwf, idxChannel, c_secMin, c_secMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secMin = c_secMin.value
            secMax = c_secMax.value
            return (secMin, secMax)

        def runSet(self, idxChannel: int, secRun: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutRunSet(self._device._hdwf, idxChannel, secRun)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def runGet(self, idxChannel: int) -> float:
            c_secRun = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutRunGet(self._device._hdwf, idxChannel, c_secRun)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secRun = c_secRun.value
            return secRun

        def runStatus(self, idxChannel: int) -> float:
            c_secRun = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutRunStatus(self._device._hdwf, idxChannel, c_secRun)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secRun = c_secRun.value
            return secRun

        def waitInfo(self, idxChannel: int) -> Tuple[float, float]:
            c_secMin = _typespec_ctypes.c_double()
            c_secMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutWaitInfo(self._device._hdwf, idxChannel, c_secMin, c_secMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secMin = c_secMin.value
            secMax = c_secMax.value
            return (secMin, secMax)

        def waitSet(self, idxChannel: int, secWait: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutWaitSet(self._device._hdwf, idxChannel, secWait)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def waitGet(self, idxChannel: int) -> float:
            c_secWait = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutWaitGet(self._device._hdwf, idxChannel, c_secWait)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secWait = c_secWait.value
            return secWait

        def repeatInfo(self, idxChannel: int) -> Tuple[int, int]:
            c_nMin = _typespec_ctypes.c_int()
            c_nMax = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutRepeatInfo(self._device._hdwf, idxChannel, c_nMin, c_nMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nMin = c_nMin.value
            nMax = c_nMax.value
            return (nMin, nMax)

        def repeatSet(self, idxChannel: int, repeat: int) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutRepeatSet(self._device._hdwf, idxChannel, repeat)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def repeatGet(self, idxChannel: int) -> int:
            c_repeat = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutRepeatGet(self._device._hdwf, idxChannel, c_repeat)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            repeat = c_repeat.value
            return repeat

        def repeatStatus(self, idxChannel: int) -> int:
            c_repeat_status = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutRepeatStatus(self._device._hdwf, idxChannel, c_repeat_status)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            repeat_status = c_repeat_status.value
            return repeat_status

        def repeatTriggerSet(self, idxChannel: int, repeatTrigger: bool) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutRepeatTriggerSet(self._device._hdwf, idxChannel, repeatTrigger)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def repeatTriggerGet(self, idxChannel: int) -> bool:
            c_repeatTrigger = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutRepeatTriggerGet(self._device._hdwf, idxChannel, c_repeatTrigger)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            repeatTrigger = bool(c_repeatTrigger.value)
            return repeatTrigger

        def limitationInfo(self, idxChannel: int) -> Tuple[float, float]:
            c_min = _typespec_ctypes.c_double()
            c_max = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutLimitationInfo(self._device._hdwf, idxChannel, c_min, c_max)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            min_ = c_min.value
            max_ = c_max.value
            return (min_, max_)

        def limitationSet(self, idxChannel: int, limit: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutLimitationSet(self._device._hdwf, idxChannel, limit)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def limitationGet(self, idxChannel: int) -> float:
            c_limit = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutLimitationGet(self._device._hdwf, idxChannel, c_limit)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            limit = c_limit.value
            return limit

        def modeSet(self, idxChannel: int, mode: DwfAnalogOutMode) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutModeSet(self._device._hdwf, idxChannel, mode.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def modeGet(self, idxChannel: int) -> DwfAnalogOutMode:
            c_mode = _typespec_ctypes.DwfAnalogOutMode()
            result = self._device._dwf._lib.FDwfAnalogOutModeGet(self._device._hdwf, idxChannel, c_mode)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            mode = DwfAnalogOutMode(c_mode.value)
            return mode

        def idleInfo(self, idxChannel: int) -> List[DwfAnalogOutIdle]:
            c_idle_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutIdleInfo(self._device._hdwf, idxChannel, c_idle_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            idle_bitset = c_idle_bitset.value
            idle_list = [idle for idle in DwfAnalogOutIdle if idle_bitset & (1 << idle.value)]
            return idle_list

        def idleSet(self, idxChannel: int, idle: DwfAnalogOutIdle) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutIdleSet(self._device._hdwf, idxChannel, idle.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def idleGet(self, idxChannel: int) -> DwfAnalogOutIdle:
            c_idle = _typespec_ctypes.DwfAnalogOutIdle()
            result = self._device._dwf._lib.FDwfAnalogOutIdleGet(self._device._hdwf, idxChannel, c_idle)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            idle = DwfAnalogOutIdle(c_idle.value)
            return idle

        def nodeInfo(self, idxChannel: int) -> List[AnalogOutNode]:
            c_node_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutNodeInfo(self._device._hdwf, idxChannel, c_node_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            node_bitset = c_node_bitset.value
            node_list = [node for node in AnalogOutNode if node_bitset & (1 << node.value)]
            return node_list

        def nodeEnableSet(self, idxChannel: int, node: AnalogOutNode, enable: bool) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutNodeEnableSet(self._device._hdwf, idxChannel, node.value, enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def nodeEnableGet(self, idxChannel: int, node: AnalogOutNode) -> bool:
            c_enable = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutNodeEnableGet(self._device._hdwf, idxChannel, node.value, c_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            enable = bool(c_enable.value)
            return enable

        def nodeFunctionInfo(self, idxChannel: int, node: AnalogOutNode) -> List[FUNC]:
            c_func_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutNodeFunctionInfo(self._device._hdwf, idxChannel, node.value, c_func_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            func_bitset = c_func_bitset.value
            func_list = [func for func in FUNC if func_bitset & (1 << func.value)]
            return func_list

        def nodeFunctionSet(self, idxChannel: int, node: AnalogOutNode, func: FUNC) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutNodeFunctionSet(self._device._hdwf, idxChannel, node.value, func.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def nodeFunctionGet(self, idxChannel: int, node: AnalogOutNode) -> FUNC:
            c_func = _typespec_ctypes.FUNC()
            result = self._device._dwf._lib.FDwfAnalogOutNodeFunctionGet(self._device._hdwf, idxChannel, node.value, c_func)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            func = FUNC(c_func.value)
            return func

        def nodeFrequencyInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]:
            c_hzMin = _typespec_ctypes.c_double()
            c_hzMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutNodeFrequencyInfo(self._device._hdwf, idxChannel, node.value, c_hzMin, c_hzMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            hzMin = c_hzMin.value
            hzMax = c_hzMax.value
            return (hzMin, hzMax)

        def nodeFrequencySet(self, idxChannel: int, node: AnalogOutNode, hzFrequency: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutNodeFrequencySet(self._device._hdwf, idxChannel, node.value, hzFrequency)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def nodeFrequencyGet(self, idxChannel: int, node: AnalogOutNode) -> float:
            c_hzFrequency = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutNodeFrequencyGet(self._device._hdwf, idxChannel, node.value, c_hzFrequency)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            hzFrequency = c_hzFrequency.value
            return hzFrequency

        def nodeAmplitudeInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]:
            c_min = _typespec_ctypes.c_double()
            c_max = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutNodeAmplitudeInfo(self._device._hdwf, idxChannel, node.value, c_min, c_max)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            min_ = c_min.value
            max_ = c_max.value
            return (min_, max_)

        def nodeAmplitudeSet(self, idxChannel: int, node: AnalogOutNode, vAmplitude: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutNodeAmplitudeSet(self._device._hdwf, idxChannel, node.value, vAmplitude)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def nodeAmplitudeGet(self, idxChannel: int, node: AnalogOutNode) -> float:
            c_vAmplitude = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutNodeAmplitudeGet(self._device._hdwf, idxChannel, node.value, c_vAmplitude)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            vAmplitude = c_vAmplitude.value
            return vAmplitude

        def nodeOffsetInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]:
            c_min = _typespec_ctypes.c_double()
            c_max = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutNodeOffsetInfo(self._device._hdwf, idxChannel, node.value, c_min, c_max)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            min_ = c_min.value
            max_ = c_max.value
            return (min_, max_)

        def nodeOffsetSet(self, idxChannel: int, node: AnalogOutNode, vOffset: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutNodeOffsetSet(self._device._hdwf, idxChannel, node.value, vOffset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def nodeOffsetGet(self, idxChannel: int, node: AnalogOutNode) -> float:
            c_vOffset = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutNodeOffsetGet(self._device._hdwf, idxChannel, node.value, c_vOffset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            vOffset = c_vOffset.value
            return vOffset

        def nodeSymmetryInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]:
            c_percentageMin = _typespec_ctypes.c_double()
            c_percentageMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutNodeSymmetryInfo(self._device._hdwf, idxChannel, node.value, c_percentageMin, c_percentageMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            percentageMin = c_percentageMin.value
            percentageMax = c_percentageMax.value
            return (percentageMin, percentageMax)

        def nodeSymmetrySet(self, idxChannel: int, node: AnalogOutNode, percentageSymmetry: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutNodeSymmetrySet(self._device._hdwf, idxChannel, node.value, percentageSymmetry)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def nodeSymmetryGet(self, idxChannel: int, node: AnalogOutNode) -> float:
            c_percentageSymmetry = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutNodeSymmetryGet(self._device._hdwf, idxChannel, node.value, c_percentageSymmetry)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            percentageSymmetry = c_percentageSymmetry.value
            return percentageSymmetry

        def nodePhaseInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]:
            c_degreeMin = _typespec_ctypes.c_double()
            c_degreeMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutNodePhaseInfo(self._device._hdwf, idxChannel, node.value, c_degreeMin, c_degreeMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            degreeMin = c_degreeMin.value
            degreeMax = c_degreeMax.value
            return (degreeMin, degreeMax)

        def nodePhaseSet(self, idxChannel: int, node: AnalogOutNode, degreePhase: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutNodePhaseSet(self._device._hdwf, idxChannel, node.value, degreePhase)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def nodePhaseGet(self, idxChannel: int, node: AnalogOutNode) -> float:
            c_degreePhase = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutNodePhaseGet(self._device._hdwf, idxChannel, node.value, c_degreePhase)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            degreePhase = c_degreePhase.value
            return degreePhase

        def nodeDataInfo(self, idxChannel: int, node: AnalogOutNode) -> Tuple[float, float]:
            c_samplesMin = _typespec_ctypes.c_int()
            c_samplesMax = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutNodeDataInfo(self._device._hdwf, idxChannel, node.value, c_samplesMin, c_samplesMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            samplesMin = c_samplesMin.value
            samplesMax = c_samplesMax.value
            return (samplesMin, samplesMax)

        def nodeDataSet(self, idxChannel: int, node: AnalogOutNode, data: np.ndarray) -> None:

            double_data = data.astype(np.float64)

            result = self._device._dwf._lib.FDwfAnalogOutNodeDataSet(self._device._hdwf, idxChannel, node.value, double_data.ctypes.data_as(_typespec_ctypes.c_double_ptr), len(double_data))
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def customAMFMEnableSet(self, idxChannel: int, enable: bool) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutCustomAMFMEnableSet(self._device._hdwf, idxChannel, enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def customAMFMEnableGet(self, idxChannel: int) -> bool:
            c_enable = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutCustomAMFMEnableGet(self._device._hdwf, idxChannel, c_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            enable = bool(c_enable.value)
            return enable

        def reset(self, idxChannel: int) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutReset(self._device._hdwf, idxChannel)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def configure(self, idxChannel: int, start: bool) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutConfigure(self._device._hdwf, idxChannel, start)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def status(self, idxChannel: int) -> DwfState:
            c_status = _typespec_ctypes.DwfState()
            result = self._device._dwf._lib.FDwfAnalogOutStatus(self._device._hdwf, idxChannel, c_status)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            status = DwfState(c_status.value)
            return status

        def nodePlayStatus(self, idxChannel: int, node: AnalogOutNode) -> Tuple[int, int, int]:
            c_dataFree = _typespec_ctypes.c_int()
            c_dataLost = _typespec_ctypes.c_int()
            c_dataCorrupted = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutNodePlayStatus(self._device._hdwf, idxChannel, node, c_dataFree, c_dataLost, c_dataCorrupted)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            dataFree = c_dataFree.value
            dataLost = c_dataLost.value
            dataCorrupted = c_dataCorrupted.value
            return (dataFree, dataLost, dataCorrupted)

        def nodePlayData(self, idxChannel:int,  node: AnalogOutNode, data: np.ndarray) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutNodePlayData(self._device._hdwf, idxChannel, node, data.ctypes.data_as(_typespec_ctypes.c_double_ptr), len(data))
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        ################################################# Obsolete functions follow:

        def triggerSourceInfo(self) -> List[TRIGSRC]:
            """Get analog out trigger source info.

            This function is OBSOLETE.
            """
            c_trigger_source_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutTriggerSourceInfo(self._device._hdwf, c_trigger_source_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_source_bitset = c_trigger_source_bitset.value
            trigger_source_list = [trigger_source for trigger_source in TRIGSRC if trigger_source_bitset & (1 << trigger_source.value)]
            return trigger_source_list

        def enableSet(self, idxChannel: int, enable: bool) -> None:
            """Enable or disable the specified AnalogOut channel.

            This function is OBSOLETE. Use `nodeEnableSet` instead.
            """
            result = self._device._dwf._lib.FDwfAnalogOutEnableSet(self._device._hdwf, idxChannel, enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def enableGet(self, idxChannel: int) -> bool:
            """Get the current enable/disable status of the specified AnalogOut channel.

            This function is OBSOLETE. Use `nodeEnableGet` instead.
            """
            c_enable = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutEnableGet(self._device._hdwf, idxChannel, c_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            enable = bool(c_enable.value)
            return enable

        def functionInfo(self, idxChannel: int) -> List[FUNC]:
            """Get AnalogOut function info.

            This function is OBSOLETE. Use `nodeFunctionInfo` instead.
            """
            c_function_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutFunctionInfo(self._device._hdwf, idxChannel, c_function_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            function_bitset = c_function_bitset.value
            function_list = [function_ for function_ in FUNC if function_bitset & (1 << function_.value)]
            return function_list

        def functionSet(self, idxChannel: int, func: FUNC) -> None:
            """Set AnalogOut function.

            This function is OBSOLETE. Use `nodeFunctionSet` instead.
            """
            result = self._device._dwf._lib.FDwfAnalogOutFunctionSet(self._device._hdwf, idxChannel, func.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def functionGet(self, idxChannel: int) -> FUNC:
            """Get AnalogOut function.

            This function is OBSOLETE. Use `nodeFunctionGet` instead.
            """
            c_func = _typespec_ctypes.FUNC()
            result = self._device._dwf._lib.FDwfAnalogOutFunctionGet(self._device._hdwf, idxChannel, c_func)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            func = FUNC(c_func.value)
            return func

        def frequencyInfo(self, idxChannel: int) -> Tuple[float, float]:
            """Get AnalogOut channel frequency range info.

            This function is OBSOLETE. Use `nodeFrequencyInfo` instead.
            """
            c_hzMin = _typespec_ctypes.c_double()
            c_hzMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutFrequencyInfo(self._device._hdwf, idxChannel, c_hzMin, c_hzMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            hzMin = c_hzMin.value
            hzMax = c_hzMax.value
            return (hzMin, hzMax)

        def frequencySet(self, idxChannel: int, hzFrequency: float) -> None:
            """Get AnalogOut channel frequency.

            This function is OBSOLETE. Use `nodeFrequencySet` instead.
            """
            result = self._device._dwf._lib.FDwfAnalogOutFrequencySet(self._device._hdwf, idxChannel, hzFrequency)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def frequencyGet(self, idxChannel: int) -> float:
            """Get AnalogOut channel frequency.

            This function is OBSOLETE. Use `nodeFrequencyGet` instead.
            """
            c_hzFrequency = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutFrequencyGet(self._device._hdwf, idxChannel, c_hzFrequency)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            hzFrequency = c_hzFrequency.value
            return hzFrequency

        def amplitudeInfo(self, idxChannel: int) -> Tuple[float, float]:
            """Get AnalogOut channel frequency range.

            This function is OBSOLETE. Use `nodeAmplitudeInfo` instead.
            """
            c_min = _typespec_ctypes.c_double()
            c_max = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutAmplitudeInfo(self._device._hdwf, idxChannel, c_min, c_max)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            min_ = c_min.value
            max_ = c_max.value
            return (min_, max_)

        def amplitudeSet(self, idxChannel: int, vAmplitude: float) -> None:
            """Set AnalogOut channel frequency.

            This function is OBSOLETE. Use `nodeAmplitudeSet` instead.
            """
            result = self._device._dwf._lib.FDwfAnalogOutAmplitudeSet(self._device._hdwf, idxChannel, vAmplitude)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def amplitudeGet(self, idxChannel: int) -> float:
            """Get AnalogOut channel frequency.

            This function is OBSOLETE. Use `nodeAmplitudeGet` instead.
            """
            c_vAmplitude = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutAmplitudeGet(self._device._hdwf, idxChannel, c_vAmplitude)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            vAmplitude = c_vAmplitude.value
            return vAmplitude

        def offsetInfo(self, idxChannel: int) -> Tuple[float, float]:
            """Get AnalogOut channel offset range.

            This function is OBSOLETE. Use `nodeOffsetInfo` instead.
            """
            c_min = _typespec_ctypes.c_double()
            c_max = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutOffsetInfo(self._device._hdwf, idxChannel,c_min, c_max)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            min_ = c_min.value
            max_ = c_max.value
            return (min_, max_)

        def offsetSet(self, idxChannel: int, vOffset: float) -> None:
            """Set AnalogOut channel offset.

            This function is OBSOLETE. Use `nodeOffsetSet` instead.
            """
            result = self._device._dwf._lib.FDwfAnalogOutOffsetSet(self._device._hdwf, idxChannel, vOffset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def offsetGet(self, idxChannel: int) -> float:
            """Get AnalogOut channel offset.

            This function is OBSOLETE. Use `nodeOffsetGet` instead.
            """
            c_vOffset = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutOffsetGet(self._device._hdwf, idxChannel, c_vOffset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            vOffset = c_vOffset.value
            return vOffset

        def symmetryInfo(self, idxChannel: int) -> Tuple[float, float]:
            """Get AnalogOut channel symmetry range.

            This function is OBSOLETE. Use `nodeSymmetryInfo` instead.
            """
            c_percentageMin = _typespec_ctypes.c_double()
            c_percentageMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutSymmetryInfo(self._device._hdwf, idxChannel, c_percentageMin, c_percentageMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            percentageMin = c_percentageMin.value
            percentageMax = c_percentageMax.value
            return (percentageMin, percentageMax)

        def symmetrySet(self, idxChannel: int, percentageSymmetry: float) -> None:
            """Set AnalogOut channel symmetry.

            This function is OBSOLETE. Use `nodeSymmetrySet` instead.
            """
            result = self._device._dwf._lib.FDwfAnalogOutSymmetrySet(self._device._hdwf, idxChannel, percentageSymmetry)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def symmetryGet(self, idxChannel: int) -> float:
            """Get AnalogOut channel symmetry.

            This function is OBSOLETE. Use `nodeSymmetryGet` instead.
            """
            c_percentageSymmetry = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutSymmetryGet(self._device._hdwf, idxChannel, c_percentageSymmetry)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            percentageSymmetry = c_percentageSymmetry.value
            return percentageSymmetry

        def phaseInfo(self, idxChannel: int) -> Tuple[float, float]:
            """Get AnalogOut channel phase range.

            This function is OBSOLETE. Use `nodePhaseInfo` instead.
            """
            c_degreeMin = _typespec_ctypes.c_double()
            c_degreeMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutPhaseInfo(self._device._hdwf, idxChannel, c_degreeMin, c_degreeMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            degreeMin = c_degreeMin.value
            degreeMax = c_degreeMax.value
            return (degreeMin, degreeMax)

        def phaseSet(self, idxChannel: int, degreePhase: float) -> None:
            """Get AnalogOut channel phase.

            This function is OBSOLETE. Use `nodePhaseSet` instead.
            """
            result = self._device._dwf._lib.FDwfAnalogOutPhaseSet(self._device._hdwf, idxChannel, degreePhase)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def phaseGet(self, idxChannel: int) -> float:
            """Get AnalogOut channel phase.

            This function is OBSOLETE. Use `nodePhaseGet` instead.
            """
            c_degreePhase = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogOutPhaseGet(self._device._hdwf, idxChannel, c_degreePhase)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            degreePhase = c_degreePhase.value
            return degreePhase

        def dataInfo(self, idxChannel: int) -> Tuple[int, int]:
            """Get AnalogOut channel data info.

            This function is OBSOLETE. Use `nodeDataInfo` instead.
            """
            c_samplesMin = _typespec_ctypes.c_int()
            c_samplesMax = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutDataInfo(self._device._hdwf, idxChannel, c_samplesMin, c_samplesMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            samplesMin = c_samplesMin.value
            samplesMax = c_samplesMax.value
            return (samplesMin, samplesMax)

        def dataSet(self, idxChannel: int, data: np.ndarray) -> None:
            """Set AnalogOut channel data.

            This function is OBSOLETE. Use `nodeDataSet` instead.
            """
            double_data = data.astype(np.float64)

            result = self._device._dwf._lib.FDwfAnalogOutDataSet(self._device._hdwf, idxChannel, double_data.ctypes.data_as(_typespec_ctypes.c_double_ptr), len(double_data))
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()


        def playStatus(self, idxChannel: int)  -> Tuple[int, int, int]:
            """Get AnalogOut channel play status.

            This function is OBSOLETE. Use `nodePlayStatus` instead.
            """
            c_dataFree = _typespec_ctypes.c_int()
            c_dataLost = _typespec_ctypes.c_int()
            c_dataCorrupted = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogOutPlayStatus(self._device._hdwf, idxChannel, c_dataFree, c_dataLost, c_dataCorrupted)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            dataFree = c_dataFree.value
            dataLost = c_dataLost.value
            dataCorrupted = c_dataCorrupted.value
            return (dataFree, dataLost, dataCorrupted)

        def playData(self, idxChannel: int, data: np.ndarray) -> None:
            result = self._device._dwf._lib.FDwfAnalogOutPlayData(self._device._hdwf, idxChannel, data.ctypes.data_as(_typespec_ctypes.c_double_ptr), len(data))
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()


    class AnalogIOAPI:

        """Provides wrappers for the 'FDwfAnalogIO' API functions.

        Version 3.14.3 of the DWF library has 17 'FDwfAnalogIO' functions, none of which are obsolete.

        The AnalogIO functions are used to control the power supplies, reference voltage supplies, voltmeters, ammeters,
        thermometers, and any other sensors on the device. These are organized into channels which contain a number of
        nodes. For instance, a power supply channel might have three nodes: an enable setting, a voltage level
        setting/reading, and current limitation setting/reading.
        """

        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def reset(self) -> None:
            """Resets and configures (by default, having auto configure enabled) all AnalogIO instrument parameters to default values."""
            result = self._device._dwf._lib.FDwfAnalogIOReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def configure(self) -> None:
            """Configures the AnalogIO instrument."""
            result = self._device._dwf._lib.FDwfAnalogIOConfigure(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def status(self) -> None:
            """Read the status of the device and stores it internally.

            The following status functions will return the information that was read from the device when this function was called."""
            result = self._device._dwf._lib.FDwfAnalogIOStatus(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def enableInfo(self) -> Tuple[bool, bool]:
            """Verifies if Master Enable Setting and/or Master Enable Status are supported for the AnalogIO instrument.

            The Master Enable setting is essentially a software switch that "enables" or "turns on" the AnalogIO channels.
            If supported, the status of this Master Enable switch (Enabled/Disabled) can be queried by calling FDwfAnalogIOEnableStatus.
            """
            c_set_supported = _typespec_ctypes.c_int()
            c_status_supported = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogIOEnableInfo(self._device._hdwf, c_set_supported, c_set_supported)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            set_supported = bool(c_set_supported.value)
            status_supported = bool(c_status_supported.value)
            return (set_supported, status_supported)

        def enableSet(self, master_enable: bool) -> None:
            """Sets the master enable switch."""
            result = self._device._dwf._lib.FDwfAnalogIOEnableSet(self._device._hdwf, master_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def enableGet(self) -> bool:
            """Returns the current state of the master enable switch. This is not obtained from the device."""
            c_master_enable = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogIOEnableGet(self._device._hdwf, c_master_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            master_enable = bool(c_master_enable.value)
            return master_enable

        def enableStatus(self) -> bool:
            """Returns the master enable status (if the device supports it).

            This can be a switch on the board or an overcurrent protection circuit state."""
            c_master_enable_status = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogIOEnableStatus(self._device._hdwf, c_master_enable_status)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            master_enable_status = bool(c_master_enable_status.value)
            return master_enable_status

        def channelCount(self) -> int:
            """Returns the number of AnalogIO channels available on the device."""
            c_channel_count = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogIOChannelCount(self._device._hdwf, c_channel_count)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            channel_count = c_channel_count.value
            return channel_count

        def channelName(self, channel_index: int) -> Tuple[str, str]:
            """Returns the name (long text) and label (short text, printed on the device) for a channel."""
            c_channel_name = ctypes.create_string_buffer(32)
            c_channel_label = ctypes.create_string_buffer(16)
            result = self._device._dwf._lib.FDwfAnalogIOChannelName(self._device._hdwf, channel_index, c_channel_name, c_channel_label)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            channel_name = c_channel_name.value.decode()
            channel_label = c_channel_label.value.decode()
            return (channel_name, channel_label)

        def channelInfo(self, channel_index: int) -> int:
            """Returns the number of nodes associated with the specified channel."""
            c_node_count = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogIOChannelInfo(self._device._hdwf, channel_index, c_node_count)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            return c_node_count.value

        def channelNodeName(self, channel_index: int, node_index: int) -> Tuple[str, str]:
            """Returns the node name ("Voltage", "Current", ...) and units ("V", "A") for an Analog I/O node."""
            c_node_name = ctypes.create_string_buffer(32)
            c_node_units = ctypes.create_string_buffer(16)
            result = self._device._dwf._lib.FDwfAnalogIOChannelNodeName(self._device._hdwf, channel_index, node_index, c_node_name, c_node_units)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            node_name = c_node_name.value.decode()
            node_units = c_node_units.value.decode()
            return (node_name, node_units)

        def channelNodeInfo(self, channel_index: int, node_index: int) -> ANALOGIO:
            """Returns the supported channel node modes."""
            c_analog_io = _typespec_ctypes.ANALOGIO()
            result = self._device._dwf._lib.FDwfAnalogIOChannelNodeInfo(self._device._hdwf, channel_index, node_index, c_analog_io)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            analog_io = ANALOGIO(c_analog_io.value)
            return analog_io

        def channelNodeSetInfo(self, channel_index: int, node_index: int) -> Tuple[float, float, int]:
            """Returns node value limits.

            Since a Node can represent many things (Power supply, Temperature sensor, etc.), the Minimum, Maximum, and Steps parameters also represent different types of values.

            The (Maximum - Minimum) / Steps is the step size.

            FDwfAnalogIOChannelNodeInfo returns the type of values to expect and FDwfAnalogIOChannelNodeName returns the units of these values.
            """
            c_min_value = _typespec_ctypes.c_double()
            c_max_value = _typespec_ctypes.c_double()
            c_num_steps = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogIOChannelNodeSetInfo(self._device._hdwf, channel_index, node_index, c_min_value, c_max_value, c_num_steps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            min_value = c_min_value.value
            max_value = c_max_value.value
            num_steps = c_num_steps.value
            return (min_value, max_value, num_steps)

        def channelNodeSet(self, channel_index: int, node_index: int, node_value: float) -> None:
            """Sets the node value for the specified node on the specified channel."""
            result = self._device._dwf._lib.FDwfAnalogIOChannelNodeSet(self._device._hdwf, channel_index, node_index, node_value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def channelNodeGet(self, channel_index: int, node_index: int) -> float:
            """Returns the currently set value of the node on the specified channel."""
            c_node_value = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogIOChannelNodeGet(self._device._hdwf, channel_index, node_index, c_node_value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            node_value = c_node_value.value
            return node_value

        def channelNodeStatusInfo(self, channel_index: int, node_index: int) -> Tuple[float, float, int]:
            """Returns node the range of reading values available for the specified node on the specified channel."""
            c_min_value = _typespec_ctypes.c_double()
            c_max_value = _typespec_ctypes.c_double()
            c_num_steps = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogIOChannelNodeStatusInfo(self._device._hdwf, channel_index, node_index, c_min_value, c_max_value, c_num_steps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            min_value = c_min_value.value
            max_value = c_max_value.value
            num_steps = c_num_steps.value
            return (min_value, max_value, num_steps)

        def channelNodeStatus(self, channel_index: int, node_index: int) -> float:
            """Returns the value reading of the node."""
            c_node_status = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogIOChannelNodeStatus(self._device._hdwf, channel_index, node_index, c_node_status)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            node_status = c_node_status.value
            return node_status

    class DigitalIOAPI:
        """Provides wrappers for the 'FDwfDigitalIO' API functions.

        Version 3.14.3 of the DWF library has 19 'FDwfDigitalIO' functions, none of which are obsolete.

        There are 3 generic functions (reset, configure, and status), and 8 functions that come in 32- and 64-bits variants.
        """

        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def reset(self) -> None:
            """Resets and configures (by default, having auto configure enabled) all DigitalIO instrument parameters to default values.

            It sets the output enables to zero (tri-state), output value to zero, and configures the DigitalIO instrument.
            """
            result = self._device._dwf._lib.FDwfDigitalIOReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def configure(self) -> None:
            """Configures the DigitalIO instrument. This doesn’t have to be used if AutoConfiguration is enabled."""
            result = self._device._dwf._lib.FDwfDigitalIOConfigure(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def status(self) -> None:
            """Reads the status and input values, of the device DigitalIO to the PC.

            The status and values are accessed from the FDwfDigitalIOInputStatus function.
            """
            result = self._device._dwf._lib.FDwfDigitalIOStatus(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def outputEnableInfo(self) -> int:
            """Returns the output enable mask (bit set) that can be used on this device.

            These are the pins that can be used as outputs on the device.
            """
            c_output_enable_mask = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalIOOutputEnableInfo(self._device._hdwf, c_output_enable_mask)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output_enable_mask = c_output_enable_mask.value
            return output_enable_mask

        def outputEnableSet(self, output_enable: int) -> None:
            """Enables specific pins for output.

            This is done by setting bits in the fsOutEnable bit field (1 for enabled, 0 for disabled).
            """
            result = self._device._dwf._lib.FDwfDigitalIOOutputEnableSet(self._device._hdwf, output_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def outputEnableGet(self) -> int:
            """Returns a bit field that specifies which output pins have been enabled."""
            c_output_enable = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalIOOutputEnableGet(self._device._hdwf, c_output_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output_enable = c_output_enable.value
            return output_enable

        def outputInfo(self) -> int:
            """Returns the settable output value mask (bit set) that can be used on this device."""
            c_output_mask = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalIOOutputInfo(self._device._hdwf, c_output_mask)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output_mask = c_output_mask.value
            return output_mask

        def outputSet(self, output: int) -> None:
            """Sets the output logic value on all output pins."""
            result = self._device._dwf._lib.FDwfDigitalIOOutputSet(self._device._hdwf, output)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def outputGet(self) -> int:
            """Returns the currently set output values across all output pins."""
            c_output = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalIOOutputGet(self._device._hdwf, c_output)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output = c_output.value
            return output

        def inputInfo(self) -> int:
            """Returns the readable input value mask (bit set) that can be used on the device."""
            c_input_mask = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalIOInputInfo(self._device._hdwf, c_input_mask)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            input_mask = c_input_mask.value
            return input_mask

        def inputStatus(self) -> int:
            """Returns the input states of all I/O pins.

            Before calling this method, call the `status` method to read the Digital I/O states from the device.
            """
            c_input = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalIOInputStatus(self._device._hdwf, c_input)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            input_ = c_input.value
            return input_

        def outputEnableInfo64(self) -> int:
            """Returns the output enable mask (bit set) that can be used on this device.

            These are the pins that can be used as outputs on the device.
            """
            c_output_enable_mask = _typespec_ctypes.c_unsigned_long_long()
            result = self._device._dwf._lib.FDwfDigitalIOOutputEnableInfo64(self._device._hdwf, c_output_enable_mask)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output_enable_mask = c_output_enable_mask.value
            return output_enable_mask

        def outputEnableSet64(self, output_enable: int) -> None:
            """Enables specific pins for output.

            This is done by setting bits in the fsOutEnable bit field (1 for enabled, 0 for disabled).
            """
            result = self._device._dwf._lib.FDwfDigitalIOOutputEnableSet64(self._device._hdwf, output_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def outputEnableGet64(self) -> int:
            """Returns a bit field that specifies which output pins have been enabled."""
            c_output_enable = _typespec_ctypes.c_unsigned_long_long()
            result = self._device._dwf._lib.FDwfDigitalIOOutputEnableGet64(self._device._hdwf, c_output_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output_enable = c_output_enable.value
            return output_enable

        def outputInfo64(self) -> int:
            """Returns the settable output value mask (bit set) that can be used on this device."""
            c_output_mask = _typespec_ctypes.c_unsigned_long_long()
            result = self._device._dwf._lib.FDwfDigitalIOOutputInfo64(self._device._hdwf, c_output_mask)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output_mask = c_output_mask.value
            return output_mask

        def outputSet64(self, output: int) -> None:
            """Sets the output logic value on all output pins."""
            result = self._device._dwf._lib.FDwfDigitalIOOutputSet64(self._device._hdwf, output)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def outputGet64(self) -> int:
            """Returns the currently set output values across all output pins."""
            c_output = _typespec_ctypes.c_unsigned_long_long()
            result = self._device._dwf._lib.FDwfDigitalIOOutputGet64(self._device._hdwf, c_output)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output = c_output.value
            return output

        def inputInfo64(self) -> int:
            """Returns the readable input value mask (bit set) that can be used on the device."""
            c_input_mask = _typespec_ctypes.c_unsigned_long_long()
            result = self._device._dwf._lib.FDwfDigitalIOInputInfo64(self._device._hdwf, c_input_mask)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            input_mask = c_input_mask.value
            return input_mask

        def inputStatus64(self) -> int:
            """Returns the input states of all I/O pins.

            Before calling this method, call the `status` method to read the Digital I/O states from the device.
            """
            c_input = _typespec_ctypes.c_unsigned_long_long()
            result = self._device._dwf._lib.FDwfDigitalIOInputStatus64(self._device._hdwf, c_input)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            input_ = c_input.value
            return input_

    class DigitalInAPI:
        """Provides wrappers for the 'FDwfDigitalIn' API functions.

        Version 3.14.3 of the DWF library has 55 'FDwfDigitalIn' functions, 2 of which (FDwfDigitalInMixedSet, FDwfDigitalInTriggerSourceInfo) are obsolete.
        """
        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def reset(self) -> None:
            """Resets and configures (by default, having auto configure enabled) all DigitalIn instrument parameters to default values."""
            result = self._device._dwf._lib.FDwfDigitalInReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def configure(self, reconfigure: bool, start: bool) -> None:
            result = self._device._dwf._lib.FDwfDigitalInConfigure(self._device._hdwf, reconfigure, start)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def status(self, readData: bool) -> DwfState:
            c_sts = _typespec_ctypes.DwfState()
            result = self._device._dwf._lib.FDwfDigitalInStatus(self._device._hdwf, readData, c_sts)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            sts = DwfState(c_sts.value)
            return sts

        def statusSamplesLeft(self) -> int:
            """Retrieve the number of samples left in the acquisition."""
            c_samplesLeft = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInStatusSamplesLeft(self._device._hdwf, c_samplesLeft)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            samplesLeft = c_samplesLeft.value
            return samplesLeft

        def statusSamplesValid(self) -> int:
            """Retrieve the number of valid/acquired data samples."""
            c_samplesValid = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInStatusSamplesValid(self._device._hdwf, c_samplesValid)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            samplesValid = c_samplesValid.value
            return samplesValid

        def statusIndexWrite(self) -> int:
            """Retrieve the buffer write pointer.

            This is needed in ScanScreen acquisition mode to display the scan bar.
            """
            c_idxWrite = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInStatusIndexWrite(self._device._hdwf, c_idxWrite)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            idxWrite = c_idxWrite.value
            return idxWrite

        def statusAutoTriggered(self) -> bool:
            """Verify if the acquisition is auto triggered."""
            c_auto = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInStatusAutoTriggered(self._device._hdwf, c_auto)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            auto = bool(c_auto.value)
            return auto

        def statusData(self, count_bytes: int) -> np.ndarray:
            """Retrieve the acquired data samples from the specified idxChannel on the DigitalIn instrument.
            It copies the data samples to the provided buffer.
            """
            samples = np.empty(count_bytes, dtype='B')
            result = self._device._dwf._lib.FDwfDigitalInStatusData(self._device._hdwf, samples.ctypes.data_as(_typespec_ctypes.c_unsigned_char_ptr), count_bytes)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            return samples

        def statusData2(self, first_sample: int, count_bytes: int) -> np.ndarray:
            """Retrieve the acquired data samples from the specified idxChannel on the DigitalIn instrument.
            """

            samples = np.empty(count_bytes, dtype='B')
            result = self._device._dwf._lib.FDwfDigitalInStatusData2(self._device._hdwf, samples.ctypes.data_as(_typespec_ctypes.c_unsigned_char_ptr), first_sample, count_bytes)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            return samples

        def statusNoise2(self, first_sample: int, count_bytes: int) -> np.ndarray:
            noise = np.empty(count_bytes, dtype='B')
            result = self._device._dwf._lib.FDwfDigitalInStatusNoise2(self._device._hdwf, noise.ctypes.data_as(_typespec_ctypes.c_unsigned_char_ptr), first_sample, count_bytes)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            return noise

        def statusRecord(self) -> Tuple[int, int, int]:

            c_data_available = _typespec_ctypes.c_int()
            c_data_lost = _typespec_ctypes.c_int()
            c_data_corrupt = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInStatusRecord(self._device._hdwf, c_data_available, c_data_lost, c_data_corrupt)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            data_free = c_data_available.value
            data_lost = c_data_lost.value
            data_corrupt = c_data_corrupt.value
            return (data_free, data_lost, data_corrupt)

        def statusTime(self) -> Tuple[int, int, int]:
            """Retrieve timestamp of status."""
            c_sec_utc = _typespec_ctypes.c_uint()
            c_tick = _typespec_ctypes.c_uint()
            c_ticks_per_second = _typespec_ctypes.c_uint()
            result = self._device._dwf._lib.FDwfAnalogInStatusTime(self._device._hdwf, c_sec_utc, c_tick, c_ticks_per_second)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            sec_utc = c_sec_utc.value
            tick = c_tick.value
            ticks_per_second = c_ticks_per_second.value
            return (sec_utc, tick, ticks_per_second)

        def internalClockInfo(self) -> float:
            c_hzFreq = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfDigitalInInternalClockInfo(self._device._hdwf, c_hzFreq)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            hzFreq = c_hzFreq.value
            return hzFreq

        def clockSourceInfo(self) -> List[DwfDigitalInClockSource]:
            """Get digital-in clock source info."""
            c_clock_source_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInClockSourceInfo(self._device._hdwf, c_clock_source_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            clock_source_bitset = c_clock_source_bitset.value
            clock_source_list = [clock_source for clock_source in DwfDigitalInClockSource if clock_source_bitset & (1 << clock_source.value)]
            return clock_source_list

        def clockSourceSet(self, clock_source: DwfDigitalInClockSource) -> None:
            result = self._device._dwf._lib.FDwfDigitalInClockSourceSet(self._device._hdwf, clock_source.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def clockSourceGet(self) -> DwfDigitalInClockSource:
            c_clock_source = _typespec_ctypes.DwfDigitalInClockSource()
            result = self._device._dwf._lib.FDwfDigitalInClockSourceGet(self._device._hdwf, c_clock_source)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            clock_source = DwfDigitalInClockSource(c_clock_source.value)
            return clock_source

        def dividerInfo(self) -> int:
            c_divMax = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalInDividerInfo(self._device._hdwf, c_divMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            divMax = c_divMax.value
            return divMax

        def dividerSet(self, div: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInDividerSet(self._device._hdwf, div)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def dividerGet(self) -> int:
            c_div = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalInDividerGet(self._device._hdwf, c_div)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            div = c_div.value
            return div

        def bitsInfo(self) -> int:
            c_nBits = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInBitsInfo(self._device._hdwf, c_nBits)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nBits = c_nBits.value
            return nBits

        def sampleFormatSet(self, nBits: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInSampleFormatSet(self._device._hdwf, nBits)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def sampleFormatGet(self) -> int:
            c_nBits = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInSampleFormatGet(self._device._hdwf, c_nBits)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nBits = c_nBits.value
            return nBits

        def inputOrderSet(self, dioFirst: bool) -> None:
            """Configures the order of values stored in the sampling array.

            If dioFirst is True, DIO 24..39 are placed at the beginning of the array followed by DIN 0..23.
            If dioFirst is False, DIN 0..23 are placed at the beginning followed by DIO 24..31.
            Valid only for Digital Discovery device.
            """
            result = self._device._dwf._lib.FDwfDigitalInInputOrderSet(self._device._hdwf, dioFirst)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def bufferSizeInfo(self) -> int:
            c_nSizeMax = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInBufferSizeInfo(self._device._hdwf, c_nSizeMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nSizeMax = c_nSizeMax.value
            return nSizeMax

        def bufferSizeSet(self, nSize: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInBufferSizeSet(self._device._hdwf, nSize)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def bufferSizeGet(self) -> int:
            c_nSize = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInBufferSizeGet(self._device._hdwf, c_nSize)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nSize = c_nSize.value
            return nSize

        def sampleModeInfo(self) -> List[DwfDigitalInSampleMode]:
            """Get digital-in sample mode info."""
            c_sample_mode_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInSampleModeInfo(self._device._hdwf, c_sample_mode_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            sample_mode_bitset = c_sample_mode_bitset.value
            sample_mode_list = [sample_mode for sample_mode in DwfDigitalInSampleMode if sample_mode_bitset & (1 << sample_mode.value)]
            return sample_mode_list

        def sampleModeSet(self, sample_mode: DwfDigitalInSampleMode) -> None:
            result = self._device._dwf._lib.FDwfDigitalInSampleModeSet(self._device._hdwf, sample_mode.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def sampleModeGet(self) -> DwfDigitalInSampleMode:
            c_sample_mode = _typespec_ctypes.DwfDigitalInSampleMode()
            result = self._device._dwf._lib.FDwfDigitalInSampleModeGet(self._device._hdwf, c_sample_mode)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            sample_mode = DwfDigitalInSampleMode(c_sample_mode.value)
            return sample_mode

        def sampleSensibleSet(self, compression_bits: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInSampleSensibleSet(self._device._hdwf, compression_bits)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def sampleSensibleGet(self) -> int:
            c_compression_bits = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalInSampleSensibleGet(self._device._hdwf, c_compression_bits)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            compression_bits = c_compression_bits.value
            return compression_bits

        def acquisitionModeInfo(self) -> List[ACQMODE]:
            """Get digital-in acquisition mode info."""
            c_acquisition_mode_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInAcquisitionModeInfo(self._device._hdwf, c_acquisition_mode_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            acquisiton_mode_bitset = c_acquisition_mode_bitset.value
            acquisition_mode_list = [acquisition_mode for acquisition_mode in ACQMODE if acquisiton_mode_bitset & (1 << acquisition_mode.value)]
            return acquisition_mode_list

        def acquisitionModeSet(self, acquisition_mode: ACQMODE) -> None:
            result = self._device._dwf._lib.FDwfDigitalInAcquisitionModeSet(self._device._hdwf, acquisition_mode.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def acquisitionModeGet(self) -> ACQMODE:
            c_acquisition_mode = _typespec_ctypes.ACQMODE()
            result = self._device._dwf._lib.FDwfDigitalInAcquisitionModeGet(self._device._hdwf, c_acquisition_mode)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            acquisition_mode = ACQMODE(c_acquisition_mode.value)
            return acquisition_mode

        # Trigger functions:

        def triggerSourceSet(self, trigger_source: TRIGSRC) -> None:
            result = self._device._dwf._lib.FDwfDigitalInTriggerSourceSet(self._device._hdwf, trigger_source.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerSourceGet(self) -> TRIGSRC:
            c_trigger_source = _typespec_ctypes.TRIGSRC()
            result = self._device._dwf._lib.FDwfDigitalInTriggerSourceGet(self._device._hdwf, c_trigger_source)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_source = TRIGSRC(c_trigger_source.value)
            return trigger_source

        def triggerSlopeSet(self, trigger_slope: DwfTriggerSlope) -> None:
            result = self._device._dwf._lib.FDwfDigitalInTriggerSlopeSet(self._device._hdwf, trigger_slope.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerSlopeGet(self) -> DwfTriggerSlope:
            c_trigger_slope = _typespec_ctypes.DwfTriggerSlope()
            result = self._device._dwf._lib.FDwfDigitalInTriggerSlopeGet(self._device._hdwf, c_trigger_slope)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_slope = DwfTriggerSlope(c_trigger_slope.value)
            return trigger_slope

        def triggerPositionInfo(self) -> int:
            c_max_samples_after_trigger = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalInTriggerPositionInfo(self._device._hdwf, c_max_samples_after_trigger)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            max_samples_after_trigger = c_max_samples_after_trigger.value
            return max_samples_after_trigger

        def triggerPositionSet(self, samples_after_trigger: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInTriggerPositionSet(self._device._hdwf, samples_after_trigger)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerPositionGet(self) -> int:
            c_samples_after_trigger = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalInTriggerPositionGet(self._device._hdwf, c_samples_after_trigger)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            samples_after_trigger = c_samples_after_trigger.value
            return samples_after_trigger

        def triggerPrefillSet(self, samples_before_trigger: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInTriggerPrefillSet(self._device._hdwf, samples_before_trigger)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerPrefillGet(self) -> int:
            c_samples_before_trigger = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalInTriggerPrefillGet(self._device._hdwf, c_samples_before_trigger)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            samples_before_trigger = c_samples_before_trigger.value
            return samples_before_trigger

        def triggerAutoTimeoutInfo(self) -> Tuple[float, float, float]:
            c_secMin = _typespec_ctypes.c_double()
            c_secMax = _typespec_ctypes.c_double()
            c_nSteps = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfDigitalInTriggerAutoTimeoutInfo(self._device._hdwf, c_secMin, c_secMax, c_nSteps)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secMin = c_secMin.value
            secMax = c_secMax.value
            nSteps = c_nSteps.value
            return (secMin, secMax, nSteps)

        def triggerAutoTimeoutSet(self, secTimout: float) -> None:
            result = self._device._dwf._lib.FDwfDigitalInTriggerAutoTimeoutSet(self._device._hdwf, secTimout)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerAutoTimeoutGet(self) -> float:
            c_secTimeout = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfDigitalInTriggerAutoTimeoutGet(self._device._hdwf, c_secTimeout)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secTimeout = c_secTimeout.value
            return secTimeout

        def triggerInfo(self) -> Tuple[int, int, int, int]:
            c_fsLevelLow  = _typespec_ctypes.c_unsigned_int()
            c_fsLevelHigh = _typespec_ctypes.c_unsigned_int()
            c_fsEdgeRise  = _typespec_ctypes.c_unsigned_int()
            c_fsEdgeFall  = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalInTriggerInfo(self._device._hdwf, c_fsLevelLow, c_fsLevelHigh, c_fsEdgeRise, c_fsEdgeFall)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            fsLevelLow  = c_fsLevelLow.value
            fsLevelHigh = c_fsLevelHigh.value
            fsEdgeRise  = c_fsEdgeRise.value
            fsEdgeFall  = c_fsEdgeFall.value
            return (fsLevelLow, fsLevelHigh, fsEdgeRise, fsEdgeFall)

        def triggerSet(self, fsLevelLow: int, fsLevelHigh: int, fsEdgeRise: int, fsEdgeFall: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInTriggerSet(self._device._hdwf, fsLevelLow, fsLevelHigh, fsEdgeRise, fsEdgeFall)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerGet(self) -> Tuple[int, int, int, int]:
            c_fsLevelLow  = _typespec_ctypes.c_unsigned_int()
            c_fsLevelHigh = _typespec_ctypes.c_unsigned_int()
            c_fsEdgeRise  = _typespec_ctypes.c_unsigned_int()
            c_fsEdgeFall  = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalInTriggerGet(self._device._hdwf, c_fsLevelLow, c_fsLevelHigh, c_fsEdgeRise, c_fsEdgeFall)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            fsLevelLow  = c_fsLevelLow.value
            fsLevelHigh = c_fsLevelHigh.value
            fsEdgeRise  = c_fsEdgeRise.value
            fsEdgeFall  = c_fsEdgeFall.value
            return (fsLevelLow, fsLevelHigh, fsEdgeRise, fsEdgeFall)

        def triggerResetSet(self, fsLevelLow: int, fsLevelHigh: int, fsEdgeRise: int, fsEdgeFall: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInTriggerResetSet(self._device._hdwf, fsLevelLow, fsLevelHigh, fsEdgeRise, fsEdgeFall)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerCountSet(self, count: int, restart: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInTriggerCountSet(self._device._hdwf, count, restart)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerLengthSet(self, secMin: float, secMax: float, idxSync: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInTriggerLengthSet(self._device._hdwf, secMin, secMax, idxSync)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerMatchSet(self, pin: int, mask: int, value: int, bitstuffing: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalInTriggerMatchSet(self._device._hdwf, pin, mask, value, bitstuffing)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        # Obsolete functions:

        def mixedSet(self, enable: bool) -> None:
            result = self._device._dwf._lib.FDwfDigitalInMixedSet(self._device._hdwf, enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerSourceInfo(self) -> List[TRIGSRC]:
            """Get digital-in trigger source info.

            Note: This function is OBSOLETE. Use the generic `DeviceAPI.triggerInfo()` method instead.
            """
            c_trigger_source_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalInTriggerSourceInfo(self._device._hdwf, c_trigger_source_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_source_bitset = c_trigger_source_bitset.value
            trigger_source_list = [trigger_source for trigger_source in TRIGSRC if trigger_source_bitset & (1 << trigger_source.value)]
            return trigger_source_list


    class DigitalOutAPI:
        """Provides wrappers for the 'FDwfDigitalOut' API functions.

        Version 3.14.3 of the DWF library has 48 'FDwfDigitalOut' functions, 1 of which (FDwfDigitalOutTriggerSourceInfo) is obsolete.
        """
        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def reset(self) -> None:
            """Resets the digital-out instrument."""
            result = self._device._dwf._lib.FDwfDigitalOutReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def configure(self, start: bool) -> None:
            """Starts or stops the digital-out instrument."""
            result = self._device._dwf._lib.FDwfDigitalOutConfigure(self._device._hdwf, start)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def status(self) -> DwfState:
            """Returns the status of the digital-out instrument."""
            c_status = _typespec_ctypes.DwfState()
            result = self._device._dwf._lib.FDwfDigitalOutStatus(self._device._hdwf, c_status)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            status_ = DwfState(c_status.value)
            return status_

        def internalClockInfo(self) -> float:
            """Gets digital-out clock frequency.

            :returns: The digital-out clock frequency, in Hz.
            """
            c_frequency_hz = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfDigitalOutInternalClockInfo(self._device._hdwf, c_frequency_hz)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            frequency_hz = c_frequency_hz.value
            return frequency_hz

        def triggerSourceSet(self, trigger_source: TRIGSRC) -> None:
            """Sets the trigger source."""
            result = self._device._dwf._lib.FDwfDigitalOutTriggerSourceSet(self._device._hdwf, trigger_source.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerSourceGet(self) -> TRIGSRC:
            """Gets the currently active trigger source."""
            c_trigger_source = _typespec_ctypes.TRIGSRC()
            result = self._device._dwf._lib.FDwfDigitalOutTriggerSourceGet(self._device._hdwf, c_trigger_source)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_source = TRIGSRC(c_trigger_source.value)
            return trigger_source

        def runInfo(self) -> Tuple[float, float]:
            """Gets minimal and maximal duration for a single digital-out pulse sequence run.

            :returns: A tuple containing the minimal and maximal digital-out run-time, in seconds.
            """
            c_secMin = _typespec_ctypes.c_double()
            c_secMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfDigitalOutRunInfo(self._device._hdwf, c_secMin, c_secMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secMin = c_secMin.value
            secMax = c_secMax.value
            return (secMin, secMax)

        def runSet(self, secRun: float) -> None:
            """Sets duration for a single digital-out pulse-sequence run.

            :param secRun: Digital-out runtime, in seconds. The value 0 means: run forever.
            """
            result = self._device._dwf._lib.FDwfDigitalOutRunSet(self._device._hdwf, secRun)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def runGet(self) -> float:
            """Gets duration for a single digital-out pulse-sequence run.

            :returns: digital out run-time, in seconds.
            """
            c_secRun = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfDigitalOutRunGet(self._device._hdwf, c_secRun)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secRun = c_secRun.value
            return secRun

        def runStatus(self) -> float:
            """Gets run-time for the currently active digital-out pulse-sequence run."""
            c_secRun = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfDigitalOutRunStatus(self._device._hdwf, c_secRun)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secRun = c_secRun.value
            return secRun

        def waitInfo(self) -> Tuple[float, float]:
            """Gets minimal and maximal wait-time between consecutive digital-out pulse-sequence runs.

            :returns: A tuple containing the minimal and maximal wait time duration between consecutive digital-out pulse-sequence runs, in seconds.
            """
            c_secMin = _typespec_ctypes.c_double()
            c_secMax = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfDigitalOutWaitInfo(self._device._hdwf, c_secMin, c_secMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secMin = c_secMin.value
            secMax = c_secMax.value
            return (secMin, secMax)

        def waitSet(self, secWait: float) -> None:
            """Sets wait-time between consecutive digital-out pulse-sequence runs.

            :param secRun: Digital-out wait-time, in seconds.
            """
            result = self._device._dwf._lib.FDwfDigitalOutWaitSet(self._device._hdwf, secWait)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def waitGet(self) -> float:
            """Gets wait-time between consecutive digital-out pulse-sequence runs.

            :returns: digital out wait-time, in seconds.
            """
            c_secWait = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfDigitalOutWaitGet(self._device._hdwf, c_secWait)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            secWait = c_secWait.value
            return secWait

        def repeatInfo(self) -> Tuple[int, int]:
            """Gets minimal and maximal repeat count for digital-out pulse-sequence runs.

            :returns: A tuple containing the minimal and maximal repeat count for digital-out pulse-sequence runs.
            """
            c_nMin = _typespec_ctypes.c_unsigned_int()
            c_nMax = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalOutRepeatInfo(self._device._hdwf, c_nMin, c_nMax)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            nMin = c_nMin.value
            nMax = c_nMax.value
            return (nMin, nMax)

        def repeatSet(self, repeat: int) -> None:
            """Sets repeat count for digital-out pulse-sequence runs.

            :param repeat: Repeat count. Specify 0 to repeat forever.
            """
            result = self._device._dwf._lib.FDwfDigitalOutRepeatSet(self._device._hdwf, repeat)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def repeatGet(self) -> int:
            """Sets repeat count for digital-out pulse-sequence runs.

            :returns: Repeat count. 0 means: run forever.
            """
            c_repeat = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalOutRepeatGet(self._device._hdwf, c_repeat)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            repeat = c_repeat.value
            return repeat

        def repeatStatus(self) -> int:
            """Gets repeat status for the currently active digital-out train of pulse-sequence runs."""
            c_repeat_status = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalOutRepeatStatus(self._device._hdwf, c_repeat_status)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            repeat_status = c_repeat_status.value
            return repeat_status

        def triggerSlopeSet(self, trigger_slope: DwfTriggerSlope) -> None:
            """Sets the slope for the digital-out trigger."""
            result = self._device._dwf._lib.FDwfDigitalOutTriggerSlopeSet(self._device._hdwf, trigger_slope.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerSlopeGet(self) -> DwfTriggerSlope:
            """Gets the slope for the digital-out trigger."""
            c_trigger_slope = _typespec_ctypes.DwfTriggerSlope()
            result = self._device._dwf._lib.FDwfDigitalOutTriggerSlopeGet(self._device._hdwf, c_trigger_slope)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_slope = DwfTriggerSlope(c_trigger_slope.value)
            return trigger_slope

        def repeatTriggerSet(self, repeatTrigger: bool) -> None:
            """Specify if each pulse sequence run should wait for its own trigger."""
            result = self._device._dwf._lib.FDwfDigitalOutRepeatTriggerSet(self._device._hdwf, repeatTrigger)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def repeatTriggerGet(self) -> bool:
            """Get if each pulse sequence run should wait for its own trigger."""
            c_repeatTrigger = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalOutRepeatTriggerGet(self._device._hdwf, c_repeatTrigger)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            repeatTrigger = bool(c_repeatTrigger.value)
            return repeatTrigger

        def count(self) -> int:
            """Get digital-out channel count."""
            c_channel_count = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalOutCount(self._device._hdwf, c_channel_count)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            channel_count = c_channel_count.value
            return channel_count

        def enableSet(self, idxChannel: int, enable: bool) -> None:
            """Enables or disables a digital-out channel."""
            result = self._device._dwf._lib.FDwfDigitalOutEnableSet(self._device._hdwf, idxChannel, enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def enableGet(self, idxChannel: int) -> bool:
            """Checks if a specific digital-out channel is enabled."""
            c_enable = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalOutEnableGet(self._device._hdwf, idxChannel, c_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            enable = bool(c_enable.value)
            return enable

        def outputInfo(self, idxChannel: int) -> List[DwfDigitalOutOutput]:
            c_output_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalOutOutputInfo(self._device._hdwf, idxChannel, c_output_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output_bitset = c_output_bitset.value
            output_list = [output for output in DwfDigitalOutOutput if output_bitset & (1 << output.value)]
            return output_list

        def outputSet(self, idxChannel: int, output_value: DwfDigitalOutOutput) -> None:
            result = self._device._dwf._lib.FDwfDigitalOutOutputSet(self._device._hdwf, idxChannel, output_value.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def outputGet(self, idxChannel: int) -> DwfDigitalOutOutput:
            c_output_value = _typespec_ctypes.DwfDigitalOutOutput()
            result = self._device._dwf._lib.FDwfDigitalOutOutputGet(self._device._hdwf, idxChannel, c_output_value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output_value = DwfDigitalOutOutput(c_output_value.value)
            return output_value

        def typeInfo(self, idxChannel: int) -> List[DwfDigitalOutType]:
            c_type_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalOutTypeInfo(self._device._hdwf, idxChannel, c_type_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            type_bitset = c_type_bitset.value
            type_list = [type_ for type_ in DwfDigitalOutType if type_bitset & (1 << type_.value)]
            return type_list

        def typeSet(self, idxChannel: int, output_type: DwfDigitalOutType) -> None:
            result = self._device._dwf._lib.FDwfDigitalOutTypeSet(self._device._hdwf, idxChannel, output_type.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def typeGet(self, idxChannel: int) -> DwfDigitalOutType:
            c_output_type = _typespec_ctypes.DwfDigitalOutType()
            result = self._device._dwf._lib.FDwfDigitalOutTypeGet(self._device._hdwf, idxChannel, c_output_type)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            output_type = DwfDigitalOutType(c_output_type.value)
            return output_type

        def idleInfo(self, idxChannel: int) -> List[DwfDigitalOutIdle]:
            c_idle_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalOutIdleInfo(self._device._hdwf, idxChannel, c_idle_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            idle_bitset = c_idle_bitset.value
            idle_list = [idle for idle in DwfDigitalOutIdle if idle_bitset & (1 << idle.value)]
            return idle_list

        def idleSet(self, idxChannel: int, idle_mode: DwfDigitalOutIdle) -> None:
            result = self._device._dwf._lib.FDwfDigitalOutIdleSet(self._device._hdwf, idxChannel, idle_mode.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def idleGet(self, idxChannel: int) -> DwfDigitalOutIdle:
            c_idle_mode = _typespec_ctypes.DwfDigitalOutIdle()
            result = self._device._dwf._lib.FDwfDigitalOutIdleGet(self._device._hdwf, idxChannel, c_idle_mode)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            idle_mode = DwfDigitalOutIdle(c_idle_mode.value)
            return idle_mode

        def dividerInfo(self, idxChannel: int) -> Tuple[int, int]:
            c_divider_init_min = _typespec_ctypes.c_unsigned_int()
            c_divider_init_max = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalOutDividerInfo(self._device._hdwf, idxChannel, c_divider_init_min, c_divider_init_max)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            divider_init_min = c_divider_init_min.value
            divider_init_max = c_divider_init_max.value
            return (divider_init_min, divider_init_max)

        def dividerInitSet(self, idxChannel: int, divider_init: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalOutDividerInitSet(self._device._hdwf, idxChannel, divider_init)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def dividerInitGet(self, idxChannel: int) -> int:
            c_divider_init = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalOutDividerInitGet(self._device._hdwf, idxChannel, c_divider_init)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            divider_init = c_divider_init.value
            return divider_init

        def dividerSet(self, idxChannel: int, divider: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalOutDividerSet(self._device._hdwf, idxChannel, divider)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def dividerGet(self, idxChannel: int) -> int:
            c_divider = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalOutDividerGet(self._device._hdwf, idxChannel, c_divider)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            divider = c_divider.value
            return divider

        def counterInfo(self, idxChannel: int) -> Tuple[int, int]:
            c_counter_min = _typespec_ctypes.c_unsigned_int()
            c_counter_max = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalOutCounterInfo(self._device._hdwf, idxChannel, c_counter_min, c_counter_max)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            counter_min = c_counter_min.value
            counter_max = c_counter_max.value
            return (counter_min, counter_max)

        def counterInitSet(self, idxChannel: int, high: bool, counter_init: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalOutCounterInitSet(self._device._hdwf, idxChannel, high, counter_init)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def counterInitGet(self, idxChannel: int) -> Tuple[int, int]:
            c_high = _typespec_ctypes.c_int()
            c_counter_init = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalOutCounterInitGet(self._device._hdwf, idxChannel, c_high, c_counter_init)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            high = c_high.value
            counter_init = c_counter_init.value
            return (high, counter_init)

        def counterSet(self, idxChannel: int, low_count: int, high_count: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalOutCounterSet(self._device._hdwf, idxChannel, low_count, high_count)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def counterGet(self, idxChannel: int) -> Tuple[int, int]:
            c_low_count = _typespec_ctypes.c_unsigned_int()
            c_high_count = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalOutCounterGet(self._device._hdwf, idxChannel, c_low_count, c_high_count)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            low_count = c_low_count.value
            high_count = c_high_count.value
            return (low_count, high_count)

        def dataInfo(self, idxChannel: int) -> int:
            """Return the maximum buffer size, the number of custom data bits."""
            c_max_databits = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalOutDataInfo(self._device._hdwf, idxChannel, c_max_databits)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            max_databits = c_max_databits.value
            return max_databits

        def dataSet(self, idxChannel: int, bits: str, tristate: bool=False) -> None:
            """Set digital-out arbitrary channel data."""

            if tristate:
                bits = bits.replace('1', '11').replace('0', '01').replace('Z', '00')

            countOfBits = len(bits)

            octets = []
            while len(bits) > 0:
                octet_str = bits[:8]
                octet = int(octet_str[::-1], 2)
                octets.append(octet)
                bits = bits[8:]

            octets_as_bytes = bytes(octets)

            result = self._device._dwf._lib.FDwfDigitalOutDataSet(self._device._hdwf, idxChannel, octets_as_bytes, countOfBits)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def playDataSet(self, rg_bits: int, bits_per_sample: int, count_of_samples: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalOutPlayDataSet(self._device._hdwf, rg_bits, bits_per_sample, count_of_samples)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def playRateSet(self, rate_hz: float) -> None:
            result = self._device._dwf._lib.FDwfDigitalOutPlayRateSet(self._device._hdwf, rate_hz)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def triggerSourceInfo(self) -> List[TRIGSRC]:
            """Get digital-out trigger source info.

            Note: This function is OBSOLETE. Use the generic DeviceAPI.triggerInfo() method instead.
            """
            c_trigger_source_bitset = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalOutTriggerSourceInfo(self._device._hdwf, c_trigger_source_bitset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            trigger_source_bitset = c_trigger_source_bitset.value
            trigger_source_list = [trigger_source for trigger_source in TRIGSRC if trigger_source_bitset & (1 << trigger_source.value)]
            return trigger_source_list

    class DigitalUartAPI:
        """Provides wrappers for the 'FDwfDigitalUart' API functions.

        Version 3.14.3 of the DWF library has 9 'FDwfDigitalUart' functions, none of which are obsolete.
        """
        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def reset(self) -> None:
            """Resets the digital-UART protocol instrument."""
            result = self._device._dwf._lib.FDwfDigitalUartReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def rateSet(self, hz: float) -> None:
            result = self._device._dwf._lib.FDwfDigitalUartRateSet(self._device._hdwf, hz)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def bitsSet(self, bits: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalUartBitsSet(self._device._hdwf, bits)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def paritySet(self, parity: int) -> None:
            # :param parity: 0 none, 1 odd, 2 even
            result = self._device._dwf._lib.FDwfDigitalUartParitySet(self._device._hdwf, parity)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def stopSet(self, stopbits: float) -> None:
            result = self._device._dwf._lib.FDwfDigitalUartStopSet(self._device._hdwf, stopbits)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def txSet(self, channel_index: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalUartTxSet(self._device._hdwf, channel_index)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def rxSet(self, channel_index: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalUartRxSet(self._device._hdwf, channel_index)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def tx(self, tx_data: bytes) -> None:
            result = self._device._dwf._lib.FDwfDigitalUartTx(self._device._hdwf, tx_data, len(tx_data))
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def rx(self, rx_max: int) -> Tuple[bytes, int]:
            """If rx_max is 0, initialize reception. Else, receive characters."""
            c_rx_count = _typespec_ctypes.c_int()
            c_parity_error = _typespec_ctypes.c_int()
            c_rx_buffer = ctypes.create_string_buffer(rx_max)
            result = self._device._dwf._lib.FDwfDigitalUartRx(self._device._hdwf, c_rx_buffer, rx_max, c_rx_count, c_parity_error)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            rx_count = c_rx_count.value
            rx_buffer = c_rx_buffer.value[:rx_count]
            parity_error = c_parity_error.value
            return (rx_buffer, parity_error)

    class DigitalSpiAPI:
        """Provides wrappers for the 'FDwfDigitalSpi' API functions.

        Version 3.14.3 of the DWF library has 18 'FDwfDigitalSpi' functions, none of which are obsolete.
        """
        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def reset(self) -> None:
            """Resets the digital-SPI protocol instrument."""
            result = self._device._dwf._lib.FDwfDigitalSpiReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def frequencySet(self, frequency: float) -> None:
            result = self._device._dwf._lib.FDwfDigitalSpiFrequencySet(self._device._hdwf, frequency)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def clockSet(self, channel_index: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalSpiClockSet(self._device._hdwf, channel_index)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def dataSet(self, data_select: int, channel_index: int) -> None:
            """Pick a hardware pin (channel_index) for an SPI function (data_select).

            data_select:
                0 = DQ0 / MOSI
                1 = DQ1 / MISO
                2 = DQ2
                3 = DQ3
            """
            result = self._device._dwf._lib.FDwfDigitalSpiDataSet(self._device._hdwf, data_select, channel_index)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def idleSet(self, idx_dq: int, idle_mode: DwfDigitalOutIdle) -> None:
            """Set idle behavior."""
            result = self._device._dwf._lib.FDwfDigitalSpiIdleSet(self._device._hdwf, idx_dq, idle_mode.value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def modeSet(self, spi_mode: int) -> None:
            """
            mode:
                0 = { CPOL = 0, CPHA = 0 }
                1 = { CPOL = 0, CPHA = 1 }
                2 = { CPOL = 1, CPHA = 0 }
                3 = { CPOL = 1, CPHA = 1 }
            """
            result = self._device._dwf._lib.FDwfDigitalSpiModeSet(self._device._hdwf, spi_mode)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def orderSet(self, bit_order: int) -> None:
            # bit order: 1 MSB first, 0 LSB first
            # TODO: check if the same as in the doc PDF
            result = self._device._dwf._lib.FDwfDigitalSpiOrderSet(self._device._hdwf, bit_order)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def select(self, channel_index: int, level: int) -> None:
            # 0 low, 1 high, -1 Z
            result = self._device._dwf._lib.FDwfDigitalSpiSelect(self._device._hdwf, channel_index, level)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def writeRead(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> List[int]:
            """Write and read, up to 8 bits per SPI word."""
            # transfer_type 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word

            tx_list = list(tx)

            number_of_words = len(tx_list)

            buffer_type = _typespec_ctypes.c_unsigned_char * number_of_words

            tx_buffer = buffer_type(*tx_list)
            rx_buffer = buffer_type()

            result = self._device._dwf._lib.FDwfDigitalSpiWriteRead(self._device._hdwf, transfer_type, bits_per_word, tx_buffer, number_of_words, rx_buffer, number_of_words)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            rx_list = list(rx_buffer)

            return rx_list

        def writeRead16(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> List[int]:
            """Write, then read, up to 16 bits per SPI word."""
            # cDQ 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word

            tx_list = list(tx)

            number_of_words = len(tx_list)

            buffer_type = _typespec_ctypes.c_unsigned_short * number_of_words

            tx_buffer = buffer_type(*tx_list)
            rx_buffer = buffer_type()

            result = self._device._dwf._lib.FDwfDigitalSpiWriteRead16(self._device._hdwf, transfer_type, bits_per_word, tx_buffer, number_of_words, rx_buffer, number_of_words)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            rx_list = list(rx_buffer)

            return rx_list

        def writeRead32(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> List[int]:
            """Write, then read, up to 32 bits per SPI word."""
            # cDQ 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word

            tx_list = list(tx)

            number_of_words = len(tx_list)

            buffer_type = _typespec_ctypes.c_unsigned_int * number_of_words

            tx_buffer = buffer_type(*tx_list)
            rx_buffer = buffer_type()

            result = self._device._dwf._lib.FDwfDigitalSpiWriteRead32(self._device._hdwf, transfer_type, bits_per_word, tx_buffer, number_of_words, rx_buffer, number_of_words)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            rx_list = list(rx_buffer)

            return rx_list

        def read(self, transfer_type: int, bits_per_word: int, number_of_words: int) -> List[int]:
            # cDQ 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word

            buffer_type = _typespec_ctypes.c_unsigned_char * number_of_words

            rx_buffer = buffer_type()

            result = self._device._dwf._lib.FDwfDigitalSpiRead(self._device._hdwf, transfer_type, bits_per_word, rx_buffer, number_of_words)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            rx_list = list(rx_buffer)

            return rx_list

        def readOne(self, dq: int, bits_per_word: int) -> int:
            # cDQ 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word
            c_rx = _typespec_ctypes.c_unsigned_int()
            result = self._device._dwf._lib.FDwfDigitalSpiReadOne(self._device._hdwf, dq, bits_per_word, c_rx)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            rx = c_rx.value
            return rx

        def read16(self, transfer_type: int, bits_per_word: int, number_of_words: int) -> List[int]:
            # cDQ 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word

            buffer_type = _typespec_ctypes.c_unsigned_short * number_of_words

            rx_buffer = buffer_type()

            result = self._device._dwf._lib.FDwfDigitalSpiRead16(self._device._hdwf, transfer_type, bits_per_word, rx_buffer, number_of_words)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            rx_list = list(rx_buffer)

            return rx_list

        def read32(self, transfer_type: int, bits_per_word: int, number_of_words: int) -> List[int]:
            # cDQ 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word

            buffer_type = _typespec_ctypes.c_unsigned_int * number_of_words

            rx_buffer = buffer_type()

            result = self._device._dwf._lib.FDwfDigitalSpiRead32(self._device._hdwf, transfer_type, bits_per_word, rx_buffer, number_of_words)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            rx_list = list(rx_buffer)

            return rx_list

        def write(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> None:
            """Write up to 8 bits per SPI word."""
            # transfer_type 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word

            tx_list = list(tx)

            number_of_words = len(tx_list)

            buffer_type = _typespec_ctypes.c_unsigned_char * number_of_words

            tx_buffer = buffer_type(*tx_list)

            result = self._device._dwf._lib.FDwfDigitalSpiWrite(self._device._hdwf, transfer_type, bits_per_word, tx_buffer, number_of_words)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def writeOne(self, transfer_type: int, bits_per_word: int, tx: int) -> None:
            """Write up to 8 bits per SPI word."""
            # transfer_type 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word

            result = self._device._dwf._lib.FDwfDigitalSpiWriteOne(self._device._hdwf, transfer_type, bits_per_word, tx)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def write16(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> None:
            """Write up to 16 bits per SPI word."""
            # transfer_type 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word

            tx_list = list(tx)

            number_of_words = len(tx_list)

            buffer_type = _typespec_ctypes.c_unsigned_short * number_of_words

            tx_buffer = buffer_type(*tx_list)

            result = self._device._dwf._lib.FDwfDigitalSpiWrite16(self._device._hdwf, transfer_type, bits_per_word, tx_buffer, number_of_words)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def write32(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> None:
            """Write up to 16 bits per SPI word."""
            # transfer_type 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad, // 1-32 bits / word

            tx_list = list(tx)

            number_of_words = len(tx_list)

            buffer_type = _typespec_ctypes.c_unsigned_int * number_of_words

            tx_buffer = buffer_type(*tx_list)

            result = self._device._dwf._lib.FDwfDigitalSpiWrite32(self._device._hdwf, transfer_type, bits_per_word, tx_buffer, number_of_words)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

    class DigitalI2cAPI:
        """Provides wrappers for the 'FDwfDigitalI2c' API functions.

        Version 3.14.3 of the DWF library has 11 'FDwfDigitalI2c' functions, none of which are obsolete.
        """
        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def reset(self) -> None:
            """Resets the digital-I2C protocol instrument."""
            result = self._device._dwf._lib.FDwfDigitalI2cReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def clear(self) -> int:
            c_bus_free = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfDigitalI2cClear(self._device._hdwf, c_bus_free)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            bus_free = c_bus_free.value
            return bus_free

        def stretchSet(self, stretch_enable: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalI2cStretchSet(self._device._hdwf, stretch_enable)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def rateSet(self, rate: float) -> None:
            result = self._device._dwf._lib.FDwfDigitalI2cRateSet(self._device._hdwf, rate)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def readNakSet(self, nak_last_read_byte: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalI2cReadNakSet(self._device._hdwf, nak_last_read_byte)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def sclSet(self, channel_index: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalI2cSclSet(self._device._hdwf, channel_index)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def sdaSet(self, channel_index: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalI2cSdaSet(self._device._hdwf, channel_index)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def writeRead(self, address: int, tx: List[int], number_of_rx_bytes: int) -> None:

            c_nak = _typespec_ctypes.c_int()

            tx_list = list(tx)

            number_of_tx_bytes = len(tx_list)

            tx_buffer_type = _typespec_ctypes.c_unsigned_char * number_of_tx_bytes
            rx_buffer_type = _typespec_ctypes.c_unsigned_char * number_of_rx_bytes

            tx_buffer = tx_buffer_type(*tx_list)
            rx_buffer = rx_buffer_type()

            result = self._device._dwf._lib.FDwfDigitalI2cWriteRead(self._device._hdwf, address, tx_buffer, number_of_tx_bytes, rx_buffer, number_of_rx_bytes, c_nak)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            nak = c_nak.value

            rx_list = list(rx_buffer)

            return (nak, rx_list)

        def read(self, address: int, number_of_words: int) -> Tuple[int, List[int]]:

            c_nak = _typespec_ctypes.c_int()

            buffer_type = _typespec_ctypes.c_unsigned_char * number_of_words

            rx_buffer = buffer_type()

            result = self._device._dwf._lib.FDwfDigitalI2cRead(self._device._hdwf, address, rx_buffer, number_of_words, c_nak)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            nak = c_nak.value

            rx_list = list(rx_buffer)

            return (nak, rx_list)

        def write(self, address: int, tx: List[int]) -> int:

            c_nak = _typespec_ctypes.c_int()

            tx_list = list(tx)

            number_of_words = len(tx_list)

            buffer_type = _typespec_ctypes.c_unsigned_char * number_of_words

            tx_buffer = buffer_type(*tx_list)

            result = self._device._dwf._lib.FDwfDigitalI2cWrite(self._device._hdwf, address, tx_buffer, number_of_words, c_nak)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            nak = c_nak.value

            return nak

        def writeOne(self, address: int, tx: int) -> None:

            c_nak = _typespec_ctypes.c_int()

            result = self._device._dwf._lib.FDwfDigitalI2cWriteOne(self._device._hdwf, address, tx, c_nak)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            nak = c_nak.value

            return nak


    class DigitalCanAPI:
        """Provides wrappers for the 'FDwfDigitalCan' API functions.

        Version 3.14.3 of the DWF library has 7 'FDwfDigitalCan' functions, none of which are obsolete.
        """
        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def reset(self) -> None:
            """Resets the digital-CAN protocol instrument."""
            result = self._device._dwf._lib.FDwfDigitalCanReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def rateSet(self, rate_hz: float) -> None:
            result = self._device._dwf._lib.FDwfDigitalCanRateSet(self._device._hdwf, rate_hz)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def polaritySet(self, high: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalCanPolaritySet(self._device._hdwf, high)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def txSet(self, channel_index: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalCanTxSet(self._device._hdwf, channel_index)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def rxSet(self, channel_index: int) -> None:
            result = self._device._dwf._lib.FDwfDigitalCanRxSet(self._device._hdwf, channel_index)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def tx(self, vID: int, extended: bool, remote: bool, data: bytes) -> None:
            if len(data) > 8:
                raise RuntimeError("CAN message too long.")
            result = self._device._dwf._lib.FDwfDigitalCanTx(self._device._hdwf, vID, extended, remote, len(data), ctypes.cast(data, _typespec_ctypes.c_unsigned_char_ptr))
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def rx(self, size:int=8) -> Tuple[int, bool, bool, bytes, int]:
            """Returns a tuple (vID, extended, remote, data, status)
            """
            # DWFAPI BOOL FDwfDigitalCanRx(HDWF hdwf, int *pvID, int *pfExtended, int *pfRemote, int *pcDLC, unsigned char *rgRX, int cRX, int *pvStatus);

            c_vID      = _typespec_ctypes.c_int()
            c_extended = _typespec_ctypes.c_int()
            c_remote   = _typespec_ctypes.c_int()
            c_dlc      = _typespec_ctypes.c_int()
            c_data     = ctypes.create_string_buffer(size)
            c_status   = _typespec_ctypes.c_int()

            result = self._device._dwf._lib.FDwfDigitalCanRx(self._device._hdwf, c_vID, c_extended, c_remote, c_dlc, ctypes.cast(c_data, _typespec_ctypes.c_unsigned_char_ptr), size, c_status)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

            vID      = c_vID.value
            extended = bool(c_extended.value)
            remote   = bool(c_remote.value)
            dlc      = c_dlc.value
            data     = c_data.value[:dlc]
            status   = c_status.value

            return (vID, extended, remote, data, status)

    class AnalogImpedanceAPI:
        """Provides wrappers for the 'FDwfAnalogImpedance' API functions.

        Version 3.14.3 of the DWF library has 22 'FDwfAnalogImpedance' functions, none of which are obsolete.
        """
        def __init__(self, device: 'DigilentWaveformDevice') -> None:
            self._device = device

        def reset(self) -> None:
            """Resets the Analog Impedance measurement instrument."""
            result = self._device._dwf._lib.FDwfAnalogImpedanceReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def modeSet(self, mode: int) -> None:
            """0 W1-C1-DUT-C2-R-GND, 1 W1-C1-R-C2-DUT-GND, 8 Impedance Analyzer for AD"""
            result = self._device._dwf._lib.FDwfAnalogImpedanceModeSet(self._device._hdwf, mode)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def modeGet(self) -> int:
            c_mode = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogImpedanceModeGet(self._device._hdwf, c_mode)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            mode = c_mode.value
            return mode

        def referenceSet(self, ohms: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogImpedanceReferenceSet(self._device._hdwf, ohms)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def referenceGet(self) -> float:
            c_ohms = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogImpedanceReferenceGet(self._device._hdwf, c_ohms)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            ohms = c_ohms.value
            return ohms

        def frequencySet(self, hz: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogImpedanceFrequencySet(self._device._hdwf, hz)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def frequencyGet(self) -> float:
            c_frequency = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogImpedanceFrequencyGet(self._device._hdwf, c_frequency)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            frequency = c_frequency.value
            return frequency

        def amplitudeSet(self, volts: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogImpedanceAmplitudeSet(self._device._hdwf, volts)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def amplitudeGet(self) -> float:
            c_amplitude = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogImpedanceAmplitudeGet(self._device._hdwf, c_amplitude)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            amplitude = c_amplitude.value
            return amplitude

        def offsetSet(self, volts: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogImpedanceOffsetSet(self._device._hdwf, volts)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def offsetGet(self) -> float:
            c_offset = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogImpedanceOffsetGet(self._device._hdwf, c_offset)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            offset = c_offset.value
            return offset

        def probeSet(self, ohmRes: float, faradCap: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogImpedanceProbeSet(self._device._hdwf, ohmRes, faradCap)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def probeGet(self) -> Tuple[float, float]:
            c_ohmRes = _typespec_ctypes.c_double()
            c_faradCap = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogImpedanceProbeGet(self._device._hdwf, c_ohmRes, c_faradCap)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            ohmRes = c_ohmRes.value
            faradCap = c_faradCap.value
            return (ohmRes, faradCap)

        def periodSet(self, period: int) -> None:
            result = self._device._dwf._lib.FDwfAnalogImpedancePeriodSet(self._device._hdwf, period)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def periodGet(self) -> int:
            c_period = _typespec_ctypes.c_int()
            result = self._device._dwf._lib.FDwfAnalogImpedancePeriodGet(self._device._hdwf, c_period)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            period = c_period.value
            return period

        def compReset(self) -> None:
            """Resets the Analog Impedance instrument."""
            result = self._device._dwf._lib.FDwfAnalogImpedanceCompReset(self._device._hdwf)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def compSet(self, ohmOpenResistance: float, ohmOpenReactance: float, ohmShortResistance: float, ohmShortReactance: float) -> None:
            result = self._device._dwf._lib.FDwfAnalogImpedanceCompSet(self._device._hdwf, ohmOpenResistance, ohmOpenReactance, ohmShortResistance, ohmShortReactance)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def compGet(self) -> Tuple[float, float, float, float]:
            c_ohmOpenResistance = _typespec_ctypes.c_double()
            c_ohmOpenReactance = _typespec_ctypes.c_double()
            c_ohmShortResistance = _typespec_ctypes.c_double()
            c_ohmShortReactance = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogImpedanceCompGet(self._device._hdwf, c_ohmOpenResistance, c_ohmOpenReactance, c_ohmShortResistance, c_ohmShortReactance)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            ohmOpenResistance = c_ohmOpenResistance.value
            ohmOpenReactance = c_ohmOpenReactance.value
            ohmShortResistance = c_ohmShortResistance.value
            ohmShortReactance =c_ohmShortReactance.value
            return (ohmOpenResistance, ohmOpenReactance, ohmShortResistance, ohmShortReactance)

        def configure(self, start: int) -> None:
            result = self._device._dwf._lib.FDwfAnalogImpedanceConfigure(self._device._hdwf, start)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()

        def status(self) -> DwfState:
            """Returns the status of the AnalogImpedance pseudo-instrument."""
            c_status = _typespec_ctypes.DwfState()
            result = self._device._dwf._lib.FDwfAnalogImpedanceStatus(self._device._hdwf, c_status)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            status_ = DwfState(c_status.value)
            return status_

        def statusInput(self, channel_index: int) -> Tuple[float, float]:
            c_gain = _typespec_ctypes.c_double()
            c_radian = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogImpedanceStatusInput(self._device._hdwf, channel_index, c_gain, c_radian)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            gain = c_gain.value
            radian = c_radian.value
            return (gain, radian)

        def statusMeasure(self, measure: DwfAnalogImpedance) -> float:
            c_value = _typespec_ctypes.c_double()
            result = self._device._dwf._lib.FDwfAnalogImpedanceStatusInput(self._device._hdwf, measure.value, c_value)
            if result != _RESULT_SUCCESS:
                raise self._device._dwf._exception()
            value = c_value.value
            return value
