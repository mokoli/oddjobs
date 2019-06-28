## Emily Van Laarhoven and Marissa Okoli
## db_viewAcct.py
## Last modified: 5/13/2017
## Get account info to display on profile page

import dbconn2
import MySQLdb
import os
from oddjobs_dsn import DSN

## global variables
DATABASE = 'oddjobs_db'
DEBUG = False

def search_uid(cursor,uid):
    '''return DICT of all account info from account table in db'''
    q1 = "select nm, rating_avg, street, town, st, skills, pic, email from account where uid=%s;"
    cursor.execute(q1,[uid])
    row1 = cursor.fetchone()
    acct_info = {}
    acct_info['uid'] = uid #eventually comment out after logins and modify form
    acct_info['name'] = row1['nm']
    new_rate_avg = average_ratings(cursor,uid)
    acct_info['rating'] = new_rate_avg
    acct_info['street'] = row1['street']
    acct_info['town'] = row1['town']
    acct_info['state'] = row1['st']
    acct_info['skills'] = row1['skills'] #multiple skills fixed
    acct_info['pic'] = row1['pic']
    acct_info['email'] = row1['email']
    q2 = "select employee_review from rating where employee_id=%s;"
    cursor.execute(q2,(uid,))
    lines1 = []
    while True:
		row2 = cursor.fetchone()
		if row2 == None:
			acct_info['eer'] = lines1
			break
		if not row2["employee_review"] is None:
			lines1.append('{employee_review}'.format(**row2))
    q3 = "select employer_review from rating where employer_id=%s;"
    cursor.execute(q3,(uid,))
    lines2 =[]
    while True:
		row3 = cursor.fetchone()
		if row3 == None:
			acct_info['err'] = lines2
			break
		if not row3["employer_review"] is None:
			lines2.append('{employer_review}'.format(**row3))
    return acct_info

def isActive(cursor,uid):
    '''returns true if active=1 for this uid'''
    q1 = "select active from account where uid=%s;"
    cursor.execute(q1,[uid])
    row = cursor.fetchone()
    if row is None:
		return False
    return int(row['active'])==1

def average_ratings(cursor,uid):
    '''returns the average rating for this uid from the rating table'''
    #check to see if they've been rated yet (if not, return 5)
    q0 = "select count(employee_rating) from rating where employee_id=%s;"
    cursor.execute(q0,[uid])
    employee_rate_count =  int(cursor.fetchone()['count(employee_rating)'])
    q5 = "select count(employer_rating) from rating where employer_id=%s;"
    cursor.execute(q5,[uid])
    employer_rate_count =  int(cursor.fetchone()['count(employer_rating)'])
    if ( (employee_rate_count ==0) and (employer_rate_count==0) ) :
        return 5 #no reviews have been made for this person yet
    else: #calculate average from rating table
        # get employee ratings
        q1 = "select sum(employee_rating) from rating where employee_id=%s;" 
        cursor.execute(q1,[uid])
        employee_total = cursor.fetchone()['sum(employee_rating)']
        if employee_total is None:
            employee_total=0
        print "employee_total"
        print employee_total
        # get employer ratings
        q2 = "select sum(employer_rating) from rating where employer_id=%s;" 
        cursor.execute(q2,[uid])
        employer_total = cursor.fetchone()['sum(employer_rating)']
        if employer_total is None:
            employer_total =0
        print "employer_total"
        print employer_total
        # get employee # of reviews
        q3 = "select count(employee_rating) from rating where employee_id=%s;" 
        cursor.execute(q3,[uid])
        employee_count = cursor.fetchone()['count(employee_rating)']
        if employee_count is None:
            employee_count =0
        print "employee_count"
        print employee_count
        # get employer # of reviews
        q4 = "select count(employer_rating) from rating where employer_id=%s;" 
        cursor.execute(q4,[uid])
        employer_count = cursor.fetchone()['count(employer_rating)']
        if employer_count is None:
            employer_count =0
        print "employer_count"
        print employer_count
        #compute average rating
        # don't have to check for division by 0 because we know at least one rating exists
        avg_rating= ((employee_total+employer_total)/(employee_count+employer_count))
        print "avg_rating"
        print avg_rating
        return avg_rating

def can_view(cursor, uid, eid):
	'''Checks if user has previously accepted a job from employer to be allowed to view profile'''
	q = "select * from rating where (employee_id=%s and employer_id=%s) or (employee_id=%s and employer_id=%s);"
	cursor.execute(q,(uid, eid, eid, uid))
	row = cursor.fetchone()
	return ((not row is None) or (str(uid)==str(eid)))