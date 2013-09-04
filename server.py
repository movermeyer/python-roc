import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
from remote_fixture import PowFixture
PowFixture  # lint: ok


def main():
    server = createServer()
    print "Listening on port 8000..."
    server.serve_forever()


def createServer(logRequests=True):
    server = SimpleXMLRPCServer(("127.0.0.1", 8000),
                                allow_none=True,
                                logRequests=logRequests)
    server.register_introspection_functions()
    server.register_function(
        lambda: threading.Thread(target=server.shutdown).start(),
        "shutdown"
    )

    @server.register_function
    def create(class_name, args=None):
        instance_name = class_name + '_inst'
        Class = globals()[class_name]
        instance = Class(*args)
        for item_name in Class.__dict__:
            if '__' not in item_name:
                item = getattr(instance, item_name)
                if callable(item):
                    name = '.'.join([instance_name, item_name])
                    # print 'register_function', name
                    server.register_function(item, name)
        return instance_name
    return server


def startServer(logRequests=True):
    thread = threading.Thread(
        target=createServer(logRequests).serve_forever
    )
    thread.start()
    return thread


if __name__ == '__main__':
    main()
