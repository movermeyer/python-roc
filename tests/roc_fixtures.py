import os
import sys
import test_data
sys.path.insert(0, os.path.join('..'))
from src import client
from src import server


TEST_DATA = os.path.dirname(test_data.__file__)


class RemoteClassFixture(object):
    def __init__(self):
        self.connection = None
        self.remote = None
        self.port = None
        self.instance = None

    def givenServerStartedAtPort(self, port):
        self.port = int(port)
        self.server_thread = server.start_server(TEST_DATA, port=self.port)
        self.connection, self.remote = client.create_remote(port=self.port)

    def createRemoteClassWithArgument(self, classname, arg1):
        Class = self.remote(classname)
        self.instance = Class(int(arg1))

    def remotePow(self, power):
        return str(self.instance.pow(int(power)))

    def shutdownServer(self):
        self.connection.shutdown()
        self.server_thread.join()
