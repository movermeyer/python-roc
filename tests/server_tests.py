import os
import unittest
import test_data
from roc.loader import load_classes, load_package


TEST_DATA = os.path.dirname(test_data.__file__)


class InspectionTestCase(unittest.TestCase):
    def test_load_package_founds_submodules(self):
        modules = [m.__name__ for m in load_package(TEST_DATA)]
        self.assertEqual(modules, ['pow_fixture', 'div_fixture'])

    def test_load_classes_from_module(self):
        pow_fixture_module = os.path.join(TEST_DATA, 'pow_fixture.py')
        classes = dict(load_classes(pow_fixture_module))
        self.assertEqual(list(classes.keys()), ['PowFixture'])
        self.assertEqual(classes['PowFixture']['methods'],
                         ['pow'])

    def test_load_classes_from_package(self):
        classes = dict(load_classes(TEST_DATA))
        self.assertEqual(classes['PowFixture']['methods'],
                         ['pow'])
        self.assertEqual(sorted(classes['DivFixture']['methods']),
                         ['div', 'random_number'])


if __name__ == '__main__':
    unittest.main()
