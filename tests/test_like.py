import unittest

import mock

from contacthub.lib.read_only_list import ReadOnlyList
from contacthub.lib.utils import resolve_mutation_tracker
from contacthub.models import properties, Properties
from contacthub.models.customer import Customer
from contacthub.models.like import Like
from contacthub.models.event import Event
from contacthub.workspace import Workspace
from datetime import datetime
from tests.utility import FakeHTTPResponse


class TestLike(unittest.TestCase):

    @classmethod
    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def setUp(cls, mock_get_customers):
        w = Workspace(workspace_id="123", token="456")
        cls.node = w.get_node("123")
        cls.customers = cls.node.get_customers()
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url_customer = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        cls.customer = Customer(id='01', node=cls.node)
        cls.like = Like(customer=cls.customer, **{'id': 'id'})

    @classmethod
    def tearDown(cls):
        pass

    def test_from_dict_no_attr(self):
        e = Like.from_dict(customer=self.customer)
        assert e.attributes == {}, e.attributes

    def test_set_like(self):
        self.like.name = "name"
        assert self.like.name == "name", self.like.name

    def test_set_like_customer(self):
        self.customers[0].base.likes[0].name = 'name1'
        self.customers[0].base.likes[0].category = 'category1'

        like = self.customers[0].base.likes[0]

        mute = {'base.likes':
                             [{'name':'name1',
                               'category':'category1',
                               'id':'id',
                               'createdTime':'1994-02-11 14:05'}]}
        mute_res= {'base': {'likes':
                             [{'name':'name1',
                               'category':'category1',
                               'id':'id',
                               'createdTime':'1994-02-11 14:05'}]}}
        assert self.customers[0].mute == mute, self.customers[0].mute
        res = resolve_mutation_tracker(self.customers[0].mute)
        assert res == mute_res, res

    def test_set_like_customer_add(self):
        self.customers[0].base.likes[0].name = 'name1'
        self.customers[0].base.likes += [Like(customer=self.customers[0], id='01')]

        mute_res = {'base': {'likes': [
            {'name': 'name1',
             'category': 'category',
             'id': 'id',
             'createdTime': '1994-02-11 14:05'},
            {u'id': u'01'}
        ]
        }
        }
        mute = {'base.likes': [
            {'name': 'name1',
             'category': 'category',
             'id': 'id',
             'createdTime': '1994-02-11 14:05'},
            {u'id': u'01'}
        ]
        }

        assert self.customers[0].mute == mute, self.customers[0].mute
        res = resolve_mutation_tracker(self.customers[0].mute)
        assert res == mute_res, res


    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_like_response'))
    def test_post_like(self, mock_post):
        j = Like(customer=self.customer, id='id', category='category', name='name', createdTime='1994-02-11T14:05M')
        j.post()

        mock_post.assert_called_with(self.base_url_customer +'/' + self.customer.id + '/likes',
                                    headers=self.headers_expected,
                                    json=j.attributes)
        assert self.customer.base.likes[0].attributes == j.attributes, (self.customer.base.likes[0].attributes
                                                                       ,j.attributes)

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_like_response'))
    def test_post_like_create_base(self, mock_post):
        c = Customer(node=self.node, default_attributes={}, id='01')
        j = Like(customer=c, id='id', category='category', name='name', createdTime='1994-02-11T14:05M')
        j.post()

        mock_post.assert_called_with(self.base_url_customer +'/' + c.id + '/likes',
                                    headers=self.headers_expected,
                                     json=j.attributes)
        assert c.base.likes[0].attributes == j.attributes, (c.base.likes[0].attributes, j.attributes)

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path='tests/util/fake_like_response'))
    def test_delete(self, mock_post):
        j = Like(customer=self.customer, id='id')
        j.delete()
        mock_post.assert_called_with(self.base_url_customer +'/' +self.customer.id + '/likes/id',
                                    headers=self.headers_expected)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_like_response'))
    def test_put(self, mock_post):
        self.customer.base.likes = [self.like]
        self.like.name = 'name'
        self.like.category = 'category'
        self.like.createdTime = '1994-02-11T14:05M'

        self.like.put()
        mock_post.assert_called_with(self.base_url_customer +'/' + self.customer.id + '/likes/id',
                                    headers=self.headers_expected, json=self.like.attributes)
        assert self.customer.base.likes[0].attributes == self.like.attributes,  (self.customer.base.likes[0].attributes,
                                                                               self.like.attributes)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_put_no_likes(self, mock_post):
        self.like.name = 'name'
        self.like.category = 'category'
        self.like.cratedTime = '1994-02-11T14:05M'
        try:
            self.like.put()
        except ValueError as e:
            assert 'Like' in str(e)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_put_no_like(self, mock_post):
        self.customer.base.likes = [self.like]
        like = Like(customer=self.customer, id='03')
        like.name = 'name'
        like.category = 'category'
        like.cratedTime = '1994-02-11T14:05M'
        try:
            like.put()
        except ValueError as e:
            assert 'Like' in str(e)
