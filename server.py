import threading
import collections
from SimpleXMLRPCServer import SimpleXMLRPCServer


def main():
    server = create_server()
    print "Listening on port 8000..."
    server.serve_forever()


def create_server(logRequests=True):
    server = SimpleXMLRPCServer(("127.0.0.1", 8000),
                                allow_none=True,
                                logRequests=logRequests)
    server.register_introspection_functions()
    server.register_function(
        lambda: stop_server(server),
        "shutdown"
    )
    available_classes = import_classes()
    existing_instances = collections.defaultdict(lambda: [])
    server.register_function(
        lambda: available_classes.keys(),
        "classes"
    )
    server.register_function(
        lambda: existing_instances.keys(),
        "instances"
    )

    @server.register_function
    def create(class_name, args=None):
        instance = available_classes[class_name]['class'](*args)
        instance_idx = len(existing_instances[class_name])
        instance_name = '%s_%d' % (class_name, instance_idx)
        for method_name in available_classes[class_name]['methods']:
            bound_name = '.'.join([instance_name, method_name])
            bound_method = getattr(instance, method_name)
            server.register_function(bound_method, bound_name)
        existing_instances[class_name].append(instance)
        return instance_name
    return server


def start_server(logRequests=True):
    thread = threading.Thread(
        target=create_server(logRequests).serve_forever
    )
    thread.start()
    return thread


def stop_server(server):
    thread = threading.Thread(target=server.shutdown)
    thread.start()
    thread.join()


def import_classes(fixtures_package_name='fixtures'):
    import inspect
    fixtures = __import__(fixtures_package_name)
    modules = inspect.getmembers(fixtures, inspect.ismodule)
    classes = {}
    for _, module in modules:
        for class_name, Class in inspect.getmembers(module, inspect.isclass):
            methods = [n
                       for n, _ in inspect.getmembers(Class, inspect.ismethod)
                       if '__' not in n]
            classes[class_name] = {
                'class': Class,
                'methods': methods,
            }
    return classes


if __name__ == '__main__':
    main()
