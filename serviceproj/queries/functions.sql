-- Active: 1727391738259@@127.0.0.1@5432@servicebase
-- CREATE EXTENSION plsh;

CREATE OR REPLACE FUNCTION public.create_dump(dump_path TEXT)
RETURNS VOID AS $$
#!/bin/bash 
sudo -u postgres pg_dump -Fc -U postgres -d servicebase -f "$1"
$$ LANGUAGE plsh;


-- sudo -u postgres pg_restore '--clean' '--create' '--disable-triggers' -U postgres -d servicebase "$1"

CREATE OR REPLACE FUNCTION public.restore_dump(dump_path TEXT)
RETURNS VOID AS $$
#!/bin/bash
sudo -u postgres pg_restore --clean --create --disable-triggers -U postgres -d servicebase "$1"
$$ LANGUAGE plsh;

CREATE EXTENSION plsh;

CREATE OR REPLACE FUNCTION public.restore_dump(dump_path TEXT)
RETURNS VOID AS $$
#!/bin/bash
sudo psql -U postgres -c "DROP DATABASE IF EXISTS test_servicebase;"
sudo -u postgres pg_restore '--clean' '--create' '--disable-triggers' -U postgres -d servicebase "$1"
$$ LANGUAGE plsh;

SELECT public.restore_dump('/tmp/dump-2024-12-26-15.dump');


CREATE OR REPLACE FUNCTION public.delete_dump(dump_path TEXT)
RETURNS VOID AS $$
#!/bin/bash
rm -f "$1"
$$ LANGUAGE plsh;



SELECT public.create_dump('/tmp/dumpfile1.dump');
SELECT public.delete_dump('/tmp/dumpfile.dump');
