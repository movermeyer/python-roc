import os
import test_data
from roc import start_server, server_proxy, remote_module


TEST_DATA = os.path.dirname(test_data.__file__)


class RemoteClassFixture(object):
    def __init__(self):
        self.proxy = None
        self.remote_module = None
        self.port = None
        self.instance = None

    def givenServerStartedAtPort(self, port):
        self.port = int(port)
        self.server_thread = start_server(TEST_DATA, port=self.port)
        self.proxy = server_proxy(port=self.port)
        self.remote_module = remote_module(self.proxy)

    def createRemoteClassWithArgument(self, classname, arg1):
        Class = getattr(self.remote_module, classname)
        self.instance = Class(int(arg1))

    def remotePow(self, power):
        return str(self.instance.pow(int(power)))

    def shutdownServer(self):
        self.proxy.shutdown()
        self.server_thread.join()


if __name__ == '__main__':
    rcf = RemoteClassFixture()
    rcf.givenServerStartedAtPort('3333')
    rcf.createRemoteClassWithArgument('PowFixture', '3')
    print(rcf.remotePow('2') == '9')
    rcf.shutdownServer()
