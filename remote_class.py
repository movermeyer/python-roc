class RemoteClass(object):
    def __init__(self, server, class_name):
        self.server = server
        self.class_name = class_name

    def __call__(self, *args):
        instance_name = self.server.create(
            self.class_name,
            args
        )
        self.remote_instance = getattr(
            self.server,
            instance_name
        )
        return self

    def __getattr__(self, name):
        return getattr(self.remote_instance, name)
