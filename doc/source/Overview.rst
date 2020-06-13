
Digilent Waveforms Overview
===========================

Digilent provides the Digilent Waveforms library to control their line of *Discovery* devices. The library is available as a DLL on Microsoft Windows, a shared object ("so") library in Linux, and a framework in Apple OSX. The provided library is accompanied by a C header file; together with the shared library file itself, this allows access to the functionality provided from the C and C++ programming languages.

Most popular programming languages provide a mechanism to access functions in shared libraries. In Python, such a mechanism is implemented in the *ctypes* module that is part of the standard Python library.

The *pydwf* module is a binding to the functionality provided by the DWF library, using the *ctypes* module. It makes all types and functions provided by the DWF library available for use in Python programs.

Overview of the C API (version 3.12.2)
--------------------------------------

The DWF library comes with a header file that lists about a dozen types, and precisely 406 function calls that make up the DWF API. Of the 406 function calls provided, 33 are labeled 'obsolete'. Their functionality is usually superseded by newer, more general functions.

The API is organized in 14 sub-categories, each providing access to a subset of the DWF functionality — for example, a specific type of instrument, or functions to send and receive messages using a certain protocol.

The function counts for each of the sub-categories of functionality are listed below, to give some idea of the complexity of the different areas of the API. From this table, it is clear that the most complex parts of the API are the AnalogIn ("oscilloscope") and AnalogOut ("waveform generator") devices, followed by the DigitalIn ("logic analyzer") and Digital Out ("pattern generator") devices. Two thirds of all the functions provided by the DWF library are directly related to control of these four powerful devices.

+---------------------+--------------------------------+------------+--------------+-----------+
| **category**        | **description**                | **active** | **obsolete** | **total** |
+---------------------+--------------------------------+------------+--------------+-----------+
| *(miscellaneous)*   | Version info etc.              |          5 |            0 |         5 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfEnum            | Device enumeration             |          8 |            4 |        12 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDevice          | Device opening and closing     |         15 |            0 |        15 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfAnalogIn        | Oscilloscope instrument        |         87 |            1 |        88 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfAnalogOut       | Waveform generator instrument  |         58 |           25 |        83 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfAnalogIO        | Static control of analog I/O   |         17 |            0 |        17 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalIO       | Static control of digital I/O  |         19 |            0 |        19 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalIn       | Logic analyzer instrument      |         52 |            2 |        54 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalOut      | Pattern generator instrument   |         45 |            1 |        46 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalUart     | UART protocol send/receive     |          9 |            0 |         9 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalSpi      | SPI protocol send/receive      |         18 |            0 |        18 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalI2c      | I2C protocol send/receive      |         11 |            0 |        11 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfDigitalCan      | CAN protocol send/receive      |          7 |            0 |         7 |
+---------------------+--------------------------------+------------+--------------+-----------+
| FDwfAnalogImpedance | Impedance measuring instrument |         22 |            0 |        22 |
+---------------------+--------------------------------+------------+--------------+-----------+
| **TOTAL**           |                                |        373 |           33 |       406 |
+---------------------+--------------------------------+------------+--------------+-----------+

Overview of the pydwf module API
================================

The *pydwf* library organizes the functionality offered by the underlying C library in two main classes.

Class `DigilentWaveformLibrary` represents the loaded DWF library itself, and provides functions that are not specific to a particular device, such as querying the library version, device enumeration, and opening a device for use.

* class DigilentWaveformLibrary:

   * miscellaneous library functions
   * enum: EnumAPI
   * device: DeviceAPI

Class `DigilentWaveformDevice` represents a specific DWF-compatible hardware device, such as an Analog Discovery 2 or a Digital Discovery. The functionality of a DigilentWaveformDevice is offered in a number of sub-modules, each representing an *instrument*, *protocol*, or *measurement type*.

* class DigilentWaveformDevice:

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
