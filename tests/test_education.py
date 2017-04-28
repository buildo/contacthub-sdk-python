import unittest

import mock

from contacthub.lib.read_only_list import ReadOnlyList
from contacthub.models import properties, Properties
from contacthub.models.customer import Customer
from contacthub.models.education import Education
from contacthub.models.event import Event
from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestEducation(unittest.TestCase):
    @classmethod
    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def setUp(cls, mock_get_customers):
        w = Workspace(workspace_id="123", token="456")
        cls.node = w.get_node("123")
        cls.customers = cls.node.get_customers()
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url_customer = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'
        cls.customer = Customer(id='01', node=cls.node)
        cls.education = Education(customer=cls.customer, **{'id': '01'})

    @classmethod
    def tearDown(cls):
        pass

    def test_from_dict_no_attr(self):
        e = Education.from_dict(customer=self.customer)
        assert e.attributes == {}, e.attributes

    def test_set_education(self):
        self.education.schoolType = Education.SCHOOL_TYPES.COLLEGE
        assert self.education.schoolType == Education.SCHOOL_TYPES.COLLEGE, self.education.schoolType

    def test_set_education_customer(self):
        self.customers[0].base.educations[0].schoolType = Education.SCHOOL_TYPES.SECONDARY_SCHOOL
        self.customers[0].base.educations[0].startYear = 1992

        edu = self.customers[0].base.educations[0]
        edu.isCurrent = False

        mute = {'base.educations':
                             [{u'schoolType': 'SECONDARY_SCHOOL',
                               u'startYear': 1992,
                               u'schoolName': u'schoolName',
                               u'schoolConcentration': u'schoolConcentration',
                               u'endYear': 2000,
                               u'isCurrent': False}]}
        assert self.customers[0].mute == mute, self.customers[0].mute

    def test_set_education_customer_add(self):
        self.customers[0].base.educations[0].isCurrent = False
        self.customers[0].base.educations += [Education(customer=self.customers[0], id='01')]

        mute = {'base.educations': [
            {u'schoolType': 'COLLEGE',
             u'startYear': 1994,
             u'schoolName': u'schoolName',
             u'schoolConcentration': u'schoolConcentration',
             u'endYear': 2000,
             u'isCurrent': False},
            {u'id': u'01'}
        ]
        }

        assert self.customers[0].mute == mute, self.customers[0].mute

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_post_education(self, mock_post):
        e = Education(customer=self.customer, id='01', schoolType='COLLEGE', startYear=1994, endYear=2000,
                      schoolName='schoolName', schoolConcentration='schoolConcentration', isCurrent=True)
        e.post()

        mock_post.asser_called_with(self.base_url_customer + '/' + self.customer.id +'/educations',
                                    headers=self.headers_expected,
                                    json=e.attributes)
        assert self.customer.base.educations[0].attributes == e.attributes, self.customer.attributes

    @mock.patch('requests.post', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_post_education_create_base(self, mock_post):
        c = Customer(node=self.node, default_attributes={}, id='01')
        e = Education(customer=c, id='01', schoolType='COLLEGE', startYear=1994, endYear=2000,
                      schoolName='schoolName', schoolConcentration='schoolConcentration', isCurrent=True)

        e.post()

        mock_post.assert_called_with(self.base_url_customer + '/' + c.id + '/educations',
                                    headers=self.headers_expected,
                                    json=e.attributes)
        assert c.base.educations[0].attributes == e.attributes, c.customer.attributes

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_delete(self, mock_post):
        e = Education(customer=self.customer, id='01')
        e.delete()
        mock_post.assert_called_with(self.base_url_customer + '/' + self.customer.id + '/educations/01',
                                    headers=self.headers_expected)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_put(self, mock_post):
        self.customer.base.educations = [self.education]
        self.education.schoolType= 'COLLEGE'
        self.education.startYear = 1994
        self.education.endYear = 2000
        self.education.schoolConcentration = 'schoolConcentration'
        self.education.schoolName = 'schoolName'
        self.education.isCurrent = True

        self.education.put()
        mock_post.assert_called_with(self.base_url_customer + '/' + self.customer.id + '/educations/01',
                                    headers=self.headers_expected, json=self.education.attributes)
        assert self.customer.base.educations[0].attributes == self.education.attributes,  self.customer.base.educations[0].attributes

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_put_no_educations(self, mock_post):
        self.education.schoolType = 'COLLEGE'
        self.education.startYear = 1994
        self.education.endYear = 2000
        self.education.schoolConcentration = 'schoolConcentration'
        self.education.schoolName = 'schoolName'
        self.education.isCurrent = True
        try:
            self.education.put()
        except ValueError as e:
            assert 'Education' in str(e)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_education_response'))
    def test_put_no_education(self, mock_post):
        self.customer.base.educations = [self.education]
        education = Education(customer=self.customer, id='03')
        education.schoolType = 'COLLEGE'
        education.startYear = 1994
        education.endYear = 2000
        education.schoolConcentration = 'schoolConcentration'
        education.schoolName = 'schoolName'
        education.isCurrent = True
        try:
            education.put()
        except ValueError as e:
            assert 'Education' in str(e)