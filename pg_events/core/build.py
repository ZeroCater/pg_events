import logging
import os

from pg_events.core.base import Command

log = logging.getLogger(__name__)


class Build(Command):

    def execute(self):
        conn = self.establish_connection()
        conn.autocommit = True

        path = os.path.dirname(__file__)
        cursor = conn.cursor()

        log.info('Creating triggers ...')
        schema_path = os.path.join(path, 'schemas/triggers.sql')
        cursor.execute(open(schema_path, 'r').read())

        schema_path = os.path.join(path, 'schemas/event_triggers.sql')
        cursor.execute(open(schema_path, 'r').read())

        cursor.execute('SELECT pgevents_create_db_triggers();')
        log.info('Creating triggers done.')
