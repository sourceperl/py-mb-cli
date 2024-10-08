import argparse
import logging
import sys

from IPython import embed
from pyModbusTCP.client import ModbusClient

from . import __version__
from .cli import Cli, Convert
from .help import HEADER_TXT, HELP_TXT


def help():
    print(HELP_TXT)


def main():
    # init logging
    logging.basicConfig(format='%(name)s:%(message)s')
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
    parser.add_argument('-c', '--cmd', type=str, default='', help='command to run')
    parser.add_argument('-H', '--host', type=str, default='localhost', help='Host (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=502, help='TCP port (default: 502)')
    parser.add_argument('-u', '--unit-id', type=int, default=1, help='unit id (default: 1)')
    parser.add_argument('-t', '--timeout', type=float, default=4.0, help='timeout (default: 4.0s)')
    parser.add_argument('-v', '--version', action='store_true', help='output version and exit')
    args = parser.parse_args()

    # version request
    if args.version:
        print(__version__)
        exit(0)

    # an helper to convert modbus data
    convert = Convert()

    # init modbus client
    cli = Cli(ModbusClient(host=args.host, port=args.port, unit_id=args.unit_id, timeout=args.timeout), 
              debug=args.debug)
    # if a command is set, run it and show result
    if args.cmd:
        try:
            print(eval(args.cmd))
        except ValueError as e:
            print(e)
    # when no command is set, start in interactive mode
    else:
        sys.exit(embed(banner1=HEADER_TXT, banner2='', exit_msg=''))
