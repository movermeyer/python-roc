import unittest
import test_data.pow_fixture
from roc.remote import RemoteClass, bound_remote_class
from roc.client import import_remote


class RemoteClassTestCase(unittest.TestCase):
    class ServerMock(object):
        def create(self, class_name, args):
            instance_name = 'PowFixture-instance'
            setattr(self, instance_name,
                    test_data.pow_fixture.PowFixture(*args))
            return instance_name

    def test_remote_power(self):
        PowFixture = RemoteClass(self.ServerMock(), 'PowFixture')
        self.assertEqual(PowFixture(3).pow(2), 9)

    def test_import_remote(self):
        import os
        here = os.path.dirname(__file__)
        BoundRemote = bound_remote_class(self.ServerMock())
        remote = import_remote(
            os.path.join(here, 'test_data'),
            BoundRemote
        )
        self.assertTrue(remote.PowFixture is not None)


if __name__ == '__main__':
    unittest.main()
