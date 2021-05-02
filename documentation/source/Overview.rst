.. include:: substitutions.rst

Digilent Waveforms Overview
===========================

|Digilent| provides the Digilent Waveforms library to control their line of line of electronic measurement and control devices.
The library is available as a DLL on Microsoft Windows, a shared object ("so") library on Linux, and a framework on Apple's macOS.
The provided library is accompanied by a C header file; together with the shared library file itself, this allows access to the functionality provided from the C and C++ programming languages.

Most popular programming languages provide a mechanism to access functions in shared libraries.
In Python, such a mechanism is provided by the |ctypes| module that is part of the standard Python library.

The |pydwf.short| package is a binding to the functionality provided by the DWF library, using the |ctypes| module.
It makes all types and functions provided by the DWF library available for use in Python programs.

Overview of the C API
---------------------

The DWF library comes with a C header file that (for version 3.16.3) defines the 24 enumeration types and 415 function calls that together make up the DWF API.
Of the 415 function calls provided, 33 are labeled 'obsolete'. Their functionality is usually superseded by newer, more general functions.

The API functions are organized in 14 sub-categories, each providing access to a subset of the DWF functionality — for example, a specific type of instrument, or functions to send and receive messages using a certain protocol.

The function counts for each of the sub-categories of functionality are listed below, to give some idea of the complexity of the different areas of the API.
From this table, it is clear that the most complex parts of the API are the AnalogIn ("oscilloscope") and AnalogOut ("waveform generator") instruments, followed by the DigitalIn ("logic analyzer") and DigitalOut ("pattern generator") instruments.
Two-thirds of all the functions provided by the DWF library are directly related to control of these four powerful instruments.

API summary: functions by category
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------+--------------------------------+------------+--------------+-----------+
| **category**        | **description**                | **active** | **obsolete** | **total** |
+---------------------+--------------------------------+------------+--------------+-----------+
| *(miscellaneous)*   | Version info etc.              |          5 |            0 |         5 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfEnum            | Device enumeration             |          8 |            4 |        12 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDevice          | Device opening and closing     |         15 |            0 |        15 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfAnalogIn        | Oscilloscope instrument        |         92 |            1 |        93 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfAnalogOut       | Waveform generator instrument  |         58 |           25 |        83 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfAnalogIO        | Static control of analog I/O   |         17 |            0 |        17 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalIO       | Static control of digital I/O  |         19 |            0 |        19 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalIn       | Logic analyzer instrument      |         53 |            2 |        55 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalOut      | Pattern generator instrument   |         47 |            1 |        48 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalUart     | UART protocol send/receive     |          9 |            0 |         9 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalSpi      | SPI protocol send/receive      |         19 |            0 |        19 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalI2c      | I2C protocol send/receive      |         11 |            0 |        11 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalCan      | CAN protocol send/receive      |          7 |            0 |         7 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfAnalogImpedance | Impedance measurements         |         22 |            0 |        22 |
+---------------------+--------------------------------+------------+--------------+-----------+
| **TOTAL**           |                                |        382 |           33 |       415 |
+---------------------+--------------------------------+------------+--------------+-----------+

Overview of the |pydwf| package API
-----------------------------------

The |pydwf.short| package encapsulates the functionality offered by the underlying C library in two main Python classes.

Class |DigilentWaveformsLibrary.long| represents the loaded DWF library itself, and provides functions that are not specific to a particular device, such as querying the library version, device enumeration, and opening a device for use.

* class |DigilentWaveformsLibrary.long|

   * methods :py:meth:`~pydwf.DigilentWaveformsLibrary.getLastError`, :py:meth:`~pydwf.DigilentWaveformsLibrary.getLastErrorMsg`,
             :py:meth:`~pydwf.DigilentWaveformsLibrary.getVersion`,
             :py:meth:`~pydwf.DigilentWaveformsLibrary.paramSet`, :py:meth:`~pydwf.DigilentWaveformsLibrary.paramGet`
   * attribute :py:attr:`~pydwf.DigilentWaveformsLibrary.enum`    of type :py:class:`~pydwf.DigilentWaveformsLibrary.EnumAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsLibrary.device`: of type :py:class:`~pydwf.DigilentWaveformsLibrary.DeviceAPI`

Class |DigilentWaveformsDevice.long| represents a specific DWF-compatible hardware device, such as an Analog Discovery 2 or a Digital Discovery.
The functionality of a |DigilentWaveformsDevice| is mostly offered via a number of instance attributes, each representing an *instrument*, *protocol*, or *measurement type*.

* class |DigilentWaveformsDevice.long|

   * methods :py:meth:`~pydwf.DigilentWaveformsDevice.close`,
             :py:meth:`~pydwf.DigilentWaveformsDevice.autoConfigureSet`, :py:meth:`~pydwf.DigilentWaveformsDevice.autoConfigureGet`,
             :py:meth:`~pydwf.DigilentWaveformsDevice.reset`,
             :py:meth:`~pydwf.DigilentWaveformsDevice.enableSet`,
             :py:meth:`~pydwf.DigilentWaveformsDevice.triggerInfo`, :py:meth:`~pydwf.DigilentWaveformsDevice.triggerSet`, :py:meth:`~pydwf.DigilentWaveformsDevice.triggerGet`,
             :py:meth:`~pydwf.DigilentWaveformsDevice.triggerPC`,
             :py:meth:`~pydwf.DigilentWaveformsDevice.triggerSlopeInfo`,
             :py:meth:`~pydwf.DigilentWaveformsDevice.paramSet`, :py:meth:`~pydwf.DigilentWaveformsDevice.paramGet`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.analogIn`        of type :py:class:`~pydwf.DigilentWaveformsDevice.AnalogInAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.analogOut`       of type :py:class:`~pydwf.DigilentWaveformsDevice.AnalogOutAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.analogIO`        of type :py:class:`~pydwf.DigilentWaveformsDevice.AnalogIOAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.digitalIO`       of type :py:class:`~pydwf.DigilentWaveformsDevice.DigitalIOAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.digitalIn`       of type :py:class:`~pydwf.DigilentWaveformsDevice.DigitalInAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.digitalOut`      of type :py:class:`~pydwf.DigilentWaveformsDevice.DigitalOutAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.digitalUart`     of type :py:class:`~pydwf.DigilentWaveformsDevice.DigitalUartAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.digitalSpi`      of type :py:class:`~pydwf.DigilentWaveformsDevice.DigitalSpiAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.digitalI2c`      of type :py:class:`~pydwf.DigilentWaveformsDevice.DigitalI2cAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.digitalCan`      of type :py:class:`~pydwf.DigilentWaveformsDevice.DigitalCanAPI`
   * attribute :py:attr:`~pydwf.DigilentWaveformsDevice.analogImpedance` of type :py:class:`~pydwf.DigilentWaveformsDevice.AnalogImpedanceAPI`
