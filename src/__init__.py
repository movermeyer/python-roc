from .server import start_server, create_server
from .remote_class import RemoteClass
from .client import create_remote
from .cli import main


__all__ = (start_server, create_server, RemoteClass, create_remote)


if __name__ == '__main__':
    main()
