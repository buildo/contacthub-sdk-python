import json
from unittest import TestSuite

import mock
from datetime import datetime

from contacthub.errors.operation_not_permitted import OperationNotPermitted
from contacthub.lib.paginated_list import PaginatedList
from contacthub.models.education import Education
from contacthub.models.event import Event
from contacthub.models.job import Job
from contacthub.models.like import Like
from contacthub.models.properties import Properties
from contacthub.models.customer import Customer
from contacthub.models.subscription import Subscription
from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestNode(TestSuite):
    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id=123, token=456)
        cls.node = w.get_node(123)
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        cls.base_events_url = 'https://api.contactlab.it/hub/v1/workspaces/123/events'

    @classmethod
    def tearDown(cls):
        pass

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_customers(self, mock_get):
        customers = self.node.get_customers()

        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        params_expected = {'nodeId': '123'}
        mock_get.assert_called_with(base_url, params=params_expected, headers=self.headers_expected)
        assert type(customers) is PaginatedList, type(customers)
        assert customers[0].enabled, customers[0]

    @mock.patch('requests.get')
    def test_query(self, mock_get):
        mock_get.return_value = FakeHTTPResponse(resp_path='tests/util/fake_query_response')
        query_expected = {'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'composite', 'conditions': [
                         {'type': 'atomic', 'attribute': 'base.contacts.email', 'operator': 'EQUALS',
                          'value': 'marco.bosio@axant.it'},
                         {'type': 'atomic', 'attribute': 'extra', 'operator': 'EQUALS',
                          'value': 'Ciao'}
                     ], 'conjunction': 'and'}
                 }
             }
                          }

        customers_query = self.node.query(Customer).filter(
            (Customer.base.contacts.email == 'marco.bosio@axant.it') & (Customer.extra == 'Ciao')).all()
        params_expected = {'nodeId': '123', 'query': json.dumps(query_expected)}
        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'

        mock_get.assert_called_with(base_url, params=params_expected, headers=self.headers_expected)

        assert customers_query[0].base.contacts.email == 'marco.bosio@axant.it', customers_query[0].base.contacts.email
        assert customers_query[0].extra == 'Ciao', customers_query[0].extra

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_customer(self, mock_get):
        customers = self.node.get_customer(id='01')
        self.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers/01'
        mock_get.assert_called_with(base_url, headers=self.headers_expected)

    def test_get_customer_id_external(self):
        try:
            customers = self.node.get_customer(id='01', external_id='03')
            assert False
        except ValueError as e:
            assert 'id' in str(e), str(e)

    def test_get_customer_not_id_external(self):
        try:
            customers = self.node.get_customer()
            assert False
        except ValueError as e:
            assert 'id' in str(e), str(e)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_get_customer_external_id(self, mock_get):
        customers = self.node.get_customer(external_id='01')
        self.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        mock_get.assert_called_with(base_url, headers=self.headers_expected,
                                    params={'externalId': '01', 'nodeId': '123'})
        assert isinstance(customers, list), type(customers)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_external_single_response'))
    def test_get_customer_external_id_single(self, mock_get):
        customers = self.node.get_customer(external_id='01')
        assert isinstance(customers, Customer), type(customers)
        self.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        mock_get.assert_called_with(base_url, headers=self.headers_expected,
                                    params={'externalId': '01', 'nodeId': '123'})

    @mock.patch('requests.delete', return_value=FakeHTTPResponse())
    def test_delete_customer(self, mock_get):
        c = Customer(node=self.node, id='01')
        self.node.delete_customer(c.id)
        mock_get.assert_called_with(self.base_url + '/01', headers=self.headers_expected)

    @mock.patch('requests.post', return_value=FakeHTTPResponse())
    def test_add_customer(self, mock_get):
        c = Customer(node=self.node, base=Properties(contacts=Properties(email='email')))
        self.node.add_customer(**c.to_dict())
        body = {'nodeId': self.node.node_id, 'base': {'contacts': {'email': 'email'}}, 'extended': {},
                'tags': {'auto': [], 'manual': []}, 'consents':{}}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, json=body)

    @mock.patch('requests.post', return_value=FakeHTTPResponse())
    def test_add_customer_extended(self, mock_get):
        c = Customer(node=self.node, base=Properties(contacts=Properties(email='email')))
        c.extended.prova = 'prova'
        self.node.add_customer(**c.to_dict())
        body = {'nodeId': self.node.node_id, 'base': {'contacts': {'email': 'email'}}, 'extended': {'prova': 'prova'},
                'tags': {'auto': [], 'manual': []}, 'consents':{}}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, json=body)

    @mock.patch('requests.post', return_value=FakeHTTPResponse())
    def test_add_customer_tags(self, mock_get):
        c = Customer(node=self.node, base=Properties(contacts=Properties(email='email')))
        c.extended.prova = 'prova'
        c.tags.auto = ['auto']
        c.tags.manual = ['manual']
        self.node.add_customer(**c.to_dict())
        body = {'nodeId': self.node.node_id, 'base': {'contacts': {'email': 'email'}}, 'extended': {'prova': 'prova'},
                'tags': {'auto': ['auto'], 'manual': ['manual']}, 'consents':{}}
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse())
    def test_update_customer_not_full(self, mock_patch):
        c = Customer(node=self.node, id='01', base=Properties(contacts=Properties(email='email')))
        c.extra = 'extra'
        self.node.update_customer(c.id, **c.get_mutation_tracker())
        body = {'extra': 'extra'}
        mock_patch.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)

    @mock.patch('requests.put', return_value=FakeHTTPResponse())
    def test_update_customer_full(self, mock_get):
        c = Customer(node=self.node, id='01', base=Properties(contacts=Properties(email='email', fax='fax')))
        c.base.contacts.email = 'email1234'
        self.node.update_customer(full_update=True, **c.to_dict())
        body = {'id': '01', 'base': {'contacts': {'email': 'email1234', 'fax': 'fax'}}, 'extended': {},
                'tags': {'auto': [], 'manual': []}, 'consents':{}}
        mock_get.assert_called_with(self.base_url + '/01', headers=self.headers_expected, json=body)

    @mock.patch('requests.post',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_session_response'))
    def test_add_customer_session(self, mock_get):
        s_id = self.node.create_session_id()
        body = {'value': str(s_id)}
        self.node.add_customer_session(session_id=s_id, customer_id='01')
        mock_get.assert_called_with(self.base_url + '/01/sessions', headers=self.headers_expected, json=body)

    @mock.patch('requests.get',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_add_tag(self, mock_patch, mock_get):
        self.node.add_tag(customer_id='b6023673-b47a-4654-a53c-74bbc0204a20', tag='tag1')
        mock_get.assert_called_with(self.base_url + '/b6023673-b47a-4654-a53c-74bbc0204a20',
                                    headers=self.headers_expected)
        mock_patch.assert_called_with(self.base_url + '/b6023673-b47a-4654-a53c-74bbc0204a20',
                                      headers=self.headers_expected, json={'tags': {'manual': ['manual', 'tag1']}})

    @mock.patch('requests.get',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_remove_tag(self, mock_patch, mock_get):
        self.node.remove_tag(customer_id='b6023673-b47a-4654-a53c-74bbc0204a20', tag='manual')
        mock_get.assert_called_with(self.base_url + '/b6023673-b47a-4654-a53c-74bbc0204a20',
                                    headers=self.headers_expected)
        mock_patch.assert_called_with(self.base_url + '/b6023673-b47a-4654-a53c-74bbc0204a20',
                                      headers=self.headers_expected, json={'tags': {'manual': []}})

    @mock.patch('requests.get',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    @mock.patch('requests.patch',
                return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_remove_tag_unexistent(self, mock_patch, mock_get):

        try:
            self.node.remove_tag(customer_id='b6023673-b47a-4654-a53c-74bbc0204a20', tag='asd')
            mock_get.assert_called_with(self.base_url + '/b6023673-b47a-4654-a53c-74bbc0204a20',
                                        headers=self.headers_expected)
        except ValueError as e:
            assert 'Tag' in str(e), str(e)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_job_response'))
    def test_add_job(self, mock_post, mock_get):
        j = self.node.add_job(customer_id='123', jobTitle='jobTitle', companyName='companyName',
                              companyIndustry='companyIndustry', isCurrent=True, id='01', startDate='1994-10-06',
                              endDate='1994-10-06')
        assert isinstance(j, Job), type(j)
        assert j.isCurrent, j.isCurrent
        mock_post.assert_called_with(self.base_url + '/123/jobs', headers=self.headers_expected,
                                     json=dict(jobTitle='jobTitle', companyName='companyName',
                                               companyIndustry='companyIndustry', isCurrent=True, id='01',
                                               startDate='1994-10-06',
                                               endDate='1994-10-06'))

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_subscription_response'))
    def test_add_subscription(self, mock_post, mock_get):
        s = self.node.add_subscription(customer_id='123', id='01', name='name', kind='SERVICE')
        assert isinstance(s, Subscription), type(s)
        assert s.id == '01'
        mock_post.assert_called_with(self.base_url + '/123/subscriptions', headers=self.headers_expected,
                                     json=dict(id='01', name='name', kind='SERVICE'))

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_add_education(self, mock_post, mock_get):
        e = self.node.add_education(customer_id='123', id='01', schoolType='schoolType', schoolName='schoolName',
                                    schoolConcentration='schoolConcentration', isCurrent=True,
                                    startYear='1994',
                                    endYear='2000')
        assert isinstance(e, Education), type(e)
        assert e.isCurrent, e.isCurrent
        mock_post.assert_called_with(self.base_url + '/123/educations', headers=self.headers_expected,
                                     json=dict(schoolType='schoolType', schoolName='schoolName',
                                               schoolConcentration='schoolConcentration', isCurrent=True, id='01',
                                               startYear='1994',
                                               endYear='2000'))

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_like_response'))
    def test_add_like(self, mock_post, mock_get):
        now = datetime.now()
        now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        l = self.node.add_like(customer_id='123', name='name', category='category',
                               createdTime=now, id='01')
        assert isinstance(l, Like), type(l)
        assert l.name == 'name', l.name
        mock_post.assert_called_with(self.base_url + '/123/likes', headers=self.headers_expected,
                                     json=dict(name='name', category='category',
                                               createdTime=now_s, id='01'))

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path=None))
    def test_remove_job(self, mock_delete):
        self.node.remove_job(customer_id='01', job_id='02')
        mock_delete.assert_called_with(self.base_url + '/01/jobs/02', headers=self.headers_expected)

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path=None))
    def test_remove_subscription(self, mock_delete):
        self.node.remove_subscription(customer_id='01', subscription_id='02')
        mock_delete.assert_called_with(self.base_url + '/01/subscriptions/02', headers=self.headers_expected)

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path=None))
    def test_remove_education(self, mock_delete):
        self.node.remove_education(customer_id='01', education_id='02')
        mock_delete.assert_called_with(self.base_url + '/01/educations/02', headers=self.headers_expected)

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path=None))
    def test_remove_like(self, mock_delete):
        self.node.remove_like(customer_id='01', like_id='02')
        mock_delete.assert_called_with(self.base_url + '/01/likes/02', headers=self.headers_expected)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_like_response'))
    def test_update_like(self, mock_put, mock_get):
        now = datetime.now()
        now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        l1 = Like(name='name', category='category1',
                  createdTime=now, id='01', customer=Customer(node=self.node, id='123'))
        l = self.node.update_like(customer_id='123', **l1.to_dict())
        assert isinstance(l, Like), type(l)
        assert l.name == 'name', l.name
        mock_put.assert_called_with(self.base_url + '/123/likes/01', headers=self.headers_expected,
                                    json=dict(name='name', category='category1',
                                              createdTime=now_s))

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_update_education(self, mock_post, mock_get):
        e1 = Education(schoolType='schoolType1', schoolName='schoolName1',
                       schoolConcentration='schoolConcentration1', isCurrent=True, id='01',
                       startYear='1994',
                       endYear='2000', customer=Customer(node=self.node, id='123'))
        e = self.node.update_education(customer_id='123', **e1.to_dict())
        assert isinstance(e, Education), type(e)
        assert e.isCurrent, e.isCurrent
        mock_post.assert_called_with(self.base_url + '/123/educations/01', headers=self.headers_expected,
                                     json=dict(schoolType='schoolType1', schoolName='schoolName1',
                                               schoolConcentration='schoolConcentration1', isCurrent=True,
                                               startYear='1994',
                                               endYear='2000'))

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_update_subscription(self, mock_post, mock_get):
        s1 = Subscription(name='name', kind='SERVICE', id='01', customer=Customer(node=self.node, id='123'))
        s = self.node.update_subscription(customer_id='123', **s1.to_dict())
        assert isinstance(s, Subscription), type(s)
        assert s.id == '01', s.id
        mock_post.assert_called_with(self.base_url + '/123/subscriptions/01', headers=self.headers_expected,
                                     json=dict(name='name', kind='SERVICE'))

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_job_response'))
    def test_update_job(self, mock_post, mock_get):
        j1 = Job(jobTitle='jobTitle1', companyName='companyName',
                 companyIndustry='companyIndustry1', isCurrent=True, id='01', startDate='1994-10-06',
                 endDate='1994-10-06', customer=Customer(node=self.node, id='123'))
        j = self.node.update_job(customer_id='123', **j1.to_dict())
        assert isinstance(j, Job), type(j)
        assert j.isCurrent, j.isCurrent
        mock_post.assert_called_with(self.base_url + '/123/jobs/01', headers=self.headers_expected,
                                     json=dict(jobTitle='jobTitle1', companyName='companyName',
                                               companyIndustry='companyIndustry1', isCurrent=True,
                                               startDate='1994-10-06',
                                               endDate='1994-10-06'))

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_event_response'))
    def test_get_all_events(self, mock_get):
        e = self.node.get_events(customer_id='8b321dce-53c4-4029-8388-1938efa2090c')
        mock_get.assert_called_with(self.base_events_url, headers=self.headers_expected, params={'customerId':'8b321dce-53c4-4029-8388-1938efa2090c'})
        assert isinstance(e, list), type(e)
        assert e[0].customerId =='8b321dce-53c4-4029-8388-1938efa2090c', e[0].customerId

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_single_event_response'))
    def test_get_event(self, mock_get):
        e = self.node.get_event(id='123')
        mock_get.assert_called_with(self.base_events_url + '/123', headers=self.headers_expected)
        assert isinstance(e, Event), type(e)
        assert e.customerId == '46cf4766-770b-4e2f-b5e2-c82273e45ab9', e.customerId

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_job_response'))
    def test_get_job(self, mock_get):
        j = self.node.get_customer_job(customer_id='123', job_id='456')
        mock_get.assert_called_with(self.base_url + '/123/jobs/456', headers=self.headers_expected)
        assert isinstance(j, Job), type(j)
        assert j.companyIndustry == 'companyIndustry', j.companyIndustry

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_subscription_response'))
    def test_get_subscription(self, mock_get):
        s = self.node.get_customer_subscription(customer_id='123', subscription_id='456')
        mock_get.assert_called_with(self.base_url + '/123/subscriptions/456', headers=self.headers_expected)
        assert isinstance(s, Subscription), type(s)
        assert s.preferences[0].key == 'key', s.preferences[0].key

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_like_response'))
    def test_get_like(self, mock_get):
        l = self.node.get_customer_like(customer_id='123', like_id='456')
        mock_get.assert_called_with(self.base_url + '/123/likes/456', headers=self.headers_expected)
        assert isinstance(l, Like), type(l)
        assert l.name == 'name', l.name

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_get_education(self, mock_get):
        e = self.node.get_customer_education(customer_id='123', education_id='456')
        mock_get.assert_called_with(self.base_url + '/123/educations/456', headers=self.headers_expected)
        assert isinstance(e, Education), type(e)
        assert e.schoolType == Education.SCHOOL_TYPES.COLLEGE, e.schoolType

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_single_event_response'))
    def test_post_event(self, mock_post):
        self.node.add_event(a=[Properties(a='b')], b='c', d=Properties(f='g', h=Properties(i='j')),
                            k=dict(l=Properties(m='n', o='p')))

        mock_post.assert_called_with(self.base_events_url, headers=self.headers_expected,
                                     json={'a': [{'a': 'b'}], 'b': 'c', 'd':
                                         {'f': 'g', 'h': {'i': 'j'}}, 'k': {'l': {'m': 'n', 'o': 'p'}}})

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_single_event_response'))
    def test_post_event_dict(self, mock_post):
        self.node.add_event(**{'a': [{'a': 'b'}], 'b': 'c', 'd':
                                         {'f': 'g', 'h': {'i': 'j'}}, 'k': {'l': {'m': 'n', 'o': 'p'}}})
        mock_post.assert_called_with(self.base_events_url, headers=self.headers_expected,
                                     json={'a': [{'a': 'b'}], 'b': 'c', 'd': {'f': 'g', 'h': {'i': 'j'}},
                                           'k': {'l': {'m': 'n', 'o': 'p'}}})

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_customer_paginated(self, mock_get):
        l = self.node.get_customers().next_page()
        assert isinstance(l, PaginatedList), type(l)
        params_expected = {'nodeId': '123', 'page': 1}
        mock_get.assert_called_with(self.base_url, params=params_expected, headers=self.headers_expected)
        assert isinstance(l[0], Customer), type(l[0])

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_response_page'))
    def test_customer_paginated_exception(self, mock_get):
        try:
            l = self.node.get_customers().next_page().next_page().next_page()
        except OperationNotPermitted as e:
            assert 'Last page reached' in str(e), str(e)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_customer_paginated_exception_prev(self, mock_get):
        try:
            l = self.node.get_customers().previous_page()
        except OperationNotPermitted as e:
            assert 'First page reached' in str(e), str(e)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_response_page_prev'))
    def test_customer_paginated_prev(self, mock_get):
        l = self.node.get_customers().previous_page()
        assert isinstance(l, PaginatedList), type(l)
        params_expected = {'nodeId': '123'}
        mock_get.assert_called_with(self.base_url, params=params_expected, headers=self.headers_expected)
        assert isinstance(l[0], Customer), type(l[0])
        assert l.size == 10, l.size
