#!/usr/bin/env bash

# the code and data is from
# https://github.com/minus34/gnaf-loader
# credit for gnaf loader goes to above repo

SECONDS=0*

echo "----------------------------------------------------------------------------------------------------------------"
echo " start dump file restore"
echo "----------------------------------------------------------------------------------------------------------------"

psql -d gnaf -U addruser -c "CREATE EXTENSION IF NOT EXISTS postgis;"

pg_restore -Fc -d gnaf -p 5432 -U addruser /addr/storage/dump/gnaf-202102.dmp

duration=$SECONDS

echo " End time : $(date)"
echo " it took $((duration / 60)) mins"
echo "----------------------------------------------------------------------------------------------------------------"