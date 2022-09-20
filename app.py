from sqlite3 import Cursor
import string
from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'testapplication'
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "payroll_system"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee_list WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        cursor.close()
        if account:
            session['loggedin'] = True
            session['id'] = account['employee_id']
            session['username'] = account['username']
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    id = session['id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT pay_rate FROM employee_list WHERE employee_id = %s", (id,))
    payrate = cursor.fetchone()
    cursor.close()
    return render_template('dashboard.html', payrate=payrate)

@app.route('/profile')
def profile():
    id = session['id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM employee_list WHERE employee_id = %s", (id,))
    profile = cursor.fetchone()
    print(profile)
    cursor.close()
    return render_template("profile.html", profile=profile)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

app.run(debug=True)