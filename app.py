from flask import Flask, render_template, g, abort, request, session, send_from_directory
from flask_session import Session
from main import main, Allocate
from input import load
import sqlite3
import pickle
import weasyprint
import requests

DATABASE = 'inputdb.sqlite'
app = Flask(__name__)
app.config['SECRET_KEY'] = None		#CHANGE SECRET KEY

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	db.row_factory = sqlite3.Row
	return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/allocate')
def allocate():
	return render_template('allocate.html')

@app.route('/do_allocation')
def do_allocation():
	text = request.args.get('jsdata')
	if text=='init':
		sessions = Allocate()
		with open('temp', 'wb') as f:
			pickle.dump((sessions, 0), f)
	elif text=='comman':
		with open('temp', 'rb+') as f:
			(sessions, _) = pickle.load(f)
			sessions.allocate_comman()
			f.seek(0)
			pickle.dump((sessions, 0), f)
	elif text=='session':
		with open('temp', 'rb+') as f:
			(sessions, i) = pickle.load(f)
			sessions.allocate(i+1)
			f.seek(0)
			pickle.dump((sessions, i+1), f)
	else:
		return abort(404)
	session['op_db'] = sessions.filename
	return render_template('chart.html', sessions = sessions.sessions)

@app.route('/input')
def inp():
	return render_template('input.html', fac_list = [fac[0:] for fac in query_db('select * from ece')])

@app.route('/allocate_all')
def allocate_all():
	sessions = main()
	session['op_db'] = sessions.filename
	return render_template('allocate_all.html', sessions=sessions.sessions)

@app.route('/admin')
def admin():
	return 'Admin page'

@app.route("/details")
def details():
	fac_list = load()
	return render_template('details.html', fac_list=fac_list)

@app.route("/details_ep", methods=["POST"])
def details_ep():
	name = request.form.get("faculty")
	if 'op_db' not in session:
		op_db_name = "2022-07-30 11:22:39.604658.db"
	else:
		op_db_name = session['op_db']
	con = sqlite3.connect(op_db_name)
	cur = con.cursor()
	result = []
	for table in ["comman", "session1", "session2", "session3", "session4", "session5", "session6"]:
		r = cur.execute(f"SELECT * from {table} WHERE name='{name}'")
		res = r.fetchone()
		if r.fetchone():
			raise Exception("More than one allocation for a faculty in one session")
		if res!=None:
			if table=="comman":
				result.append([res[0], res[1]])
			else:
				result.append([res[0], res[1], table, res[2]])
	return render_template('details_ep.html', result=result)

@app.route("/details_print", methods=["POST"])
def details_print():
	name = request.form.get("faculty")
	response = requests.post("http://127.0.0.1:5000/details_ep", data={"faculty":name})
	html = weasyprint.HTML(string=response.text)
	html.write_pdf("tmp.pdf")
	return send_from_directory("/home/laksh/Projects/Smart-Invigilator-Allotment-Tool/", "tmp.pdf", as_attachment=True)

@app.route("/details_all", methods=["GET"])
def details_all():
	fac_list = load()
	html=""
	for fac in fac_list:
		response = requests.post("http://127.0.0.1:5000/details_ep", data={"faculty":fac.name})
		html+=response.text
	html = weasyprint.HTML(string=html)
	html.write_pdf("tmp.pdf")
	return send_from_directory("/home/laksh/Projects/Smart-Invigilator-Allotment-Tool/", "tmp.pdf", as_attachment=True)

@app.route("/jquery-3.1.1-min.js")
def jquery_js():
	return send_from_directory("/home/laksh/Projects/Smart-Invigilator-Allotment-Tool", "jquery-3.1.1-min.js")
"""
Details to store per user:
name
output db name
"""

if __name__=='__main__':
	app.run(debug=True)
