import mock
from contacthub.workspace import Workspace
from unittest import TestSuite

from tests.utility import FakeHTTPResponse


class TestWorkspace(TestSuite):

    @classmethod
    def setUp(cls):
        cls.workspace_id = '123'
        cls.node_id = '456'
        cls.token = 'abc'


    @classmethod
    def tearDown(cls):
        pass

    def test_workspace_from_ini_file(self):
        w = Workspace.from_ini_file('tests/util/config.ini')
        assert w.workspace_id == str(123), w.workspace_id
        assert w.token == str(456), w.token

    def test_workspace_from_incorrect_ini_file(self):
        try:
            w = Workspace.from_ini_file('tests/util/wrong_config.ini')
        except KeyError as e:
            assert e.args[0] == 'workspace_id or token parameter not found in INI file', e.message

    def test_workspace_from_unexistent_ini_file(self):
        try:
            w = Workspace.from_ini_file('file')
        except IOError as e:
            assert 'No such file or directory' == e.args[1], e.args[1]

    def test_workspace_from_ini_file_base_url(self):
        w = Workspace.from_ini_file('tests/util/config_base.ini')
        assert w.workspace_id == str(123), w.workspace_id
        assert w.token == str(456), w.token
        assert w.base_url == 'http', w.base_url

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_node(self, mock_get):
        w = Workspace(workspace_id=self.workspace_id, token=self.token)
        n = w.get_node(self.node_id).get_customers()
        node_in_req = mock_get.call_args[1]['params']['nodeId']
        assert node_in_req == self.node_id, node_in_req

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_node_with_int_param(self, mock_get):
        w = Workspace(workspace_id=self.workspace_id, token=self.token)
        n = w.get_node(1).get_customers()
        assert mock_get.call_args[1]['params']['nodeId'] == '1', mock_get.call_args[1]['params']['nodeId']

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_workspace(self, mock_get):
        w = Workspace(workspace_id=self.workspace_id, token=self.token)
        n = w.get_node(self.node_id).get_customers()
        authorization = mock_get.call_args[1]['headers']['Authorization']
        request_url = mock_get.call_args[0][0]
        assert authorization == 'Bearer ' + self.token, authorization
        assert self.workspace_id in request_url, request_url

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_workspace_with_int_params(self, mock_get):
        w = Workspace(workspace_id=1, token=2)
        n = w.get_node(3).get_customers()
        authorization = mock_get.call_args[1]['headers']['Authorization']
        request_url = mock_get.call_args[0][0]
        assert authorization == 'Bearer 2', authorization
        assert '1' in request_url, request_url




