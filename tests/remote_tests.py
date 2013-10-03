from roc.remote import RemoteModule
import unittest


class SomeClass(object):
    def __init__(self):
        self.bar = 'not a func'

    def foo(self, a, b):
        return a + b

    def bar(self, a, b):
        return a + b


class ProxyMock(object):
    def classes(self):
        return 'Foo', 'Bar'

    def create(self, class_name, args):
        self.foo_instance = getattr(self, class_name)(*args)
        return 'foo_instance'

    class Foo(object):
        def __init__(self, symbol):
            self.symbol = symbol

        def baz(self):
            return 'baz ' + self.symbol

    class Bar(object):
        def __init__(self, symbol):
            self.symbol = symbol

        def baz(self):
            return 'BAZ ' + self.symbol


class RemoteModuleTestCase(unittest.TestCase):
    def test_finds_classes(self):
        proxy = ProxyMock()
        rmodule = RemoteModule(proxy)
        self.assertTrue(hasattr(rmodule, 'Foo'))
        self.assertTrue(hasattr(rmodule, 'Bar'))
        self.assertFalse(hasattr(rmodule, 'Baz'))

    def test_creates_class(self):
        r_foo = RemoteModule(ProxyMock()).Foo('A')
        self.assertTrue(r_foo.baz(), 'remote A')

    def test_creates_different_classes(self):
        rmodule = RemoteModule(ProxyMock())
        r_foo = rmodule.Foo('A')
        r_bar = rmodule.Bar('B')
        self.assertEqual(r_foo.baz(), 'baz A')
        self.assertEqual(r_bar.baz(), 'BAZ B')


if __name__ == '__main__':
    unittest.main()
