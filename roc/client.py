import six
import collections
from .remote_class import bound_remote_class
from .loader import load_classes


def create_remote(host='127.0.0.1', port=8000):
    if six.PY2:
        from xmlrpclib import ServerProxy
    elif six.PY3:
        from xmlrpc.client import ServerProxy
    connection = ServerProxy(
        "http://%s:%d/" % (host, port),
        allow_none=True
    )
    return connection, bound_remote_class(connection)


def import_remote(package, bound_remote):
    classes = [(class_name, bound_remote(data['class']))
               for class_name, data in load_classes(package)]
    RemoteModule = collections.namedtuple('RemoteModule',
                                          [n for (n, _) in classes])
    return RemoteModule(*[c for (_, c) in classes])
