import unittest
import test_data.pow_fixture
from roc.remote_class import RemoteClass


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


if __name__ == '__main__':
    unittest.main()
