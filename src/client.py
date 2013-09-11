import six
from .remote_class import RemoteClass


def create_remote(host='127.0.0.1', port=8000):
    if six.PY2:
        from xmlrpclib import ServerProxy
    elif six.PY3:
        from xmlrpc.client import ServerProxy
    connection = ServerProxy(
        "http://%s:%d/" % (host, port),
        allow_none=True
    )
    return connection, lambda name: RemoteClass(connection, name)
