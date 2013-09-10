import six


def create_remote(host='127.0.0.1', port=8000):
    if six.PY2:
        from xmlrpclib import ServerProxy
    elif six.PY3:
        from xmlrpc.client import ServerProxy
    from .remote_class import RemoteClass
    connection = ServerProxy(
        "http://%s:%d/" % (host, port),
        allow_none=True
    )
    return connection, lambda name: RemoteClass(connection, name)

if __package__ is None:
    __package__ = "roc.client"
