CREATE OR REPLACE FUNCTION pgevents_data_update_notify() RETURNS TRIGGER AS $body$
DECLARE
    v_old_data json;
    v_new_data json;
BEGIN
    IF (TG_OP = 'UPDATE') THEN
        v_old_data := row_to_json(OLD);
        v_new_data := row_to_json(NEW);
        PERFORM pg_notify('pgevents_data_update', json_build_object('table_schema', TG_TABLE_SCHEMA::TEXT,'table_name',
            TG_TABLE_NAME::TEXT,'session_user', session_user::TEXT, 'method', TG_OP,'old_data', v_old_data,
            'new_data', v_new_data, 'query', current_query())::TEXT);
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        v_old_data := row_to_json(OLD);
        PERFORM pg_notify('pgevents_data_update', json_build_object('table_schema', TG_TABLE_SCHEMA::TEXT,'table_name',
            TG_TABLE_NAME::TEXT,'session_user', session_user::TEXT, 'method', TG_OP,'old_data', v_old_data,'query',
            current_query())::TEXT);
        RETURN OLD;
    ELSIF (TG_OP = 'INSERT') THEN
        v_new_data := row_to_json(NEW);
        PERFORM pg_notify('pgevents_data_update', json_build_object('table_schema', TG_TABLE_SCHEMA::TEXT,'table_name',
            TG_TABLE_NAME::TEXT,'session_user', session_user::TEXT, 'method', TG_OP,'new_data', v_new_data, 'query',
            current_query())::TEXT);
        RETURN NEW;
    ELSE
        RETURN NULL;
    END IF;
END;
$body$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION pgevents_create_db_triggers() RETURNS SETOF TEXT AS $body$
DECLARE
    rec RECORD;
    command TEXT;
BEGIN
    FOR rec IN
        SELECT
            *
        FROM
            information_schema.tables
        WHERE
            table_schema NOT IN ('pg_catalog', 'information_schema')
            AND table_schema NOT LIKE 'pg_toast%'
            AND table_name NOT LIKE 'pg_%'
    LOOP
        command := format(
            'DROP TRIGGER IF EXISTS %s ON %s; ' ||
            'CREATE TRIGGER %1$s AFTER INSERT OR UPDATE OR DELETE ON %2$s FOR EACH ROW EXECUTE PROCEDURE pgevents_data_update_notify();',
            format('%s__%s', quote_ident(rec.table_schema), quote_ident(rec.table_name)),
            quote_ident(rec.table_name)
        );
        EXECUTE command;
        RETURN NEXT command;
    END LOOP;
    RETURN;
END;
$body$ LANGUAGE plpgsql;
