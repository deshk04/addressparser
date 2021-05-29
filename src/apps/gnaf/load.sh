#! /bin/bash -xv

# data can be download from
# https://data.gov.au/data/dataset/19432f89-dc3a-4ef3-b943-5326ef1dbecc/resource/4b084096-65e4-4c8e-abbe-5e54ff85f42f/download/aug19_gnaf_pipeseparatedvalue.zip
# and store below

export PGDATABASE=gnaf
export GNAFPATH="/addr/storage/dump/G-NAF_MAY21_AUSTRALIA_GDA94/G-NAF"

# export PSMAVERSION=201905
export PG_HOST='addr_database'
export PG_USER='addruser'
export PG_PASSWORD='M1ll4murr4'
python3 load_gnaf.py --gnaf-file-path=$GNAFPATH
if [ $? -ne 0 ]
then
    echo "load_gnaf.py failed!!!! - "
else
   psql -d $PGDATABASE -f ./scripts/01_create_tables.sql
   if [ $? -ne 0 ]
   then
      echo "failed: 01_create_tables"
   fi

   psql -d $PGDATABASE -f ./scripts/02_load_data.sql
   if [ $? -ne 0 ]
   then
      echo "failed: 02_load_data.sql"
   fi

   psql -d $PGDATABASE -f ./scripts/03_create_indexes.sql
   if [ $? -ne 0 ]
   then
      echo "failed: 03_create_indexes.sql"
   fi

   psql -d $PGDATABASE -f ./scripts/05_add_fk_constraints.sql
   if [ $? -ne 0 ]
   then
      echo "failed: 05_add_fk_constraints.sql"
   fi

   psql -d $PGDATABASE -f ./scripts/06_create_view.sql
   if [ $? -ne 0 ]
   then
      echo "failed: 06_create_view.sql"
   fi

fi

