import sys

from pg_events.core.build import Build
from pg_events.core.worker import Worker


def worker(args):
    worker = Worker(args)
    worker.execute()


def build(args):
    build = Build(args)
    build.execute()


def add_commands(subparsers):
    attach_parser = subparsers.add_parser('worker')
    attach_parser.add_argument('--settings')
    attach_parser.set_defaults(func=worker)

    attach_parser = subparsers.add_parser('build')
    attach_parser.add_argument('--settings')
    attach_parser.set_defaults(func=build)
