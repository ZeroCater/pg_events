import logging
import select

from pg_events.core.base import Command

log = logging.getLogger(__name__)


DATA_UPDATE_CHANNELS = ['pgevents_data_update']
TABLE_UPDATE_CHANNELS = ['pgevents_table_alter', 'pgevents_table_drop']


class Worker(Command):

    def execute(self):
        conn = self.establish_connection()

        curs = conn.cursor()
        for channel in DATA_UPDATE_CHANNELS + TABLE_UPDATE_CHANNELS:
            curs.execute('LISTEN {};'.format(channel))

        while 1:
            if select.select([conn], [], [], 5) == ([], [], []):
                log.info('Notification Timeout')
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    log.info('Notification {} received'.format(notify.channel))
                    if notify.channel in DATA_UPDATE_CHANNELS:
                        self.data_update_callback(notify.payload)
                    elif notify.channel in TABLE_UPDATE_CHANNELS:
                        self.db_schema_update_callback(notify.payload)
