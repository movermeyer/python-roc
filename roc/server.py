import itertools
import collections
import threading
import six

if six.PY2:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
elif six.PY3:
    from xmlrpc.server import SimpleXMLRPCServer

from .loader import load_classes


def start_server(package_path, port=8000, log_requests=True):
    server = create_server(
        package_path,
        port=port,
        logRequests=log_requests,
    )

    def serve_forever_or_die_trying():
        server.serve_forever()
        server.shutdown()  # break request_handle loop
        server.server_close()  # close socket
    thread = threading.Thread(
        target=serve_forever_or_die_trying
    )
    thread.start()
    return thread


def create_server(package_path, port=8000, logRequests=True):
    return RocServer(package_path, port, logRequests).server


class RocServer(object):
    def __init__(self, package_path, port, logRequests=True):
        self.server = SimpleXMLRPCServer(("127.0.0.1", port),
                                         allow_none=True,
                                         logRequests=logRequests)
        self.available_classes = dict(load_classes(package_path))
        self.existing_instances = collections.defaultdict(lambda: [])
        self.server.register_introspection_functions()
        self.server.register_instance(self)

    def shutdown(self):
        threading.Thread(target=self.server.shutdown).start()

    def classes(self):
        return list(self.available_classes.keys())

    def instances(self):
        return list(itertools.chain(*self.existing_instances.values()))

    def create(self, class_name, args=None):
        if args is None:
            args = []
        instance = self.available_classes[class_name]['class'](*args)
        instance_idx = len(self.existing_instances[class_name])
        instance_name = '%s_%d' % (class_name, instance_idx)
        for method_name in self.available_classes[class_name]['methods']:
            bound_name = '.'.join([instance_name, method_name])
            bound_method = getattr(instance, method_name)
            self.server.register_function(bound_method, bound_name)
        self.existing_instances[class_name].append(instance_name)
        return instance_name
