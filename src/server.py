import itertools
import collections
import threading
import six

if six.PY2:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
elif six.PY3:
    from xmlrpc.server import SimpleXMLRPCServer


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
        self.available_classes = import_classes(package_path)
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


def import_classes(package_path):
    from inspect import getmembers, isclass, ismethod
    classes = {}
    for module in import_modules(package_path):
        for class_name, Class in getmembers(module, isclass):
            methods = [n
                       for n, _ in getmembers(Class, ismethod)
                       if '__' not in n]
            classes[class_name] = {
                'class': Class,
                'methods': methods,
            }
    return classes


def import_modules(package_path):
    import os
    import pkgutil
    for loader, name, is_pkg in pkgutil.walk_packages([package_path]):
        if is_pkg:
            subpackage_path = os.path.join(package_path, name)
            for module in import_modules(subpackage_path):
                yield module
        else:
            yield loader.find_module(name).load_module(name)
