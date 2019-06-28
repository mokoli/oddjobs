## Emily Van Laarhoven modified by Marissa Okoli
## db_review.py
## Last modified: 5/13/2017
## Insert review into rating table in db

import dbconn2
import MySQLdb
import os
from oddjobs_dsn import DSN

def insert_review(cursor,form_info,oid):
    '''inserts a review into rating table'''
    jid = form_info['jid']
    rating = form_info['rating']
    comment = form_info['review_comments']
    res = update_review(cursor, jid, oid)
    q1 = "update rating set "+res[0]+"=%s, "+res[1]+"=%s where jid=%s;"
    inputs = [rating,comment,jid]  
    cursor.execute(q1,inputs)
    #check if insertion was successful and return boolean
    q2 = "select "+res[0]+", "+res[1]+" from rating where jid=%s"
    cursor.execute(q2,(jid,))
    return not cursor.fetchone()[res[0]] == None

def update_review(cursor,jid,oid):
    '''helper method returns true if there is already a row for that jid'''
    #figure out if oid is for employee or employer without burdening the user
    q = "select employee_id, employer_id from rating where jid=%s;"
    cursor.execute(q,[jid])
    row = cursor.fetchone()
    #been using str because ran into some issues with equality
    if str(row['employee_id']) == str(oid):
		return ["employee_rating", "employee_review"]
    elif str(row['employer_id']) == str(oid):
		return ["employer_rating", "employer_review"]

def jobs_incommon(cursor, uid, oid):
	'''helper method returns list of jobs reviewer and reviewee have in common'''
	q = "select jid, title, dt from job inner join rating using (jid) where (rating.employer_id=%s and rating.employee_id=%s) or (rating.employer_id=%s and rating.employee_id=%s);"
	cursor.execute(q,(uid,oid,oid,uid))
	query_list = []
	while True:
		row = cursor.fetchone()
		if row == None:
			return query_list
		query_list.append(row)
	return query_list