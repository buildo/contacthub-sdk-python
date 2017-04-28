[![Build Status](https://travis-ci.org/axant/contacthub-sdk-python.svg?branch=master)](https://travis-ci.org/axant/contacthub-sdk-python) 
[![Coverage Status](https://coveralls.io/repos/github/axant/contacthub-sdk-python/badge.svg)](https://coveralls.io/github/axant/contacthub-sdk-python)
[![Documentation Status](https://readthedocs.org/projects/contacthub-sdk-python/badge/?version=latest)](http://contacthub-sdk-python.readthedocs.io/en/latest/?badge=latest)

# Contacthub Python SDK

This is the official Python SDK for [ContactHub REST API](https://contactlab.github.io/contacthub-json-schemas/apidoc.html).
This SDK easily allows to access your data on ContactHub, making the authentication immediate and simplifying reading/writing operations.

For all information about ContactHub, check [here](http://contactlab.com/en/offer/engagement-marketing-platform/contacthub/)

## Table of contents
-   [Introduction](http://contacthub-sdk-python.readthedocs.io/en/latest/)
-   [Getting started](http://contacthub-sdk-python.readthedocs.io/en/latest/getting_started.html)
    -   [Installing and importing the SDK](http://contacthub-sdk-python.readthedocs.io/en/latest/getting_started.html#installing-the-sdk)
	-   [Performing simple operations on customers](http://contacthub-sdk-python.readthedocs.io/en/latest/getting_started.html#performing-simple-operations-on-customers)
-   [Authentication](http://contacthub-sdk-python.readthedocs.io/en/latest/authentication.html)
    -    [Authentication via configuration file](http://contacthub-sdk-python.readthedocs.io/en/latest/authentication.html#authenticating-via-configuration-file)
    -    [Proxies](http://contacthub-sdk-python.readthedocs.io/en/latest/authentication.html#proxies)
-   [Operations on Customers](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html)
    -   [Add a new customer](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#create-and-add-a-new-customer)
    -   [Get all customers](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#get-all-customers)
    -   [Get a single customer](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#get-a-single-customer)
    -   [Query on customers](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#query    )
    -   [Update a customer](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#update-a-customer)
        - [Full update - Put](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#full-update-put)
        - [Partial update - Patch](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#partial-update-patch)
    -   [Delete a customer](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#delete-a-customer)
    -   [Tag](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#tags)
    -   [Additional entities](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#additional-entities)
        -   [Education](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#education)
        -   [Job](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#job)
        -   [Like](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#like)
        -   [Subscription](http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#subscription)
-   [Operations on Events](http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html)
    - [Add a new event](http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html#add-a-new-event)
        - [Sessions](http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html#sessions)
        - [External ID](http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html#externalid)
    - [Get all events](http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html#get-all-events)
    - [Get a single event](http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html#get-a-single-event)
-   [Exception Handling](http://contacthub-sdk-python.readthedocs.io/en/latest/exception_handling.html)
-   [API Reference](http://contacthub-sdk-python.readthedocs.io/en/latest/api_reference.html)