## Emily Van Laarhoven and Marissa Okoli
## db_curs.py
## Last modified: 4/19/2017
## gets cursor to use in all other functions

import dbconn2
import MySQLdb
import os
from oddjobs_dsn import DSN

## global variables
DATABASE = 'oddjobs_db'
DEBUG = False

def cursor(database=DATABASE):
    '''returns a cursor to the database'''
    DSN['db'] = database #set db in DSN dict to oddjobs_db
    conn = dbconn2.connect(DSN)
    return conn.cursor(MySQLdb.cursors.DictCursor)
