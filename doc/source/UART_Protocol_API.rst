
UART Protocol API
=================

The UART Protocol API provides functionality to use a Digilent device as a simple Universal Asynchronous Receiver/Transmitter (UART).

The UART protocol as implemented in DWF supports a single digital pin to act as a transmitter (TX), and a single digital pin to act as a receiver (RX).
Transmission and reception are relative to the viewpoint of the Digilent device; so 'transmission' means that the Digilent device sends outgoing data, and 'reception' means that the Digilent device receives incoming data.

The Digilent UART protocol only supports these two basic serial TX and RX signals. Other signals commonly encountered on serial ports (e.g., hardware handshaking using RTS/CTS) are not supported.

Using the UART protocol API
---------------------------

To use the UART protocol API functionality you first need to initialize a DigitalWaveformLibrary instance. Next, you open a specific device. The device's UART protocol API can now be accessed via its *digitalUart* attribute, which is an instance of the DigitalUartAPI class.

Version 3.16.3 of the underlying C library supports 9 UART-related functions, none of which are obsolete. These map precisely onto 9 methods of the DigitalUartAPI class:

* The reset() method resets the UART protocol instrument.
* The rateSet(), bitsSet(), paritySet(), and stopSet() methods set the serial protocol parameters.
* The txSet() and rxSet() methods assign digital hardware pins to be used for the TX and RX signals.
  For testing purposes, it can be useful to set these to the same pin, effectively creating a so-called *loopback*.
* The rx() and tx() methods are used to receive and transmit serial data.
  In addition, the rx() method, when called with parameter 0, initializes the receiver.
  This must be done prior to using the rx() method to receive actual data.

Remarks
^^^^^^^

* Note that the UART protocol API does not provide methods to read back parameter values.
* The number of stop bits can also be specified as a floating point value.
  This makes sense; an uncommon but valid choice for stop bits is 1.5 (one-and-a-half).
* The 'parity_error' value returned by rx() needs to be explained.

Example
-------

.. literalinclude:: examples/digital_uart_api_example1.py
   :language: python
   :linenos:
