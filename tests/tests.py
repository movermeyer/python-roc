import os
import random
import unittest
import six
if six.PY2:
    from xmlrpclib import ServerProxy
elif six.PY3:
    from xmlrpc.client import ServerProxy
from . import test_data
from .test_data.pow_fixture import PowFixture
try:
    from remote_class import RemoteClass
except ImportError:
    import sys
    sys.path.append('src')
    sys.path.append(os.path.join('..', 'src'))
    from remote_class import RemoteClass
from server import start_server, import_classes, import_modules


TEST_DATA = os.path.dirname(test_data.__file__)


class PowFixtureTestCase(unittest.TestCase):
    def test_3_in_power_of_2_is_9(self):
        self.assertEqual(PowFixture(3).pow(2), 9)


class RemoteClassTestCase(unittest.TestCase):
    class ServerMock(object):
        def create(self, class_name, args):
            instance_name = class_name + '0'
            setattr(self, instance_name,
                    globals()[class_name](*args))
            return instance_name

    def test_remote_power(self):
        PowFixture = RemoteClass(self.ServerMock(), 'PowFixture')
        self.assertEqual(PowFixture(3).pow(2), 9)


class RealServerTestCase(unittest.TestCase):
    def setUp(self):
        port = random.randint(2000, 8000)
        self.server_thread = start_server(
            TEST_DATA,
            port=port,
            log_requests=False
        )
        self.proxy = ServerProxy(
            "http://127.0.0.1:%d/" % (port),
            allow_none=True
        )

    def test_whats_registered(self):
        must_be_provided = ('classes', 'create', 'instances', 'shutdown')
        provided_methods = self.proxy.system.listMethods()
        self.assertTrue(all([method in provided_methods
                             for method in must_be_provided]))

    def test_create_adds_methods(self):
        provided_0 = set(self.proxy.system.listMethods())
        self.proxy.create('PowFixture', [7])
        provided_1 = set(self.proxy.system.listMethods())
        self.assertFalse(provided_0 == provided_1,
                         ".create() does not add new methods to server")

    def test_remote_class_with_real_server(self):
        PowFixture = RemoteClass(self.proxy, 'PowFixture')
        pow_3 = PowFixture(3)
        nine = pow_3.pow(2)
        self.assertEqual(nine, 9)

    def test_server_instances(self):
        self.assertEqual(self.proxy.instances(), [])
        self.proxy.create('PowFixture', [2])
        self.proxy.create('PowFixture', [5])
        self.assertEqual(sorted(self.proxy.instances()),
                         ['PowFixture_0', 'PowFixture_1'])
        self.assertEqual(self.proxy.PowFixture_0.pow(10),
                         1024)
        self.assertEqual(self.proxy.PowFixture_1.pow(2),
                         25)

    def tearDown(self):
        self.proxy.shutdown()
        self.server_thread.join()


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
