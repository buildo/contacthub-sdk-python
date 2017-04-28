.. _getting_started:

Getting started
===============

Installing the SDK
------------------

The ContactHub SDK can be installed from PyPi::

    pip install contacthub

After installing, for importing the contacthub SDK just::

    import contacthub

Performing simple operations on customers
-----------------------------------------

Getting Customer's data
^^^^^^^^^^^^^^^^^^^^^^^

Retrieving entity's data can be easily achieved with simple operations.

First of all, you need to authenticate with credentials provided by `ContactHub`::

    from contacthub import Workspace

    workspace = Workspace(workspace_id='workspace_id', token='token')

After that you can get a `Node` object to perform all operations on customers and events::

    node = workspace.get_node(node_id='node_id')

With a node, is immediate to get all customers data in a ``list`` of ``Customer`` objects::

    customers = node.get_customers()

    for customer in customers:
        print(customer.base.firstName)

Getting a single ``Customer``::

    my_customer = node.get_customer(id='id')

    print('Welcome back %s' % my_customer.base.firstName)

or querying on customers by theirs own attributes::

    fetched_customers = node.query(Customer).filter((Customer.base.firstName == 'Bruce') & (Customer.base.secondName == 'Wayne')).all()

Add a new Customer
^^^^^^^^^^^^^^^^^^

Creating and posting a Customer is simple as getting. The method `add_customer` of the node take a dictionary containing
the structure of your customer as parameter and returns a new Customer object::


    customer_struct =   {
                        'base': {'contacts': {'email': 'myemail@email.com'}},
                        'extra': 'extra',
                        'extended': {'my_string':'my new extended property string'}
                        }
    my_customer = c.add_customer(**customer_struct)

For creating the customer structure, you can also create a new Customer object and convert it to a dictionary for posting::

    from contacthub.models import Customer

    my_customer = Customer(node = node)
    my_customer.base.contacts.email = 'myemail@email.com'
    my_customer.extra = 'extra'
    my_customer.extended.my_string = 'my new extended property string'
    my_customer = node.add_customer(**my_customer.to_dict())

or posting it directly with the `post` method::

    my_customer.post()

Relationship between Customers and Events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this SDK entities are easily connected.
For retrieving all events associated to a ``Customer``, just::

    my_customer = node.get_customer(id='id')
    events = my_customer.get_events()

Note that relations are immutable objects. You can just consult events associated to a ``Customer``,
but you cannot add new ones or delete.