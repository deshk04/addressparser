"""
  Author:
  Create date:
  Description:    PDM database module


  Version     Date                Description(of Changes)
  1.0                             Created
"""

import sys
import psycopg2
import json
import os
import logging

from psycopg2.extras import NamedTupleConnection, RealDictCursor
# from django.core.serializers.json import DjangoJSONEncoder

from hub.general import settings
from hub.general import exceptions
from hub.pattern import Singleton
import pdb

class Database(metaclass=Singleton):
    """
        Database class to run database queries
    """

    def __init__(self, database=settings.CURRENT_DB):
        self.host = os.getenv("PGHOST", settings.DB_HOST)
        self.port = os.getenv("PGPORT", settings.DB_PORT)
        self.db = database
        self.user = os.getenv("PGUSER", settings.DB_USER)
        self.password = os.getenv("PGPASSWORD", "password")
        self.pgconnectstring = "dbname='{0}' host='{1}' port='{2}' \
                                user='{3}' password='{4}'".format(
            self.db, self.host, self.port,
            self.user, self.password)
        try:
            self.connstring = psycopg2.connect(self.pgconnectstring)
        except psycopg2.Error as err:
            logging.debug(err.diag.message_primary)
            raise exceptions.PDMDBConnError(err.diag.message_primary)
        self.connstring.autocommit = True

        self.cursor = self.connstring.cursor(
            cursor_factory=psycopg2.extras.NamedTupleCursor)

    def setdict(self):
        """
            set cursor factory dict
        """
        self.cursor = self.connstring.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)


    def query(self, sqlstring, param=None):
        """
            general query
            sqlstring: sql string
            param: list of parameters to query
        """

        cursor = self.cursor
        try:
            if param:
                cursor.execute(sqlstring, tuple(param))
            else:
                cursor.execute(sqlstring)
        except psycopg2.Error as err:
            logging.debug("Query: " + sqlstring)
            logging.debug(err.diag.message_primary)
            raise exceptions.PDMDBQueryError(err.diag.message_primary)
        return cursor

    def queryasdict(self, sqlstring, param=None):
        """
            return output as dict
        """
        # self.setdict()
        tcursor = self.query(sqlstring, param)
        records = tcursor.fetchall()
        result = []
        columns = [desc[0] for desc in tcursor.description]
        for row in records:
            result.append(dict(zip(columns, row)))

        return result

    def copy(self, sqlstring, filename):
        """
            copy files to postgresql
            sqlstring: sql string
            filename: file to be loaded
        """

        cursor = self.cursor
        try:
            with open(filename, 'rb') as fp:
                cursor.copy_expert(sql=sqlstring, file=fp)
        except psycopg2.Error as err:
            logging.debug("Query: " + sqlstring)
            logging.debug(err.diag.message_primary)
            raise exceptions.PDMDBQueryError(err.diag.message_primary)

        return cursor

    def commit(self):
        self.connstring.commit()

    def __del__(self):
        self.cursor.close()
        self.connstring.close()
