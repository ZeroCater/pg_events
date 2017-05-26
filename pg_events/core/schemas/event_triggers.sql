CREATE OR REPLACE FUNCTION pgevents_table_alter_event() RETURNS event_trigger AS $$
DECLARE rec RECORD;
BEGIN
    FOR rec IN SELECT * FROM pg_event_trigger_ddl_commands() LOOP
        PERFORM pg_notify('pgevents_table_alter', json_build_object('classid', rec.classid, 'objid', rec.objid,
            'objsubid', rec.objsubid, 'command_tag', rec.command_tag, 'object_type', rec.object_type::TEXT,
            'schema_name', rec.schema_name::TEXT, 'object_identity', rec.object_identity::TEXT,
            'in_extension', rec.in_extension)::TEXT);
    END LOOP;

    PERFORM pgevents_create_db_triggers();
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION pgevents_table_drop_event() RETURNS event_trigger AS $$
DECLARE rec RECORD;
BEGIN
    FOR rec IN SELECT * FROM pg_event_trigger_dropped_objects() LOOP
        IF rec.original THEN
            PERFORM pg_notify('pgevents_table_drop', json_build_object('classid', rec.classid, 'objid', rec.objid,
                'objsubid', rec.objsubid, 'original', rec.original, 'normal', rec.normal,
                'is_temporary', rec.is_temporary, 'object_type', rec.object_type::TEXT,
                'schema_name', rec.schema_name::TEXT, 'object_name', rec.object_name::TEXT,
                'object_identity', rec.object_identity::TEXT)::TEXT);
        END IF;
    END LOOP;

    PERFORM pgevents_create_db_triggers();
END;
$$
LANGUAGE plpgsql;


DROP EVENT TRIGGER IF EXISTS pgevents_notice_alter_table;

CREATE EVENT TRIGGER pgevents_notice_alter_table
  ON ddl_command_end WHEN TAG IN ('ALTER TABLE', 'CREATE TABLE', 'DROP TABLE')
  EXECUTE PROCEDURE pgevents_table_alter_event();


DROP EVENT TRIGGER IF EXISTS pgevents_notice_drop_table;

CREATE EVENT TRIGGER pgevents_notice_drop_table
  ON sql_drop WHEN TAG IN ('ALTER TABLE', 'DROP TABLE')
  EXECUTE PROCEDURE pgevents_table_drop_event();
