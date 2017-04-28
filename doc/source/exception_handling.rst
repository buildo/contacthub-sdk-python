.. _exception_handling:

Exception handling
==================

When ContactHub API's returns a different status codes than 2xx Success, an `ApiError` Exception will be thrown.
A sample of an `ApiError` message::

    contacthub.errors.api_error.APIError: Status code: 409. Message: Conflict with exiting customer 8b321dce-53c4-4029-8388-1938efa2090c. Errors: []. Data: data}. Logref: logref_n

