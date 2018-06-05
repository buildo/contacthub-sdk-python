.. _event_operations:

Operations on Events
====================

The second important entity of ContactHub are events, particular actions performed by customers in particular contexts.

The attribute `type` of an `Event` defines the schema that you must follow for his attributes. His schema must be specified
in the `properties` attribute of the `Event`.

Eg:
If you create a new event whose type is `serviceSubscribed`, you must specify these attributes in the `properties`
attribute of the Event:

+-----------------+--------+
| Name            | Type   |
+-----------------+--------+
| subscriberId    | string |
+-----------------+--------+
| serviceId       | string |
+-----------------+--------+
| serviceName     | string |
+-----------------+--------+
| serviceType     | string |
+-----------------+--------+
| startDate       | string |
+-----------------+--------+
| endDate         | string |
+-----------------+--------+
| extraProperties | object |
+-----------------+--------+

**Active event types and their related schemas can be found on** `ContactHub Settings <https://hub.contactlab.it/#/settings/events />`_

Events are also associated to a context of use. The available contexts for an event are:

* CONTACT_CENTER
* WEB
* MOBILE
* ECOMMERCE
* RETAIL
* IOT
* SOCIAL
* DIGITAL_CAMPAIGN
* OTHER

When you create an `Event`, the attributes `type`, `context` and `properties` are required.

For each type of `context`, you can also provide some additional properties in
the optional `contextInfo` object. The schema for this object varies depending
on the specified `context`. All the schemas can be found at `this link
<http://developer.contactlab.com/documentation/contacthub/schemas/index />`_.

Add a new event
---------------
To create a new event, you have to define its schema (according to the specified type) in `Event` class constructor::

    event = Event(
        node=node,
        customerId=my_customer.id,
        type=Event.TYPES.SERVICE_SUBSCRIBED,
        context=Event.CONTEXTS.WEB,
        contextInfo=Properties(
            client=Properties(
                ip="127.0.0.1"
            )
        )
        properties=Properties(
            subscriberId='s_id', serviceId='service_id', serviceName='serviceName', startDate=datetime.now(),
            extraProperties=Properties(extra='extra')
        )
    )

**The attribute `customerId` is required for specifying the customer who will be associated with the event.**

After the creation, you can add the event via the node method::

    posted = node.add_event(**event.to_dict())

or directly by the object::

    event.post()

For some events, you have to specify the `mode` attribute. Its value must be:

* ACTIVE: if the customer made the event
* PASSIVE: if the customer receive the event

Sessions
--------

ContactHub allows saving anonymous events of which it is expected that the customer will be identified in the future.
For this purpose, you can save an event using a Session ID, an unique identifier that is assigned to the anonymous
customer, without specify the customer ID.

To save an event with a Session ID, use the `bringBackProperties` attribute.

You can generate a new session ID conforming to the UUID standard V4 by the `create_session_id` method of the `Node`::

    session_id = node.create_session_id()

    event = Event(node=node, bringBackProperties=Properties(type='SESSION_ID', value=session_id),
    type=Event.TYPES.SERVICE_SUBSCRIBED, context=Event.CONTEXTS.WEB,
    properties=Properties(subscriberId = 's_id', serviceId='service_id', serviceName='serviceName', startDate=datetime.now(),
    extraProperties=Properties(extra='extra')))

If the anonymous customer will perform the authentication, you can add a new `Customer` on ContactHub, obtaining a new
customer ID.
To reconcile the events stored with the session ID previously associated to the anonymous Customer::

    node.add_customer_session(customer_id='c_id', session_id=session_id)

In this way, every event stored with the same session ID specified as parameter in the `add_customer_session` method,
will be associated to the customer specified.

ExternalId
----------

In the same way of the Session ID, you can add a new event specifying the external ID of a customer::

    from contacthub.model import Event

    event = Event(node=node, bringBackProperties=Properties(type='externalId', value='e_id'),
    type=Event.TYPES.SERVICE_SUBSCRIBED, context=Event.CONTEXTS.WEB,
    properties=Properties(subscriberId = 's_id', serviceId='service_id', serviceName='serviceName', startDate=datetime.now(),
    extraProperties=Properties(extra='extra')))

Get all events
--------------
To get all events associated to a customer, use `Node` method::

    events = node.get_events(customer_id='c_id')

You can filter events specifying the following parameters in `get_events` method:

* event_type
* context
* event_mode
* date_from
* date_to
* page
* size

::

    events = node.get_events(customer_id='c_id', event_type=Event.TYPES.SERVICE_SUBSCRIBED, context=Event.CONTEXTS.WEB)

This method will return a `PaginatedList` (see :ref:`paging_customers`).

A shortcut for customer events is available as a property in a `Customer` object::

    for event in my_customer.get_events():
        print (event.type)

In this last case, the property will return an immutable list of `Event`: you can only read the events associated to a
customer from it and adding events to the list is not allowed.

Get a single event
------------------
Retrieve a single event by its ID, obtaining a new `Event` object::

    customer_event = event.get_event(id='event_id')

