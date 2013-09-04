import xmlrpclib
import unittest
from pow_fixture import PowFixture
from remote_class import RemoteClass
from server import startServer


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
        self.server_thread = startServer(logRequests=False)
        self.proxy = xmlrpclib.ServerProxy(
            "http://127.0.0.1:8000/",
            allow_none=True
        )

    def test_remote_power(self):
        PowFixture = RemoteClass(self.proxy, 'PowFixture')
        self.assertEqual(PowFixture(3).pow(2), 9)

    def tearDown(self):
        self.proxy.shutdown()
        self.server_thread.join()


if __name__ == '__main__':
    unittest.main()
