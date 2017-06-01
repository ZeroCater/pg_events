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
    attach_parser.add_argument('--settings', required=True)
    attach_parser.set_defaults(func=worker)

    attach_parser = subparsers.add_parser('build')
    attach_parser.add_argument('--settings', required=True)
    attach_parser.add_argument('--auto-rebuild', default=True, type=bool, dest='auto_rebuild')
    attach_parser.set_defaults(func=build)
