import os
import random
import unittest
import test_data
import test_data.pow_fixture
from roc.client import server_proxy, remote_module
from roc.server import start_server


TEST_DATA = os.path.dirname(test_data.__file__)


class RealServerTestCase(unittest.TestCase):
    def setUp(self):
        port = random.randint(2000, 8000)
        self.server_thread = start_server(
            TEST_DATA,
            port=port,
            log_requests=False
        )
        self.proxy = server_proxy(port=port)

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

    def test_remote_module_has_defined_classes(self):
        rmodule = remote_module(self.proxy)
        self.assertTrue(hasattr(rmodule, 'PowFixture'))
        self.assertTrue(hasattr(rmodule, 'DivFixture'))
        self.assertFalse(hasattr(rmodule, 'NonExisting'))

    def test_remote_class_with_real_server(self):
        PowFixture = remote_module(self.proxy).PowFixture
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


if __name__ == '__main__':
    unittest.main()
