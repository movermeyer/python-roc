def create_remote(host='127.0.0.1', port=8000):
    import xmlrpclib
    from remote_class import RemoteClass
    connection = xmlrpclib.ServerProxy(
        "http://%s:%d/" % (host, port),
        allow_none=True
    )
    return connection, lambda name: RemoteClass(connection, name)
