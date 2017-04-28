import unittest

from contacthub import Workspace
from contacthub.lib.utils import resolve_mutation_tracker
from contacthub.models import Properties
from contacthub.models.customer import Customer


class TestProperties(unittest.TestCase):

    @classmethod
    def setUp(cls):
        w = Workspace(workspace_id="123", token="456")
        cls.node = w.get_node("123")

    @classmethod
    def tearDown(cls):
        pass

    def test_properties_from_dict_empty(self):
        p = Properties.from_dict()
        assert p.attributes == {}, p.attributes

    def test_generate_mutation_tracker_new(self):
        p = Properties(parent=Customer(node=self.node))
        p.prova = Properties(a='b')
        assert p.mute == {'prova': {'a': 'b'}}, p.mute

    def test_to_dict(self):
        p = Properties(parent=Customer(node=self.node))
        assert p.to_dict() == p.attributes, p.to_dict()

    def test_properties_mute_list(self):
        p = Properties(prova=list())
        p.prova += [Properties(a='b'), {'c': 'd'}]
        assert isinstance(p.prova[0], Properties), p.prova[0]
        assert p.prova[0].a == 'b', p.prova[0].a
        assert p.prova[1].c == 'd', p.prova[1].c
        assert isinstance(p.__repr__(), str), type(p.__repr__())

    def test_new_prop(self):
        p = Properties(a=Properties(b=Properties(c=[Properties(e='f')])), d='e')
        assert isinstance(p.a, Properties), type(p.a)
        assert isinstance(p.a.b, Properties), type(p.a.b)
        assert isinstance(p.a.b.c, list), type(p.a.b.c)
        assert isinstance(p.a.b.c[0], Properties), type(p.a.b.c[0])
        assert p.a.b.c[0].e == 'f', p.a.b.c[0].e
        assert p.d == 'e', p.d

        p.a.b = Properties(f='g')
        assert p.mute == {'a.b': {'c': [], 'f': 'g'}}, p.mute

        p.a.b = 'a'
        assert p.mute == {'a.b': 'a'}, p.mute

        p.a.b = [Properties(c='d')]
        assert p.mute == {'a.b': [{'c': 'd'}]}, p.mute

        p.a.b = 'a'
        assert p.mute == {'a.b': 'a'}, p.mute
        res = resolve_mutation_tracker(p.mute)
        assert res == {'a': {'b': 'a'}}, res






