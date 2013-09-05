import xmlrpclib
import unittest
from fixtures.pow_fixture import PowFixture
from remote_class import RemoteClass
from server import start_server, import_classes, import_modules


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
        self.server_thread = start_server(logRequests=False)
        self.proxy = xmlrpclib.ServerProxy(
            "http://127.0.0.1:8000/",
            allow_none=True
        )
        self.remote = lambda name: RemoteClass(self.proxy, name)

    def test_whats_registered(self):
        must_be_provided = ('classes', 'create', 'instances', 'shutdown')
        provided_methods = self.proxy.system.listMethods()
        self.assertTrue(all([method in provided_methods
                             for method in must_be_provided]))

    def test_remote_power(self):
        PowFixture = self.remote('PowFixture')
        self.assertEqual(PowFixture(3).pow(2), 9)

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
        modules = [m.__name__ for m in import_modules()]
        self.assertEqual(modules, ['pow_fixture', 'div_fixture'])

    def test_import_classes_founds_submodules(self):
        classes = import_classes()
        self.assertEqual(sorted(classes.keys()),
                         ['DivFixture', 'PowFixture'])


if __name__ == '__main__':
    unittest.main()
