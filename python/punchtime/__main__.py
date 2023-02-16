"""Default execution entry point if running the package via python -m."""
import punchtime.cli
import sys


def main():
    """Run punchtime from script entry point."""
    return punchtime.cli.main()


if __name__ == '__main__':
    sys.exit(main())