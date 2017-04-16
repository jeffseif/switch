import datetime

from switch import __author__
from switch import __description__
from switch import __version__
from switch import __year__
from switch.amazon import amazon
from switch.walmart import walmart
from switch.target import target


ZIPCODE = 94703


def main():
    import argparse

    __version__author__year__ = '{} | {} {}'.format(
        __version__,
        __author__,
        __year__,
    )

    parser = argparse.ArgumentParser(
        description=__description__,
        epilog='Version {}'.format(__version__author__year__),
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__author__year__),
    )
    subparsers = parser.add_subparsers()

    # Parent
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='Increase output verbosity',
    )
    parent.add_argument(
        '-z',
        '--zipcode',
        default=ZIPCODE,
        type=int,
        help='Zipcode for location searching (e.g., %(default)s)',
    )
    parents = (parent,)

    # Amazon
    amazon_parser = subparsers.add_parser(
        'amazon',
        parents=parents,
        help='Check amazon',
    )
    amazon_parser.set_defaults(func=amazon)

    # Target
    target_parser = subparsers.add_parser(
        'target',
        parents=parents,
        help='Check target',
    )
    target_parser.set_defaults(func=target)

    # Walmart
    walmart_parser = subparsers.add_parser(
        'walmart',
        parents=parents,
        help='Check walmart',
    )
    walmart_parser.set_defaults(func=walmart)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)


if __name__ == '__main__':
    import sys
    sys.exit(main())
