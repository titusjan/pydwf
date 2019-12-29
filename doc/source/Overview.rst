
Digilent Waveforms Overview
===========================

Overview of the C API (version 3.12.2)
--------------------------------------

+---------------------+------------+--------------+-----------+
| **category**        | **active** | **obsolete** | **total** |
+---------------------+------------+--------------+-----------+
| *(miscellaneous)*   |          5 |            0 |         5 |
+---------------------+------------+--------------+-----------+
| FDwfEnum            |          8 |            4 |        12 |
+---------------------+------------+--------------+-----------+
| FDwfDevice          |         15 |            0 |        15 |
+---------------------+------------+--------------+-----------+
| FDwfAnalogIn        |         87 |            1 |        88 |
+---------------------+------------+--------------+-----------+
| FDwfAnalogOut       |         58 |           25 |        83 |
+---------------------+------------+--------------+-----------+
| FDwfAnalogIO        |         17 |            0 |        17 |
+---------------------+------------+--------------+-----------+
| FDwfDigitalIO       |         19 |            0 |        19 |
+---------------------+------------+--------------+-----------+
| FDwfDigitalIn       |         52 |            2 |        54 |
+---------------------+------------+--------------+-----------+
| FDwfDigitalOut      |         45 |            1 |        46 |
+---------------------+------------+--------------+-----------+
| FDwfDigitalUart     |          9 |            0 |         9 |
+---------------------+------------+--------------+-----------+
| FDwfDigitalSpi      |         18 |            0 |        18 |
+---------------------+------------+--------------+-----------+
| FDwfDigitalI2c      |         11 |            0 |        11 |
+---------------------+------------+--------------+-----------+
| FDwfDigitalCan      |          7 |            0 |         7 |
+---------------------+------------+--------------+-----------+
| FDwfAnalogImpedance |         22 |            0 |        22 |
+---------------------+------------+--------------+-----------+
| **TOTAL**           |        373 |           33 |       406 |
+---------------------+------------+--------------+-----------+


Overview of the pydwf module API
================================

* class DigilentWaveformLibrary:

   * (misc library functions)
   * enum: EnumAPI
   * device: DeviceAPI

* class DigilentWaveformDevice:

   * (misc device functions)
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
   * analogImpedance: AnalogImedanceAPI
