import os
import unittest
import test_data
try:
    from server import load_classes, load_package
except ImportError:
    import sys
    sys.path.append('src')
    sys.path.append(os.path.join('..', 'src'))
    from server import load_classes, load_package


TEST_DATA = os.path.dirname(test_data.__file__)


class InspectionTestCase(unittest.TestCase):
    def test_load_package_founds_submodules(self):
        modules = [m.__name__ for m in load_package(TEST_DATA)]
        self.assertEqual(modules, ['pow_fixture', 'div_fixture'])

    def test_load_classes_from_module(self):
        pow_fixture_module = os.path.join(TEST_DATA, 'pow_fixture.py')
        classes = load_classes(pow_fixture_module)
        self.assertEqual(list(classes.keys()), ['PowFixture'])
        self.assertEqual(classes['PowFixture']['methods'],
                         ['pow'])

    def test_load_classes_from_package(self):
        classes = load_classes(TEST_DATA)
        self.assertEqual(classes['PowFixture']['methods'],
                         ['pow'])
        self.assertEqual(classes['DivFixture']['methods'],
                         ['div'])


if __name__ == '__main__':
    unittest.main()
