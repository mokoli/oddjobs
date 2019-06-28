## Emily Van Laarhoven and Marissa Okoli
## db_allAccts.py
## Last modified: 5/13/2017
## Get list of all uids and all names from past interacted with accounts

import dbconn2
import MySQLdb
import os
from oddjobs_dsn import DSN

def list_users(cursor, uid):
    '''return DICTIONARY of all account uids and names for search account'''
    q1 = "select uid,nm,active from account inner join rating on account.uid=rating.employee_id where employer_id=%s;"
    cursor.execute(q1,(uid,))
    query_list = []
    while True:
		row1 = cursor.fetchone()
		if row1 == None:
			break
		query_list.append(row1)
    q2 = "select uid,nm,active from account inner join rating on account.uid=rating.employer_id where employee_id=%s;"
    cursor.execute(q1,(uid,))
    while True:
		row2 = cursor.fetchone()
		if row2 == None:
			break
		query_list.append(row2)
    if query_list == []:
		return {}
    all_accounts = {acct['uid']:acct['nm'] for acct in query_list if (int(acct['active'])==1 and str(acct['uid'])!=str(uid))}
    return all_accounts


    
