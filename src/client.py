import xmlrpclib
from remote_class import RemoteClass


proxy = xmlrpclib.ServerProxy("http://127.0.0.1:8000/",
                              allow_none=True)
PowFixture = RemoteClass(proxy, 'PowFixture')
pow_fixture = PowFixture(3)

assert pow_fixture.pow(2) == 9
proxy.shutdown()
