# Postgres events for Python

This package provides a framework for setting and receiving events from a Postgres database. It will call the defined callback function when data in tables or the schema of the database (tables added/removed, columns modified, etc) changes.

Once properly setup, this package will automatically pick up any changes made to the database and set proper triggers and events. There is no additional steps required to keep the triggers up to date. The build method is idempotent and could be called as many times. We use a combination of Postgres built-in TRIGGER and LISTEN/NOTIFY to call defined methods in python.

**Note:** The auto rebuild feature only works if you have superuser permissions on the database. If you are using a Postgres database on Heroku you cannot use this feature. For more details see the `build` method below.

## Installation

Install the package using `pip`:

```
pip install pg_events
```

The package requires the following constants, the best is to include them in a python file and pass the file as a command-line argument:

```python
PG_EVENTS_DATABASE_URL = <the DATABASE_URL>
PG_EVENTS_DATA_UPDATE_CALLBACK = <my_module.callback_func>
PG_EVENTS_DB_SCHEMA_UPDATE_CALLBACK = <my_module.callback_func>
```

## Initial Build

To create the initial triggers in the database run the following command from the command-line:

```
pg_events build --settings <my_module.settings> [--auto-rebuild <true/false>]
```

The argument `--settings` is the file containing required constants mentioned above.

This prepares the database to send notifications to the worker. The command is idempotent and could be called as many times.
It is only required to be called once on a database. No need to call this after migrations or deploys, it will be fine and have no effect if you do so.
If you are running on a highly active database, it is recommended not to call this method too often, since it recreates all triggers and there is a chance to miss events in between.

If you do not have superuser permissions on the database you should disable auto rebuild. To disable the auto rebuild feature, you can pass the `--auto-rebuild` argument as `false`, the default value is `True`. We recommend using the `build` method as a post deploy or post migration script. The method is idempotent and it's safe to call multiple times.



## Worker

In order to listen to notifications from the database, we will have a worker that constantly listens to these notifications. Once an event is triggered, it calls the defined callback function with the payload of the event.

To start a worker:

```
pg_events worker --settings <my_module.settings>  [--auto-rebuild <true/false>]
```

The worker is very efficient in handling many events. It's recommended to keep callback functions light and process events asynchronously. Otherwise, you might need multiple worker processes.

## Callback functions

There are 2 type of callback functions:

- `PG_EVENTS_DATA_UPDATE_CALLBACK`
- `PG_EVENTS_DB_SCHEMA_UPDATE_CALLBACK` (Only when auto rebuild is not disabled)

### `PG_EVENTS_DATA_UPDATE_CALLBACK`

This function is used when there are changes in any of the tables in the database. The function signature should be as follows:

```
def callback_func(payload):
    ...
```

The only argument is the payload which is a JSON string. The JSON string has the following key/values:

- `table_schema`
- `table_name`,
- `session_user`
- `method`
- `old_data`
- `new_data`
- `query`

The payload could include all or some of the keys depending on if the object is being created, updated or deleted.


### `PG_EVENTS_DB_SCHEMA_UPDATE_CALLBACK`

This function is used when there are changes to tables. For instance, columns have been modified on a table, a table being added or removed, etc. This is not required if you have disabled the auto rebuild feature. The function signature should be as follows:

```
def callback_func(payload):
    ...
```

The only argument is the payload which is a JSON string. Postgres supports very limited amount of data with these events. For more information on what the values are please see [here](https://www.postgresql.org/docs/9.5/static/functions-event-triggers.html). The JSON string has the following key/values.

- `classid`
- `objid`
- `objsubid`
- `command_tag`
- `object_type`
- `object_name`
- `object_identity`
- `schema_name`
- `original`
- `normal`
- `in_extension`
- `is_temporary`

The payload includes only a subset of these keys depending on the type of event being triggered.

