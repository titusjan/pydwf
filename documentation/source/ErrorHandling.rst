
Error Handling
==============

Error handling in the C API
---------------------------

Each function in the C API returns an integer, indicating its success or error status. A value of 0 indicates an error, while a value of 1 indicates success. Note that this is different from the convention used in most C libraries, where a 0 return value indicates success.

In case a function return 0, indicating some kind of failure, the C API provides two functions to inquire the reason of the failure. The 'getLastError()' function returns a value of enumeration type DWFERC indicating the cause of the last error, while function 'getLastErrorMsg()' returns a string describing the error.

Error handling in the *pydwf* package
-------------------------------------

Python provides exceptions to handle errors, which is quite different from the lower level return-value based mechanism used in the the C API.
Fortunately, it is possible to turn the low-level errors reported by the C API functions into Python exceptions.

To do this, the *pydwf* package inspects the return value of each call to the C API, and, in case of an error (i.e., a return value unequal to 1), it raises a 'DigilentWaveformsLibraryError' exception that contains both the DWERC error code of the last function called and its corresponding textual description, as obtained by calling the 'getLastError()' and 'getLastErrorMsg()' functions.

Other exceptions raised by the *pydwf* package
----------------------------------------------

There are a few circumstances where *pydwf* detects an error condition besides a call to a function of the underlying C library. Such errors are handled by raising a PyDwfError exception, which derives from Python's standard RuntimeError exception.

In fact, the DigilentWaveformsLibraryError exception type discussed above itself derives from PyDwfError.
This makes it possible to easily catch any *pydwf* error in code depending on *pydwf*, e.g.

.. code-block:: python

   from pydwf import DigilentWaveformsLibrary, PyDwfError

   dwf = DigilentWaveformsLibrary()

   try:

       # Call a function that uses pydwf.
       #
       # The function may raise an exception:
       #   either a PyDwfError or a more specific DigilentWaveformsLibraryError.

       use_pydwf(dwf)

   except PyDwfError as e:

       print("oops:", e)
