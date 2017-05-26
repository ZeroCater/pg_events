
"""Entry-point for the :program:`pg_events` umbrella command."""
import argparse
import logging

from pg_events.core import commands

__all__ = ['main']


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(prog='pg_events')
    subparsers = parser.add_subparsers()

    commands.add_commands(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':  # pragma: no cover
    main()
