import logging
import re
import sys

from pg_events.core.build import Build
from pg_events.core.worker import Worker


def worker(args):
    if not args.settings:
        log.info("Please pass in settings module using --settings")
        sys.exit(1)

    module_path = re.sub('.py$', '', args.settings)
    settings = __import__(module_path)
    worker = Worker(settings)
    worker.execute()


def build(args):
    if not args.settings:
        log.info("Please pass in settings module using --settings")
        sys.exit(1)

    module_path = re.sub('.py$', '', args.settings)
    settings = __import__(module_path)
    build = Build(settings)
    build.execute()


def add_commands(subparsers):
    attach_parser = subparsers.add_parser('worker')
    attach_parser.add_argument('--settings')
    attach_parser.set_defaults(func=worker)

    attach_parser = subparsers.add_parser('build')
    attach_parser.add_argument('--settings')
    attach_parser.set_defaults(func=build)
