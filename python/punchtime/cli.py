"""cli entry point for punchtime probe.
Parse command line arguments in, start punchtime probe.
"""
from pathlib import Path

import argparse
import signal
import sys
import textwrap
import traceback

import punchtime.logger
import punchtime.version


def main(args=None):
    """Entry point for punchtime cli.
    The setup_py entry_point wraps this in sys.exit already so this effectively
    becomes sys.exit(main()).
    The __main__ entry point similarly wraps sys.exit().
    """
    if args is None:
        args = sys.argv[1:]

    parsed_args = get_args(args)

    try:
        punchtime.logger.set_root_logger(log_level=parsed_args.log_level,
                                         log_path=parsed_args.log_path)

        # Execute runner code here #

    except KeyboardInterrupt:
        # Shell standard is 128 + signum = 130 (SIGINT = 2)
        sys.stdout.write("\n")
        return 128 + signal.SIGINT
    except Exception as e:
        # stderr and exit code 255
        sys.stderr.write("\n")
        sys.stderr.write(f"\033[91m{type(e).__name__}: {str(e)}\033[0;0m")
        sys.stderr.write("\n")
        # at this point, you're guaranteed to have args and thus log_level
        if parsed_args.log_level:
            if parsed_args.log_level < 10:
                # traceback prints to stderr by default
                traceback.print_exc()

        return 255

# region cli args


def get_args(args):
    """Parse arguments passed in from shell."""
    return get_parser().parse_args(args)


def get_parser():
    """Return ArgumentParser for punchtime cli."""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description='punchtime probe',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--log', '--loglevel', dest='log_level', type=int,
                        default=None,
                        help=wrap(
                            'Integer log level. Defaults to 25 (NOTIFY).\n'
                            '10=DEBUG \n'
                            '20=INFO\n'
                            '25=NOTIFY\n'
                            '30=WARNING\n'
                            '40=ERROR\n'
                            '50=CRITICAL\n'
                            'Log Level < 10 gives full traceback on errors.'))
    parser.add_argument('--logpath', dest='log_path',
                        help=wrap(
                            'Log-file path. Append log output to this path.'))
    parser.add_argument('--version', action='version',
                        help='Echo version number.',
                        version=f'{punchtime.version.get_version()}')
    return parser


def wrap(text, **kwargs):
    """Wrap lines in argparse so they align nicely in 2 columns.
    Default width is 70.
    With gratitude to paul.j3 https://bugs.python.org/issue12806
    """
    # apply textwrap to each line individually
    text = text.splitlines()
    text = [textwrap.fill(line, **kwargs) for line in text]
    return '\n'.join(text)

# endregion cli args
