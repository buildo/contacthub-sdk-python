import unittest

import mock

from contacthub.lib.read_only_list import ReadOnlyList
from contacthub.lib.utils import resolve_mutation_tracker
from contacthub.models import properties, Properties
from contacthub.models.customer import Customer
from contacthub.models.job import Job
from contacthub.models.event import Event
from contacthub.workspace import Workspace
from datetime import datetime
from tests.utility import FakeHTTPResponse


class TestJob(unittest.TestCase):

    @classmethod
    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def setUp(cls, mock_get_customers):
        w = Workspace(workspace_id="123", token="456")
        cls.node = w.get_node("123")
        cls.customers = cls.node.get_customers()
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url_customer = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        cls.customer = Customer(id='01', node=cls.node)
        cls.job = Job(customer=cls.customer, **{'id': '01'})

    @classmethod
    def tearDown(cls):
        pass

    def test_from_dict_no_attr(self):
        e = Job.from_dict(customer=self.customer)
        assert e.attributes == {}, e.attributes

    def test_set_job(self):
        self.job.jobTitle = "title"
        assert self.job.jobTitle == "title", self.job.jobTitle

    def test_set_job_customer(self):
        self.customers[0].base.jobs[0].jobTitle = "title"
        self.customers[0].base.jobs[0].endDate = u'1994-10-06'

        edu = self.customers[0].base.jobs[0]
        edu.isCurrent = False

        mute = {'base.jobs':
                             [{u'companyIndustry': u'companyIndustry',
                               u'companyName': u'companyName',
                               u'startDate': u'1994-10-06',
                               u'endDate': u'1994-10-06',
                               u'jobTitle': u'title',
                               u'isCurrent': False}]}
        mute_res = {'base': {'jobs':
                             [{u'companyIndustry': u'companyIndustry',
                               u'companyName': u'companyName',
                               u'startDate': u'1994-10-06',
                               u'endDate': u'1994-10-06',
                               u'jobTitle': u'title',
                               u'isCurrent': False}]}}
        assert self.customers[0].mute == mute, self.customers[0].mute
        res = resolve_mutation_tracker(self.customers[0].mute)
        assert res == mute_res, res

    def test_set_job_customer_add(self):
        self.customers[0].base.jobs[0].isCurrent = False
        self.customers[0].base.jobs += [Job(customer=self.customers[0], id='01')]

        mute = {'base.jobs': [
            {u'companyIndustry': u'companyIndustry',
             u'companyName': u'companyName',
             u'startDate': u'1994-10-06',
             u'endDate': u'1994-10-06',
             u'jobTitle': u'jobTitle',
             u'isCurrent': False},
            {u'id': u'01'}
        ]
        }
        mute_res = {'base': {'jobs': [
            {u'companyIndustry': u'companyIndustry',
             u'companyName': u'companyName',
             u'startDate': u'1994-10-06',
             u'endDate': u'1994-10-06',
             u'jobTitle': u'jobTitle',
             u'isCurrent': False},
            {u'id': u'01'}
        ]
        }
        }
        assert self.customers[0].mute == mute, self.customers[0].mute
        res = resolve_mutation_tracker(self.customers[0].mute)
        assert res == mute_res, res

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_job_response'))
    def test_post_job(self, mock_post):
        j = Job(customer=self.customer, id='01', companyIndustry='companyIndustry', startDate=u'1994-10-06',
                endDate=u'1994-10-06', companyName='companyName', jobTitle='jobTitle',
                isCurrent=True)
        j.post()

        mock_post.assert_called_with(self.base_url_customer + '/' + self.customer.id + '/jobs',
                                    headers=self.headers_expected,
                                    json=j.attributes)
        assert self.customer.base.jobs[0].attributes == j.attributes, (self.customer.base.jobs[0].attributes
                                                                       ,j.attributes)

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_job_response'))
    def test_post_job_create_base(self, mock_post):
        c = Customer(node=self.node, default_attributes={}, id='01')
        j = Job(customer=c, id='01', companyIndustry='companyIndustry', startDate=u'1994-10-06',
                endDate=u'1994-10-06', companyName='companyName', jobTitle='jobTitle',
                isCurrent=True)
        j.post()

        mock_post.assert_called_with(self.base_url_customer + '/' + c.id + '/jobs',
                                    headers=self.headers_expected,
                                    json=j.attributes)
        assert c.base.jobs[0].attributes == j.attributes, (c.base.jobs[0].attributes, j.attributes)

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path='tests/util/fake_job_response'))
    def test_delete(self, mock_post):
        j = Job(customer=self.customer, id='01')
        j.delete()
        mock_post.assert_called_with(self.base_url_customer + '/' + self.customer.id + '/jobs/01',
                                    headers=self.headers_expected)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_job_response'))
    def test_put(self, mock_post):
        self.customer.base.jobs = [self.job]
        self.job.companyIndustry= 'companyIndustry'
        self.job.companyName = 'companyName'
        self.job.jobTitle = 'jobTitle'
        self.job.startDate = '1994-10-06'
        self.job.endDate = '1994-10-06'
        self.job.isCurrent = True

        self.job.put()
        mock_post.assert_called_with(self.base_url_customer + '/' + self.customer.id + '/jobs/01',
                                    headers=self.headers_expected, json=self.job.attributes)
        assert self.customer.base.jobs[0].attributes == self.job.attributes,  (self.customer.base.jobs[0].attributes,
                                                                               self.job.attributes)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_put_no_jobs(self, mock_post):
        self.job.companyIndustry= 'companyIndustry'
        self.job.companyName = 'companyName'
        self.job.jobTitle = 'jobTitle'
        self.job.startDate = '1994-10-06'
        self.job.endDate = '1994-10-06'
        self.job.isCurrent = True
        try:
            self.job.put()
        except ValueError as e:
            assert 'Job' in str(e)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_put_no_job(self, mock_post):
        self.customer.base.jobs = [self.job]
        job = Job(customer=self.customer, id='03')
        job.companyIndustry = 'companyIndustry'
        job.companyName = 'companyName'
        job.jobTitle = 'jobTitle'
        job.startDate = '1994-10-06'
        job.endDate = '1994-10-06'
        job.isCurrent = True
        try:
            job.put()
        except ValueError as e:
            assert 'Job' in str(e)

    def test_create_job_new_c(self):
        j = Job(customer=Customer(node=self.node), a='b')
        try:
            j.post()
        except AttributeError as e:
            assert "Customer object has no attribute 'id'" in str(e), str(e)