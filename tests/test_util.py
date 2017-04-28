import unittest

from contacthub.lib.paginated_list import PaginatedList
from contacthub.lib.read_only_list import ReadOnlyList
import json

from contacthub.lib.utils import DateEncoder, get_dictionary_paths, generate_mutation_tracker, remove_empty_attributes
import datetime


class TestEvent(unittest.TestCase):
    def setUp(cls):
        cls.list = [1, 2, 3]

    @classmethod
    def tearDown(cls):
        pass

    def test_read_only_list_iter(self):
        rol = ReadOnlyList(self.list)
        for i in rol:
            ret = i
        assert ret == 3, ret

    def test_read_only_list_repr(self):
        rol = ReadOnlyList(self.list)
        assert rol.__repr__() == [1, 2, 3].__repr__(), rol.__repr__()

    def test_read_only_list_len(self):
        rol = ReadOnlyList(self.list)
        assert len(rol) == 3, len(rol)

    def test_read_only_list_not_reverse(self):
        try:
            ReadOnlyList(self.list).reverse()
        except ValueError as e:
            assert 'proxy' in str(e)

    def test_date_encoder(self):
        try:
            json.dumps(ReadOnlyList, cls=DateEncoder)
        except TypeError as e:
            assert 'JSON' in str(e)

    def test_date_encoder_date(self):
        j = json.dumps(datetime.date(2017, 10, 1), cls=DateEncoder)
        assert "2017-10-01" in j, j

    def test_get_dictionary_paths(self):
        a = {'b': {'c': {'d': 1, 'e': 2}, 'f': {'g': 1}}}
        paths_exp = [['b', 'c', 'd'], ['b', 'c', 'e'], ['b', 'f', 'g']]
        paths = []
        get_dictionary_paths(a, paths)

        for path in paths:
            assert path in paths_exp, path

    def test_generate_mutation_tracker(self):
        d1 = {'a': {'b': 'c', 'd': 'e'}, 'f': 'g'}
        d2 = {'a': {'beta': 'c'}}

        d_exp = {'a': {'beta': 'c', 'b': None, 'd': None}, 'f': None}
        tracker = generate_mutation_tracker(d1, d2)
        assert d_exp == tracker, tracker

    def test_remove_empty_attributes(self):
        d = {'s': [], 'a': None, 'b': {'r': None, 's': [], 'c': [{'a': None, 'd': 'd'}]}}
        d1 = {'s': [], 'b': {'s': [], 'c': [{'d': 'd'}]}}
        r = remove_empty_attributes(d)
        assert d1 == r, r
