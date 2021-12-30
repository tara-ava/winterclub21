from flask import Flask, request, render_template
import sqlite3

# db setup
db = sqlite3.connect('flask.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (\
ID INTEGER PRIMARY KEY AUTOINCREMENT, \
USER TEXT NOT NULL, \
EMAIL TEXT, \
PASS TEXT NOT NULL)')
db.commit()
# /db setup

app = Flask(__name__)

# function for using db in flask 
def sql(cmd, vals=None):
    conn = sqlite3.connect('flask.db')
    cur = conn.cursor()
    res = cur.execute(cmd, vals).fetchall()
    conn.commit()
    conn.close()
    return res

@app.route('/')
def app_index():
  return render_template("index.html") #renders the homepage

@app.route('/intro-to-stem')
def app_stemintro():
  return render_template("1-stemintro.html") #renders the homepage

@app.route('/the-gap')
def app_thegap():
  return render_template("2-thegap.html") #renders the homepage

@app.route('/closing-the-gap')
def app_closingthegap():
  return render_template("3-closingthegap.html") #renders the homepage

@app.route('/events')
def app_events():
  events = sql('SELECT * FROM events', ())
  return render_template("events.html", pevents=events)


@app.route('/regform/<eid>')
def app_regform(eid):
  ss = "SELECT event_id, event_name, event_date FROM events WHERE event_id = '" + eid + "'"
  einfo = sql(ss, ())
  return render_template("regform.html", peinfo=einfo[0] ) #renders the signup page

@app.route('/user')
def app_user():
  users = sql('SELECT * FROM users', ())
  return render_template("user.html", pusers=users)

@app.route('/add', methods=['POST'])      #to add new users to data base
def app_add():
  password = request.form['password']
  confirm_password = request.form['confirm_password']  

  if password != confirm_password:
    return 'Password and Confirm Password not match!'   #making password
  
  username = request.form['username']
  email = request.form['email']

  sql('INSERT INTO users (USER, EMAIL, PASS) VALUES (?, ?, ?)', (
      username,
      email,
      password,
  ))
  return 'user already added!'



@app.route('/reg', methods=['POST'])      #to add new users to data base
def app_reg():
  email = request.form['email']
  eid = request.form['eid']
  
  sql('INSERT INTO registered (EMAIL, EID) VALUES (?, ?)', (
      email,
      eid,
  ))
  return render_template("index.html")







@app.route('/loginform')
def app_loginform():
  return render_template("loginform.html")





@app.route('/login', methods=['POST'])   #login process
def app_login():
  email = request.form['email']

  ss = "select email, eid, event_name, event_date from registered [inner] join events on eid = event_id where email = '" + email + "'"
  myevents = sql(ss, ())

  return render_template("myevents.html", pmyevents=myevents)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)