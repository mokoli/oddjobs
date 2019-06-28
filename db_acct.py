## Emily Van Laarhoven
## db_acct.py
## Last modified: 5/4/17
## Contains functions which interact with db to insert account
# Modified by Marissa Okoli 5/12/17 to support file upload and logins
#MO = Marissa's comments

import dbconn2
import MySQLdb
import os
import imghdr
import hashlib, binascii
from werkzeug import secure_filename
from oddjobs_dsn import DSN

## global variables
DATABASE = 'oddjobs_db'
DEBUG = False

def create_account(cursor,form_info,skills_list,f):
    '''inserts a new account into the db and returns True when successful
	notifies if file upload was successful or not'''
	## NOTE: I've added a column to db to tell if an account is active; 1=yes 0=no
    q1 = "Insert into account (nm, rating_avg, street, town, st, skills, active, pwd, salt, email) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
	# MO: no need to insert "None" and re-add proper uid because auto_increment takes care of adding a UID already
	## the line below employs the two helper functions below to get proper inputs for query
    skills = ",".join(skills_list)
    cursor.execute(q1,getInputs(form_info,skills))
    uid = cursor.lastrowid
    err1 = ""
    err2 = ""
    if f.filename != "":
		try:
			mime_type = imghdr.what(f.stream)
			if (mime_type=='jpeg') or (mime_type=='png') or (mime_type=='gif'):
				filename = secure_filename(str(uid)+'.'+mime_type)
				pathname = 'ojups/'+filename
				f.save(pathname)
				q2 = "Update account set pic=%s where uid=%s;"
				cursor.execute(q2,[pathname, uid])
			else:
				err1 = "We're sorry, that file couldn't be uploaded. Is it a png, jpg or gif?"
		except Exception as err:
			err2 = 'Upload failed {why}'.format(why=err)
	## check if insertion was successful and return boolean
    q3 = "Select count(*) from account where uid=%s;"
    cursor.execute(q3,[uid])
    return int(cursor.fetchone()['count(*)']) ==1, err1, err2


def getInputs(form_info,skills):
	'''gets inputs for prepared sql query from form'''
	nm = form_info['nm']
	street = form_info['street']
	town = form_info['town']
	st = form_info['st']
	rating = 5 ## start off with 5 rating?
	active = 1 #MO start off as an active member
	salt = binascii.hexlify(os.urandom(16))
	pwd = encrypt_pass(form_info, salt)
	email = form_info['email']
	inputs = [nm,rating,street,town,st,skills,active,pwd,salt,email]
	return inputs
	
def encrypt_pass(form_info, salt):
	## MO create encrypted version of password
	user_pass = form_info["pwd"]
	# doesn't work, need python 2.7.8: 
	# dk = hashlib.pbkdf2_hmac('sha256', bytes(pwd, encoding='utf-8'), bytes(salt, encoding='utf-8'), 100000)
	sh = hashlib.sha256()
	sh.update(user_pass)
	sh.update(salt)
	return sh.hexdigest()
	

def average_ratings(cursor,uid):
    '''returns the average rating for this uid from the rating table'''
    # get employee ratings
    q1 = "select sum(employee_rating) from rating where employee_id=%s;" 
    cursor.execute(q1,[uid])
    employee_total = int(cursor.fetchone()['sum(employee_rating)'])
    print "employee_total"
    print employee_total
    # get employer ratings
    q2 = "select sum(employer_rating) from rating where employer_id=%s;" 
    cursor.execute(q2,[uid])
    employer_total = int(cursor.fetchone()['sum(employer_rating)'])
    print "employer_total"
    print employer_total
    # get employee # of reviews
    q3 = "select count(employee_rating) from rating where employee_id=%s;" 
    cursor.execute(q3,[uid])
    employee_count = int(cursor.fetchone()['count(employee_rating)'])
    print "employee_count"
    print employee_count
    # get employer # of reviews
    q4 = "select count(employer_rating) from rating where employer_id=%s;" 
    cursor.execute(q4,[uid])
    employer_count = int(cursor.fetchone()['count(employer_rating)'])
    print "employer_count"
    print employer_count
    #compute average rating
    avg_rating= ((employee_total+employer_total)/(employee_count+employer_count))
    print "avg_rating"
    print avg_rating
    return avg_rating


def deleteAcct(cursor,uid):
    '''sets the account to inactive, returns true when successful'''
    q = "update account set active=0 where uid=%s;"
    cursor.execute(q,[uid])
    q2 = "select active from account where uid=%s;"
    cursor.execute(q2,[uid])
    return int(cursor.fetchone()['active'])==0

def login(cursor, form_info):
	'''Logs user into account'''
	q = "select uid,pwd,salt from account where email=%s;"
	cursor.execute(q,(form_info['user'],))
	row = cursor.fetchone()
	if row != None:
		pwd = encrypt_pass(form_info, row['salt'])
		# if is true, error string will be ignored (see app.py), so can include either way
		return pwd == row['pwd'], row['uid'], "Incorrect password. Please try again."
	else:
		return False, "", "Username not found. Please try again"
		