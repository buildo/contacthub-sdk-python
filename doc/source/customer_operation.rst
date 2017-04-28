.. _customer_operations:

Operations on Customers
=======================

After the :ref:`authentication` you are ready to perform all operations on ContactHub's entities.

Create and add a new customer
-----------------------------

Like every other entities in ContactHub, you can perform an operation via two methods:
    1. Via the methods provided by the `Node` class
    2. Performing the operation directly by your entity's object

1. Adding a new customer via the methods provided by the `Node` class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In this first case, a new customer can be added in ContactHub by the `Node` object. By default, the `add_customer`
method takes as parameter a dictionary containing the structure of your new customer and return a new `Customer`
object::

    customer_structure = {
                            'externalId': '01',
                            'extra': 'extra',
                            'base':
                                    {
                                    'timezone': 'Europe/Rome',
                                    'firstName': 'Bruce',
                                    'lastName': 'Wayne',
                                    'contacts': {
                                                'email': 'email@email.com'
                                                }
                                    }
                            }

    my_customer = node.add_customer(**customer_structure)

To specify the structure of your new customer, you can also use the `Customer` class, creating a new `Customer` object
and converting it to a dictionary::

    from contacthub.models import Customer

    post_customer = Customer(node = node)
    post_customer.base.firstName = 'Bruce'
    post_customer.base.lastName = 'Wayne'
    post_customer.base.contacts.email = 'email@example.com'
    post_customer.extra = 'extra'
    post_customer.extended.my_string = 'my new extended property string'

    new_customer = node.add_customer(**post_customer.to_dict())


When you declare a new `Customer`, by default its internal structure start with this template::

    {'base':{
            'contacts': {}
            },
    'extended': {},
    'tags': {
            'manual':[],
            'auto':[]
            }
    }

You can directly access every simple attribute (strings, numbers) in a new customer created with the above structure.

It's possibile to re-define your own internal structure for a customer with the `default_attributes` parameter of the
`Customer` constructor::

    c = Customer(node=node, default_attributes={'base':{}})

In this case, you can directly set the `base` attribute, but you have to define beforehand all other objects in the internal structure.

Properties class
````````````````
An important tool for this SDK it's the `Properties` class. It represents a default generic object and you should use it
for simplify the declarations of entity's properties. In `Properties` object constructor you can declare every field you
need for creating new properties. These fields can be strings, integer, datetime object, other `Properties` and lists
of above types.

For example::

    from contacthub.models import Properties

    my_customer = Customer(node=node)
    my_customer.base.contacts = Properties(email='bruce.wayne@darkknight.it', fax='fax', otherContacts=[Properties(value='123', name='phone', type='MOBILE')])
    my_customer.base.address = Properties(city='city', province='province', geo=Properties(lat=40, lon=100))

    my_customer.post()

Extended properties
```````````````````

By default the extended properties are already defined in the `Customer` structure, so you can populate it with new
integers, strings or `Properties` object for storing what you need. Extended properties follow a standardized schema
defined in the `ContactHub settings <https://hub.contactlab.it/#/settings/properties/>`_.

::

    my_customer.extended.my_extended_int = 1
    my_customer.extended.my_extended_string = 'string'
    my_customer.extended.my_extended_object = Properties(key='value', k='v')

2. Posting a customer directly by its object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the second case, after the creation of the `Customer` you can post it directly with the `post` method::

    my_customer.post()


Force update
^^^^^^^^^^^^

If the customer already exists in the node, you can force its update with the new structure specified. If the system
notice a match between the new customer posted and an existent one in the node, with the flag `force_update` set to
True, the customer will be updated with new data.::

    my_customer = node.add_customer(**customer_structure, forceUpdate=True)

or alternatively::

    my_customer.post(forceUpdate=True)

The match criteria between customers is a configurable option in
the `ContactHub settings <https://hub.contactlab.it/#/settings/properties/>`_.

For adding a new customer, you have to define its structure with all attributes you need.
You must specify all required attribute, according to your ContactHub configuration. You can find the required
attributes in your `ContactHub dashboard <https://hub.contactlab.it/#/settings/properties/>`_.

**N.B.: You must follow the ContatHub schema selected for your base properties.** Check the `ContactHub dashboard
<https://hub.contactlab.it/#/settings/properties/>`_ for further information.

For errors related to the addition of customers, see :ref:`exception_handling`.

Get all customers
-----------------

To retrieve a list of customers in a node, just::

    customers = node.get_customers()

This method return a list of `Customer` objects.

For example, for accessing the email of a customer::

    print(my_customer.base.contacts.email)

or getting the manual tags associated to a customer in a list::

    for tag in my_customer.tags.manual:
        print(tag)


In this way you can access every attribute of a single `Customer`.

Note that if you'll try to access for example the `base` attribute of a `Customer`, it will return an `Properties`
object, that will contain all the base properties of the `Customer` object.

.. _paging_customers:

Paging the customers
^^^^^^^^^^^^^^^^^^^^

When you retrieve a list of entities (e.g. `get_customers`) , a new `PaginatedList` object will be returned.
The `PaginatedList` object allows you scrolling through the result pages from the API. By default you'll get the first
10 elements of total result, coming from the first page, but you can specify the maximum number of customers per page
and the page to get.

For example, if you have 50 customers and you want to divide them in 5 per page, getting only the second page, use
the `size` and the `page` parameters in this way::

    customers = node.get_customers(size=5, page=2)


This call will return a `PaginatedList` of 5 customers, taken from the second subset (size 5) of 50 total customers.

Now you can navigate trough the result pages with two metods::

    customers.next_page()

    customer.previous_page()

By these two methods you can navigate through pages containing `Customers` object. The number of Customers for each page
is determined by the `size` parameter of the `get_customer`, by default 10.

In a `PaginatedList` object you can find these attributes:

    * `size`: the number of elements per each page
    * `total_elements`: the number of total elements obtained
    * `total_pages`: the number of total pages in wich are divided the elements
    * `total_unfiltered_elements`: the element excluded from this set of elements
    * `page_number`: the number of the current page. For increment it or decrement it, use the `next_page` and the `previous_page` methods.

Note that a `PaginatedList` is immutable: you can only read the elements from it and adding or removing elements to the
list is not allowed.

Get a customer by their externalId
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can obtain a `PaginatedList` of `Customer` objects associated to an external ID by::

    customers = node.get_customers(external_id="01")

If there's only one customer associated to the given external ID, this method will create a single `Customer` object
instead of a `PaginatedList`

Get specific fields of customers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's possible to filter the fields present in a `Customer`, specifying them in a list strings representing the
attributes::

   node.get_customers(fields=['base.firstName', 'base.lastName'])

**None of the previous parameter passed to the `get_customers` method is required and you can combine them for getting
the list of customers that suits your needs.**

Get a single customer
---------------------

You can get a single customer by specifying its `id` or `externalId`, obtaining a new `Customer` object.

By id::

    my_customer = node.get_customer(id='01')

or by the externalId::

    my_customer = node.get_customer(external_id='02')

Query
-----

Simple queries
^^^^^^^^^^^^^^

ContactHub allows you to retrieve subsets of customers entry in a node, by querying on `Customer` entity.

To retrieve a list of Customers that satisfy your fetching criteria, just create a new `Query` object::

    new_query = node.query(Customer)

Now you're ready to apply multiple filters on this  `Query`, specifying new criteria as parameter of the `.filter`method
of `Query` class::

    new_query = new_query.filter((Customer.base.firstName == 'Bruce') & (Customer.base.lastName == 'Wayne'))

Each filter applied subsequently will put your new criteria in the `AND` condition, adding it to the criteria already
present in the query::

    new_query = new_query.filter((Customer.base.dob <= datetime(1994, 6, 10))

Once obtained a full filtered query, call the `.all()` method to apply the filters and get a `PaginatedList` of queried customers:

    filtered_customers = new_query.all()

Available operations for creating a filter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


+-------------+------------------------------------------------+
| Criteria    | Operator                                       |
+-------------+------------------------------------------------+
| EQUAL       | ==                                             |
+-------------+------------------------------------------------+
| NE          | !=                                             |
+-------------+------------------------------------------------+
| GT          | >                                              |
+-------------+------------------------------------------------+
| GTE         | >=                                             |
+-------------+------------------------------------------------+
| LT          | <                                              |
+-------------+------------------------------------------------+
| LTE         | <=                                             |
+-------------+------------------------------------------------+
| IN          | function `in_` in contacthub.query module      |
+-------------+------------------------------------------------+
| NOT_IN      | function `not_in_` in contacthub.query module  |
+-------------+------------------------------------------------+
| BETWEEN     | function `between_` in contacthub.query module |
+-------------+------------------------------------------------+
| IS_NULL     | == None                                        |
+-------------+------------------------------------------------+
| IS_NOT_NULL | != None                                        |
+-------------+------------------------------------------------+


Equality operator
`````````````````

::

    new_query = node.query(Customer).filter(Customer.base.firstName == 'Bruce')

Not equals
``````````

::

    new_query = node.query(Customer).filter(Customer.base.firstName != 'Bruce')

Greater than
````````````
::

    new_query = node.query(Customer).filter(Customer.base.dob > datetime(1994,6,10))

Greater than or equal
`````````````````````
::

    new_query = node.query(Customer).filter(Customer.base.dob >= datetime(1994,6,10))

Less than
`````````
::

    new_query = node.query(Customer).filter(Customer.registeredAt < datetime(2010,6,10))

Less than or equal
``````````````````
::


    new_query = node.query(Customer).filter(Customer.registeredAt <= datetime(2010,6,10))

In, Not in
``````````
You can verify the presence of a specific value in a customer attribute with the `in_` and `not_in_` methods of the
`query` module:

::

    from contacthub.models.query import in_

    new_query = node.query(Customer).filter(in_('manual_tag', Customer.tags.manual))

::

    from contacthub.models.query import not_in_

    new_query = node.query(Customer).filter(not_in_('manual_tag', Customer.tags.manual))

Between
```````

You can check if a customer date attribute is between two dates. These two dates can be `datetime` objects or normal string following the ISO8601 standard for dates.

::

    from contacthub.models.query import between_

    new_query = node.query(Customer).filter(between_(Customer.base.dob, datetime(1950,1,1), datetime(1994,1,1)))

Is null
```````
::

    new_query = node.query(Customer).filter(Customer.base.firstName == None)

Is not null
```````````

::

    new_query = node.query(Customer).filter(Customer.base.firstName != None)

Combine criteria
^^^^^^^^^^^^^^^^

To combine the above criteria and create complex ones, you can use the `&` and  `|` operators:

AND
```

::

    customers = node.query(Customer).filter((Customer.base.firstName == 'Bruce') & (Customer.base.lastName == 'Wayne')).all()

OR
``

::

    customers = node.query(Customer).filter(((Customer.base.firstName == 'Bruce')) | ((Customer.base.firstName == 'Batman'))).all()

Combined query
^^^^^^^^^^^^^^

It's possibile to combine simple queries to create a combined query.
For this purpose, you can use the `&` operator to put two simple queries in the `AND` condition and the `|` operator
for putting them in the `OR` condition::

    q1 = node.query(Customer).filter(Customer.base.firstName == 'Bruce')
    q2 = node.query(Customer).filter(Customer.base.lastName == 'Wayne')

    and_query = q1 & q2

    or_query = q1 | q2

For apply all filters created in the new combined query, just like the simple queries call the `.all()`:

    filtered_customers = and_query.all()

Update a customer
-----------------

Customers can be updated with new data. The update can be carried on an entire customer or only on a few attributes.

Full update - Put
^^^^^^^^^^^^^^^^^

The full update on customer - PUT method - totally replace old customer attributes with new ones.
As all operations on this SDK, you can perform the full update in two ways: by the the methods in the `Node` class or
directly by the `Customer` object.

Note that if you perform the full update operation by the `update_customer` method of the node,
you have to pass all attributes previously set on the customer, otherwise an APIError will occur (see :ref:`exception_handling`).
These attributes can be easily retrieved via the `to_dict` method.

Set the `full_update` flag to `True` for a full update, eg::

    my_customer = node.get_customer(id='id')
    my_customer.base.contacts.email = 'anotheremail@example.com'

    updated_customer = node.update_customer(**my_customer.to_dict(), full_update=True)

To directly execute a full update on a customer by the `Customer` object::

    my_customer = node.get_customer(id='customer_id')
    my_customer.base.contacts.email = 'anotheremail@example.com'

    my_customer.put()

There are no difference between these two ways of working. By default the parameter `full_update` is set to False,
so without specifying it you'll perform a partial update (see the next section **Partial update - Patch**).

Partial update - Patch
^^^^^^^^^^^^^^^^^^^^^^
The partial update - PATCH method -  applies partial modifications to a customer.

Since all list attributes don't allow normal list operation (`append`, `reverse`, `pop`, `insert`, `remove`,
`__setitem__`, `__delitem__`, `__setslice__`), for adding an element in an
existing list attribute of a customer, you can use the `+=` operator::

    customer.base.subscriptions += [Properties(id='id', name='name', type='type', kind=Cutomer.SUBSCRPTION_KINDS.SERVICE)]

Once the customer is modified, you can get the changes occurred on its attributes by the `get_mutation_tracker` method,
that returns a new dictionary::

    my_customer = node.get_customer(id='customer_id')
    my_customer.base.contacts.email = 'anotheremail@example.com'

    updated_customer = node.update_customer(**my_customer.get_mutation_tracker())

You can also pass to the `update_customer` method a dictionary representing the mutations you want to apply on customer
attributes and the id of the customer for applying it::

    mutations = {'base':{'contacts':{'email':'anotheremail@example.com'}}}

    updated_customer = node.update_customer(id='customer_id',**mutations)

To partially update a customer by the `Customer` object, just::

    my_customer.base.contacts.email = 'anotheremail@example.com'

    my_customer.patch()


Delete a customer
-----------------

Via the node method, passing the id of a customer::

    node.delete_customer(id='customer_id')

or passing the dictionary form of the customer::

    node.delete_customer(**my_customer.to_dict())

Via `Customer` object::

    my_customer.delete()


Tags
----

Tags are particular string values stored in two arrays: `auto` (autogenerated from elaborations) and `manual` (manually inserted).
To get the tags associated to a customer, just access the `tags` attribute of a `Customer` object::

    for auto in my_customer.tags.auto:
        print(auto)

    for manual in my_customer.tags.manual:
        print(manual)

The `Node` class provides two methods for inserting and removing `manual` tags::

    node.add_tag('manual_tag')

When removing a manual tag, if it doesn't exists in the customer tags a ValueError will be thrown::

    try:
        node.remove_tag('manual_tag')
    except ValueError as e:
	    #actions

Additional entities
-------------------

ContactHub provides three endpoints to reach some particular and relevant attributes of a customer.
These endpoint simplify the add, the delete, the update and the get operations of `educations` , `likes`, `jobs` and
`subscriptions` base attributes.
For this purpose, this SDK provides three additional classes for managing these attributes:

* `Education`
* `Job`
* `Like`
* `Subscription`

You can operate on these classes alike other entities (`Customer` and `Event`): via the methods of the `Node` class  or directly by the classes.
These entities are identified by an internal ID and have their own attributes.

Education
---------
Get
^^^
You can get an education associated to a customer by the customer ID and an education ID previously assigned to the
education::

    customer_education = node.get_education(customer_id='c_id', education_id='education_id')

This method creates an `Education` object. You can find the same object in the list of the educations for a customer,
accessing the `base.educations` attribute of a `Customer` object.

Add
^^^
Add via the node method, creating a new `Education` object::

    new_educ = node.add_education(customer_id='123', id='01', schoolType=Education.SCHOOL_TYPES.COLLEGE,
    schoolName='schoolName',schoolConcentration='schoolConcentration', isCurrent=False, startYear='1994', endYear='2000')

or directly by the object::

    from contacthub.model import Education

    new_educ = Education(customer=my_customer, id='01', schoolType=Education.SCHOOL_TYPES.COLLEGE, schoolName='schoolName',
    schoolConcentration='schoolConcentration', isCurrent=False, startYear='1994', endYear='2000')

    new_educ.post()

Remove
^^^^^^
Remove via the node method::

    node.remove_education(customer_id='c_id', education_id='education_id')

or directly by the object::

    education.delete()

Update
^^^^^^

After some changes on a `Education`::

    my_education = node.get_education(customer_id='c_id', education_id='education_id')
    my_education.schoolConcentration = 'updated'

you can update it via the node method::

    node.update_education(customer_id='c_id', **my_education.to_dict())

or directly by the object::

    my_education.put()

Job
---
Get
^^^
You can get a job associated to a customer by the customer ID and a job ID::

    customer_job = node.get_job(customer_id='c_id', job_id='job_id')

This method creates a `Job` object.

Add
^^^

Add via the node method, creating a new `Job` object::

    new_job = node.add_job(customer_id='123', id='01', jobTitle='jobTitle', companyName='companyName',
    companyIndustry='companyIndustry', isCurrent=True, startDate='1994-10-06', endDate='1994-10-06')

or directly by the object::

    new_job = Job(customer=my_customer, id='01', jobTitle='jobTitle', companyName='companyName', companyIndustry='companyIndustry',
    isCurrent=True, startDate='1994-10-06', endDate='1994-10-06')

    new_job.post()

Remove
^^^^^^

Remove via the node method::

    node.remove_job(customer_id='c_id', job_id='job_id')

or directly by the object::

    job.delete()

Update
^^^^^^

After some changes on a `Job`::

    my_job = node.get_job(customer_id='c_id', job_id='job_id')
    my_job.jobTitle = 'updated'

you can update it via the node method::

    node.update_job(customer_id='c_id', **my_job.to_dict())

or directly by the object::

    my_job.put()

Like
----
Get
^^^
You can get a like associated to a customer by the customer ID and a like ID::

    my_like = node.get_like(customer_id='c_id', like_id='like_id')

This method creates a `Like` object.

Add
^^^
Add via the node method, creating a new `Like` object::

    new_like= node.add_like(customer_id='123', id='01', name='name', category='category',
    createdTime=datetime.now())

or directly by the object::

    new_like = Like(customer=my_customer, id='01', name='name', category='category', createdTime=datetime.now())

    new_like.post()

Remove
^^^^^^
Remove via the node method::

    node.remove_like(customer_id='c_id', like_id='like_id')

or directly by the object::

    like.delete()

Update
^^^^^^

After some changes on a `Like`::

    my_like = node.get_like(customer_id='c_id', like_id='like_id')
    my_like.name = 'updated'

you can update it via the node method::

    node.update_like(customer_id='c_id', **my_like.to_dict())

or directly by the object::

    my_like.put()

Subscription
------------

Get
^^^
You can get a subscription associated to a customer by the customer ID and a subscription ID previously assigned to the
subscription::

    customer_sub = node.get_subscription(customer_id='c_id', subscription_id='subscription_id')

Add
^^^
Add via the node method, creating a new `Subscription` object::

    new_sub = node.add_subscription(customer_id='01', id='02', name='name', kind=Subscription.KINDS.SERVICE,
    subscriberId='id', subscribed=True, preferences=[{'key':'value'}])

or directly by the object::

    new_sub = Subscription(customer=my_customer, id='02', name='name', kind=Subscription.KINDS.SERVICE,
    subscriberId='id', subscribed=True, preferences=[{'key':'value'}])

    new_sub.post()

Remove
^^^^^^
Remove via the node method::

    node.remove_subscription(customer_id='c_id', subscription_id='subscription_id')

or directly by the object::

    subscription.delete()

Update
^^^^^^

After some changes on a `Subscription`::

    my_sub = node.get_subscription(customer_id='c_id', subscription_id='subscription_id')
    my_sub.name = 'updated'

you can update it via the node method::

    node.update_subscription(customer_id='c_id', **my_sub.to_dict())

or directly by the object::

    my_sub.put()
