from switch import __author__
from switch import __description__
from switch import __version__
from switch import __year__
from switch.amazon import amazon
from switch.ifttt import maybe_load_configs
from switch.logger import set_logging_verbosity
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
        '-b',
        '--beyond-console',
        action='store_true',
        default=False,
        help='Check products beyond just the console',
    )
    parent.add_argument(
        '-c',
        '--config-path',
        default=None,
        help='Path to IFTTT config json file',
    )
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

    # All
    all_parser = subparsers.add_parser(
        'all',
        parents=parents,
        help='Check all',
    )
    all_parser.set_defaults(funcs=(amazon, target, walmart))

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
    set_logging_verbosity(args.verbose)
    maybe_load_configs(args)
    if hasattr(args, 'func'):
        args.func(args)
    if hasattr(args, 'funcs'):
        for func in args.funcs:
            func(args)


if __name__ == '__main__':
    import sys
    sys.exit(main())
