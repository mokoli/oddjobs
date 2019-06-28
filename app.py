#!/usr/local/bin/python2.7

## Emily Van Laarhoven and Marissa Okoli
## app.py
## Last modified: 5/4/2017
## driver for web pages and forms

from flask import Flask, render_template, flash, request, redirect, url_for, make_response, session
import os
import db_curs
import db_acct
import db_job
import showJobs
import acceptJob
import db_review
import db_viewAcct
import db_allAccts
import deleteJob

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 #1 MB max file size
app.secret_key = "asgaoihrnasdfkjd" #secret key needed for flashing
app.add_url_rule('/ojups/<path:filename>', endpoint='ojups', view_func=app.send_static_file)

DATABASE = "oddjobs_db"

@app.errorhandler(413)
def img_too_large(e):
	flash("We're sorry, maximum upload size is 1MB. Please try to create account again.")
	return render_template("create_account.html",page_title="Create Account"), 413

@app.route('/')
def home():
	if 'user' in session:
		uid = uid=session['user']
	else:
		uid = ""
	return render_template("home.html", is_logged=('user' in session), uid=uid)
    
@app.route('/login/',methods=['POST','GET'])
def login():
	'''Logs user into the app'''
	if request.method=="POST":
		cursor = db_curs.cursor()
		resp, user_id, err = db_acct.login(cursor, request.form)
		if resp:
			session['user'] = user_id
			flash("Login successful")
			return redirect(url_for('view_jobs'))
		else:
			flash(err)
	return render_template("login.html", page_title="Login", is_custom=True)

@app.route('/logout/')
def logout():
	# remove the username from the session if it is there
	session.pop('user', None)
	flash('Logged out succesfully.')
	return redirect(url_for('home'))
		
@app.route('/create_account/',methods=['POST','GET'])
def create_account():
## '''inserts data from form into account table'''
	if request.method=="POST":
		cursor = db_curs.cursor()
		skills = request.form.getlist('skills')
		f = request.files['file']
		a, b, c = db_acct.create_account(cursor,request.form,skills,f)
		if a:
			flash("Account has been created successfully!")
			if b != "":
				flash(b)
			if c != "":
				flash(c)
		return redirect(url_for('login'))
		flash("We're sorry, something went wrong...")
	return render_template("create_account.html")

@app.route('/create_job/',methods=['POST','GET'])
def create_job():
## '''inserts data from form into job table'''
	if 'user' in session:
		if request.method=="POST":
			cursor = db_curs.cursor()
			a, b = db_job.create_job(cursor,request.form, session['user'])
			if a:
				flash("Job has been created successfully!")
				return redirect(url_for('job_detail', jid=b))
			else:
				flash("We're sorry, something went wrong...")
		return render_template("create_job.html",page_title="Post a New Job", is_logged=True, uid=session['user'])
	else:
		flash("Please login to create jobs.")
		return redirect(url_for('login'))

@app.route('/view_jobs/',methods=['POST','GET'])
def view_jobs():
## '''displays list of jobs and allows user to accept or delete job'''
	if 'user' in session:
		if request.method == 'POST':
			zipcode = request.form['zipcode']
			session['zip'] = zipcode
		if 'zip' in session:
			zip = session['zip']
		else:
			zip = 0
		jobList = showJobs.main()
		return render_template("joblistings.html",location=zip, jobs=jobList, 
		page_title="Job Board", is_logged=True, uid=session['user'])
	else:
		flash("Please login to view jobs.")
		return redirect(url_for('login'))
    
@app.route('/job/<jid>/',methods=['POST','GET'])
def job_detail(jid):
	if 'user' in session:
		cursor = db_curs.cursor()
		if request.method=="POST":
			uid = session['user']
			if request.form['btn'] == "Accept":
				#returns boolean and employee id if true, boolean and error message if false
				resp, e = acceptJob.main(uid, jid)
				if resp:
					flash("Job accepted!")
					return redirect(url_for('view_account', uid=e))
				else:
					flash(e)
					return render_template("view_job.html", jid=jid, page_title=deetsList[0], deetsList=deetsList, is_logged=True, 
					is_owner=(session['user']==job[1]), uid=uid)
			else:
				deleteJob.deleteJob(cursor, uid, jid)
				flash("Job has been deleted.")
				return redirect(url_for('view_jobs'))
    	#job is a symbol separated string of job info
		job = showJobs.showJob(cursor, jid)
		#split job into list so easy to add pieces of info to template
		if job[0] == "":
			flash("We're sorry, that job can't be found.")
			return redirect(url_for('view_jobs'))
		deetsList = job[0].split('(~/~)')
		return render_template("view_job.html", jid=jid, page_title=deetsList[0], deetsList=deetsList, is_logged=True, 
		is_owner=(session['user']==job[1]), uid=session['user'])
	else:
		flash("Please login to view this job.")
		return redirect(url_for('login'))

@app.route('/review/<oid>',methods=['POST','GET'])
def review(oid):
## '''allows both employees and employers to review, link from account page'''
	if 'user' in session:
		cursor = db_curs.cursor()
		if db_viewAcct.can_view(cursor,session['user'],oid):
			if request.method=="POST":
				if db_review.insert_review(cursor,request.form, oid):
					flash("Review submitted.")
					return redirect(url_for('search_account'))
				else:
					flash("We're sorry, something went wrong...")
			jobs = db_review.jobs_incommon(cursor, session['user'], oid)
			return render_template("review.html",page_title="Leave a Review", jobs_worked=jobs, is_logged=True)
		else:
			flash("The user must be in your connections in order to leave a review.")
			return redirect (url_for('search_account'))
	else:
		flash("Please login to leave a review.")
		return redirect(url_for('login'))


@app.route('/view_account/<uid>/',methods=['POST','GET'])
def view_account(uid):
	if 'user' in session:
		cursor = db_curs.cursor()
		if db_viewAcct.can_view(cursor,session['user'],uid):
			if db_viewAcct.isActive(cursor,uid):
				if request.method == "POST":
					if  db_acct.deleteAcct(cursor,uid):
						flash("You have successfully deleted your account.")
						return redirect(url_for('home'))
				acct_info = db_viewAcct.search_uid(cursor,uid)
				return render_template("view_account.html",acct_info=acct_info, 
				page_title=acct_info['name']+"'s Profile", is_logged=True, uid=session['user'], 
				is_owner=(str(session['user'])==str(uid)), rev_id=uid)
			else:
				flash("We're sorry, this account has been deleted.")
				return redirect(url_for('home'))
		else:
			flash("Must be account owner, hired the person, or have worked a job associated with account to view.")
			return redirect (url_for('search_account'))
	flash("Must be logged in to view account.")
	return redirect(url_for('login'))

@app.route('/search_account/',methods=['POST','GET'])
def search_account():
	if 'user' in session:
		cursor = db_curs.cursor()
		if request.method == "POST":
			return redirect(url_for('view_account',uid=request.form['uid']))
		all_accounts = db_allAccts.list_users(cursor, session['user'])
		if all_accounts == {}:
			flash("You haven't connected with anyone yet.")
		return render_template("search_account.html",all_accounts=all_accounts,page_title="View Past Connections", 
		is_logged=True, uid=session['user'])
	flash("Must be logged in to view page.")
	return redirect(url_for('login'))



if __name__=='__main__':
    app.debug = True
    app.run('0.0.0.0', os.getuid())
