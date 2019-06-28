## Emily Van Laarhoven and Marissa Okoli
## db_job.py
## Last modified: 5/13/2017
## Contains functions which interact with db to insert job

import dbconn2
import MySQLdb
import os
from oddjobs_dsn import DSN

## global variables
DATABASE = 'oddjobs_db'
DEBUG = False

def create_job(cursor,form_info,uid):
    '''inserts a new job into the db and returns True when successful'''
    ## insert new job into db with None jid
    q1 = "Insert into job (title,description,location,dt,pay,poster,skills_required,available) values (%s,%s,%s,%s,%s,%s,%s,%s);" 
    cursor.execute(q1,getInputs(form_info, uid))
    ## update jid
    jid = cursor.lastrowid
    #q2 = "Update job set jid=%s where jid is null;"
    #cursor.execute(q2,[new_jid])
    ## check if insertion was successful and return boolean
    q3 = "Select count(*) from job where jid=%s;"
    cursor.execute(q3,[jid])
    return (int(cursor.fetchone()['count(*)']) == 1), jid


def getInputs(form_info, uid):
    '''returns list of inputs for query from form'''
    title = form_info['title']
    description = form_info['description']
    location = form_info['location']
    dt = form_info['dt']
    pay = form_info['pay']
    skills_required = form_info['skills_required']
    print skills_required
    available = 1; #1 = available
    inputs = [title,description,location,dt,pay,uid,skills_required,available]
    return inputs








