import socket
import unittest
from roc.client import wait, is_online


class ProxyMock(object):
    def __init__(self, is_raising=False, errno=10060):
        self.classes_called = 0
        self.is_raising = is_raising
        self.errno = errno

    def classes(self):
        self.classes_called += 1
        if self.is_raising:
            raise socket.error(self.errno, 'Something bad')


class OnlineTestCase(unittest.TestCase):
    def test_online_checks_on_classes_function(self):
        proxy = ProxyMock()
        self.assertTrue(is_online(proxy))
        self.assertEqual(proxy.classes_called, 1)

    def test_wait_check_online_once(self):
        proxy = ProxyMock()
        self.assertTrue(wait(proxy))
        self.assertEqual(proxy.classes_called, 1)


class WaitTestCase(unittest.TestCase):
    def test_wait_repeats_ok(self):
        proxy = ProxyMock(is_raising=True)
        self.assertFalse(wait(proxy, repeat_timout_sec=0))
        self.assertEqual(proxy.classes_called, 10)

    def test_wait_reraises(self):
        proxy = ProxyMock(is_raising=True, errno=666)
        self.assertRaises(socket.error, lambda: wait(proxy))


if __name__ == '__main__':
    unittest.main()
