import os
import unittest
import test_data
try:
    from server import import_classes, import_modules
except ImportError:
    import sys
    sys.path.append('src')
    sys.path.append(os.path.join('..', 'src'))
    from server import import_classes, import_modules


TEST_DATA = os.path.dirname(test_data.__file__)


class InspectionTestCase(unittest.TestCase):
    def test_import_modules_founds_submodules(self):
        modules = [m.__name__ for m in import_modules(TEST_DATA)]
        self.assertEqual(modules, ['pow_fixture', 'div_fixture'])

    def test_import_classes_founds_methods(self):
        classes = import_classes(TEST_DATA)
        self.assertEqual(sorted(classes['PowFixture']['methods']),
                         ['pow'])


if __name__ == '__main__':
    unittest.main()
