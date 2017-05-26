import psycopg2
import psycopg2.extensions
import sys

REQUIRED_SETTINGS_ATTRIBUTES = [
    'PG_EVENTS_DATABASE_URL',
    'PG_EVENTS_DATA_UPDATE_CALLBACK',
    'PG_EVENTS_DB_SCHEMA_UPDATE_CALLBACK',
]


class PgEventWorkerValidationError(Exception):
    pass


class Command(object):

    def __init__(self, settings):
        self.validate_settings(settings)

        self.database_url = settings.PG_EVENTS_DATABASE_URL

        self.data_update_callback = self._get_function(settings.PG_EVENTS_DATA_UPDATE_CALLBACK)
        self.db_schema_update_callback = self._get_function(settings.PG_EVENTS_DB_SCHEMA_UPDATE_CALLBACK)

    def validate_settings(self, settings):
        for attribute in REQUIRED_SETTINGS_ATTRIBUTES:
            if not hasattr(settings, attribute):
                raise PgEventWorkerValidationError('Settings should include attribute {}'.format(attribute))

    def establish_connection(self):
        conn = psycopg2.connect(self.database_url)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        return conn

    def _get_function(self, path):
        module, method = path.rsplit('.', 1)
        return getattr(__import__(module), method)
