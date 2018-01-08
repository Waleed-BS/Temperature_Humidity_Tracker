#---------------------------------------
import plotly.tools as tls

tls.set_credentials_file(
        username="waleed-bs",
        api_key="bdeNJOC2IQfL6oB6CppV")

# to get your credentials
credentials = tls.get_credentials_file()


import csv
import plotly.plotly as py
import plotly.graph_objs as go
#----------------------------------------------------------------------
import os


def plot_temp(csv_path):
    """
    http://census.ire.org/data/bulkdata.html
    """
    counties = {}
    county = []
    pop = []

    counter = 0
    with open(csv_path) as csv_handler:
        reader = csv.reader(csv_handler)
        for row in reader:
            print row
            if counter  == 0:
                counter += 1
                continue
            county.append(row[1]) #y-axis
            pop.append(row[0]) # x-axis

    trace = dict(x=county, y=pop)
    data = [trace]
    layout = go.Layout(
    title='Temperature VS Time',
    xaxis=dict(
        title='Time',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Temperature (C)',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='temperature vs time')

    os.remove("temp_humd.csv")

def plot_hum(csv_path):
    """
    http://census.ire.org/data/bulkdata.html
    """
    counties = {}
    county = []
    pop = []

    counter = 0
    with open(csv_path) as csv_handler:
        reader = csv.reader(csv_handler)
        for row in reader:
            print row
            if counter  == 0:
                counter += 1
                continue
            county.append(row[1]) #y-axis
            pop.append(row[0]) # x-axis

    trace = dict(x=county, y=pop)
    data = [trace]
    layout = go.Layout(
    title='Humidity VS Time',
    xaxis=dict(
        title='Time',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Relative Humidity (%)',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='humidity vs time')

    os.remove("temp_humd.csv")


#-------------------------------------------

from flask import *
# import flask_login
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import sqlite3
from datetime import datetime,tzinfo,timedelta


DATABASE = '../TempLogger/temp_humd.db'

app = Flask(__name__)
app.config.from_object(__name__)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'Shokoloki'
sess = Session()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

x = []
y = []



class User(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))

	def __init__(self, username, password):
		self.username = username
		self.password = password



@app.route('/createuser', methods=['GET', 'POST'])
def createuser():
    print "createuser() called"
    """Register Form"""
    if request.method == 'POST':
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('log.html')
    return render_template('createuser.html')



def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_template('home.html', data=getfollowedby(username))
        return render_template('home.html')



@app.route('/logout')
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('log'))

import os

@app.route('/display', methods=['GET', 'POST'])
#@login_required
def display():
	graph = False;
	if request.method == 'POST':
		if request.form['submit'] == 'Display Data':
			#age = request.form['age']
			print "request.form['submit'] == 'Display'"
			date = request.form['date']
			conn = connect_db()
			curs = conn.cursor()
			#curs.execute('select * from climate')

			curs.execute("select * from climate where date(rDatetime) = date(?);", (date,))

			climate = [dict(rDatetime = row[0], tempC = ("%.1f" % row[1]), hum = row[2]) for row in curs.fetchall()]

			print climate
			conn.close()
			return render_template('display.html', climate = climate, date = date)

	if request.method == 'POST':
		if request.form['submit'] == "Graph Data":
			date = request.form['date']

			conn = connect_db()
	 		curs = conn.cursor()
	 		#curs.execute('select * from climate')
	 		curs.execute("select tempC, rDatetime from climate where date(rDatetime) = date(?);", (date,))
			with open('temp_humd.csv','wb') as out_csv_file:
  				csv_out = csv.writer(out_csv_file)
  				# write header
  				csv_out.writerow([d[0] for d in curs.description])
  				# write data
  				for result in curs:
					csv_out.writerow(result)
			conn.close()

			print "Graph The Displayed Data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			csv_path = 'temp_humd.csv'
			plot_temp(csv_path)
	if request.method == 'POST':
		if request.form['submit'] == "Graph The Humidity Data":
			date = request.form['date']

			conn = connect_db()
	 		curs = conn.cursor()
	 		#curs.execute('select * from climate')
	 		curs.execute("select hum, rDatetime from climate where date(rDatetime) = date(?);", (date,))
			with open('temp_humd.csv','wb') as out_csv_file:
  				csv_out = csv.writer(out_csv_file)
  				# write header
  				csv_out.writerow([d[0] for d in curs.description])
  				# write data
  				for result in curs:
					csv_out.writerow(result)
			conn.close()

			print "Graph The Displayed Data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			csv_path = 'temp_humd.csv'
			plot_hum(csv_path)
        if request.method == 'POST':
            if request.form['submit'] == "Log":
                #os.system('python /home/pi/Desktop/Temperature_Humidity_Displayer/TempLogger/log_temp_humd.py')
                run("../TempLogger/log_temp_humd.py")


	return render_template('display.html')

def run(runfile):
    with open(runfile, "r") as rnf:
        exec(rnf.read())

@app.route('/log', methods=['GET', 'POST'])
def log():
    """Login Form"""
    if request.method == 'GET':
        return render_template('log.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
			data = User.query.filter_by(username=name, password=passw).first()
			if data is not None:
				session['logged_in'] = True
				return redirect(url_for('display'))
			else:
				return 'Username or Password is not found'
        except:
			return "Bad Login"


if __name__ == '__main__':
    app.run(debug = True)
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    #app.run(host='192.168.0.58', port=9000, debug=False)
