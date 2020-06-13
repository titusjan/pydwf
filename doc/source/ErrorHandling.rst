
Error Handling
==============

Error handling in the C API
---------------------------

Each function in the C API returns an integer, indicating its success or error status; a value of 0 indicates an error, while a value of 1 indictates success. Note that this is different from most other C libraries, where 0 indicates success.

In case a function return 0, indicating some kind of failure, the C API provides two functions to inquire the reason of failure. The 'getLastError()' function returns a value of enum type DWFERC indicating the cause of the last error, while function 'getLastErrorMsg()' returns a string describing the error.

Error handling in the pydwf module
----------------------------------

In Python, error handling is supported by the core language in the form of exceptions.

To support exception-based error handling, the 'pydwf' module inspects the return value of each call to the C API, and, in case of error, raises a 'DigilentWaveformLibraryError' exception that contains both the DWERC error code of the last function called and its corresponding textural description.
