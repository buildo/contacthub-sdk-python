import unittest

import mock

from contacthub.models.customer import Customer
from contacthub.models.subscription import Subscription
from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestSubscription(unittest.TestCase):
    @classmethod
    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def setUp(cls, mock_get_customers):
        w = Workspace(workspace_id="123", token="456")
        cls.node = w.get_node("123")
        cls.customers = cls.node.get_customers()
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url_customer = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        cls.customer = Customer(id='01', node=cls.node)
        cls.subscription = Subscription(customer=cls.customer, **{'id': '01'})

    @classmethod
    def tearDown(cls):
        pass

    def test_from_dict_no_attr(self):
        e = Subscription.from_dict(customer=self.customer)
        assert e.attributes == {}, e.attributes

    def test_set_job(self):
        self.subscription.name = "name"
        assert self.subscription.name == "name", self.subscription.name

    def test_to_dict(self):
        self.subscription.name = "name"
        assert self.subscription.to_dict() == {'id': '01', 'name': 'name'}

    def test_get_list(self):
        s = Subscription(customer=self.customer, **{'id': '01'})
        s.preferences = ['a']
        assert s.preferences == ['a'], s.preferences

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_customer_subscription(self, mock_get):
        customers = self.node.get_customers()
        assert customers[0].base.subscriptions[0].a == ['a'], customers[0].base.subscriptions[0].a

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_customer_mute_subscription(self, mock_get):
        customers = self.node.get_customers()
        customers[0].base.subscriptions[0].kind = 'kind'
        assert customers[0].mute == {'base.subscriptions': [{'id': '01', 'name': 'name', 'type': 'type',
                                                                 'kind': 'kind', 'subscribed': True,
                                                                 'startDate': '1994-10-06', 'endDate': '1994-10-10',
                                                                 'subscriberId': 'subscriberId',
                                                                 'registeredAt': '1994-10-06',
                                                                 'updatedAt': '1994-10-06',
                                                                 'preferences': [{'key': 'key', 'value': 'value'}],
                                                                 'a': ['a']}]}, customers[0].mute

    def test_set_subscription_customer_add(self):
        self.customers[0].base.subscriptions[0].name = 'name1'
        self.customers[0].base.subscriptions += [Subscription(customer=self.customers[0], id='02')]

        mute = {'base.subscriptions': [{'id': '01', 'name': 'name1', 'type': 'type',
                                            'kind': 'SERVICE', 'subscribed': True,
                                            'startDate': '1994-10-06', 'endDate': '1994-10-10',
                                            'subscriberId': 'subscriberId',
                                            'registeredAt': '1994-10-06',
                                            'updatedAt': '1994-10-06',
                                            'preferences': [{'key': 'key', 'value': 'value'}],
                                            'a': ['a']}, {'id': '02'}]}
        assert self.customers[0].mute == mute, self.customers[0].mute

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_subscription_response'))
    def test_post_job(self, mock_post):
        s = Subscription(customer=self.customer, id='01', name='name', type='type', kind='SERVICE', subscribed=True,
                         startDate='1994-10-06', endDate='1994-10-10', subscriberId='subscriberId',
                         preferences=[{'key': 'key', 'value': 'value'}])
        s.post()

        mock_post.assert_called_with(self.base_url_customer + '/' + self.customer.id + '/subscriptions',
                                     headers=self.headers_expected,
                                     json=s.attributes)
        assert self.customer.base.subscriptions[0].attributes == s.attributes, \
            (self.customer.base.subscriptions[0].attributes, s.attributes)

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_subscription_response'))
    def test_post_job_create_base(self, mock_post):
        c = Customer(node=self.node, default_attributes={}, id='01')
        s = Subscription(customer=c, id='01', name='name', type='type', kind='SERVICE', subscribed=True,
                         startDate='1994-10-06', endDate='1994-10-10', subscriberId='subscriberId',
                         preferences=[{'key': 'key', 'value': 'value'}])
        s.post()

        mock_post.assert_called_with(self.base_url_customer + '/' + c.id + '/subscriptions',
                                    headers=self.headers_expected,
                                    json=s.attributes)
        assert c.base.subscriptions[0].attributes == s.attributes, (c.base.subscriptions[0].attributes, s.attributes)

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path='tests/util/fake_job_response'))
    def test_delete(self, mock_post):
        s = Subscription(customer=self.customer, id='01')
        s.delete()
        mock_post.assert_called_with(self.base_url_customer + '/' + self.customer.id + '/subscriptions/01',
                                    headers=self.headers_expected)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_subscription_response'))
    def test_put(self, mock_post):
        self.customer.base.subscriptions = [self.subscription]
        self.subscription.name = 'name'
        self.subscription.type = 'type'
        self.subscription.kind = 'SERVICE'
        self.subscription.subscriberId = 'subscriberId'
        self.subscription.startDate = '1994-10-06'
        self.subscription.endDate = '1994-10-10'
        self.subscription.subscribed = True
        self.subscription.preferences = [{'key': 'key', 'value': 'value'}]

        self.subscription.put()
        mock_post.assert_called_with(self.base_url_customer + '/' + self.customer.id + '/subscriptions/01',
                                    headers=self.headers_expected, json=self.subscription.attributes)
        assert self.customer.base.subscriptions[0].attributes == self.subscription.attributes,  (self.customer.base.subscriptions[0].attributes,
                                                                               self.subscription.attributes)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_subscription_response'))
    def test_put_no_subscriptions(self, mock_post):
        self.subscription.name = 'name'
        self.subscription.type = 'type'
        self.subscription.kind = 'kind'
        self.subscription.subscriberId = 'subscriberId'
        self.subscription.startDate = '1994-10-06'
        self.subscription.endDate = '1994-10-10'
        self.subscription.subscribed = True
        self.subscription.preferences = [{'key': 'key', 'value': 'value'}]
        try:
            self.subscription.put()
        except ValueError as e:
            assert 'Subscription' in str(e)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_put_no(self, mock_post):
        self.customer.base.subscriptions = [self.subscription]
        subscription = Subscription(customer=self.customer, id='03')
        subscription.name = 'name'
        subscription.type = 'type'
        subscription.kind = 'kind'
        subscription.subscriberId = 'subscriberId'
        subscription.startDate = '1994-10-06'
        subscription.endDate = '1994-10-10'
        subscription.subscribed = True
        subscription.preferences = [{'key': 'key', 'value': 'value'}]
        try:
            subscription.put()
        except ValueError as e:
            assert 'Subscription' in str(e)
