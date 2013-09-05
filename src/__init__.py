from .server import start_server, create_server
from .remote_class import RemoteClass


__all__ = (start_server, create_server, RemoteClass)


if __name__ == '__main__':
    from .cli import main
    main()
