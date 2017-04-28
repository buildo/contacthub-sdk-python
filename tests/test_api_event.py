import json
import unittest

import mock
from datetime import datetime
from requests import HTTPError

from contacthub._api_manager._api_event import _EventAPIManager
from contacthub.models.event import Event
from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestEventAPIManager(unittest.TestCase):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.event_manager = _EventAPIManager(w.get_node(123))
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/events'


    @classmethod
    def tearDown(cls):
        pass

    if __name__ == '__main__':
        unittest.main()

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_get_all_events(self, mock_get_all):
        params_expected = {'customerId': '123'}
        resp = self.event_manager.get_all(customer_id="123")
        mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)
        assert type(resp) is dict, type(resp)
        assert 'elements' in resp, resp
        assert type(resp['elements']) is list, type(resp['elements'])

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response", status_code=401))
    def test_get_all_events_unauthorized(self, mock_get_all):
        params_expected = {'customerId': '123'}
        try:
            self.event_manager.get_all(customer_id="123")
        except HTTPError as e:
            mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_get_all_events_type(self, mock_get_all):
        params_expected = {'customerId': '123', 'type':'type'}
        resp = self.event_manager.get_all(customer_id="123", type='type')
        mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_get_all_events_context(self, mock_get_all):
        params_expected = {'customerId': '123', 'context': 'context'}
        resp = self.event_manager.get_all(customer_id="123", context='context')
        mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_get_all_events_mode(self, mock_get_all):
        params_expected = {'customerId': '123', 'mode': 'mode'}
        resp = self.event_manager.get_all(customer_id="123", mode='mode')
        mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_get_all_events_dateFrom_dateTo(self, mock_get_all):
        params_expected = {'customerId': '123', 'dateFrom': '2000-01-01T00:00:00Z', 'dateTo':'2010-01-01T00:00:00Z'}
        resp = self.event_manager.get_all(customer_id="123", dateFrom=datetime(2000,1,1), dateTo=datetime(2010,1,1))
        mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_get_all_events_dateFrom_dateTo_str(self, mock_get_all):
        params_expected = {'customerId': '123', 'dateFrom': '2000-01-01T00:00:00Z', 'dateTo': '2010-01-01T00:00:00Z'}
        resp = self.event_manager.get_all(customer_id="123", dateFrom='2000-01-01T00:00:00Z', dateTo='2010-01-01T00:00:00Z')
        mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_get_all_events_page_size(self, mock_get_all):
        params_expected = {'customerId': '123', 'page': 1, 'size': 2}
        resp = self.event_manager.get_all(customer_id="123", page=1, size=2)
        mock_get_all.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_get(self, mock_get):
        self.event_manager.get(_id='01')
        mock_get.assert_called_with(self.base_url + '/01', headers=self.headers_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response", status_code=400))
    def test_get_error(self, mock_get):
        try:
            self.event_manager.get(_id='01')
        except HTTPError as e:
            assert 'Message' in str(e)

    @mock.patch('requests.post',
                return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response"))
    def test_post(self, mock_post):
        self.event_manager.post(body={'a':'b'})
        mock_post.assert_called_with(self.base_url, headers=self.headers_expected, json={'a':'b'})

    @mock.patch('requests.post',
                return_value=FakeHTTPResponse(resp_path="tests/util/fake_event_response", status_code=400))
    def test_post_error(self, mock_post):
        try:
            self.event_manager.post(body={'a': 'b'})
        except HTTPError as e:
            mock_post.assert_called_with(self.base_url, headers=self.headers_expected, json={'a': 'b'})
            assert 'Message' in str(e)




