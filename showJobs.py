#!/usr/local/bin/python2.7
'''Author: Emily Van Laarhoven Marissa Okoli
   CS 304 OddJobs Alpha
Helper module for flask application to retrieve listed jobs from database
Contains functions for connecting to the database port:7332	
'''

import sys
import MySQLdb
import dbconn2
import db_curs
from oddjobs_dsn import DSN

def getJobs(cursor):
	'''Returns a list of jobs'''
#	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	cursor.execute('select jid,title,location,dt,pay from job where available=1')
	lines = []
	while True:
		row = cursor.fetchone()
		if row == None:
			return lines
		# prepare for split on (~/~), not entirely robust, but unlikely to be typed by user
		lines.append('{jid}(~/~){title}(~/~){location}(~/~){dt}(~/~)${pay}'.format(**row))

def showJob(cursor, jid):
	'''Returns a single job with all details'''
	q1 = "select title,description,dt,pay,poster,skills_required,available from job where jid=%s;"	
	cursor.execute(q1, (jid,))
	row1 = cursor.fetchone()
	if row1 == None:
		return [""]
	#collect the id of the poster to compare for delete/accept privileges in template
	uid = row1["poster"]
	# get the name of the poster
	q2 = "select nm from account inner join job on (account.uid=job.poster) where job.poster=%s;"
	cursor.execute(q2, (row1["poster"],))
	row2 = cursor.fetchone()
	# use name of poster instead of poster id in returned query
	row1["poster"] = row2["nm"]
	return ["{title}(~/~){description}(~/~){dt}(~/~){pay}(~/~){poster}(~/~){skills_required}(~/~){available}".format(**row1), uid]

def main():
	'''Returns a list of available jobs'''
	return getJobs(db_curs.cursor())
	
if __name__ == '__main__':
	print main()
	print showJob(db_curs.cursor(), 3)
