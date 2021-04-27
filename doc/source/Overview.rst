
Digilent Waveforms Overview
===========================

Digilent provides the Digilent Waveforms library to control their line of *Discovery* devices. The library is available as a DLL on Microsoft Windows, a shared object ("so") library on Linux, and a framework on Apple's macOS. The provided library is accompanied by a C header file; together with the shared library file itself, this allows access to the functionality provided from the C and C++ programming languages.

Most popular programming languages provide a mechanism to access functions in shared libraries. In Python, such a mechanism is provided by the *ctypes* module that is part of the standard Python library.

The *pydwf* module is a binding to the functionality provided by the DWF library, using the *ctypes* module. It makes all types and functions provided by the DWF library available for use in Python programs.

Overview of the C API (version 3.16.3)
--------------------------------------

The DWF library comes with a header file that defines the 24 enumeration types and 415 function calls that together make up the DWF API. Of the 415 function calls provided, 33 are labeled 'obsolete'. Their functionality is usually superseded by newer, more general functions.

The API functions are organized in 14 sub-categories, each providing access to a subset of the DWF functionality — for example, a specific type of instrument, or functions to send and receive messages using a certain protocol.

The function counts for each of the sub-categories of functionality are listed below, to give some idea of the complexity of the different areas of the API. From this table, it is clear that the most complex parts of the API are the AnalogIn ("oscilloscope") and AnalogOut ("waveform generator") instruments, followed by the DigitalIn ("logic analyzer") and DigitalOut ("pattern generator") instruments. Two-thirds of all the functions provided by the DWF library are directly related to control of these four powerful instruments.

API summary: functions by category
==================================

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

Overview of the pydwf module API
================================

The *pydwf* library organizes the functionality offered by the underlying C library in two main classes.

Class `DigilentWaveformsLibrary` represents the loaded DWF library itself, and provides functions that are not specific to a particular device, such as querying the library version, device enumeration, and opening a device for use.

* class DigilentWaveformsLibrary:

   * miscellaneous library functions
   * enum: EnumAPI
   * device: DeviceAPI

Class `DigilentWaveformsDevice` represents a specific DWF-compatible hardware device, such as an Analog Discovery 2 or a Digital Discovery. The functionality of a DigilentWaveformsDevice is offered in a number of sub-modules, each representing an *instrument*, *protocol*, or *measurement type*.

* class DigilentWaveformsDevice:

   * miscellaneous device functions
   * analogIn: AnalogInAPI
   * analogOut: AnalogOutAPI
   * analogIO: AnalogIOAPI
   * digitalIO: DigitalIOAPI
   * digitalIn: DigitalInAPI
   * digitalOut: DigitalOutAPI
   * digitalUart: DigitalUartAPI
   * digitalSpi: DigitalSpiAPI
   * digitalI2c: DigitalI2cAPI
   * digitalCan: DigitalCanAPI
   * analogImpedance: AnalogImpedanceAPI
