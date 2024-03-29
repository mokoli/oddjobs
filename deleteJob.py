#!/usr/local/bin/python2.7

'''Author: Emily Van Laarhoven Marissa Okoli
   CS 304 OddJobs Beta
   Deletes a job from the jobs list by setting it to unavailable 
   If logins were implemented this would only be an option for the person who posted the job
'''

import sys
import MySQLdb
import dbconn2
import db_curs
from oddjobs_dsn import DSN


def deleteJob(cursor, uid, jid):
	'''Marks job from the job table as unavailable'''
	cursor.execute('update job set available=0 where jid= %s', (jid,))
	cursor.execute('select count(*) from job where jid= %s and available=0;', (jid,))
	return int(cursor.fetchone()['count(*)']) == 1

def main(uid,jid):
	'''removes specified job from listing'''
	if int(uid)==0:
		return deleteJob(db_curs.cursor(), uid, jid)
	else:
		print "enter uid = 0 to confirm deletion"
		return False
	
if __name__ == '__main__':
	print main(1, 4)
