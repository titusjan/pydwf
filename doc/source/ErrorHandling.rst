
Error Handling
==============

Error handling in the C API
---------------------------

Each function in the C API returns an integer, indicating its success or error status. A value of 0 indicates an error, while a value of 1 indictates success. Note that this is different from most other C libraries, where a 0 return value indicates success.

In case a function return 0, indicating some kind of failure, the C API provides two functions to inquire the reason of failure. The 'getLastError()' function returns a value of enum type DWFERC indicating the cause of the last error, while function 'getLastErrorMsg()' returns a string describing the error.

Error handling in the pydwf module
----------------------------------

Python provides exceptions to handle errors, which is quite different from the lower level return-value based mechanism used in the the C API. Fortunately, it turns out to be quite easy to turn errors reported by the C API functions into Python exceptions.

To do this, the 'pydwf' module inspects the return value of each call to the C API, and, in case of an error (i.e., a zero return value), it raises a 'DigilentWaveformLibraryError' exception that contains both the DWERC error code of the last function called and its corresponding textual description, as obtained by calling the 'getLastError()' and 'getLastErrorMsg()' functions.
