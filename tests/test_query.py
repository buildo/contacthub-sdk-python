import json
import unittest

import mock
from datetime import datetime

from contacthub.errors.operation_not_permitted import OperationNotPermitted
from contacthub.models.customer import Customer
from contacthub.models.query import between_, in_, not_in_
from contacthub.models.query.criterion import Criterion
from contacthub.models.query.entity_field import EntityField
from contacthub.models.query.entity_meta import EntityMeta
from contacthub.models.query.query import Query
from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestQuery(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.entity_field = (Customer.attr)
        w = Workspace(workspace_id=123, token=456)
        cls.node = w.get_node(123)
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'

    @classmethod
    def tearDown(cls):
        pass

    def test_enitity_field_get_attr(self):
        e1 = EntityField(Customer, 'attr1')
        e2 = EntityField(e1, 'attr2')
        e = Customer.attr1.attr2
        assert isinstance(e, EntityField), type(e)
        assert isinstance(e.entity, EntityField), type(e.entity)
        assert e.entity == e2.entity, e.entity
        assert e.field == e2.field, e.field
        assert e.entity.field == e2.entity.field, e.entity

    def test_entity_field_eq(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.EQUALS, 'attr')
        c = (Customer.attr == 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_neq(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.NOT_EQUALS, 'attr')
        c = (Customer.attr != 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_lt(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.LT, 'attr')
        c = (Customer.attr < 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_le(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.LTE, 'attr')
        c = (Customer.attr <= 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_gt(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.GT, 'attr')
        c = (Customer.attr > 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_ge(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.GTE, 'attr')
        c = (Customer.attr >= 'attr')

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element == cEqual.second_element, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_null(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.IS_NULL)
        c = (Customer.attr == None)
        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element is None, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_field_not_null(self):
        cEqual = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.IS_NOT_NULL)
        c = (Customer.attr != None)

        assert c.first_element == cEqual.first_element, c.first_element
        assert c.second_element is None, c.second_element
        assert c.operator == cEqual.operator, c.operator

    def test_entity_meta(self):
        assert isinstance(Customer.attr1, EntityField), type(Customer.attr1)

    def test_criterion_and(self):
        c1 = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.IS_NOT_NULL)
        c2 = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.EQUALS, 'attr')

        c3 = c1 & c2

        assert isinstance(c3, Criterion), type(c3)
        assert isinstance(c3.first_element, Criterion), type(c3.first_element)
        assert c3.first_element.operator == c1.operator, c3.first_element.operator
        assert isinstance(c3.second_element, Criterion), type(c3.second_element)
        assert c3.second_element.operator == c2.operator, c3.first_element.operator
        assert c3.operator == Criterion.COMPLEX_OPERATORS.AND

    def test_criterion_or(self):
        c1 = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.IS_NOT_NULL)
        c2 = Criterion(self.entity_field, Criterion.SIMPLE_OPERATORS.EQUALS, 'attr')
        c3 = c1 | c2
        assert isinstance(c3, Criterion), type(c3)
        assert isinstance(c3.first_element, Criterion), type(c3.first_element)
        assert c3.first_element.operator == c1.operator, c3.first_element.operator
        assert isinstance(c3.second_element, Criterion), type(c3.second_element)
        assert c3.second_element.operator == c2.operator, c3.first_element.operator
        assert c3.operator == Criterion.COMPLEX_OPERATORS.OR

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_between(self, mock_get):
        self.node.query(Customer).filter(
            between_(Customer.base.dob, datetime(2011, 12, 11), datetime(2015, 12, 11))).all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'base.dob', 'operator': 'BETWEEN',
                      'value': ["2011-12-11T00:00:00Z", "2015-12-11T00:00:00Z"]}}},
                                      })
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_between_str(self, mock_get):
        self.node.query(Customer).filter(
            between_(Customer.base.dob, '2011-12-11', '2015-12-11')).all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'base.dob', 'operator': 'BETWEEN',
                      'value': ['2011-12-11', '2015-12-11']}}}
                                      })

        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_equals(self, mock_get):
        self.node.query(Customer).filter(Customer.base.firstName == 'firstName').all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'EQUALS', 'value': 'firstName'}}}})
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_not_equals(self, mock_get):
        self.node.query(Customer).filter(Customer.base.firstName != 'firstName').all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'NOT_EQUALS',
                      'value': 'firstName'}}}})
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_gt(self, mock_get):
        self.node.query(Customer).filter(Customer.base.firstName > 'firstName').all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'GT',
                      'value': 'firstName'}}}})
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_gte(self, mock_get):
        self.node.query(Customer).filter(Customer.base.firstName >= 'firstName').all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'GTE',
                      'value': 'firstName'}}}})
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_lt(self, mock_get):
        self.node.query(Customer).filter(Customer.base.firstName < 'firstName').all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'LT',
                      'value': 'firstName'}}}})
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_lte(self, mock_get):
        self.node.query(Customer).filter(Customer.base.firstName <= 'firstName').all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'LTE',
                      'value': 'firstName'}}}})
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_in(self, mock_get):
        self.node.query(Customer).filter(in_('prova', Customer.tags.auto)).all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'tags.auto', 'operator': 'IN',
                      'value': 'prova'}}}})
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_not_in(self, mock_get):
        self.node.query(Customer).filter(not_in_('prova', Customer.tags.auto)).all()
        params = {'nodeId': self.node.node_id}

        params['query'] = json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'tags.auto', 'operator': 'NOT_IN',
                      'value': 'prova'}}}})
        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_is_null(self, mock_get):
        self.node.query(Customer).filter(Customer.base.firstName == None).all()
        params = {'nodeId': self.node.node_id, 'query': json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'IS_NULL'}}}})}

        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def test_is_not_null(self, mock_get):
        self.node.query(Customer).filter(Customer.base.firstName != None).all()
        params = {'nodeId': self.node.node_id, 'query': json.dumps({'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'IS_NOT_NULL'}}}})}

        mock_get.assert_called_with(self.base_url, headers=self.headers_expected, params=params)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_or(self, mock_get):
        self.node.query(Customer).filter(
            (Customer.base.firstName == 'firstName') | (Customer.base.firstName == 'firstName1')).all()
        query= {'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'composite', 'conjunction': 'or', 'conditions': [
                         {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'EQUALS', 'value': 'firstName'},
                         {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'EQUALS', 'value': 'firstName1'}
                     ]
                      }
                 }
             }
                                                                    }
        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_and(self, mock_get):
        self.node.query(Customer).filter(
            (Customer.base.firstName == 'firstName') & (Customer.base.lastName == 'lastName')).all()
        query = {'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'composite', 'conjunction': 'and', 'conditions': [
                         {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'EQUALS', 'value': 'firstName'},
                         {'type': 'atomic', 'attribute': 'base.lastName', 'operator': 'EQUALS', 'value': 'lastName'}
                     ]
                      }
                 }
             }
                                                                    }
        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_and_or(self, mock_get):
        self.node.query(Customer).filter(
            ((Customer.base.firstName == 'firstName') & (Customer.base.lastName == 'lastName') | (
            Customer.extra == 'extra'))).all()
        query= {'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'composite', 'conjunction': 'or', 'conditions': [
                         {'type': 'composite', 'conjunction': 'and', 'conditions': [
                             {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'EQUALS',
                              'value': 'firstName'},
                             {'type': 'atomic', 'attribute': 'base.lastName', 'operator': 'EQUALS',
                              'value': 'lastName'}
                         ]
                          },
                         {'type': 'atomic', 'attribute': 'extra', 'operator': 'EQUALS', 'value': 'extra'}
                     ]
                      }
                 }
             }
                                                                    }

        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_or_and(self, mock_get):
        self.node.query(Customer).filter(
            (((Customer.base.firstName == 'firstName') | (Customer.base.lastName == 'lastName')) & (
                Customer.extra == 'extra'))).all()
        query={'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'composite', 'conjunction': 'and', 'conditions': [
                         {'type': 'composite', 'conjunction': 'or', 'conditions': [
                             {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'EQUALS',
                              'value': 'firstName'},
                             {'type': 'atomic', 'attribute': 'base.lastName', 'operator': 'EQUALS',
                              'value': 'lastName'}
                         ]
                          },
                         {'type': 'atomic', 'attribute': 'extra', 'operator': 'EQUALS', 'value': 'extra'}
                     ]
                      }
                 }
             }
                                                                    }

        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_succesive_simple_filters(self, mock_get):
        q1 = self.node.query(Customer).filter(Customer.base.firstName == 'firstName')
        q2 = q1.filter(Customer.base.lastName == 'lastName')
        q2.all()
        query = {'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'type': 'composite', 'conjunction': 'and', 'conditions': [
                         {'type': 'atomic', 'attribute': 'base.firstName', 'operator': 'EQUALS', 'value': 'firstName'},
                         {'type': 'atomic', 'attribute': 'base.lastName', 'operator': 'EQUALS', 'value': 'lastName'}
                     ]
                      }
                 }
             }
                                                                    }

        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all', return_value=json.loads(FakeHTTPResponse().text))
    def test_succesive_complex_filters(self, mock_get):
        q1 = self.node.query(Customer).filter((Customer.base.firstName == 'firstName') | (Customer.extra == 'extra'))
        q2 = q1.filter(Customer.base.lastName == 'lastName')
        q2.all()
        query = {'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'conjunction': 'and',  'type': 'composite', 'conditions': [
                         {'type': 'composite', 'conjunction': 'or', 'conditions': [

                             {'operator': 'EQUALS', 'attribute': 'base.firstName', 'type': 'atomic',
                              'value': 'firstName'},
                             {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                              'value': 'extra'},
                         ]
                          },
                         {'operator': 'EQUALS', 'attribute': 'base.lastName', 'type': 'atomic',
                          'value': 'lastName'}
                     ],

                      }
                 }
             }
                                                                    }
        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_succesive_complex_filters_or(self, mock_get):
        q1 = self.node.query(Customer).filter((Customer.base.firstName == 'firstName') | (Customer.extra == 'extra'))
        q2 = q1.filter((Customer.base.lastName == 'lastName') | (Customer.extra == 'extra'))
        q2.all()
        query = {'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'conjunction': 'and', 'type': 'composite', 'conditions': [
                         {'type': 'composite', 'conjunction': 'or', 'conditions': [

                             {'operator': 'EQUALS', 'attribute': 'base.firstName', 'type': 'atomic',
                              'value': 'firstName'},
                             {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                              'value': 'extra'},
                         ]
                          },
                         {'type': 'composite', 'conjunction': 'or', 'conditions': [

                             {'operator': 'EQUALS', 'attribute': 'base.lastName', 'type': 'atomic',
                              'value': 'lastName'},
                             {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                              'value': 'extra'},
                         ]
                          }
                     ],

                      }
                 }
             }
                 }
        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_succesive_complex_filters_and(self, mock_get):
        q1 = self.node.query(Customer).filter((Customer.base.firstName == 'firstName') & (Customer.extra == 'extra'))
        q2 = q1.filter((Customer.base.lastName == 'lastName') | (Customer.extra == 'extra'))
        q2.all()
        query = {'name': 'query', 'query':
            {'type': 'simple', 'name': 'query', 'are':
                {'condition':
                     {'conjunction': 'and', 'type': 'composite', 'conditions': [

                             {'operator': 'EQUALS', 'attribute': 'base.firstName', 'type': 'atomic',
                              'value': 'firstName'},
                             {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                              'value': 'extra'}
                          ,
                         {'type': 'composite', 'conjunction': 'or', 'conditions': [

                             {'operator': 'EQUALS', 'attribute': 'base.lastName', 'type': 'atomic',
                              'value': 'lastName'},
                             {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                              'value': 'extra'},
                         ]
                          }
                     ],

                      }
                 }
             }
                 }
        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_and_query(self, mock_get):
        q1 = self.node.query(Customer).filter((Customer.base.firstName == 'firstName') | (Customer.extra == 'extra'))
        q2 = self.node.query(Customer).filter((Customer.base.lastName == 'lastName') | (Customer.extra == 'extra'))
        q = q1 & q2
        q.all()
        query = {'name': 'query', 'query':
            {'name': 'query', 'type': 'combined', 'conjunction': 'INTERSECT', 'queries':[
                {'type': 'simple', 'name': 'query', 'are':
                    {'condition':{'type': 'composite', 'conjunction': 'or', 'conditions': [

                             {'operator': 'EQUALS', 'attribute': 'base.firstName', 'type': 'atomic',
                              'value': 'firstName'},
                             {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                              'value': 'extra'},
                         ]
                          }}
                },
                {'type': 'simple', 'name': 'query', 'are':
                    {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                        {'operator': 'EQUALS', 'attribute': 'base.lastName', 'type': 'atomic',
                         'value': 'lastName'},
                        {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                         'value': 'extra'},
                    ]
                                   }}
                 }


            ]
             }
                 }

        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_or_query(self, mock_get):
        q1 = self.node.query(Customer).filter((Customer.base.firstName == 'firstName') | (Customer.extra == 'extra'))
        q2 = self.node.query(Customer).filter((Customer.base.lastName == 'lastName') | (Customer.extra == 'extra'))
        q = q1 | q2
        q.all()
        query = {'name': 'query', 'query':
            {'name': 'query', 'type': 'combined', 'conjunction': 'UNION', 'queries': [
                {'type': 'simple', 'name': 'query', 'are':
                    {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                        {'operator': 'EQUALS', 'attribute': 'base.firstName', 'type': 'atomic',
                         'value': 'firstName'},
                        {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                         'value': 'extra'},
                    ]
                                   }}
                 },
                {'type': 'simple', 'name': 'query', 'are':
                    {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                        {'operator': 'EQUALS', 'attribute': 'base.lastName', 'type': 'atomic',
                         'value': 'lastName'},
                        {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                         'value': 'extra'},
                    ]
                                   }}
                 }

            ]
             }
                 }

        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_or_combined_query(self, mock_get):
        q1 = self.node.query(Customer).filter(
            (Customer.base.firstName == 'firstName') | (Customer.extra == 'extra'))
        q2 = self.node.query(Customer).filter((Customer.base.lastName == 'lastName') | (Customer.extra == 'extra'))
        qor = q1 | q2
        qand = q1 & q2
        q = qor | qand

        q.all()
        query = {'name': 'query', 'query': {'name': 'query', 'type': 'combined', 'conjunction': 'UNION', 'queries':
            [

                {'type': 'simple', 'name': 'query', 'are':
                    {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                        {'operator': 'EQUALS', 'attribute': 'base.firstName', 'type': 'atomic',
                         'value': 'firstName'},
                        {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                         'value': 'extra'},
                    ]
                                   }}
                 },
                {'type': 'simple', 'name': 'query', 'are':
                    {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                        {'operator': 'EQUALS', 'attribute': 'base.lastName', 'type': 'atomic',
                         'value': 'lastName'},
                        {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                         'value': 'extra'},
                    ]
                                   }}
                 }
            ,
                 {'name': 'query', 'type': 'combined', 'conjunction': 'INTERSECT', 'queries': [
                     {'type': 'simple', 'name': 'query', 'are':
                         {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                             {'operator': 'EQUALS', 'attribute': 'base.firstName', 'type': 'atomic',
                              'value': 'firstName'},
                             {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                              'value': 'extra'},
                         ]
                                        }}
                      },
                     {'type': 'simple', 'name': 'query', 'are':
                         {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                             {'operator': 'EQUALS', 'attribute': 'base.lastName', 'type': 'atomic',
                              'value': 'lastName'},
                             {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                              'value': 'extra'},
                         ]
                                        }}
                      }

                 ]
                  }]
                 }}

        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_and_combined_query(self, mock_get):
        q1 = self.node.query(Customer).filter(
            (Customer.base.firstName == 'firstName') | (Customer.extra == 'extra'))
        q2 = self.node.query(Customer).filter((Customer.base.lastName == 'lastName') | (Customer.extra == 'extra'))
        qor = q1 | q2
        qand = q1 & q2
        q = qor & qand

        q.all()
        query = {'name': 'query', 'query': {'name': 'query', 'type': 'combined', 'conjunction': 'INTERSECT', 'queries':
            [

                {'type': 'simple', 'name': 'query', 'are':
                    {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                        {'operator': 'EQUALS', 'attribute': 'base.firstName', 'type': 'atomic',
                         'value': 'firstName'},
                        {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                         'value': 'extra'},
                    ]
                                   }}
                 },
                {'type': 'simple', 'name': 'query', 'are':
                    {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                        {'operator': 'EQUALS', 'attribute': 'base.lastName', 'type': 'atomic',
                         'value': 'lastName'},
                        {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                         'value': 'extra'},
                    ]
                                   }}
                 }
                ,
                {'name': 'query', 'type': 'combined', 'conjunction': 'UNION', 'queries': [
                    {'type': 'simple', 'name': 'query', 'are':
                        {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                            {'operator': 'EQUALS', 'attribute': 'base.firstName', 'type': 'atomic',
                             'value': 'firstName'},
                            {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                             'value': 'extra'},
                        ]
                                       }}
                     },
                    {'type': 'simple', 'name': 'query', 'are':
                        {'condition': {'type': 'composite', 'conjunction': 'or', 'conditions': [

                            {'operator': 'EQUALS', 'attribute': 'base.lastName', 'type': 'atomic',
                             'value': 'lastName'},
                            {'operator': 'EQUALS', 'attribute': 'extra', 'type': 'atomic',
                             'value': 'extra'},
                        ]
                                       }}
                     }

                ]
                 }]
                                            }}
        mock_get.assert_called_with(page=0, query=query)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_filter_complex(self, mock_get):
        try:
            q1 = self.node.query(Customer).filter(
                (Customer.base.firstName == 'firstName') | (Customer.extra == 'extra'))
            q2 = self.node.query(Customer).filter((Customer.base.lastName == 'lastName') | (Customer.extra == 'extra'))
            qor = q1 | q2
            qor.filter(Customer.base.firstName == 'firstName')
        except OperationNotPermitted as e:
            assert 'Cannot apply a filter on a combined query' in str(e), str(e)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_combine_empty_or(self, mock_get):
        try:
            q1 = self.node.query(Customer)
            q2 = self.node.query(Customer)
            qor = q1 | q2
        except OperationNotPermitted as e:
            assert 'Cannot combine empty queries.' in str(e), str(e)

    @mock.patch('contacthub._api_manager._api_customer._CustomerAPIManager.get_all',
                return_value=json.loads(FakeHTTPResponse().text))
    def test_combine_empty_and(self, mock_get):
        try:
            q1 = self.node.query(Customer)
            q2 = self.node.query(Customer)
            qor = q1 & q2
        except OperationNotPermitted as e:
            assert 'Cannot combine empty queries.' in str(e), str(e)

