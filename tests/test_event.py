import unittest

import mock

from contacthub.lib.paginated_list import PaginatedList
from contacthub.lib.read_only_list import ReadOnlyList
from contacthub.models import properties, Properties
from contacthub.models.event import Event
from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestEvent(unittest.TestCase):
    @classmethod
    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_event_response'))
    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def setUp(cls, mock_get_customers, mock_get_events):
        w = Workspace(workspace_id="123", token="456")
        cls.node = w.get_node("123")
        cls.customer = cls.node.get_customers()[0]
        cls.events = cls.customer.get_events()
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/events'
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}

    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_event_response'))
    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_event_from_customers(self, mock_get_customers, mock_get_events):
        events = self.node.get_customers()[0].get_events()
        assert isinstance(events, PaginatedList), type(events)
        assert isinstance(events[0], Event), type(events[0])
        try:
            events.append(Event(node=self.node))
        except ValueError as e:
            assert 'Read Only' in str(e)

    def test_get_properties(self):
        prop = self.events[0].properties
        assert isinstance(prop, Properties), type(prop)

    def test_get_unexsistent(self):
        try:
            prop = self.events[0].attr
        except AttributeError as e:
            assert 'attr' in str(e), str(e)

    def test_create_new_event_properties(self):
        e = Event(node=self.node)
        e.properties = Properties(attr='attr')
        assert isinstance(e.properties, Properties), type(e.properties)

    def test_set_event_properties(self):
        e = self.events[0]
        assert isinstance(e.properties, Properties)
        e.context = Event.CONTEXTS.DIGITAL_CAMPAIGN
        assert e.context == Event.CONTEXTS.DIGITAL_CAMPAIGN, e.context

    def test_event_from_dict_void(self):
        e = Event.from_dict(node=self.node)
        assert e.attributes == {}, e.attributes

    def test_event_from_dict(self):
        d = {}
        e = Event.from_dict(node=self.node, attributes=d)
        assert e.attributes is d, (e.attributes, d)

    def test_to_dict(self):
        e = Event(node=self.node, a=Properties(b=Properties(c=Properties(d=Properties(e='f')))))
        assert e.to_dict() == {'a': {'b': {'c': {'d': {'e': 'f'}}}}}, e.to_dict()

    def test_list_properies(self):
        e = Event(node=self.node)
        e.a = [Properties(a='b')]
        assert e.attributes == {'a': [{'a': 'b'}]}, e.attributes

    def test_list_properies_constructor(self):
        e = Event(node=self.node, a=[Properties(a='b')])
        assert e.attributes == {'a': [{'a': 'b'}]}, e.attributes

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_event_response'))
    def test_post(self, mock_post):
        e = Event(node=self.node, a=[Properties(a='b')], b='c', d=Properties(f='g', h=Properties(i='j')),
                  k=dict(l=Properties(m='n', o='p')))
        e.post()
        mock_post.assert_called_with(self.base_url, headers=self.headers_expected,
                                     json={'a': [{'a': 'b'}], 'b': 'c', 'd':
                                         {'f': 'g', 'h': {'i': 'j'}}, 'k': {'l': {'m': 'n', 'o': 'p'}}})

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_event_response'))
    def test_post_bring_back(self, mock_post):
        e = Event(node=self.node, a=[Properties(a='b')], b='c', bringBackProperties=Properties(type='EXTERNAL_ID',
                                                                                               value='01'),
                  d=Properties(f='g', h=Properties(i='j')), k=dict(l=Properties(m='n', o='p')))
        e.post()
        mock_post.assert_called_with(self.base_url, headers=self.headers_expected,
                                     json={'bringBackProperties':{'type':'EXTERNAL_ID', 'value': '01',
                                                                  'nodeId':self.node.node_id},'a': [{'a': 'b'}],
                                           'b': 'c', 'd': {'f': 'g', 'h': {'i': 'j'}}, 'k': {'l': {'m': 'n',
                                                                                                   'o': 'p'}}})
