
from unittest import TestSuite

import mock
from requests import HTTPError
from contacthub.workspace import Workspace
from contacthub._api_manager._api_customer import _CustomerAPIManager
from tests.utility import FakeHTTPResponse


class TestCustomerAPIManager(TestSuite):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.node = w.get_node(123)
        cls.customer_manager = _CustomerAPIManager(node=cls.node)
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'


    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=200))
    def test_get_all_custumers(self, mock_get):
        params_expected = {'nodeId': '123'}
        resp = self.customer_manager.get_all()
        mock_get.assert_called_with(self.base_url, params=params_expected, headers=self.headers_expected)
        assert type(resp) is dict, type(resp)
        assert 'elements' in resp, resp

    @mock.patch('requests.get', return_value=FakeHTTPResponse(status_code=401))
    def test_get_customer_unathorized(self, mock_get):
        params_expected = {'nodeId': '123'}
        try:
            self.customer_manager.get_all()
        except HTTPError as e:
            mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_customer_extra(self, mock_get):
        params_expected = {'nodeId': '123'}
        self.customer_manager.get(_id='01', urls_extra='extra')
        mock_get.assert_called_with(self.base_url + '/01/extra', headers=self.headers_expected)


    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response'))
    def test_post_customer(self, mock_get):
        body = {'base': {'contacts': {'email': 'email@email.it'}}}
        data_expected = {'base': {'contacts': {'email': 'email@email.it'}}, 'nodeId': '123'}

        self.customer_manager.post(body=body)
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, json  =data_expected)

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response', status_code=401))
    def test_post_customer_unathorized(self, mock_get):
        try:
            self.customer_manager.post(body={})
        except HTTPError as e:
            assert 'Message' in str(e), str(e)

    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response', status_code=401))
    def test_patch_customer_unathorized(self, mock_get):
        try:
            self.customer_manager.patch(_id='id', body={})
        except HTTPError as e:
            assert 'Message' in str(e), str(e)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response'))
    def test_put_customer(self, mock_get):
        body = {'base': {'contacts': {'email': 'email@email.it'}}}

        self.customer_manager.put(_id='01', body=body)
        mock_get.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response', status_code=400))
    def test_put_customer_unauthorized(self, mock_get):
        try:
            self.customer_manager.put(_id='id', body={})
        except HTTPError as e:
            assert 'Message' in str(e), str(e)

    @mock.patch('requests.delete',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response'))
    def test_delete_extra_url(self, mock_delete):
        self.customer_manager.delete(_id="01", urls_extra='likes/02')
        mock_delete.assert_called_with(self.base_url + '/01/likes/02', headers=self.headers_expected)

    @mock.patch('requests.put',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_query_response'))
    def test_put_extra_url(self, mock_delete):
        self.customer_manager.put(_id="01", urls_extra='likes/02', body={})
        mock_delete.assert_called_with(self.base_url + '/01/likes/02', headers=self.headers_expected, json={})

    @mock.patch('requests.delete',
                return_value=FakeHTTPResponse(resp_path=None))
    def test_delete_null_response(self, mock_delete):
        a = self.customer_manager.delete(_id="01", urls_extra='likes/02')
        mock_delete.assert_called_with(self.base_url + '/01/likes/02', headers=self.headers_expected)
        assert not a, a

    @mock.patch('requests.get',
                return_value=FakeHTTPResponse())
    def test_get_all_external_id(self, mock_get):
        a = self.customer_manager.get_all(externalId='01')
        params_expected = {'nodeId': '123', 'externalId':'01'}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)

    @mock.patch('requests.get',
                return_value=FakeHTTPResponse())
    def test_get_all_page_size(self, mock_get):
        self.customer_manager.get_all(page=1, size=2)
        params_expected = {'nodeId': '123', 'page': 1, 'size':2}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)

    @mock.patch('requests.get',
                return_value=FakeHTTPResponse(status_code=400))
    def test_get_error(self, mock_get):
        try:
            self.customer_manager.get(_id='01')
        except HTTPError as e:
            assert 'Message' in str(e), str(e)

    @mock.patch('requests.get',
                return_value=FakeHTTPResponse())
    def test_get_all_fields(self, mock_get):
        self.customer_manager.get_all(fields=['a','b','c'])
        params_expected = {'nodeId': '123', 'fields': 'a,b,c'}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params_expected)














