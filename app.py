from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('C:/Users/Sarvesh Chakradeo/Desktop/flights/templates'))
template = env.get_template('hello.html')
  
app = Flask(__name__)
  
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sarvesh31#'
app.config['MYSQL_DB'] = 'dbpro'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE u_eid = % s AND u_password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['u_id']
            session['name'] = user['u_name']
            session['email'] = user['u_eid']
            mesage = 'Logged in successfully !'
            return render_template('dashboard_test.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login_test.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE u_eid = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL,% s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register_test.html', mesage = mesage)

@app.route('/find')
def find():
    return render_template('search.html')

@app.route('/dashboard_test', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('find'))

@app.route('/result', methods =['GET', 'POST'])
def result():
    print("bhagbsdk")
    if request.method == 'POST':
        arrival = request.form['pick']
        final = request.form['drop']
        d1 = request.form['d1']
        d2 = request.form['d2']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #data = []
        headings=("f_id","a_name","f_adest","f_fdest","f_adatetime","f_fdatetime","f_cost")
        data=[]
        print(arrival)
        print(final)
        cursor.execute('SELECT * FROM flight WHERE f_adest = %s AND f_fdest = % s', (arrival, final))
        res=cursor.fetchall()
        p=[]
        # for r in res:
        #     #print(r)
        #     data.append(r)
            
        #     for j in r:
        #         print(r[j])
        data=res
        flight = cursor.fetchone()
       # print(data)
        return template.render(headings=headings, data = data)
        # if flight:
        #     #session['loggedin'] = True
        #     session['f_id'] = flight['f_id']
        #     session['arrival'] = flight['f_adest']
        #     session['final'] = flight['f_fdest']
        #     mesage = 'Logged in successfully !'
        #     return render_template('search.html', headings=headings,data=data)
        # else:
        #     mesage = 'Please enter correct email / password !'
    # return render_template('login_test.html', mesage = mesage)

# @app.route('/result', methods =['GET', 'POST'])
# def payment_page():
#     print("inside pay,ment")
#     return render_template("pay.html")
@app.route("/reservation",methods= ['GET','POST'])
def reservation():
    mesage="Booked!"
    if request.method == 'POST':
        adate = request.form['d1']
        fdate = request.form['d2']
        flight_id = request.form['flight_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO reservation VALUES (NULL,% s, % s, % s,% s)', (session['userid'], flight_id, adate,fdate,))
        mysql.connection.commit()
        return render_template('hello.html',mesage=mesage)




if __name__ == "__main__":
  app.run(debug=True)

