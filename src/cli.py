from optparse import OptionParser
from .server import create_server


def main():
    parser = OptionParser()
    parser.add_option("-p", "--port", help="Server port")
    parser.add_option("-d", "--dir", help="Package directory path")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print log messages to stdout")
    (options, args) = parser.parse_args()
    if options.verbose:
        print "Listening on port %d..." % (options.port)
    create_server(options.port, options.verbose).serve_forever()
