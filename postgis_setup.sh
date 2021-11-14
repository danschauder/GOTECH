pg_ctl -D db initdb;
pg_ctl -D db -l db/log start;
createuser -s GOTECH;
createdb -O GOTECH coral_data;
psql -d coral_data -U GOTECH -c 'CREATE EXTENSION postgis;';
psql -d coral_data -U GOTECH -c 'CREATE EXTENSION postgis_raster;';
psql -d coral_data -U GOTECH -c 'CREATE EXTENSION postgis_topology;';
psql -d coral_data -U GOTECH -c 'CREATE SCHEMA raw;';