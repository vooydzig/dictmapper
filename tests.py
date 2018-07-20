from unittest import TestCase

from mapper import JSONMapper, Mapping


class MapperTestCase(TestCase):

    def test_map_returns_dict(self):
        m = JSONMapper(mapping=[])
        self.assertDictEqual(m.map({}), {})

    def test_simple_values_mapping(self):
        m = JSONMapper(mapping=[Mapping(source='foo', destination='bar', transform=None)])
        self.assertDictEqual(m.map({}), {})
        self.assertDictEqual(m.map({'foo': 1}), {'bar': 1})
        self.assertDictEqual(m.map({'foo': 1, 'bar': 2}), {'bar': 1})
        self.assertDictEqual(m.map({'foo': [1, 2]}), {'bar': [1, 2]})
        self.assertDictEqual(m.map({'foo': {'prop': 1}}), {'bar': {'prop': 1}})

    def test_nested_objects_mapping_to_simple_value(self):
        m = JSONMapper(mapping=[Mapping(source='foo.bar', destination='bar', transform=None)])
        self.assertDictEqual(m.map({}), {})
        self.assertDictEqual(m.map({'foo': 1}), {})
        self.assertDictEqual(m.map({'foo': {'bar': 1}}), {'bar': 1})
        self.assertDictEqual(m.map({'foo': {'bar': 1}, 'bar': 2}), {'bar': 1})

    def test_mapping_to_object(self):
        m = JSONMapper(mapping=[Mapping(source='foo.bar', destination='a.b.c.d', transform=None)])
        self.assertDictEqual(m.map({}), {})
        self.assertDictEqual(m.map({'foo': {'a': 0, 'bar': 1}}), {'a': {'b': {'c': {'d': 1}}}})

    def test_list_item_to_simple_value(self):
        m = JSONMapper(mapping=[Mapping(source='foo[1]', destination='bar', transform=None)])
        self.assertDictEqual(m.map({}), {})
        self.assertDictEqual(m.map({'foo': [0, 1, 2, 3]}), {'bar': 1})

    def test_item_property_in_list_to_simple_value(self):
        m = JSONMapper(mapping=[Mapping(source='foo[*].f', destination='bar', transform=None)])
        self.assertDictEqual(m.map({}), {})
        self.assertDictEqual(m.map({'foo': [{'f': 1}]}), {'bar': 1})

    def test_item_property_in_list_to_another_property_in_list(self):
        m = JSONMapper(mapping=[Mapping(source='foo[*].f', destination='bar[*].b', transform=None)])
        self.assertDictEqual(m.map({}), {})
        self.assertDictEqual(m.map({'foo': [{'f': 1}]}), {'bar': [{'b': 1}]})

    def test_merge_lists(self):
        m = JSONMapper(mapping=[Mapping(source='foo[*].f', destination='bar[*].b', transform=None),
                                Mapping(source='foz[*].f', destination='bar[*].baz', transform=None)])
        self.assertDictEqual(m.map({}), {})
        self.assertDictEqual(m.map({'foo': [{'f': 1}], 'foz': [{'f': 2}]}), {'bar': [{'b': 1, 'baz': 2}]})

    def test_list_item_to_root(self):
        m = JSONMapper(mapping=[Mapping(source='foo', destination='$', transform=None)])
        self.assertDictEqual(m.map({}), {})
        self.assertListEqual(m.map({'foo': [0, 1, 2, 3]}), [0, 1, 2, 3])
        self.assertListEqual(m.map({'foo': [{'a': 1, 'b': 2}, {'c': 3, 'p': 0}]}), [{'a': 1, 'b': 2}, {'c': 3, 'p': 0}])

    def test_duplicate_mappings(self):
        m = JSONMapper(mapping=[
            Mapping(source='foo', destination='bar', transform=None),
            Mapping(source='foz', destination='bar', transform=None),
        ])

        self.assertDictEqual(m.map({}), {})
        self.assertDictEqual(m.map({'foz': 1}), {'bar': 1})
        self.assertDictEqual(m.map({'foo': 2}), {'bar': 2})
        self.assertDictEqual(m.map({'foo': 1, 'foz': 2}), {'bar': 2})

    def test_multiple_mappings(self):
        m = JSONMapper(mapping=[
            Mapping(source='foo', destination='bar', transform=None),
            Mapping(source='foz', destination='baz', transform=None),
        ])

        self.assertDictEqual(m.map({}), {})
        self.assertDictEqual(m.map({'foo': [0, 1, 2, 3]}), {'bar': [0, 1, 2, 3]})
        self.assertDictEqual(m.map({'foz': [0, 1, 2, 3]}), {'baz': [0, 1, 2, 3]})
        self.assertDictEqual(m.map({'foo': [0, 1, 2, 3], 'foz': [0, 1, 2, 3]}),
                             {'bar': [0, 1, 2, 3], 'baz': [0, 1, 2, 3]})
