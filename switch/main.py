import datetime

from switch import __author__
from switch import __description__
from switch import __version__
from switch import __year__
from switch.amazon import amazon
from switch.bestbuy import bestbuy
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

    # BestBuy
    bestbuy_parser = subparsers.add_parser(
        'bestbuy',
        parents=parents,
        help='Check bestbuy',
    )
    bestbuy_parser.set_defaults(func=bestbuy)

    # Target
    target_parser = subparsers.add_parser(
        'target',
        parents=parents,
        help='Check target',
    )
    target_parser.set_defaults(func=target)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)


if __name__ == '__main__':
    import sys
    sys.exit(main())
