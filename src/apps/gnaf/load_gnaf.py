import os
import psycopg2
import argparse
from datetime import datetime
import logging
import pandas
import pdb

"""
    gnaf loader source is from https://github.com/minus34/gnaf-loader
    credit for this part of code goes to https://github.com/minus34/gnaf-loader
"""
def main():

    # setup Logging component
    # if you want basic logic on terminal use the below
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    log_filename = 'load_gnaf.log'
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.basicConfig(filename=log_filename, filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    # if you want to log all the message use the below statment instead of the above
    # logging.basicConfig(filename='log_filename.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # set command line arguments
    args = set_arguments()

    # get settings from arguments
    settings = get_settings(args)

    # connect to Postgres
    try:
        pg_conn = psycopg2.connect(settings['pg_connect_string'])
    except psycopg2.Error:
        logging.info(
            "Unable to connect to database - ACTION: Check your Postgres parameters and/or database security")
        return False

    pg_conn.autocommit = True
    pg_cur = pg_conn.cursor()

    logging.info("Start loading program...")
    start_time = datetime.now()

    logging.info("Step 1 : Create Tables {0}".format(start_time))

    create_tables_script(pg_cur, settings)
    create_load_script(settings)
    create_index_script(settings)
    # analyse_raw_gnaf_tables(pg_cur, settings)
    create_contraint_script(pg_cur, settings)
    create_view_script(settings)

    # close Postgres connection
    pg_cur.close()
    pg_conn.close()

    # populate_raw_gnaf(settings)
    # index_raw_gnaf(settings)
    # if settings['primary_foreign_keys']:
    #     create_primary_foreign_keys(settings)
    # else:
    #     logging.info("\t- Step 6 of 7 : primary & foreign keys NOT created")
    # analyse_raw_gnaf_tables(pg_cur, settings)

    # Call the Main Address Validation Function
    # addressValidation(rangeNum)


############################################################################################################################
#  set the command line arguments
############################################################################################################################

def set_arguments():

    parser = argparse.ArgumentParser(
        description='Tool to load the complete GNAF into Postgres, '
        'GNAF geocodes for address validation')

    # directories
    parser.add_argument(
        '--gnaf-file-path', required=True,
        help='Path to source GNAF tables (*.psv files). make sure user has read permission on this folder ')

    return parser.parse_args()

############################################################################################################################
#  get the command line arguments
############################################################################################################################

# create the dictionary of settings


def get_settings(args):
    settings = dict()

    settings['gnaf_file_path'] = args.gnaf_file_path

    # create postgres connect string
    settings['pg_host'] = os.getenv("PG_HOST", "addr_database")
    settings['pg_port'] = os.getenv("PG_PORT", 5432)
    settings['pg_db'] = "gnaf"
    settings['pg_user'] = os.getenv("PG_USER", "addruser")
    settings['pg_password'] = os.getenv("PG_PASSWORD", "password")

    settings['pg_connect_string'] = "dbname='{0}' host='{1}' port='{2}' user='{3}' password='{4}'".format(
        settings['pg_db'], settings['pg_host'], settings['pg_port'], settings['pg_user'], settings['pg_password'])

    # set postgres script directory
    settings['scripts'] = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "scripts")

    return settings


############################################################################################################################
#  Run the gnaf create table
############################################################################################################################

def create_tables_script(pg_cur, settings):

    logging.info("Creating table script: {0}".format(datetime.now()))

    # let's find the path for sql scripts created by GNAF
    gnafFile = settings['gnaf_file_path'] + \
        '/Extras/GNAF_TableCreation_Scripts/create_tables_ansi.sql'

    # let's read gnaf file create_tables_ansi.sql and remove 'REM'
    fpr = open(gnafFile, "r")
    lines = fpr.readlines()
    fpr.close()

    osqlfile = settings['scripts'] + "/01_create_tables.sql"

    fpw = open(osqlfile, "w")
    for line in lines:
        if line[:4] != 'REM ':
            fpw.write(line)

    fpw.close()

############################################################################################################################
#  Let's create a script for load of psv files
############################################################################################################################


def create_load_script(settings):

    logging.info("Creating load script : {0}".format(datetime.now()))

    # let's process the authority files before
    # authority contains the reference data and needs to be loaded first

    loadfile = settings['scripts'] + "/02_load_data.sql"
    fpload = open(loadfile, "w")

    prefix = 'authority_code'
    for root, dirs, files in os.walk(settings['gnaf_file_path']):
        for file_name in files:
            if file_name.lower().startswith(prefix) and file_name.lower().endswith(".psv"):
                file_path = os.path.join(root, file_name)
                table = file_name.lower().replace(prefix + "_", "", 1).replace("_psv.psv", "")

                sql = "\COPY {0} FROM '{1}' DELIMITER '|' CSV HEADER;"\
                    .format(table, file_path)
                fpload.write(sql)
                fpload.write("\n")

    states = ['act', 'nsw', 'nt', 'ot', 'qld', 'sa', 'tas', 'vic', 'wa']
    for state in states:
        prefix = state
        logging.info("processing state: " + state)
        for root, dirs, files in os.walk(settings['gnaf_file_path']):
            for file_name in files:
                if file_name.lower().startswith(prefix) and file_name.lower().endswith(".psv"):
                    file_path = os.path.join(root, file_name)
                    table = file_name.lower().replace(prefix + "_", "", 1).replace("_psv.psv", "")

                    sql = "\COPY {0} FROM '{1}' DELIMITER '|' CSV HEADER;"\
                        .format(table, file_path)
                    fpload.write(sql)
                    fpload.write("\n")

    fpload.close()

############################################################################################################################
#  Run the gnaf create table
############################################################################################################################


def create_index_script(settings):

    logging.info("Creating index script: {0}".format(datetime.now()))

    # we have created a generic file which contains the indexes, lets change the schema from raw_gnaf to input schema
    genIdxfile = settings['scripts'] + "/00_generic_create_indexes.sql"

    # let's read gnaf file create_tables_ansi.sql and remove 'REM'
    fpr = open(genIdxfile, "r")
    lines = fpr.readlines()
    fpr.close()

    osqlfile = settings['scripts'] + "/03_create_indexes.sql"

    fpw = open(osqlfile, "w")
    for line in lines:
        fpw.write(line)

    fpw.close()

############################################################################################################################
#  analyse_raw_gnaf_tables: analyse tables
############################################################################################################################


def analyse_raw_gnaf_tables(pg_cur, settings):

    logging.info("Creating index script: {0}".format(datetime.now()))

    # get list of tables that haven't been analysed (i.e. that have no real row count)
    sql = "SELECT nspname|| '.' || relname AS table_name " \
        "FROM pg_class C LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)" \
        "WHERE nspname = '{0}' AND relkind='r' AND reltuples = 0".format(
            'public')
    pg_cur.execute(sql)

    anlyfile = settings['scripts'] + "/04_analyze_tables.sql"

    fpw = open(anlyfile, "w")

    for pg_row in pg_cur:
        sql = "ANALYZE {0}".format(pg_row[0]) + ";"
        fpw.write(sql)
        fpw.write("\n")

    fpw.close()


############################################################################################################################
#  generate FK constraints
############################################################################################################################

def create_contraint_script(pg_cur, settings):

    logging.info("Creating fk contraint script: {0}".format(datetime.now()))

    # let's find the path for sql scripts created by GNAF
    gnafFile = settings['gnaf_file_path'] + \
        '/Extras/GNAF_TableCreation_Scripts/add_fk_constraints.sql'

    # let's read gnaf file create_tables_ansi.sql and remove 'REM'
    fpr = open(gnafFile, "r")
    lines = fpr.readlines()
    fpr.close()

    osqlfile = settings['scripts'] + "/05_add_fk_constraints.sql"

    fpw = open(osqlfile, "w")
    for line in lines:
        if line[:4] != 'REM ':
            fpw.write(line)

    fpw.close()


############################################################################################################################
#  create view
############################################################################################################################

def create_view_script(settings):

    logging.info("Creating view script: {0}".format(datetime.now()))

    # we have created a generic file which contains the indexes, lets change the schema from raw_gnaf to input schema
    genIdxfile = settings['scripts'] + "/00_generic_address_view.sql"

    # let's read gnaf file create_tables_ansi.sql and remove 'REM'
    fpr = open(genIdxfile, "r")
    lines = fpr.readlines()
    fpr.close()

    osqlfile = settings['scripts'] + "/06_create_view.sql"

    fpw = open(osqlfile, "w")
    for line in lines:
        fpw.write(line)

    fpw.close()


############################################################################################################################
#  Call of main program
############################################################################################################################

if __name__ == '__main__':
    # For the time call the main program without any parameters
    main()
